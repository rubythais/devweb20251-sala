from adocato.models import Coordenador
from django.core.exceptions import ValidationError


class CasoUsoCoordenador:
    @staticmethod
    def listar_coordenadores():
        """Lista todos os coordenadores cadastrados no banco de dados."""
        return Coordenador.objects.all()
    
    @staticmethod
    def buscar_coordenador_por_id(coordenador_id):
        """Busca um coordenador pelo ID."""
        try:
            return Coordenador.objects.get(id=coordenador_id)
        except Coordenador.DoesNotExist:
            return None
    
    @staticmethod
    def buscar_coordenadores(nome=None, cpf=None, username=None):
        """Busca coordenadores com filtros opcionais: nome, CPF ou username."""
        query = Coordenador.objects.all()
        
        if nome:
            query = query.filter(nome__icontains=nome)
        if cpf:
            query = query.filter(cpf__icontains=cpf)
        if username:
            query = query.filter(username__icontains=username)
        
        return query
    
    @staticmethod
    def cadastrar_coordenador(nome, cpf, username, password, email=None):
        """Cadastra um novo coordenador no banco de dados."""
        coordenador = Coordenador(
            nome=nome,
            cpf=cpf,
            username=username,
            email=email or ""
        )
        
        # Define a senha usando o método set_password para hash
        coordenador.set_password(password)
        
        try:
            coordenador.full_clean()
        except ValidationError as e:
            raise e
        
        coordenador.save()
        return coordenador
    
    @staticmethod
    def atualizar_coordenador(coordenador_id, nome=None, cpf=None, username=None, password=None, email=None):
        """Atualiza as informações de um coordenador existente."""
        coordenador = CasoUsoCoordenador.buscar_coordenador_por_id(coordenador_id)
        if not coordenador:
            raise ValueError("Coordenador não encontrado.")
        
        # Atualiza apenas os campos fornecidos
        if nome is not None:
            coordenador.nome = nome
        if cpf is not None:
            coordenador.cpf = cpf
        if username is not None:
            coordenador.username = username
        if email is not None:
            coordenador.email = email
        if password is not None:
            coordenador.set_password(password)
        
        try:
            coordenador.full_clean()
        except ValidationError as e:
            raise e
        
        coordenador.save()
        return coordenador
    
    @staticmethod
    def excluir_coordenador(coordenador_id):
        """Exclui um coordenador do banco de dados."""
        coordenador = CasoUsoCoordenador.buscar_coordenador_por_id(coordenador_id)
        if not coordenador:
            raise ValueError("Coordenador não encontrado.")
        
        coordenador.delete()
        return True
    
    @staticmethod
    def buscar_coordenador_por_username(username):
        """Busca um coordenador pelo username."""
        try:
            return Coordenador.objects.get(username=username)
        except Coordenador.DoesNotExist:
            return None
    
    @staticmethod
    def buscar_coordenador_por_cpf(cpf):
        """Busca um coordenador pelo CPF."""
        try:
            return Coordenador.objects.get(cpf=cpf)
        except Coordenador.DoesNotExist:
            return None
