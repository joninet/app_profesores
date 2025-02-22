from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Colegio, AnoLectivo, Materia, AnoLectivo, Curso, Persona, Alumno, Parcial, Nota, Evento, ConfiguracionEmail

class CustomAuthenticationForm(AuthenticationForm):
    ano_lectivo = forms.ModelChoiceField(
        queryset=AnoLectivo.objects.all(),
        empty_label="Seleccione un año lectivo",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

class ColegioForm(ModelForm):
    class Meta:
        model = Colegio
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del colegio'
            })
        }

class AnoLectivoForm(ModelForm):
    class Meta:
        model = AnoLectivo
        fields = ['ano', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['nombre', 'colegio']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la materia'
            }),
            'colegio': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        ano_lectivo_id = kwargs.pop('ano_lectivo_id', None)
        super(MateriaForm, self).__init__(*args, **kwargs)
        
        if user and ano_lectivo_id:
            self.fields['colegio'].queryset = Colegio.objects.filter(
                user=user,
                ano_lectivo_id=ano_lectivo_id
            ).select_related('ano_lectivo')

ANO_CHOICES = [
    ('PRIMERO', 'PRIMERO'),
    ('SEGUNDO', 'SEGUNDO'),
    ('TERCERO', 'TERCERO'),
    ('CUARTO', 'CUARTO'),
    ('QUINTO', 'QUINTO'),
    ('SEXTO', 'SEXTO'),
    ('SEPTIMO', 'SEPTIMO'),
]

class CursoForm(forms.ModelForm):
    ano = forms.ChoiceField(
        choices=ANO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Curso
        fields = ['ano', 'division', 'materia']
        widgets = {
            'division': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'materia': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def clean_division(self):
        division = self.cleaned_data.get('division')
        return division.upper() if division else division

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        ano_lectivo_id = kwargs.pop('ano_lectivo_id', None)
        super(CursoForm, self).__init__(*args, **kwargs)
        
        if user and ano_lectivo_id:
            self.fields['materia'].queryset = Materia.objects.filter(
                user=user,
                ano_lectivo_id=ano_lectivo_id
            ).select_related('ano_lectivo')

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'dni', 'fecha_nacimiento', 'email', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese los nombres'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese los apellidos'
            }),
            'dni': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el DNI'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@correo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el teléfono'
            })
        }
    def clean(self):
        cleaned_data = super().clean()
        for field in ['nombre', 'apellido', 'dni', 'email', 'telefono']:
            value = cleaned_data.get(field)
            if value:
                cleaned_data[field] = value.upper()
        return cleaned_data

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['curso']
        widgets = {
            'curso': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        ano_lectivo_id = kwargs.pop('ano_lectivo_id', None)
        super(AlumnoForm, self).__init__(*args, **kwargs)
        
        if user and ano_lectivo_id:
            self.fields['curso'].queryset = Curso.objects.filter(
                user=user,
                ano_lectivo_id=ano_lectivo_id
            ).select_related('materia')

class ParcialForm(forms.ModelForm):
    class Meta:
        model = Parcial
        fields = ['tema', 'fecha', 'curso']
        widgets = {
            'tema': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'curso': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        ano_lectivo_id = kwargs.pop('ano_lectivo_id', None)
        super().__init__(*args, **kwargs)
        
        if user and ano_lectivo_id:
            self.fields['curso'].queryset = Curso.objects.filter(
                user=user,
                ano_lectivo_id=ano_lectivo_id
            )

from django import forms
from .models import Nota, Parcial

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['nota', 'recuperatorio1', 'recuperatorio2', 'recuperatorio3', 'recuperatorio4']
        widgets = {
            'nota': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'recuperatorio1': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'recuperatorio2': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'recuperatorio3': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'recuperatorio4': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
        }

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'fecha', 'hora', 'recordatorio']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'recordatorio': forms.Select(attrs={'class': 'form-control'})
        }

class ConfiguracionEmailForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionEmail
        fields = ['email', 'smtp_server', 'smtp_port', 'use_tls', 'email_password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'smtp_server': forms.TextInput(attrs={'class': 'form-control'}),
            'smtp_port': forms.NumberInput(attrs={'class': 'form-control'}),
            'use_tls': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese contraseña de 16 digitos'
            })
        }