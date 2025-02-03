from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Colegio, AnoLectivo

from ..forms import ColegioForm, AnoLectivoForm, MateriaForm, CustomAuthenticationForm
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

def home(request):
    ano_lectivo = AnoLectivo.objects.get(id=request.session.get('ano_lectivo_id'))
    anos_lectivos = AnoLectivo.objects.all()
    return render(request, 'home.html', {'ano_lectivo': ano_lectivo, 'anos_lectivos': anos_lectivos})