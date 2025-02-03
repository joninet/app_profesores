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
    ano_lectivo_id = request.session.get('ano_lectivo_id')
    
    if request.method == "GET":
        form = MateriaForm(user=request.user)
        return render(request, 'materia/materia_crear.html', {'form': form})
    else:
        try:
            form = MateriaForm(data=request.POST, user=request.user)
            if form.is_valid():
                materia = form.save(commit=False)
                materia.user = request.user
                if ano_lectivo_id:
                    materia.ano_lectivo_id = ano_lectivo_id
                materia.save()
                messages.success(request, 'Materia creada exitosamente.')
                return redirect('materia_crear')
        except ValueError:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    
    return render(request, 'materia/materia_crear.html', {'form': form})