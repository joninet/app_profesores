from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Nota, Parcial, Alumno, ConfiguracionEmail
from ..forms import NotaForm
from .email_views import enviar_email

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
            'form': NotaForm(instance=nota_obj, prefix=str(alumno.id)),
            'tiene_email': bool(alumno.persona.email)
        })
        notas_list.append(float(nota_obj.nota))
    
    promedio_general = sum(notas_list) / len(notas_list) if notas_list else 0.0
    
    if request.method == 'POST':
        alumno_id = request.POST.get('alumno_id')
        action = request.POST.get('action')
        alumno = get_object_or_404(Alumno, id=alumno_id)
        nota_obj = get_object_or_404(Nota, alumno=alumno, parcial=parcial)
        
        if action == 'update':
            form = NotaForm(request.POST, instance=nota_obj, prefix=str(alumno_id))
            if form.is_valid():
                n = form.save(commit=False)
                n.user = request.user
                n.ano_lectivo_id = ano_lectivo_id
                n.save()
                messages.success(request, 'Nota actualizada correctamente.')
                
        elif action == 'send_email':
            try:
                config = ConfiguracionEmail.objects.get(user=request.user)
                if alumno.persona.email:
                    # Crear lista de notas rendidas
                    notas_rendidas = [
                        float(nota_obj.nota) if nota_obj.nota is not None else 0,
                        float(nota_obj.recuperatorio1) if nota_obj.recuperatorio1 is not None else None,
                        float(nota_obj.recuperatorio2) if nota_obj.recuperatorio2 is not None else None,
                        float(nota_obj.recuperatorio3) if nota_obj.recuperatorio3 is not None else None,
                        float(nota_obj.recuperatorio4) if nota_obj.recuperatorio4 is not None else None
                    ]
                    
                    # Filtrar solo las notas que no son None
                    notas_validas = [nota for nota in notas_rendidas if nota is not None]
                    
                    # Calcular promedio solo con las notas válidas
                    promedio = sum(notas_validas) / len(notas_validas) if notas_validas else 0
                    
                    asunto = f"Nota de {parcial.curso.materia} - {parcial.tema}"
                    mensaje = f"""
                    Estimado/a {alumno.persona.nombre} {alumno.persona.apellido},
                    
                    Su nota para {parcial.tema} de {parcial.curso.materia} es: {nota_obj.nota}
                    Recuperatorio 1: {nota_obj.recuperatorio1 or 'No rendido'}
                    Recuperatorio 2: {nota_obj.recuperatorio2 or 'No rendido'}
                    Recuperatorio 3: {nota_obj.recuperatorio3 or 'No rendido'}
                    Recuperatorio 4: {nota_obj.recuperatorio4 or 'No rendido'}

                    Promedio general: {promedio:.2f} (calculado sobre {len(notas_validas)} notas)
                    
                    Saludos cordiales,
                    {request.user.get_full_name()}
                    """
                    
                    if enviar_email(request.user, asunto, mensaje, alumno.persona.email):
                        messages.success(request, f'Email enviado correctamente a {alumno.persona.nombre}')
                    else:
                        messages.error(request, 'Error al enviar el email')
                else:
                    messages.warning(request, 'El alumno no tiene un correo registrado.')
                    
            except ConfiguracionEmail.DoesNotExist:
                messages.error(request, 'Debe configurar su email primero')
        
        return redirect('registrar_notas', parcial_id=parcial_id)

    # Limpia los mensajes ANTES de renderizar la plantilla
    storage = messages.get_messages(request)
    storage.used = True

    return render(request, 'nota/registrar_notas.html', {
        'parcial': parcial,
        'notas_data': notas_data,
        'promedio_general': promedio_general,
        'notas_list': notas_list,
        'tiene_config_email': ConfiguracionEmail.objects.filter(user=request.user).exists()
    })