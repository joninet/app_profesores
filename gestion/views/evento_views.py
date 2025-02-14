from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Evento
from ..forms import EventoForm

@login_required
def evento_lista(request):
    ano_lectivo_id = request.session.get('ano_lectivo_id')
    eventos = Evento.objects.filter(
        user=request.user,
        ano_lectivo_id=ano_lectivo_id
    ).order_by('fecha', 'hora')
    return render(request, 'evento/evento_lista.html', {'eventos': eventos})

from ..tasks import enviar_recordatorio_evento
from django.utils import timezone
from datetime import timedelta

@login_required
def evento_crear(request):
    ano_lectivo_id = request.session.get('ano_lectivo_id')
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.user = request.user
            evento.ano_lectivo_id = ano_lectivo_id
            evento.save()
            
            # Programar recordatorio
            fecha_hora_evento = timezone.make_aware(
                timezone.datetime.combine(evento.fecha, evento.hora)
            )
            tiempo_recordatorio = timedelta(minutes=evento.recordatorio)
            fecha_recordatorio = fecha_hora_evento - tiempo_recordatorio
            
            # Programar tarea
            if fecha_recordatorio > timezone.now():
                enviar_recordatorio_evento.apply_async(
                    args=[evento.id],
                    eta=fecha_recordatorio
                )
                messages.success(request, 'Evento creado y recordatorio programado')
            else:
                messages.success(request, 'Evento creado')
            
            return redirect('evento_lista')
    else:
        form = EventoForm()
    return render(request, 'evento/evento_form.html', {'form': form})

@login_required
def evento_editar(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, user=request.user)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento actualizado exitosamente')
            return redirect('evento_lista')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'evento/evento_form.html', {'form': form, 'evento': evento})

@login_required
def evento_eliminar(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, user=request.user)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento eliminado exitosamente')
    return redirect('evento_lista')