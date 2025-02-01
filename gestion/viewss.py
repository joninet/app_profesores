from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Colegio

from .forms import ColegioForm, AnoLectivoForm, MateriaForm

# Create your views here.
#Login
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('colegio')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})

@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('colegio')

def home(request):
    return render(request, 'home.html')

#Colegios
@login_required
def colegio(request):
    colegios = Colegio.objects.filter(user=request.user)
    return render(request, 'colegio.html', {"colegios": colegios})

@login_required
def crear_colegio(request):
    if request.method == "GET":
        return render(request, 'colegio_crear.html', {"form": ColegioForm})
    else:
        try:
            form = ColegioForm(request.POST)
            new_colegio = form.save(commit=False)
            new_colegio.user = request.user
            new_colegio.save()
            return redirect('colegio')
        except ValueError:
            return render(request, 'colegio_crear.html', {"form": ColegioForm, "error": "Error creating task."})

"""@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')"""

#Ano Lectivo
@login_required
def ano_crear(request):
    if request.method == "GET":
        return render(request, 'ano_crear.html', {"form": AnoLectivoForm})
    else:
        try:
            form = AnoLectivoForm(request.POST)
            if form.is_valid():
                new_ano = form.save(commit=False)
                new_ano.user = request.user
                new_ano.save()
                return redirect('home')
            else:
                return render(request, 'ano_crear.html', {"form": form, "error": form.errors})
        except ValueError:
            return render(request, 'ano_crear.html', {"form": AnoLectivoForm, "error": "Error creating ano."})

#Materia
@login_required
def materia_crear(request):
    if request.method == "GET":
        # Crear formulario vacío con las opciones filtradas por usuario
        form = MateriaForm(user=request.user)
        return render(request, 'materia_crear.html', {'form': form})
    
    if request.method == "POST":
        # Procesar el formulario con los datos enviados
        form = MateriaForm(data=request.POST, user=request.user)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.user = request.user
            materia.save()
            messages.success(request, 'Materia creada exitosamente.')
            return redirect('materia_crear')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    
    return render(request, 'materia_crear.html', {'form': form})
