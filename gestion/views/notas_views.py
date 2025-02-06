from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Nota, Parcial, Alumno
from ..forms import NotaForm

@login_required
def seleccionar_parcial(request):
    ano_lectivo_id = request.session.get('ano_lectivo_id')
    parciales = Parcial.objects.filter(
        user=request.user,
        ano_lectivo_id=ano_lectivo_id
    ).select_related('curso__materia')
    
    return render(request, 'nota/seleccionar_parcial.html', {
        'parciales': parciales
    })

@login_required
def registrar_notas(request, parcial_id):
    ano_lectivo_id = request.session.get('ano_lectivo_id')
    parcial = get_object_or_404(Parcial, id=parcial_id, user=request.user)
    
    # Obtener todos los alumnos del curso asociado al parcial
    alumnos = Alumno.objects.filter(
        curso=parcial.curso,  # Changed from parcial.materia.curso
        ano_lectivo_id=ano_lectivo_id
    ).select_related('persona')
    
    # Obtener o crear notas para cada alumno
    notas_data = []
    for alumno in alumnos:
        nota, created = Nota.objects.get_or_create(
            alumno=alumno,
            parcial=parcial,
            user=request.user,
            ano_lectivo_id=ano_lectivo_id,
            defaults={'nota': 0}
        )
        notas_data.append({
            'alumno': alumno,
            'nota': nota,
            'form': NotaForm(instance=nota, prefix=str(alumno.id))
        })
    
    if request.method == 'POST':
        alumno_id = request.POST.get('alumno_id')
        alumno = get_object_or_404(Alumno, id=alumno_id)
        nota = get_object_or_404(Nota, alumno=alumno, parcial=parcial)
        form = NotaForm(request.POST, instance=nota, prefix=str(alumno_id))
        
        if form.is_valid():
            nota = form.save(commit=False)
            nota.user = request.user
            nota.ano_lectivo_id = ano_lectivo_id
            nota.save()
            messages.success(request, 'Nota actualizada correctamente.')
            return redirect('registrar_notas', parcial_id=parcial_id)
    
    return render(request, 'nota/registrar_notas.html', {
        'parcial': parcial,
        'notas_data': notas_data
    })