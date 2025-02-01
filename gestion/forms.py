from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Colegio, AnoLectivo, Materia, AnoLectivo

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

class AnoLectivoForm(ModelForm):
    class Meta:
        model = AnoLectivo
        fields = ['ano', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

class MateriaForm(ModelForm):
    class Meta:
        model = Materia
        fields = ['nombre', 'colegio', 'ano_lectivo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la materia'
            }),
            'colegio': forms.Select(attrs={
                'class': 'form-control'
            }),
            'ano_lectivo': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        # Extraer el usuario de kwargs antes de llamar a super()
        user = kwargs.pop('user', None)
        super(MateriaForm, self).__init__(*args, **kwargs)
        
        if user:
            # Filtrar para mostrar solo los colegios del usuario
            self.fields['colegio'].queryset = Colegio.objects.filter(user=user)
            # Filtrar para mostrar solo los años lectivos del usuario
            self.fields['ano_lectivo'].queryset = AnoLectivo.objects.filter(user=user)