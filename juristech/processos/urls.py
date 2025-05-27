from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_processo, name='cadastrar_processo'),
    path('listar/', views.listar_processos, name='listar_processos'),
    path('upload/<int:processo_id>/', views.upload_documento, name='upload_documento'),
    path('detalhar/<int:processo_id>/', views.detalhar_processo, name='detalhar_processo'),
   path('editar/<int:processo_id>/', views.editar_processo, name='editar_processo'),
]
