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
        return f"{self.ano} {self.division} - {self.materia.nombre}"

    class Meta:
        ordering = ['ano']