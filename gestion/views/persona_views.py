from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Persona
from ..forms import PersonaForm, AnoLectivoForm

@login_required
def persona(request):
    personas = Persona.objects.filter(
        user=request.user
        )
    form = PersonaForm()
    return render(request, 'persona/persona.html', {
        "personas": personas,
        "form": form
    })

@login_required
def crear_persona(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            try:
                persona = form.save(commit=False)
                persona.user = request.user
                persona.save()
                return JsonResponse({'success': True, 'message': 'Persona creada correctamente'})
            except IntegrityError as e:
                # Si el error proviene de la constraint 'dni'
                if 'unique' in str(e).lower() and 'dni' in str(e).lower():
                    return JsonResponse({'success': False, 'error': 'El DNI ingresado ya existe en la base de datos'})
                return JsonResponse({'success': False, 'error': f'Error de integridad: {e}'})
        else:
            # Si el form es inválido, revisa si el error está en ‘dni’
            if 'dni' in form.errors:
                return JsonResponse({'success': False, 'error': 'El DNI ingresado ya existe en la base de datos'})
            return JsonResponse({'success': False, 'error': 'Por favor verifique los datos ingresados'})
    else:
        form = PersonaForm()
    return render(request, 'persona/persona.html', {
        'form': form,
        'personas': Persona.objects.all()
    })
@login_required
def eliminar_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id, user=request.user)
    if request.method == "POST":
        persona.delete()
        return redirect('persona')
    return render(request, 'persona/persona_confirmar_eliminar.html', {'persona': persona})

@login_required
def persona_editar(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)
    if request.method == 'POST':
        try:
            data = request.POST.dict()
            for field in ['nombre', 'apellido', 'dni', 'email', 'telefono']:
                setattr(persona, field, data.get(field, '').upper())
            persona.fecha_nacimiento = data.get('fecha_nacimiento')
            persona.save()
            return JsonResponse({
                'success': True,
                'message': 'Persona editada correctamente'
            })
        except IntegrityError as e:
            if 'unique' in str(e).lower() and 'dni' in str(e).lower():
                return JsonResponse({
                    'success': False,
                    'error': 'El DNI ingresado ya existe en la base de datos'
                })
            return JsonResponse({
                'success': False, 
                'error': 'Por favor verifique los datos ingresados'
            })
    return JsonResponse({'success': False, 'error': 'Método no permitido'})