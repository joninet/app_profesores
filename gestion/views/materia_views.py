from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Materia

from ..forms import AnoLectivoForm, MateriaForm
@login_required
def materia(request):
    ano_lectivo_id = request.session.get('ano_lectivo_id')
    materias = Materia.objects.filter(
        user=request.user, 
        ano_lectivo_id=ano_lectivo_id
        ).select_related('ano_lectivo')
    form = MateriaForm(user=request.user, ano_lectivo_id=ano_lectivo_id)
    return render(request, 'materia/materia.html', {
        "materias": materias,
        "form": form,
        "ano_lectivo_id": ano_lectivo_id
        })
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
                return redirect('materia')
        except ValueError:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    
    return render(request, 'materia/materia_crear.html', {'form': form})

@login_required
def eliminar_materia(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id, user=request.user)
    if request.method == "POST":
        materia.delete()
        return redirect('materia')
    return render(request, 'materia/materia_confirmar_eliminar.html', {'materia': materia})