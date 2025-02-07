from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class AnoLectivo(models.Model):
    ano = models.PositiveIntegerField(unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ano)

class Colegio(models.Model):
    nombre = models.CharField(max_length=200)
    ano_lectivo = models.ForeignKey(
        AnoLectivo, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Materia(models.Model):
    nombre = models.CharField(max_length=200)
    colegio = models.ForeignKey(Colegio, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ano_lectivo = models.ForeignKey(AnoLectivo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.colegio.nombre}"

    class Meta:
        ordering = ['nombre']

class Curso(models.Model):
    ano = models.CharField(max_length=255)
    division = models.CharField(max_length=255)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    ano_lectivo = models.ForeignKey(AnoLectivo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ano} {self.division} - {self.materia} - {self.ano_lectivo}"

    class Meta:
        ordering = ['ano']

class Persona(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    dni = models.CharField(max_length=10)
    fecha_nacimiento = models.DateField()
    email = models.EmailField()
    telefono = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['apellido', 'nombre']
        unique_together = ['dni']

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

class Alumno(models.Model):
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        # Remove unique=True if exists
    )
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ano_lectivo = models.ForeignKey('AnoLectivo', on_delete=models.CASCADE)

    class Meta:
        # Add unique_together instead of unique on persona
        unique_together = ['persona', 'curso', 'ano_lectivo']

class Parcial(models.Model):
    tema = models.CharField(max_length=200)
    fecha = models.DateField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ano_lectivo = models.ForeignKey(AnoLectivo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tema} - {self.curso.materia.nombre}"

class Nota(models.Model):
    nota = models.DecimalField(max_digits=5, decimal_places=2)
    recuperatorio1 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    recuperatorio2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    recuperatorio3 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    recuperatorio4 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    parcial = models.ForeignKey(Parcial, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ano_lectivo = models.ForeignKey(AnoLectivo, on_delete=models.CASCADE)

    def calcular_promedio(self):
        notas = [self.nota]
        if self.recuperatorio1:
            notas.append(self.recuperatorio1)
        if self.recuperatorio2:
            notas.append(self.recuperatorio2)
        if self.recuperatorio3:
            notas.append(self.recuperatorio3)
        if self.recuperatorio4:
            notas.append(self.recuperatorio4)
        
        return sum(notas) / len(notas) if notas else 0

    def __str__(self):
        return f"{self.parcial.tema} - {self.alumno.persona.apellido}, {self.alumno.persona.nombre} - {self.nota}"

    class Meta:
        ordering = ['parcial__fecha']

class PreguntaParcial(models.Model):
    parcial = models.ForeignKey(Parcial, on_delete=models.CASCADE)
    pregunta = models.TextField()
    puntaje = models.DecimalField(max_digits=5, decimal_places=2)
    orden = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['orden']

class OpcionPregunta(models.Model):
    pregunta = models.ForeignKey(PreguntaParcial, on_delete=models.CASCADE)
    opcion = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Evento(models.Model):
    REMINDER_CHOICES = [
        (15, '15 minutos antes'),
        (30, '30 minutos antes'),
        (60, '1 hora antes'),
        (120, '2 horas antes'),
        (1440, '1 día antes'),
        (10080, '1 semana antes'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ano_lectivo = models.ForeignKey(AnoLectivo, on_delete=models.CASCADE)
    recordatorio = models.IntegerField(choices=REMINDER_CHOICES, default=60)
    recordatorio_enviado = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f"{self.titulo} - {self.fecha}"

    def debe_enviar_recordatorio(self):
        if self.recordatorio_enviado:
            return False
            
        fecha_hora_evento = datetime.combine(self.fecha, self.hora)
        tiempo_recordatorio = timedelta(minutes=self.recordatorio)
        ahora = datetime.now()
        
        return (fecha_hora_evento - tiempo_recordatorio) <= ahora < fecha_hora_evento