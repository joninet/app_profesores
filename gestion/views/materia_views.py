from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Colegio

from ..forms import ColegioForm, AnoLectivoForm, MateriaForm
#Materia
@login_required
def materia_crear(request):
    if request.method == "GET":
        # Crear formulario vacío con las opciones filtradas por usuario
        form = MateriaForm(user=request.user)
        return render(request, 'materia/materia_crear.html', {'form': form})
    
    if request.method == "POST":
        # Procesar el formulario con los datos enviados
        form = MateriaForm(data=request.POST, user=request.user)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.user = request.user
            materia.save()
            messages.success(request, 'Materia creada exitosamente.')
            return redirect('materia_crear')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    
    return render(request, 'materia/materia_crear.html', {'form': form})