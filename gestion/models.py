from django.db import models
from django.contrib.auth.models import User

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
        return f"{self.ano} {self.division} - {self.materia}"

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
    tema = models.CharField(max_length=255)
    fecha = models.DateField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)  # Changed from materia
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