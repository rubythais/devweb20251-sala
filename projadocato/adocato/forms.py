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
