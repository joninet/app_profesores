from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import ColegioForm, AnoLectivoForm, MateriaForm, CustomAuthenticationForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Alumno, Materia, Parcial, Curso, Evento, AnoLectivo, Colegio
from datetime import datetime
#Login
def signup(request):
    if request.method == 'GET':
        return render(request, 'auth/signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('colegio')
            except IntegrityError:
                return render(request, 'auth/signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'auth/signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        form = CustomAuthenticationForm()
        # Corregir aquí - usar el modelo AnoLectivo en lugar del form
        form.fields['ano_lectivo'].queryset = AnoLectivo.objects.all()
        return render(request, 'auth/signin.html', {"form": form})
    else:
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            ano_lectivo = form.cleaned_data.get('ano_lectivo')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['ano_lectivo_id'] = ano_lectivo.id
                request.session['ano_lectivo'] = str(ano_lectivo.ano)
                return redirect('colegio')
                
        return render(request, 'auth/signin.html', {
            "form": form,
            "error": "Usuario o contraseña incorrectos"
        })

@login_required
def home(request):
    ano_lectivo_id = request.session.get('ano_lectivo_id')
    
    # Verificar que existe el año lectivo
    if not ano_lectivo_id:
        return render(request, 'home.html', {
            'error': 'Debe seleccionar un año lectivo'
        })
    
    # Obtener últimos 5 registros de cada modelo
    ultimos_alumnos = Alumno.objects.filter(
        user=request.user,
        ano_lectivo_id=ano_lectivo_id
    ).select_related('persona', 'curso', 'curso__materia').order_by('-id')[:5]
    
    ultimas_materias = Materia.objects.filter(
        user=request.user
    ).select_related('colegio').order_by('-id')[:5]
    
    ultimos_parciales = Parcial.objects.filter(
        user=request.user,
        ano_lectivo_id=ano_lectivo_id
    ).select_related('curso__materia').order_by('-fecha')[:5]
    
    ultimos_cursos = Curso.objects.filter(
        user=request.user,
        ano_lectivo_id=ano_lectivo_id
    ).select_related('materia').order_by('-id')[:5]
    
    proximos_eventos = Evento.objects.filter(
        user=request.user,
        ano_lectivo_id=ano_lectivo_id,
    ).order_by('fecha')[:5]
    
    # Imprimir para debug
    print(f"Año lectivo: {ano_lectivo_id}")
    print(f"Alumnos: {ultimos_alumnos.count()}")
    print(f"Materias: {ultimas_materias.count()}")
    print(f"Parciales: {ultimos_parciales.count()}")
    print(f"Cursos: {ultimos_cursos.count()}")
    print(f"Eventos: {proximos_eventos.count()}")
    
    context = {
        'ultimos_alumnos': ultimos_alumnos,
        'ultimas_materias': ultimas_materias,
        'ultimos_parciales': ultimos_parciales,
        'ultimos_cursos': ultimos_cursos,
        'proximos_eventos': proximos_eventos,
    }
    
    return render(request, 'home.html', context)