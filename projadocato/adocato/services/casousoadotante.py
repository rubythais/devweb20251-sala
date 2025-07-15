from adocato.models import Adotante
from django.core.exceptions import ValidationError


class CasoUsoAdotante:
    @staticmethod
    def listar_adotantes():
        """Lista todos os adotantes cadastrados no banco de dados."""
        return Adotante.objects.all()
    
    @staticmethod
    def buscar_adotante_por_id(adotante_id):
        """Busca um adotante pelo ID."""
        try:
            return Adotante.objects.get(id=adotante_id)
        except Adotante.DoesNotExist:
            return None
    
    @staticmethod
    def buscar_adotantes(nome=None, cpf=None, username=None, cidade=None, estado=None):
        """Busca adotantes com filtros opcionais: nome, CPF, username, cidade ou estado."""
        query = Adotante.objects.all()
        
        if nome:
            query = query.filter(nome__icontains=nome)
        if cpf:
            query = query.filter(cpf__icontains=cpf)
        if username:
            query = query.filter(username__icontains=username)
        if cidade:
            query = query.filter(cidade__icontains=cidade)
        if estado:
            query = query.filter(estado__icontains=estado)
        
        return query
    
    @staticmethod
    def cadastrar_adotante(nome, cpf, username, password, data_nascimento, telefone=None, cidade=None, estado=None, email=None):
        """Cadastra um novo adotante no banco de dados."""
        adotante = Adotante(
            nome=nome,
            cpf=cpf,
            username=username,
            dataNascimento=data_nascimento,
            telefone=telefone,
            cidade=cidade,
            estado=estado,
            email=email or ""
        )
        
        # Define a senha usando o método set_password para hash
        adotante.set_password(password)
        
        try:
            adotante.full_clean()
        except ValidationError as e:
            raise e
        
        adotante.save()
        return adotante
    
    @staticmethod
    def atualizar_adotante(adotante_id, nome=None, cpf=None, username=None, password=None, data_nascimento=None, telefone=None, cidade=None, estado=None, email=None):
        """Atualiza as informações de um adotante existente."""
        adotante = CasoUsoAdotante.buscar_adotante_por_id(adotante_id)
        if not adotante:
            raise ValueError("Adotante não encontrado.")
        
        # Atualiza apenas os campos fornecidos
        if nome is not None:
            adotante.nome = nome
        if cpf is not None:
            adotante.cpf = cpf
        if username is not None:
            adotante.username = username
        if data_nascimento is not None:
            adotante.dataNascimento = data_nascimento
        if telefone is not None:
            adotante.telefone = telefone
        if cidade is not None:
            adotante.cidade = cidade
        if estado is not None:
            adotante.estado = estado
        if email is not None:
            adotante.email = email
        if password is not None:
            adotante.set_password(password)
        
        try:
            adotante.full_clean()
        except ValidationError as e:
            raise e
        
        adotante.save()
        return adotante
    
    @staticmethod
    def excluir_adotante(adotante_id):
        """Exclui um adotante do banco de dados."""
        adotante = CasoUsoAdotante.buscar_adotante_por_id(adotante_id)
        if not adotante:
            raise ValueError("Adotante não encontrado.")
        
        adotante.delete()
        return True
    
    @staticmethod
    def buscar_adotante_por_username(username):
        """Busca um adotante pelo username."""
        try:
            return Adotante.objects.get(username=username)
        except Adotante.DoesNotExist:
            return None
    
    @staticmethod
    def buscar_adotante_por_cpf(cpf):
        """Busca um adotante pelo CPF."""
        try:
            return Adotante.objects.get(cpf=cpf)
        except Adotante.DoesNotExist:
            return None
    