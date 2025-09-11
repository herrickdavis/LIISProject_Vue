from datetime import datetime, timedelta
from django.shortcuts import redirect

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener la última actividad del usuario
        last_activity = request.session.get('last_activity')
        if last_activity:
            last_activity_time = datetime.fromisoformat(last_activity)
        else:
            last_activity_time = datetime.now()

        # Actualizar la última actividad del usuario
        request.session['last_activity'] = datetime.now().isoformat()
        request.session.modified = True

        # Comprobar si ha pasado suficiente tiempo desde la última actividad
        inactive_time = datetime.now() - last_activity_time
        if inactive_time > timedelta(minutes=30):
            # La sesión ha expirado, cerrar la sesión del usuario
            request.session.flush()
            return redirect('users:login')

        response = self.get_response(request)
        return response