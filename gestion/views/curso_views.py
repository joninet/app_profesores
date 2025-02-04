from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Curso

from ..forms import AnoLectivoForm, CursoForm

@login_required
def curso(request):
    ano_lectivo_id = request.session.get('ano_lectivo_id')
    cursos = Curso.objects.filter(
        user=request.user, 
        ano_lectivo_id=ano_lectivo_id
        ).select_related('ano_lectivo')
    form = CursoForm(user=request.user, ano_lectivo_id=ano_lectivo_id)
    return render(request, 'curso/curso.html', {
        "cursos": cursos,
        "form": form,
        "ano_lectivo_id": ano_lectivo_id
        })

@login_required
def curso_crear(request):
    ano_lectivo_id = request.session.get('ano_lectivo_id')
    
    if request.method == "GET":
        form = CursoForm(user=request.user)
        return render(request, 'curso/curso_crear.html', {'form': form})
    else:
        try:
            form = CursoForm(data=request.POST, user=request.user)
            if form.is_valid():
                curso = form.save(commit=False)
                curso.user = request.user
                if ano_lectivo_id:
                    curso.ano_lectivo_id = ano_lectivo_id
                curso.save()
                messages.success(request, 'Materia creada exitosamente.')
                return redirect('curso')
        except ValueError:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    
    return render(request, 'curso/curso_crear.html', {'form': form})

@login_required
def eliminar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id, user=request.user)
    if request.method == "POST":
        curso.delete()
        return redirect('curso')
    return render(request, 'curso/curso_confirmar_eliminar.html', {'curso': curso})