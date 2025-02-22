from django.contrib import admin
from django.urls import path
from gestion.views.auth_views import signup, signin, signout, home
from gestion.views.colegio_views import colegio, crear_colegio, eliminar_colegio
from gestion.views.ano_views import ano_crear
from gestion.views.materia_views import materia_crear, materia, eliminar_materia
from gestion.views.ano_views import cambiar_ano_lectivo, ano_lectivo_lista
from gestion.views.curso_views import curso, curso_crear, eliminar_curso
from gestion.views.alumno_views import buscar_persona_dni, alumno_crear, alumno_lista, eliminar_alumno
from gestion.views.persona_views import persona, crear_persona, eliminar_persona, persona_editar
from gestion.views.parcial_views import parcial, parcial_crear, eliminar_parcial, generar_parcial, imprimir_parcial, clonar_parcial
from gestion.views.notas_views import seleccionar_parcial, registrar_notas
from gestion.views.limpiar_views import limpiar_mensajes
from gestion.views.evento_views import evento_lista, evento_crear, evento_editar, evento_eliminar
from gestion.views.email_views import configuracion_email

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('limpiar-mensajes/', limpiar_mensajes, name='limpiar_mensajes'),
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
    path('ano-lectivo/', ano_lectivo_lista, name='ano_lectivo_lista'),
    path('ano-lectivo/cambiar/', cambiar_ano_lectivo, name='cambiar_ano_lectivo'),
    #Materia
    path('materia/', materia, name='materia'),
    path('materia_crear/', materia_crear, name='materia_crear'),
    path('materia/eliminar/<int:materia_id>/', eliminar_materia, name='eliminar_materia'),
    #Curso
    path('curso/', curso, name='curso'),
    path('curso_crear/', curso_crear, name='curso_crear'),
    path('curso/eliminar/<int:curso_id>/', eliminar_curso, name='eliminar_curso'),
    #persona
    path('persona/', persona, name='persona'),
    path('crear_persona/', crear_persona, name='crear_persona'),
    path('persona/eliminar/<int:persona_id>/', eliminar_persona, name='eliminar_persona'),
    path('persona/editar/<int:persona_id>/', persona_editar, name='persona_editar'),
    #Alumno
    path('alumno/buscar-dni/', buscar_persona_dni, name='buscar_persona_dni'),
    path('alumno/crear/', alumno_crear, name='alumno_crear'),
    path('alumno/', alumno_lista, name='alumno_lista'),
    path('alumno/eliminar/<int:alumno_id>/', eliminar_alumno, name='eliminar_alumno'),
    #Parcial
    path('parcial/', parcial, name='parcial'),
    path('parcial_crear/', parcial_crear, name='parcial_crear'),
    path('parcial/eliminar/<int:parcial_id>/', eliminar_parcial, name='eliminar_parcial'),
    path('parcial/<int:parcial_id>/generar/', generar_parcial, name='generar_parcial'),
    path('parcial/<int:parcial_id>/imprimir/', imprimir_parcial, name='imprimir_parcial'),
    path('parcial/<int:parcial_id>/clonar/', clonar_parcial, name='clonar_parcial'),
    #Notas
    path('notas/', seleccionar_parcial, name='seleccionar_parcial'),
    path('notas/<int:parcial_id>/', registrar_notas, name='registrar_notas'),
    #Evento
    path('eventos/', evento_lista, name='evento_lista'),
    path('eventos/crear/', evento_crear, name='evento_crear'),
    path('eventos/<int:evento_id>/editar/', evento_editar, name='evento_editar'),
    path('eventos/<int:evento_id>/eliminar/', evento_eliminar, name='evento_eliminar'),
    #email
    path('configuracion/email/', configuracion_email, name='configuracion_email'),
]
