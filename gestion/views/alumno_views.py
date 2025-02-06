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
    
    if request.method == 'POST':
        try:
            persona_id = request.POST.get('persona_id')
            curso_id = request.POST.get('curso')
            
            # Validar que tengamos todos los datos necesarios
            if not all([persona_id, curso_id, ano_lectivo_id]):
                return JsonResponse({
                    'success': False,
                    'error': 'Faltan datos requeridos'
                }, status=400)

            # Debug print
            print(f"Creating alumno with: persona_id={persona_id}, curso_id={curso_id}, ano_lectivo_id={ano_lectivo_id}")
            
            persona = get_object_or_404(Persona, id=persona_id)
            
            # Verificar si ya existe el alumno
            if Alumno.objects.filter(persona=persona, ano_lectivo_id=ano_lectivo_id).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'El alumno ya existe en este año lectivo'
                }, status=400)
            
            alumno = Alumno(
                persona=persona,
                curso_id=curso_id,
                user=request.user,
                ano_lectivo_id=ano_lectivo_id
            )
            alumno.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Alumno creado correctamente'
            })
            
        except IntegrityError as e:
            print(f"IntegrityError: {str(e)}")  # Debug print
            return JsonResponse({
                'success': False,
                'error': 'El alumno ya existe o hay un problema con los datos'
            }, status=400)
        except Exception as e:
            print(f"Exception: {str(e)}")  # Debug print
            return JsonResponse({
                'success': False,
                'error': f'Error al crear el alumno: {str(e)}'
            }, status=400)

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