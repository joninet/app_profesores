from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Curso, Parcial, PreguntaParcial, OpcionPregunta

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
    
    if request.method == 'POST':
        form = ParcialForm(request.POST)
        if form.is_valid():
            parcial = form.save(commit=False)
            parcial.user = request.user
            parcial.ano_lectivo_id = ano_lectivo_id
            parcial.save()
            messages.success(request, 'Parcial creado exitosamente')
            return redirect('parcial')
    else:
        form = ParcialForm()
    
    return render(request, 'parcial/parcial.html', {
        'form': form,
        'parciales': Parcial.objects.filter(user=request.user, ano_lectivo_id=ano_lectivo_id)
    })


@login_required
def eliminar_parcial(request, parcial_id):
    parcial = get_object_or_404(Parcial, id=parcial_id, user=request.user)
    if request.method == "POST":
        parcial.delete()
        return redirect('parcial')
    return render(request, 'parcial/parcial_confirmar_eliminar.html', {'parcial': parcial})

@login_required
def generar_parcial(request, parcial_id):
    parcial = get_object_or_404(Parcial, id=parcial_id, user=request.user)
    preguntas = PreguntaParcial.objects.filter(parcial=parcial).order_by('orden')
    
    if request.method == 'POST':
        pregunta = request.POST.get('pregunta')
        puntaje = request.POST.get('puntaje')
        opciones = request.POST.getlist('opciones[]')
        correctas = request.POST.getlist('correctas[]')
        
        nueva_pregunta = PreguntaParcial.objects.create(
            parcial=parcial,
            pregunta=pregunta,
            puntaje=puntaje,
            orden=preguntas.count() + 1,
            user=request.user
        )
        
        for i, opcion in enumerate(opciones):
            OpcionPregunta.objects.create(
                pregunta=nueva_pregunta,
                opcion=opcion,
                es_correcta=(str(i) in correctas),
                user=request.user
            )
        
        messages.success(request, 'Pregunta agregada correctamente')
        return redirect('generar_parcial', parcial_id=parcial_id)
    
    return render(request, 'parcial/generar_parcial.html', {
        'parcial': parcial,
        'preguntas': preguntas
    })

@login_required
def imprimir_parcial(request, parcial_id):
    parcial = get_object_or_404(Parcial, id=parcial_id, user=request.user)
    preguntas = PreguntaParcial.objects.filter(parcial=parcial).order_by('orden')
    
    return render(request, 'parcial/imprimir_parcial.html', {
        'parcial': parcial,
        'preguntas': preguntas
    })

@login_required
def clonar_parcial(request, parcial_id):
    parcial_original = get_object_or_404(Parcial, id=parcial_id, user=request.user)
    
    # Get all user's courses without año lectivo filter
    cursos = Curso.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = ParcialForm(request.POST)
        if form.is_valid():
            try:
                nuevo_parcial = form.save(commit=False)
                nuevo_parcial.user = request.user
                # Use the año lectivo from the selected course
                nuevo_parcial.ano_lectivo = form.cleaned_data['curso'].ano_lectivo
                nuevo_parcial.save()
                
                # Clone questions and options
                preguntas = PreguntaParcial.objects.filter(parcial=parcial_original)
                for pregunta in preguntas:
                    nueva_pregunta = PreguntaParcial.objects.create(
                        parcial=nuevo_parcial,
                        pregunta=pregunta.pregunta,
                        puntaje=pregunta.puntaje,
                        orden=pregunta.orden,
                        user=request.user
                    )
                    
                    for opcion in pregunta.opcionpregunta_set.all():
                        OpcionPregunta.objects.create(
                            pregunta=nueva_pregunta,
                            opcion=opcion.opcion,
                            es_correcta=opcion.es_correcta,
                            user=request.user
                        )
                
                messages.success(request, 'Parcial clonado exitosamente')
                return redirect('parcial')
            except Exception as e:
                messages.error(request, f'Error al clonar el parcial: {str(e)}')
    else:
        form = ParcialForm(initial={
            'tema': f"Copia de {parcial_original.tema}",
            'fecha': timezone.now().date(),
        })
        form.fields['curso'].queryset = cursos
    
    return render(request, 'parcial/clonar_parcial.html', {
        'form': form,
        'parcial_original': parcial_original
    })