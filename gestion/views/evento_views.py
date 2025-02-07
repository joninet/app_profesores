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
            messages.success(request, 'Evento creado exitosamente')
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