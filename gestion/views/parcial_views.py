from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Curso, Parcial

from ..forms import AnoLectivoForm, MateriaForm, ParcialForm

@login_required
def parcial(request):
    ano_lectivo_id = request.session.get('ano_lectivo_id')
    
    if not ano_lectivo_id:
        messages.error(request, 'Debe seleccionar un año lectivo')
        return redirect('home')
        
    parciales = Parcial.objects.filter(
        user=request.user, 
        ano_lectivo_id=ano_lectivo_id
    ).select_related('curso', 'ano_lectivo')
    
    form = ParcialForm(user=request.user, ano_lectivo_id=ano_lectivo_id)
    
    return render(request, 'parcial/parcial.html', {
        "parciales": parciales,
        "form": form,
        "ano_lectivo_id": ano_lectivo_id
    })

@login_required
def parcial_crear(request):
    ano_lectivo_id = request.session.get('ano_lectivo_id')
    
    if not ano_lectivo_id:
        messages.error(request, 'Debe seleccionar un año lectivo')
        return redirect('home')
    
    if request.method == "POST":
        form = ParcialForm(
            data=request.POST, 
            user=request.user, 
            ano_lectivo_id=ano_lectivo_id
        )
        if form.is_valid():
            parcial = form.save(commit=False)
            parcial.user = request.user
            parcial.ano_lectivo_id = ano_lectivo_id
            parcial.save()
            messages.success(request, 'Parcial creado exitosamente.')
            return redirect('parcial')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ParcialForm(user=request.user, ano_lectivo_id=ano_lectivo_id)
    
    return render(request, 'parcial/parcial_crear.html', {
        'form': form,
        'ano_lectivo_id': ano_lectivo_id
    })


@login_required
def eliminar_parcial(request, parcial_id):
    parcial = get_object_or_404(Parcial, id=parcial_id, user=request.user)
    if request.method == "POST":
        parcial.delete()
        return redirect('parcial')
    return render(request, 'parcial/parcial_confirmar_eliminar.html', {'parcial': parcial})