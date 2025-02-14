from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import get_connection, EmailMessage
from ..models import Nota, Parcial, Alumno, ConfiguracionEmail
from .email_views import enviar_email, configuracion_email
from ..forms import NotaForm, ConfiguracionEmailForm
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
    action = request.POST.get('action')
    
    # Procesar formulario POST
    if request.method == 'POST' and action == 'save':
        for alumno in alumnos:
            nota_value = request.POST.get(f'nota_{alumno.id}')
            if nota_value:
                try:
                    nota_value = float(nota_value)
                    if 0 <= nota_value <= 10:
                        nota_obj, created = Nota.objects.update_or_create(
                            alumno=alumno,
                            parcial=parcial,
                            user=request.user,
                            defaults={'nota': nota_value}
                        )
                        notas_list.append(nota_obj)
                    else:
                        messages.error(request, f'La nota debe estar entre 0 y 10 para {alumno.persona.nombre}')
                except ValueError:
                    messages.error(request, f'Nota inválida para {alumno.persona.nombre}')
        
        if notas_list:
            messages.success(request, 'Notas guardadas correctamente')
        return redirect('registrar_notas', parcial_id=parcial_id)
    
    # Procesar envío de email
    elif request.method == 'POST' and action == 'send_email':
        alumno_id = request.POST.get('alumno_id')
        alumno = get_object_or_404(Alumno, id=alumno_id)
        nota_obj = get_object_or_404(Nota, alumno=alumno, parcial=parcial)
        
        try:
            config = ConfiguracionEmail.objects.get(user=request.user)
            
            # Preparar y enviar email
            subject = f"Nota de {parcial.curso.materia} - {parcial.tema}"
            message = f"""
            Estimado/a {alumno.persona.nombre} {alumno.persona.apellido},
            
            Su nota para {parcial.tema} de {parcial.curso.materia} es: {nota_obj.nota}
            
            Saludos cordiales,
            {request.user.get_full_name()}
            """
            
            if enviar_email(request.user, subject, message, alumno.persona.email):
                messages.success(request, f'Email enviado correctamente a {alumno.persona.nombre}')
            else:
                messages.error(request, 'Error al enviar el email')
                
        except ConfiguracionEmail.DoesNotExist:
            messages.error(request, 'Debe configurar su email primero')
        
        return redirect('registrar_notas', parcial_id=parcial_id)
    
    # Preparar datos para mostrar
    for alumno in alumnos:
        nota_obj, _ = Nota.objects.get_or_create(
            alumno=alumno,
            parcial=parcial,
            user=request.user,
            defaults={'nota': None}
        )
        notas_data.append({
            'alumno': alumno,
            'nota': nota_obj,
            'tiene_email': bool(alumno.persona.email)
        })
    
    return render(request, 'nota/registrar_notas.html', {
        'parcial': parcial,
        'notas_data': notas_data,
        'tiene_config_email': ConfiguracionEmail.objects.filter(user=request.user).exists()
    })