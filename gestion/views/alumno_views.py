from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import Persona, Alumno, Curso
from django.db import IntegrityError
from django.db.models import Q
from django.core.paginator import Paginator

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
            
            # Validar datos necesarios
            if not all([persona_id, curso_id, ano_lectivo_id]):
                missing = []
                if not persona_id: missing.append('persona')
                if not curso_id: missing.append('curso')
                if not ano_lectivo_id: missing.append('año lectivo')
                return JsonResponse({
                    'success': False,
                    'error': f'Faltan datos requeridos: {", ".join(missing)}'
                }, status=400)

            print(f"Creating alumno with: persona_id={persona_id}, curso_id={curso_id}, ano_lectivo_id={ano_lectivo_id}")
            
            persona = get_object_or_404(Persona, id=persona_id)
            
            # Verificar si ya existe el alumno en el mismo curso
            existing_alumno = Alumno.objects.filter(
                persona=persona,
                curso_id=curso_id,
                ano_lectivo_id=ano_lectivo_id
            ).first()
            
            if existing_alumno:
                print(f"DEBUG - Alumno already exists in this curso: {existing_alumno.id}")
                return JsonResponse({
                    'success': False,
                    'error': 'El alumno ya está inscrito en este curso'
                }, status=400)
            
            # Crear nuevo alumno
            alumno = Alumno(
                persona=persona,
                curso_id=curso_id,
                user=request.user,
                ano_lectivo_id=ano_lectivo_id
            )
            alumno.save()
            print(f"DEBUG - Alumno created successfully: {alumno.id}")
            
            return JsonResponse({
                'success': True,
                'message': 'Alumno creado correctamente'
            })
            
        except Exception as e:
            print(f"DEBUG - Error creating alumno: {str(e)}")
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

    # Obtener alumnos
    alumnos = Alumno.objects.filter(
        user=request.user,
        ano_lectivo_id=ano_lectivo_id
    ).select_related('persona', 'curso__materia__colegio')

    # Obtener cursos y colegios para los filtros
    cursos = Curso.objects.filter(
        user=request.user,
        ano_lectivo_id=ano_lectivo_id
    ).select_related('materia__colegio')

    # Obtener listas únicas de materias, cursos y colegios
    materias = set(curso.materia.nombre for curso in cursos)
    cursos_lista = set(f"{curso.ano} {curso.division}" for curso in cursos)
    colegios = set(curso.materia.colegio.nombre for curso in cursos)

    # Obtener los valores seleccionados en los filtros
    materia_seleccionada = request.GET.get('materia', '')
    curso_seleccionado = request.GET.get('curso', '')
    colegio_seleccionado = request.GET.get('colegio', '')
    busqueda = request.GET.get('busqueda', '')  # <-- Nuevo campo de búsqueda

    # Aplicar filtros según lo seleccionado
    if materia_seleccionada:
        alumnos = alumnos.filter(curso__materia__nombre=materia_seleccionada)
    
    if curso_seleccionado:
        alumnos = alumnos.filter(curso__ano=curso_seleccionado.split()[0], curso__division=curso_seleccionado.split()[1])

    if colegio_seleccionado:
        alumnos = alumnos.filter(curso__materia__colegio__nombre=colegio_seleccionado)

    if busqueda:
        alumnos = alumnos.filter(
            Q(persona__nombre__icontains=busqueda) | 
            Q(persona__apellido__icontains=busqueda) | 
            Q(persona__dni__icontains=busqueda)
        )

    # Aplicar la paginación solo cuando haya resultados
    paginator = Paginator(alumnos, 20)  # Muestra 20 alumnos por página
    page_number = request.GET.get('page')  # Obtiene el número de página de la URL
    page_obj = paginator.get_page(page_number)  # Obtiene los alumnos de esa página
    alumnos = page_obj  # Asigna los alumnos de la página a la variable alumnos

    context = {
        'alumnos': alumnos,
        'cursos': cursos,
        'materias': materias,
        'cursos_lista': cursos_lista,
        'colegios': colegios,
        'materia_seleccionada': materia_seleccionada,
        'curso_seleccionado': curso_seleccionado,
        'colegio_seleccionado': colegio_seleccionado,
        'busqueda': busqueda,  # <-- Enviar el valor al template
        'ano_lectivo_id': ano_lectivo_id
    }

    return render(request, 'alumno/alumno.html', context)




@login_required
def eliminar_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id, user=request.user)
    if request.method == "POST":
        alumno.delete()
        return redirect('alumno_lista')
    return render(request, 'alumno/alumno_confirmar_eliminar.html', {'alumno': alumno})