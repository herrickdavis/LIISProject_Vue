from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from django.db.models import Q
from .models import Equipo, Medicion
from .serializers import EquipoSerializer, MedicionSerializer
import serial
import pandas as pd
import socket
import os
from datetime import datetime
from django.http import HttpResponse, FileResponse

# para eximir temporalmente CSRF
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class EquipoListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EquipoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        busqueda = self.request.query_params.get('busqueda', 'all')
        queryset = Equipo.objects.all().order_by('codigo')
        if busqueda != 'all':
            queryset = queryset.filter(
                Q(codigo__icontains=busqueda) |
                Q(codigo_interno__icontains=busqueda) |
                Q(equipo__icontains=busqueda) |
                Q(marca__icontains=busqueda) |
                Q(modelo__icontains=busqueda) |
                Q(pais__icontains=busqueda)
            )
        return queryset

    def perform_create(self, serializer):
        # Guarda creador automáticamente
        serializer.save(
            creador=self.request.user.username,
            creacion=datetime.now()
        )


class EquipoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Mantener el creador original si no viene
        if not request.data.get("creador"):
            request.data["creador"] = instance.creador or request.user.username

        # Actualizar fecha y usuario automáticamente
        request.data["update"] = datetime.now()
        request.data["update_user"] = request.user.username

        return super().update(request, *args, **kwargs)


# Decoramos la clase para eximir temporalmente CSRF y permitir pruebas sin sesión
@method_decorator(csrf_exempt, name='dispatch')
class CapturarPesoAPIView(APIView):
    # poner [] para pruebas; en producción usar IsAuthenticated
    permission_classes = []

    def post(self, request):
        print(">>> POST recibido en /liis/capturar-peso/")
        print(">>> Data recibida:", request.data)
        ip = request.META.get('REMOTE_ADDR')

        if 'codigo_balanza' in request.data:
            codigo_balanza = request.data['codigo_balanza']
            print(f">>> Buscando equipo con código de balanza: {codigo_balanza}")
            if not Equipo.objects.filter(codigo=codigo_balanza).exists():
                print(f">>> Error: No existe el código {codigo_balanza}.")
                return Response({"cb_error": f"No existe el código: {codigo_balanza} en registro."}, status=status.HTTP_404_NOT_FOUND)

            equipo = Equipo.objects.get(codigo=codigo_balanza)
            print(f">>> Equipo encontrado: {equipo.equipo}")

            if 'conectar' in request.data:
                try:
                    print(f">>> Intentando conexión con equipo en puerto {equipo.puerto} desde {ip}")
                    url = f'socket://{ip}:{equipo.puerto}'
                    ser = serial.serial_for_url(url, timeout=1)
                    ser.close()
                    return Response({"balanza": EquipoSerializer(equipo).data, "conectado": True}, status=status.HTTP_200_OK)
                except Exception as e:
                    print(f">>> Error de conexión con la balanza: {e}")
                    return Response({"error_conexion": "No se pudo conectar"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            codigo_muestra = request.data.get('codigo_muestra')
            if codigo_muestra:
                print(f">>> Buscando métodos para muestra: {codigo_muestra}")
                unidades = [equipo.unidad]
                placeholders = ",".join(["%s"] * len(unidades))
                sql = f"""SELECT DISTINCT REPLACE(M.[DESCMETODO],'*','') AS METODO,
                          VEM.[NMVEMETODO],
                          VEM.[IDVEMETODO],
                          VEM.[LIMITEINF] AS MINIMO,
                          VEM.[LIMITESUP] AS MAXIMO,
                          MA.[CDAMOSTRA], VEM.[CDMETODO]
                          FROM [MYLIMS_PRODUCAO].[dbo].[METODOSAM] MA
                          LEFT JOIN [MYLIMS_PRODUCAO].[dbo].[METODOANALISE] M ON M.[CDMETODO] = MA.[CDMETODO]
                          LEFT JOIN [MYLIMS_PRODUCAO].[dbo].[LABORATORIO] L ON L.[CDLABORATORIO] = MA.[CDLABORATORIO]
                          LEFT JOIN [MYLIMS_PRODUCAO].[dbo].[VEMETODO] VEM ON VEM.[CDMETODO] = MA.[CDMETODO]
                          LEFT JOIN [MYLIMS_PRODUCAO].[dbo].[VARENTRADA] VE ON VE.[CDVE] = VEM.[CDVE]
                          WHERE MA.[CDAMOSTRA] = ? --AND VE.UNIDADE IN ({placeholders})"""

                params = [codigo_muestra] #+ unidades
                print(f">>> Ejecutando consulta SQL con params: {params}")
                with connection.cursor() as cursor:
                    cursor.execute(sql, params)
                    row = cursor.fetchall()
                
                print(f">>> Consulta SQL finalizada. Filas encontradas: {len(row)}")
                metodos = []
                for r in row:
                    metodos.append({
                        "metodo": r[0],
                        'NMVEMETODO': r[1],
                        'idve': r[2],
                        'min': str(r[3]) if r[3] is not None else None,
                        'max': str(r[4]) if r[4] is not None else None,
                        'cdometodo' : r[6],
                    })
                
                mediciones_existentes = list(Medicion.objects.filter(muestra=codigo_muestra).values_list('idve', flat=True))
                metodos = [m for m in metodos if m['idve'] not in mediciones_existentes]
                
                return Response({"balanza": EquipoSerializer(equipo).data, "metodos": metodos, "codigo_muestra": codigo_muestra}, status=status.HTTP_200_OK)

        if 'medicion' in request.data:
            codigo_balanza = request.data['codigo_balanza']
            codigo_muestra = request.data['codigo_muestra']
            medicion_valor = request.data['medicion']
            ensayo = request.data['ensayo']

            print(f">>> Guardando medición: muestra={codigo_muestra}, equipo={codigo_balanza}, valor={medicion_valor}, ensayo={ensayo}")

            equipo = Equipo.objects.get(codigo=codigo_balanza)
            ensayo_split = ensayo.split('-')
            idve = ensayo_split[0]

            Medicion.objects.create(
                muestra=codigo_muestra,
                idve=idve,
                medida=medicion_valor,
                equipo=equipo,
                host=ip,
                ip_host=ip,
                creador=request.user.username if request.user and request.user.is_authenticated else 'anonymous'
            )

            fecha = datetime.now().strftime("%d-%m-%Y %H-%M")
            data = {
                'Codigo': [codigo_muestra, codigo_muestra, codigo_muestra],
                'IDVE': [idve, f'Instrum_{idve}', f'Analyst_{idve}'],
                'Fecha': [fecha, fecha, fecha],
                'Valor': [medicion_valor.replace('.', ','), equipo.codigo_interno, request.user.first_name if request.user and request.user.is_authenticated else ''],
            }
            df = pd.DataFrame(data).set_index('Codigo')
            ruta_csv = f'C:/Users/francisco.rotundo/Downloads/{idve}-{datetime.now().strftime("%d-%m-%Y_%H-%M")}.csv'
            df.to_csv(ruta_csv, sep=";")

            print(f">>> CSV generado en: {ruta_csv}")

            return Response({"message": f'Se generó el archivo {os.path.basename(ruta_csv)}'}, status=status.HTTP_201_CREATED)

        return Response({}, status=status.HTTP_200_OK)


def ejecutable_view(request, nombre):
    archivo_path = os.path.join(r'C:\Users\Francisco.Rotundo\Downloads\Proyectos\Nueva carpeta (2)\media', f'{ nombre }.exe')
    print(f">>> Descargando ejecutable solicitado: {archivo_path}")
    if os.path.exists(archivo_path):
        response = FileResponse(open(archivo_path, 'rb'), as_attachment=True, filename=f'{ nombre }.exe')
        response['Content-Type'] = 'application/octet-stream'
        return response
    print(">>> Archivo no encontrado")
    return HttpResponse('Archivo no encontrado', status=404)
