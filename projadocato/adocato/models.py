from django.db import models
from datetime import date
# Create your models here.
class Raca(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Gato(models.Model):
    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=[('M', 'Macho'), ('F', 'Fêmea')])
    cor = models.CharField(max_length=50)
    dataNascimento = models.DateField()
    descricao = models.TextField(blank=True, null=True)
    disponivel = models.BooleanField(default=True)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE, related_name='gatos')

    def __str__(self):
        return f"{self.nome} ({self.raca.nome})"
    
    @property
    def idade(self):
        return (date.today() - self.dataNascimento).days // 365