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

@login_required
def colegio(request):
    colegios = Colegio.objects.filter(user=request.user)
    form = ColegioForm()
    return render(request, 'colegio/colegio.html', {
        "colegios": colegios,
        "form": form  # Add form to context
    })

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
                # Asignar el año lectivo antes de guardar
                if ano_lectivo_id:
                    new_colegio.ano_lectivo_id = ano_lectivo_id
                new_colegio.save()
                return redirect('colegio')
            
        except ValueError:
            return render(request, 'colegio/colegio_crear.html', 
                        {"form": ColegioForm, 
                         "error": "Error al crear el colegio."})

@login_required
def eliminar_colegio(request, colegio_id):
    colegio = get_object_or_404(Colegio, id=colegio_id, user=request.user)
    if request.method == "POST":
        colegio.delete()
        return redirect('colegio')
    return render(request, 'colegio/colegio_confirmar_eliminar.html', {'colegio': colegio})