from django.db import models
from datetime import date,datetime, timedelta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .utils import Utilitaria
class Raca(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def clean(self):
        erros = {}
        if len(self.nome) < 3:
            erros['nome'] = "O nome da raça deve ter pelo menos 3 caracteres."
        if erros:
            raise ValidationError(erros)
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    class Meta:
        verbose_name_plural = "Raças"
        verbose_name="Raça"
        ordering = ['nome']


class Gato(models.Model):
    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=[('M', 'Macho'), ('F', 'Fêmea')])
    cor = models.CharField(max_length=50)
    dataNascimento = models.DateField()
    descricao = models.TextField(blank=True, null=True)
    disponivel = models.BooleanField(default=True)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE, related_name='gatos')
    foto= models.ImageField(upload_to='gatos/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.nome} ({self.raca.nome})"
    @property
    def idade(self):
        return (date.today() - self.dataNascimento).days // 365
    def clean(self):
        erros={}
        if isinstance(self.dataNascimento, str):
            try:
                data_nasc = datetime.strptime(self.dataNascimento, "%Y-%m-%d").date()
            except ValueError:
                erros['dataNascimento'] = "Formato de data de nascimento inválido. Use AAAA-MM-DD."
                data_nasc = None
        else:
            data_nasc = self.dataNascimento
        if data_nasc and data_nasc > date.today():
            erros['dataNascimento'] = "A data de nascimento não pode ser no futuro."
        if len(self.nome) < 3:
            erros['nome']="O nome do gato deve ter pelo menos 3 caracteres."
        if len(self.cor) < 3:
            erros['cor']="A cor do gato deve ter pelo menos 3 caracteres."
        if not self.raca:
            erros="O gato deve ter uma raça associada."
        if erros:
            raise ValidationError(erros)

class Adotante(User):
    nome= models.CharField(max_length=100)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    dataNascimento = models.DateField(verbose_name="Data de Nascimento")
    cpf=models.CharField(max_length=11, unique=True, verbose_name="CPF")
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return self.nome
    def clean(self):
        erros={}
        if len(self.username) < 3:
            erros['username']="O nome de usuário deve ter pelo menos 3 caracteres."
        if len(self.password) < 6:
            erros['password']="A senha deve ter pelo menos 6 caracteres."
        if len(self.nome) < 3:
            erros['nome']="O nome do adotante deve ter pelo menos 3 caracteres."
        if len(self.cpf) != 11 or not self.cpf.isdigit():
            erros['cpf']="O CPF deve ter 11 dígitos numéricos."
        if len(self.telefone) < 10 or len(self.telefone) > 15:
            erros['telefone']="O telefone deve ter entre 10 e 15 caracteres."
        if self.telefone and not self.telefone.isdigit():
            erros['telefone']="O telefone deve conter apenas dígitos numéricos."
        if not self.dataNascimento:
            erros['dataNascimento']="A data de nascimento é obrigatória."
        if self.dataNascimento > date.today():
            erros['dataNascimento'] = "A data de nascimento não pode ser no futuro."
        else:
            idade = (date.today() - self.dataNascimento).days // 365
            if idade < 18:
                erros['dataNascimento'] = "O adotante deve ter mais de 18 anos."
        if erros:
            raise ValidationError(erros)
    def cpf_formatado(self):
        """Retorna o CPF formatado como XXX.XXX.XXX-XX."""
        if self.cpf:
            return Utilitaria.formatar_cpf(self.cpf)
        return self.cpf

    class Meta:
        verbose_name_plural = "Adotantes"
        verbose_name = "Adotante"
        ordering = ['nome']
class Coordenador(User):
    nome= models.CharField(max_length=100)
    cpf=models.CharField(max_length=11, unique=True, verbose_name="CPF")
    
    def cpf_formatado(self):
        """Retorna o CPF formatado como XXX.XXX.XXX-XX."""
        if self.cpf:
            return Utilitaria.formatar_cpf(self.cpf)
        return self.cpf
    
    def __str__(self):
        return self.nome
    def clean(self):
        erros={}
        if len(self.username) < 3:
            erros['username']="O nome de usuário deve ter pelo menos 3 caracteres."
        if len(self.password) < 6:
            erros['password']="A senha deve ter pelo menos 6 caracteres."
        if len(self.nome) < 3:
            erros['nome']="O nome do coordenador deve ter pelo menos 3 caracteres."
        if len(self.cpf) != 11 or not self.cpf.isdigit():
            erros['cpf']="O CPF deve ter 11 dígitos numéricos."
        if erros:
            raise ValidationError(erros)
    class Meta:
        verbose_name_plural = "Coordenadores"
        verbose_name = "Coordenador"
        ordering = ['nome']

class Solicitacao(models.Model):
    adotante = models.ForeignKey(Adotante, on_delete=models.CASCADE, related_name='solicitacoes_adotante')
    gato = models.ForeignKey(Gato, on_delete=models.CASCADE, related_name='solicitacoes_gato')
    dataSolicitacao = models.DateTimeField(auto_now=True) #Modificado para auto_now=True para registrar a data e hora da solicitação automaticamente
    status = models.CharField(max_length=20, choices=[('Em_Analise', 'Em Análise'), ('Aprovada', 'Aprovada'), ('Reprovada', 'Reprovada'),('Em_Recurso','Em Recurso')], default='Reprovada')
    recurso= models.TextField(blank=True, null=True, verbose_name="Motivo do Recurso")
    avaliadores = models.ManyToManyField(Coordenador, blank=True, related_name='avaliacoes_solicitadas',through='Avaliacao')
    def esta_atrasado(self):
        """Verifica se a solicitação está atrasada."""
        prazo = self.dataSolicitacao + timedelta(days=7) #Nesse caso, seria necessário atualizar a data da solicitação para o dia atual quando o status for 'Em Recurso'
        return (self.status == 'Em_Analise' or self.status == 'Em_Recurso') and datetime.now() > prazo 
    
    def clean(self):
        erros={}
        if not self.adotante:
            erros['adotante'] = "O adotante é obrigatório."
        if not self.gato:
            erros['gato'] = "O gato é obrigatório."
        if self.status not in ['Em_Analise', 'Aprovada', 'Reprovada', 'Em_Recurso']:
            erros['status'] = "Status inválido."
        if self.status == 'Em_Recurso' and not self.recurso:    
            erros['recurso'] = "O motivo do recurso é obrigatório quando o status é 'Em Recurso'."
        if erros:
            raise ValidationError(erros)
    
    

    def __str__(self):
        return f"{self.adotante.nome} - {self.gato.nome} ({self.status})"
    
    class Meta:
        verbose_name_plural = "Solicitações"
        verbose_name = "Solicitação"
        ordering = ['-dataSolicitacao']

class Avaliacao(models.Model):
    solicitacao = models.ForeignKey(Solicitacao, on_delete=models.CASCADE, related_name='avaliacoes')
    coordenador = models.ForeignKey(Coordenador, on_delete=models.CASCADE, related_name='avaliacoes')
    dataAvaliacao = models.DateTimeField(auto_now_add=True)
    
    parecer = models.TextField(blank=True, null=True)
    
    def clean(self):
        erros={}
        if not self.solicitacao:
            erros['solicitacao'] = "A solicitação é obrigatória."
        if not self.coordenador:
            erros['coordenador'] = "O coordenador é obrigatório."
        if not self.parecer:
            erros['parecer'] = "O parecer é obrigatório."
        if erros:
            raise ValidationError(erros)
    
    def __str__(self):
        return f"{self.coordenador.nome} - {self.solicitacao.gato.nome}"
    
    class Meta:
        verbose_name_plural = "Avaliações"
        verbose_name = "Avaliação"
        ordering = ['-dataAvaliacao']

class Documento(models.Model):
    solicitacao = models.ForeignKey(Solicitacao, on_delete=models.CASCADE, related_name='documentos')
    arquivo = models.FileField(upload_to='documentos/', verbose_name="Arquivo")
    descricao = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descrição")
    enviado_em = models.DateTimeField(auto_now_add=True, verbose_name="Enviado em")
    
    def clean(self):
        erros={}
        if not self.solicitacao:
            erros['solicitacao'] = "A solicitação é obrigatória."
        if not self.arquivo:
            erros['arquivo'] = "O arquivo é obrigatório."
        if len(self.descricao) < 3:
            erros['descricao'] = "A descrição deve ter pelo menos 3 caracteres."
        if not self.arquivo.name.lower().endswith(('.pdf', '.odt', '.docx')):
            erros['arquivo'] = "O arquivo deve ser um PDF, ODT ou DOCX."
        if erros:
            raise ValidationError(erros)
    
    def __str__(self):
        return f"{self.solicitacao.adotante.nome} - {self.arquivo.name}"
    
    class Meta:
        verbose_name_plural = "Documentos"
        verbose_name = "Documento"
        ordering = ['solicitacao__adotante__nome']