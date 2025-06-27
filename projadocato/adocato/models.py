from django.db import models
from django.contrib.auth.models import User
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
    dataNascimento = models.DateField(verbose_name='Data de Nascimento')
    descricao = models.TextField(verbose_name="Descrição",blank=True, null=True)
    disponivel = models.BooleanField(default=True)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE, related_name='gatos')
    foto = models.ImageField(upload_to='gatos/', blank=True, null=True)
    def __str__(self):
        return f"{self.nome} ({self.raca.nome})"
    
    @property
    def idade(self):
        return (date.today() - self.dataNascimento).days // 365
    def esta_disponivel(self):
        """Verifica se o gato está disponível para adoção."""
        return "Sim" if self.disponivel else "Não"

class Coordenador(User):
    nome= models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return self.nome