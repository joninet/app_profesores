from django.contrib import admin
from django.urls import path
from gestion.views.auth_views import signup, signin, signout, home
from gestion.views.colegio_views import colegio, crear_colegio, eliminar_colegio
from gestion.views.ano_views import ano_crear
from gestion.views.materia_views import materia_crear
from gestion.views.ano_views import cambiar_ano_lectivo

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('logout/', signout, name='logout'),
    path('signin/', signin, name='signin'),
    path('crear_colegio/', crear_colegio, name='crear_colegio'),
    path('colegio/', colegio, name='colegio'),
    path('ano_crear/', ano_crear, name='ano_crear'),
    path('materia_crear/', materia_crear, name='materia_crear'),
    path('cambiar_ano_lectivo/', cambiar_ano_lectivo, name='cambiar_ano_lectivo'),
    path('colegio/eliminar/<int:colegio_id>/', eliminar_colegio, name='eliminar_colegio'),
]
