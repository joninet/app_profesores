from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from ..models import Evento
from ..views.email_views import enviar_email

@shared_task
def enviar_recordatorio_evento(evento_id):
    try:
        evento = Evento.objects.get(id=evento_id)
        if not evento.recordatorio_enviado:
            asunto = f"Recordatorio: {evento.titulo}"
            mensaje = f"""
            Recordatorio de evento:
            
            Título: {evento.titulo}
            Fecha: {evento.fecha.strftime('%d/%m/%Y')}
            Hora: {evento.hora.strftime('%H:%M')}
            Descripción: {evento.descripcion}
            
            Este es un recordatorio automático.
            """
            
            if enviar_email(evento.user, asunto, mensaje, evento.user.email):
                evento.recordatorio_enviado = True
                evento.save()
                return f"Recordatorio enviado para evento {evento.titulo}"
            return f"Error al enviar recordatorio para evento {evento.titulo}"
    except Evento.DoesNotExist:
        return f"Evento {evento_id} no encontrado"