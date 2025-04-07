from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_cliente, name='cadastrar_cliente'),
]
