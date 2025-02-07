from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Nota, Parcial, Alumno
from ..forms import NotaForm
import json
from django.core.mail import send_mail

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
    
    alumnos = Alumno.objects.filter(
        curso=parcial.curso,
        ano_lectivo_id=ano_lectivo_id
    ).select_related('persona')
    
    notas_data = []
    notas_list = []
    
    for alumno in alumnos:
        nota_obj, _ = Nota.objects.get_or_create(
            alumno=alumno,
            parcial=parcial,
            user=request.user,
            ano_lectivo_id=ano_lectivo_id,
            defaults={'nota': 0}
        )
        notas_data.append({
            'alumno': alumno,
            'nota': nota_obj,
            'form': NotaForm(instance=nota_obj, prefix=str(alumno.id))
        })
        notas_list.append(float(nota_obj.nota))
    
    promedio_general = sum(notas_list) / len(notas_list) if notas_list else 0.0
    
    if request.method == 'POST':
        alumno_id = request.POST.get('alumno_id')
        action = request.POST.get('action')
        alumno = get_object_or_404(Alumno, id=alumno_id)
        nota_obj = get_object_or_404(Nota, alumno=alumno, parcial=parcial)
        form = NotaForm(request.POST, instance=nota_obj, prefix=str(alumno_id))
        
        if action == 'update':
            if form.is_valid():
                n = form.save(commit=False)
                n.user = request.user
                n.ano_lectivo_id = ano_lectivo_id
                n.save()
                messages.success(request, 'Nota actualizada correctamente.')
        elif action == 'send_email':
            email_destino = alumno.persona.email
            asunto = f"Nota de {alumno.persona.nombre} {alumno.persona.apellido}"
            mensaje = f"Hola {alumno.persona.nombre}, tu nota es: {nota_obj.nota}"
            if email_destino:
                send_mail(
                    asunto,
                    mensaje,
                    'no-reply@tu-dominio.com',
                    [email_destino],
                    fail_silently=False,
                )
                messages.success(request, 'Correo enviado correctamente.')
            else:
                messages.warning(request, 'El alumno no tiene un correo registrado.')
        
        return redirect('registrar_notas', parcial_id=parcial_id)

    # 🔹 Limpia los mensajes ANTES de renderizar la plantilla
    storage = messages.get_messages(request)
    storage.used = True

    return render(request, 'nota/registrar_notas.html', {
        'parcial': parcial,
        'notas_data': notas_data,
        'promedio_general': promedio_general,
        'notas_list': notas_list  # Pasa la lista de notas al contexto
    })
