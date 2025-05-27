from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from processos.views import home_view
import debug_toolbar

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home_view, name='home'),
    path('clientes/', include('clientes.urls')),
    path('processos/', include('processos.urls')),
    path('usuarios/', include('usuarios.urls')),
    path("__debug__/", include(debug_toolbar.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
