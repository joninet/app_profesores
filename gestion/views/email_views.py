from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend
from ..models import ConfiguracionEmail
from ..forms import ConfiguracionEmailForm

@login_required
def configuracion_email(request):
    config, created = ConfiguracionEmail.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ConfiguracionEmailForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuración guardada')
            return redirect('configuracion_email')
    else:
        form = ConfiguracionEmailForm(instance=config)
        
    return render(request, 'email/email.html', {'form': form})

from django.core.mail import EmailMessage
import smtplib
from email.mime.text import MIMEText

def enviar_email(user, asunto, mensaje, destinatario):
    try:
        config = ConfiguracionEmail.objects.get(user=user)
        
        # Crear servidor SMTP
        server = smtplib.SMTP(config.smtp_server, config.smtp_port)
        server.ehlo()
        
        # Iniciar TLS si está configurado
        if config.use_tls:
            server.starttls()
            server.ehlo()
        
        # Login
        server.login(config.email, config.email_password)
        
        # Crear mensaje
        msg = MIMEText(mensaje)
        msg['Subject'] = asunto
        msg['From'] = config.email
        msg['To'] = destinatario
        
        # Enviar email
        server.send_message(msg)
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"Error enviando email: {str(e)}")
        return False
    
"""Plan

    Configurar correctamente Gmail para usar apps menos seguras
    Generar contraseña de aplicación en Google
    Actualizar el código para usar las credenciales correctamente

Pasos para configurar Gmail:

    Ir a https://myaccount.google.com/security
    Activar verificación en dos pasos
    Crear contraseña de aplicación:
        Ir a "Contraseñas de aplicación"
        Seleccionar "Otra (nombre personalizado)"
        Poner nombre "Django App"
        Copiar la contraseña generada de 16 caracteres

Actualizar configuración en Django admin:

    Ir a /admin/
    Buscar ConfiguracionEmail del usuario
    Actualizar con:
        smtp_server: smtp.gmail.com
        smtp_port: 587
        email: tu.email@gmail.com
        email_password: (pegar contraseña de 16 caracteres generada)
        use_tls: True
"""