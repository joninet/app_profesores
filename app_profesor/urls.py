from django.contrib import admin
from django.urls import path
from gestion.views.auth_views import signup, signin, signout, home
from gestion.views.colegio_views import colegio, crear_colegio, eliminar_colegio
from gestion.views.ano_views import ano_crear
from gestion.views.materia_views import materia_crear, materia, eliminar_materia
from gestion.views.ano_views import cambiar_ano_lectivo
from gestion.views.curso_views import curso, curso_crear, eliminar_curso

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    #Auth
    path('signup/', signup, name='signup'),
    path('logout/', signout, name='logout'),
    path('signin/', signin, name='signin'),
    #Colegio
    path('crear_colegio/', crear_colegio, name='crear_colegio'),
    path('colegio/', colegio, name='colegio'),
    path('colegio/eliminar/<int:colegio_id>/', eliminar_colegio, name='eliminar_colegio'),
    #Año Lectivo
    path('ano_crear/', ano_crear, name='ano_crear'),
    path('cambiar_ano_lectivo/', cambiar_ano_lectivo, name='cambiar_ano_lectivo'),
    #Materia
    path('materia/', materia, name='materia'),
    path('materia_crear/', materia_crear, name='materia_crear'),
    path('materia/eliminar/<int:materia_id>/', eliminar_materia, name='eliminar_materia'),
    #Curso
    path('curso/', curso, name='curso'),
    path('curso_crear/', curso_crear, name='curso_crear'),
    path('curso/eliminar/<int:curso_id>/', eliminar_curso, name='eliminar_curso'),
]
