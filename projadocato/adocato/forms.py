from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from datetime import date


class AdotanteForm(forms.Form):
    """Form para cadastro e edição de adotantes."""
    
    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Digite o nome completo'
        }),
        label='Nome Completo'
    )
    
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Digite o nome de usuário'
        }),
        label='Nome de Usuário'
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'input',
            'placeholder': 'Digite o e-mail'
        }),
        label='E-mail'
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Digite a senha'
        }),
        label='Senha'
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Confirme a senha'
        }),
        label='Confirmar Senha'
    )
    
    cpf = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Digite apenas números',
            'maxlength': '11'
        }),
        label='CPF'
    )
    
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'input',
            'type': 'date'
        }),
        label='Data de Nascimento'
    )
    
    telefone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Digite apenas números'
        }),
        label='Telefone'
    )
    
    cidade = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Digite a cidade'
        }),
        label='Cidade'
    )
    
    estado = forms.CharField(
        max_length=2,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'UF',
            'maxlength': '2'
        }),
        label='Estado (UF)'
    )
    
    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)
        
        if self.is_edit:
            # Em modo de edição, senha não é obrigatória
            self.fields['password'].required = False
            self.fields['confirm_password'].required = False
            self.fields['password'].help_text = 'Deixe em branco para manter a senha atual'
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf and (len(cpf) != 11 or not cpf.isdigit()):
            raise ValidationError("O CPF deve ter 11 dígitos numéricos.")
        return cpf
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            if len(telefone) < 10 or len(telefone) > 15:
                raise ValidationError("O telefone deve ter entre 10 e 15 caracteres.")
            if not telefone.isdigit():
                raise ValidationError("O telefone deve conter apenas dígitos numéricos.")
        return telefone
    
    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if data_nascimento:
            if data_nascimento > date.today():
                raise ValidationError("A data de nascimento não pode ser no futuro.")
            
            idade = (date.today() - data_nascimento).days // 365
            if idade < 18:
                raise ValidationError("O adotante deve ter mais de 18 anos.")
        return data_nascimento
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if not self.is_edit or password:  # Valida senha apenas se não for edição ou se senha foi fornecida
            if password != confirm_password:
                raise ValidationError("As senhas não coincidem.")
            
            if password and len(password) < 6:
                raise ValidationError("A senha deve ter pelo menos 6 caracteres.")
        
        return cleaned_data


class AdotantePerfilForm(forms.Form):
    """Form simplificado para edição de perfil do adotante."""
    
    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Digite o nome completo'
        }),
        label='Nome Completo'
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'input',
            'placeholder': 'Digite o e-mail'
        }),
        label='E-mail'
    )
    
    telefone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Digite apenas números'
        }),
        label='Telefone'
    )
    
    cidade = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Digite a cidade'
        }),
        label='Cidade'
    )
    
    estado = forms.CharField(
        max_length=2,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'UF',
            'maxlength': '2'
        }),
        label='Estado (UF)'
    )
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            if len(telefone) < 10 or len(telefone) > 15:
                raise ValidationError("O telefone deve ter entre 10 e 15 caracteres.")
            if not telefone.isdigit():
                raise ValidationError("O telefone deve conter apenas dígitos numéricos.")
        return telefone


class CoordenadorForm(forms.Form):
    """Form para cadastro e edição de coordenadores."""
    
    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Digite o nome completo'
        }),
        label='Nome Completo'
    )
    
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Digite o nome de usuário'
        }),
        label='Nome de Usuário'
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'input',
            'placeholder': 'Digite o e-mail'
        }),
        label='E-mail'
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Digite a senha'
        }),
        label='Senha'
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Confirme a senha'
        }),
        label='Confirmar Senha'
    )
    
    cpf = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Digite apenas números',
            'maxlength': '11'
        }),
        label='CPF'
    )
    
    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)
        
        if self.is_edit:
            # Em modo de edição, senha não é obrigatória
            self.fields['password'].required = False
            self.fields['confirm_password'].required = False
            self.fields['password'].help_text = 'Deixe em branco para manter a senha atual'
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf and (len(cpf) != 11 or not cpf.isdigit()):
            raise ValidationError("O CPF deve ter 11 dígitos numéricos.")
        return cpf
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if not self.is_edit or password:  # Valida senha apenas se não for edição ou se senha foi fornecida
            if password != confirm_password:
                raise ValidationError("As senhas não coincidem.")
            
            if password and len(password) < 6:
                raise ValidationError("A senha deve ter pelo menos 6 caracteres.")
        
        return cleaned_data


class CoordenadorPerfilForm(forms.Form):
    """Form simplificado para edição de perfil do coordenador."""
    
    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Digite o nome completo'
        }),
        label='Nome Completo'
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'input',
            'placeholder': 'Digite o e-mail'
        }),
        label='E-mail'
    )


class CustomAuthenticationForm(AuthenticationForm):
    """Form personalizado de login com estilo Bulma."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'input',
            'placeholder': 'Digite seu nome de usuário'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'input',
            'placeholder': 'Digite sua senha'
        })

class ContatoForm(forms.Form):
    
    titulo = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Digite o título da mensagem'
        }),
        label='Título'
    )

    remetente = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input',
            'placeholder': 'Digite seu e-mail'
        }),
        label='E-mail'
    )
    
    mensagem = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'textarea',
            'placeholder': 'Digite sua mensagem'
        }),
        label='Mensagem'
    )
        
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if titulo and len(titulo) < 3:
            raise ValidationError("O título deve ter pelo menos 3 caracteres.")
        return titulo
    
    def clean_mensagem(self):
        mensagem = self.cleaned_data.get('mensagem')
        if mensagem and len(mensagem) < 30:
            raise ValidationError("A mensagem deve ter pelo menos 30 caracteres.")
        return mensagem


class AvaliacaoSolicitacaoForm(forms.Form):
    """Form para avaliação de solicitação de adoção pelo coordenador."""
    
    parecer = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'textarea',
            'placeholder': 'Digite sua avaliação detalhada da solicitação...',
            'rows': 6
        }),
        label='Parecer da Avaliação',
        help_text='Descreva sua análise detalhadamente. Considere fatores como adequação do perfil do adotante, condições de moradia, experiência com animais, etc.'
    )
    
    decisao = forms.ChoiceField(
        choices=[
            ('aprovar', 'Aprovar Solicitação'),
            ('reprovar', 'Reprovar Solicitação')
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'radio'
        }),
        label='Decisão'
    )
    
    def clean_parecer(self):
        parecer = self.cleaned_data.get('parecer')
        if parecer and len(parecer.strip()) < 10:
            raise ValidationError("O parecer deve ter pelo menos 10 caracteres.")
        return parecer.strip() if parecer else parecer


class RecursoForm(forms.Form):
    """Form para impetrar recurso."""
    motivo = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'textarea',
            'placeholder': 'Descreva os motivos do seu recurso (mínimo 10 caracteres)',
            'rows': 4
        }),
        label='Motivo do Recurso',
        min_length=10
    )


class DocumentoForm(forms.Form):
    """Form para upload de documentos."""
    arquivo = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'file-input',
            'accept': '.pdf,.odt,.docx'
        }),
        label='Arquivo',
        help_text='Formatos aceitos: PDF, ODT, DOCX (máximo 10MB por arquivo).'
    )
    
    descricao = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Descreva o documento (ex: RG, Comprovante de residência)'
        }),
        label='Descrição do Documento',
        required=False
    )
    
    def clean_arquivo(self):
        arquivo = self.cleaned_data.get('arquivo')
        if arquivo:
            # Verificar extensão
            nome = arquivo.name.lower()
            if not nome.endswith(('.pdf', '.odt', '.docx')):
                raise ValidationError("O arquivo deve ser um PDF, ODT ou DOCX.")
            
            # Verificar tamanho (máximo 10MB)
            if arquivo.size > 10 * 1024 * 1024:
                raise ValidationError("O arquivo deve ter no máximo 10MB.")
        
        return arquivo