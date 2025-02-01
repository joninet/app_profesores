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
#Colegios
@login_required
def colegio(request):
    colegios = Colegio.objects.filter(user=request.user)
    return render(request, 'colegio/colegio.html', {"colegios": colegios})

@login_required
def crear_colegio(request):
    ano_lectivo_id = request.session.get('ano_lectivo_id')
    
    if request.method == "GET":
        return render(request, 'colegio/colegio_crear.html', {"form": ColegioForm})
    else:
        try:
            form = ColegioForm(request.POST)
            if form.is_valid():
                new_colegio = form.save(commit=False)
                new_colegio.user = request.user
                new_colegio.save()
                # Después de guardar el colegio, agregamos el año lectivo
                if ano_lectivo_id:
                    new_colegio.anolectivo.add(ano_lectivo_id)
                return redirect('colegio')
            
        except ValueError:
            return render(request, 'colegio/colegio_crear.html', 
                        {"form": ColegioForm, 
                         "error": "Error al crear el colegio."})