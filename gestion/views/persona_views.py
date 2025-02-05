from django.shortcuts import render, redirect, get_object_or_404
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
    ano_lectivo_id = request.session.get('ano_lectivo_id')
    
    if request.method == "GET":
        return render(request, 'persona/persona_crear.html', {"form": PersonaForm})
    else:
        try:
            form = PersonaForm(request.POST)
            if form.is_valid():
                new_persona = form.save(commit=False)
                new_persona.user = request.user
                # Asignar el año lectivo antes de guardar
                if ano_lectivo_id:
                    new_persona.ano_lectivo_id = ano_lectivo_id
                new_persona.save()
                return redirect('persona')
            
        except ValueError:
            return render(request, 'persona/persona_crear.html', 
                        {"form": PersonaForm, 
                         "error": "Error al crear el colegio."})

@login_required
def eliminar_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id, user=request.user)
    if request.method == "POST":
        persona.delete()
        return redirect('persona')
    return render(request, 'persona/persona_confirmar_eliminar.html', {'persona': persona})