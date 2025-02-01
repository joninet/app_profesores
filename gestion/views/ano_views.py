from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Colegio

from ..forms import ColegioForm, AnoLectivoForm, MateriaForm
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