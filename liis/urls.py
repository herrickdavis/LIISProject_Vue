from django.urls import path
from . import views

urlpatterns = [
    path('equipos/', views.EquipoListCreateAPIView.as_view(), name='equipo-list-create'),
    path('equipos/<int:id>/', views.EquipoRetrieveUpdateDestroyAPIView.as_view(), name='equipo-detail'),
    path('liis/capturar-peso/', views.CapturarPesoAPIView.as_view(), name='capturar-peso'),
    path('ejecutable/<str:nombre>/', views.ejecutable_view, name='ejecutable'),
]
