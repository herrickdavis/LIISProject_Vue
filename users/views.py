from django.contrib.auth import authenticate, login, logout
from django.db import connections
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from ldap3 import Server, Connection, NTLM, ALL
import hashlib
from Crypto.Hash import MD4

# 🔧 Parche para restaurar soporte de MD4 en Python 3.13+
hashlib.md4 = lambda data=b'': MD4.new(data)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


def validate_user(username, password):
    domain = 'CORP.ALSGlobal.org'
    user = f'{domain}\\{username}'
    server_address = 'CORP.ALSGlobal.org'
    print(f"Paso 1: Intentando autenticar al usuario '{user}' en LDAP.")
    try:
        server = Server(server_address, get_info=ALL)
        conn = Connection(server, user=user, password=password, authentication=NTLM)
        if conn.bind():
            print(f"Paso 2: Conexión LDAP exitosa para el usuario '{user}'.")
            conn.unbind()
            return True
        else:
            print(f"Paso 2: Conexión LDAP fallida. Detalles: {conn.result}")
            return False
    except Exception as e:
        print(f"Paso 2: Se produjo una excepción en validate_user: {e}")
        return False


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '').lower()
        password = request.data.get('password', '')
        user_mylims = None

        if not username or not password:
            return Response({'error': 'Faltan credenciales'}, status=status.HTTP_400_BAD_REQUEST)

        # 🔑 Paso 1: Autenticación en LDAP
        if validate_user(username, password):
            print("Paso 3: Validación de usuario en la base de datos MSSQL (MYLIMS_PRODUCAO).")
            try:
                # 🔑 Usamos la conexión 'mylims_db' definida en settings.py
                with connections['mylims_db'].cursor() as cursor:
                    sql_query = """
                        SELECT [LOGIN], [FLATIVO], [NMUSUARIO]
                        FROM [dbo].[USUARIO]
                        WHERE [LOGIN] = %s
                    """
                    print(f"Ejecutando consulta SQL en MYLIMS_PRODUCAO: {sql_query} con username={username}")
                    cursor.execute(sql_query, [username])
                    row = cursor.fetchone()

                    if not row:
                        print("Paso 4: Usuario no encontrado en la base de datos MYLIMS_PRODUCAO.")
                        return Response({'error': 'Username sin permiso de acceso.'},
                                        status=status.HTTP_403_FORBIDDEN)

                    db_username, user_status, name_user = row

                    if user_status == 'S':
                        user_mylims = True
                        print("Paso 4: Usuario encontrado en MYLIMS_PRODUCAO y activo.")
                    else:
                        print(f"Paso 4: Usuario '{username}' encontrado, pero con estado inactivo ('{user_status}').")
                        return Response({'error': 'Username sin permiso de acceso.'},
                                        status=status.HTTP_403_FORBIDDEN)

            except Exception as e:
                print(f"Paso 3: Error al conectar con la base de datos MYLIMS_PRODUCAO: {e}")
                return Response({'error': 'Error consultando la base de datos.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # 🔑 Paso 5: Si todo bien en LDAP + MYLIMS, creamos/autenticamos en Django
            if user_mylims:
                print("Paso 5: Autenticación final en Django.")
                pwd = 'h7T-3=aB'  # contraseña dummy para Django

                # Crear usuario en Django si no existe
                if not User.objects.filter(username=username).exists():
                    User.objects.create_user(username=username, password=pwd, first_name=name_user)
                    print(f"Paso 5: Usuario '{username}' creado en Django.")

                # Autenticación interna en Django
                user = authenticate(request, username=username, password=pwd)

                if user:
                    login(request, user)
                    print("Paso 6: Login exitoso. Retornando respuesta.")
                    return Response(
                        {'message': 'Login exitoso', 'username': user.username, 'first_name': user.first_name},
                        status=status.HTTP_200_OK
                    )
                else:
                    print("Paso 6: Error de autenticación interna en Django.")
                    return Response({'error': 'Error de autenticación de Django'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("Paso 3: La validación LDAP falló. Retornando 401.")
            return Response({'error': 'Nombre de usuario o contraseña inválida'},
                            status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Sesión cerrada exitosamente'}, status=status.HTTP_200_OK)

