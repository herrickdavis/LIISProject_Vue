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

class EquipoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Equipo.objects.all().order_by('codigo')
    serializer_class = EquipoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        busqueda = self.request.query_params.get('busqueda', 'all')
        if busqueda != 'all':
            return self.queryset.filter(
                Q(codigo__icontains=busqueda) | Q(codigo_interno__icontains=busqueda) |
                Q(equipo__icontains=busqueda) | Q(marca__icontains=busqueda) |
                Q(modelo__icontains=busqueda) | Q(pais__icontains=busqueda)
            )
        return self.queryset

    def post(self, request, *args, **kwargs):
        try:
            serializer = EquipoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(creador=request.user.username)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "El codigo utilizado ya existe en la base de datos."}, status=status.HTTP_400_BAD_REQUEST)

class EquipoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Modificar los datos del request antes de la actualización
        request.data['update'] = datetime.now()
        request.data['update_user'] = request.user.username
        return super().update(request, *args, **kwargs)

class CapturarPesoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data)
        ip = request.META.get('REMOTE_ADDR')
        
        # Lógica para manejar la conexión con la balanza
        if 'codigo_balanza' in request.data:
            codigo_balanza = request.data['codigo_balanza']
            if not Equipo.objects.filter(codigo=codigo_balanza).exists():
                return Response({"cb_error": f"No existe el código: {codigo_balanza} en registro."}, status=status.HTTP_404_NOT_FOUND)
            
            equipo = Equipo.objects.get(codigo=codigo_balanza)
            nombre_equipo = None
            try:
                nombre_equipo = socket.gethostbyaddr(ip)[0]
            except socket.herror:
                pass
            
            # if equipo.host != nombre_equipo:
            #     return Response({"cb_error": f"El equipo {nombre_equipo} no corresponde a la información guardada del equipo {codigo_balanza}."}, status=status.HTTP_403_FORBIDDEN)
            
            if 'conectar' in request.data:
                try:
                    url = f'socket://{ip}:{equipo.puerto}'
                    ser = serial.serial_for_url(url, timeout=1)
                    ser.close()
                    return Response({"balanza": EquipoSerializer(equipo).data, "conectado": True}, status=status.HTTP_200_OK)
                except Exception:
                    return Response({"error_conexion": "No se pudo conectar"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Lógica para obtener métodos y mediciones
            codigo_muestra = request.data.get('codigo_muestra')
            if codigo_muestra:
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
                          WHERE MA.[CDAMOSTRA] = %s AND VE.UNIDADE IN ({placeholders})"""

                params = [codigo_muestra] #+ unidades
                with connection.cursor() as cursor:
                    
                    cursor.execute(sql, params)
                    row = cursor.fetchall()
                
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

        # Lógica para la medición y guardar CSV
        if 'medicion' in request.data:
            codigo_balanza = request.data['codigo_balanza']
            codigo_muestra = request.data['codigo_muestra']
            medicion_valor = request.data['medicion']
            ensayo = request.data['ensayo']
            
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
                creador=request.user.username
            )
            
            fecha = datetime.now().strftime("%d-%m-%Y %H-%M")
            data = {
                'Codigo': [codigo_muestra, codigo_muestra, codigo_muestra],
                'IDVE': [idve, f'Instrum_{idve}', f'Analyst_{idve}'],
                'Fecha': [fecha, fecha, fecha],
                'Valor': [medicion_valor.replace('.', ','), equipo.codigo_interno, request.user.first_name],
            }
            df = pd.DataFrame(data).set_index('Codigo')
            ruta_csv = f'C:/Users/francisco.rotundo/Downloads/{idve}-{datetime.now().strftime("%d-%m-%Y_%H-%M")}.csv'
            df.to_csv(ruta_csv, sep=";")
            
            return Response({"message": f'Se generó el archivo {os.path.basename(ruta_csv)}'}, status=status.HTTP_201_CREATED)
        
        return Response({}, status=status.HTTP_200_OK)

def ejecutable_view(request, nombre):
    # La misma lógica que en tu archivo original
    archivo_path = os.path.join(r'C:\Users\Francisco.Rotundo\Downloads\Proyectos\Nueva carpeta (2)\media', f'{ nombre }.exe')
    if os.path.exists(archivo_path):
        response = FileResponse(open(archivo_path, 'rb'), as_attachment=True, filename=f'{ nombre }.exe')
        response['Content-Type'] = 'application/octet-stream'
        return response
    return HttpResponse('Archivo no encontrado', status=404)