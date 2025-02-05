from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import Persona, Alumno, Curso
from django.db import IntegrityError

@login_required
def buscar_persona_dni(request):
    dni = request.GET.get('dni')
    try:
        persona = Persona.objects.get(dni=dni)
        return JsonResponse({
            'encontrado': True,
            'nombre': persona.nombre,
            'apellido': persona.apellido,
            'email': persona.email,
            'telefono': persona.telefono,
            'id': persona.id
        })
    except Persona.DoesNotExist:
        return JsonResponse({'encontrado': False})

@login_required
def alumno_crear(request):
    ano_lectivo_id = request.session.get('ano_lectivo_id')
    
    if request.method == "POST":
        try:
            persona_id = request.POST.get('persona_id')
            curso_id = request.POST.get('curso')
            
            persona = get_object_or_404(Persona, id=persona_id)
            
            alumno = Alumno(
                persona=persona,
                curso_id=curso_id,
                user=request.user,
                ano_lectivo_id=ano_lectivo_id
            )
            alumno.save()
            return redirect('alumno')
            
        except IntegrityError:
            return render(request, 'alumno/alumno_crear.html', {
                'error': 'Error al crear el alumno'
            })
    
    cursos = Curso.objects.filter(
        user=request.user,
        ano_lectivo_id=ano_lectivo_id
    ).select_related('materia')
    
    return render(request, 'alumno/alumno_crear.html', {'cursos': cursos})

@login_required
def alumno_lista(request):
    ano_lectivo_id = request.session.get('ano_lectivo_id')
    
    # Get alumnos
    alumnos = Alumno.objects.filter(
        user=request.user,
        ano_lectivo_id=ano_lectivo_id
    ).select_related('persona', 'curso')
    
    # Get cursos for dropdown
    cursos = Curso.objects.filter(
        user=request.user,
        ano_lectivo_id=ano_lectivo_id
    ).select_related('materia')
    
    print(f"Año lectivo: {ano_lectivo_id}")
    print(f"Cursos encontrados: {cursos.count()}")
    
    context = {
        'alumnos': alumnos,
        'cursos': cursos,
        'ano_lectivo_id': ano_lectivo_id
    }
    
    return render(request, 'alumno/alumno.html', context)

@login_required
def eliminar_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id, user=request.user)
    if request.method == "POST":
        alumno.delete()
        return redirect('alumno')
    return render(request, 'alumno/alumno_confirmar_eliminar.html', {'alumno': alumno})