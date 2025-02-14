from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Colegio, AnoLectivo
from django.http import JsonResponse

from ..forms import ColegioForm, AnoLectivoForm, MateriaForm
#Ano Lectivo
@login_required
def ano_crear(request):
    if request.method == "GET":
        return render(request, 'ano_crear.html', {"form": AnoLectivoForm})
    else:
        try:
            form = AnoLectivoForm(request.POST)
            if form.is_valid():
                new_ano = form.save(commit=False)
                new_ano.user = request.user
                new_ano.save()
                return redirect('home')
            else:
                return render(request, 'ano_crear.html', {"form": form, "error": form.errors})
        except ValueError:
            return render(request, 'ano_crear.html', {"form": AnoLectivoForm, "error": "Error creating ano."})

@login_required
def mostrar_ano_lectivo(request):
    ano_lectivo_id = request.session.get('ano_lectivo_id')
    return redirect('ano_lectivo', ano_lectivo_id=ano_lectivo_id)

@login_required
def cambiar_ano_lectivo(request):
    if request.method == 'POST':
        ano_lectivo_id = request.POST.get('ano_lectivo_id')
        try:
            ano_lectivo = AnoLectivo.objects.get(id=ano_lectivo_id)
            request.session['ano_lectivo_id'] = ano_lectivo.id
            request.session['ano_lectivo'] = str(ano_lectivo.ano)
            return JsonResponse({'success': True, 'ano_lectivo': ano_lectivo.ano})
        except AnoLectivo.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Año lectivo no encontrado.'})
    return JsonResponse({'success': False, 'error': 'Método no permitido.'})

@login_required
def ano_lectivo_lista(request):
    ano_lectivo_actual = request.session.get('ano_lectivo')
    anos_lectivos = AnoLectivo.objects.filter()
    return render(request, 'ano_lectivo.html', {
        'ano_lectivo_actual': ano_lectivo_actual,
        'anos_lectivos': anos_lectivos
    })