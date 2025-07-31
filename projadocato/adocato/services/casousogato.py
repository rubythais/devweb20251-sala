from adocato.models import Gato, Raca 
from django.core.exceptions import ValidationError
class CasoUsoGato:
    @staticmethod
    def listar_gatos(): 
        """Lista todos os gatos cadastrados no banco de dados. Esse método pode ser removido, em função da extensão do método buscar_gatos."""
        return Gato.objects.all()
    @staticmethod
    def listar_racas():
        """Lista todas as raças de gatos cadastradas no banco de dados."""
        return Raca.objects.all().order_by('nome')
    @staticmethod
    def buscar_gato_por_id(gato_id):
        """Busca um gato pelo ID."""
        try:
            return Gato.objects.get(id=gato_id)
        except Gato.DoesNotExist:
            return None
    @staticmethod
    def buscar_gatos_disponiveis():
        """Lista todos os gatos disponíveis para adoção."""
        return Gato.objects.filter(disponivel=True).order_by('nome')
    @staticmethod
    def buscar_gatos(nome=None, raca_nome=None, disponivel=None):
        """Aqui temos uma refatoração, incluindo uma busca genérica, com 2 parâmetros opcionais: nome e raça"""
        query = Gato.objects.all()
        if nome:
            query = query.filter(nome__icontains=nome)
        if raca_nome:
            query=query.filter(raca__nome__icontains=raca_nome)
        return query
    @staticmethod
    def cadastrar_gato(nome, sexo, cor, data_nascimento, descricao=None, disponivel=True, raca_id=None,foto=None):
        """Cadastra um novo gato no banco de dados."""
        try:
            raca_obj = Raca.objects.get(id=raca_id)
        except Raca.DoesNotExist:
            raise ValueError("Raça não encontrada.")
        
        gato = Gato(
            nome=nome,
            sexo=sexo,
            cor=cor,
            dataNascimento=data_nascimento,
            descricao=descricao,
            disponivel=disponivel,
            raca=raca_obj,
            foto=foto
        )
        try:
            gato.full_clean()
        except ValidationError as e:
            raise e
        gato.save()
        return gato
    
    def atualizar_gato(gato_id, nome=None, sexo=None, cor=None, data_nascimento=None, descricao=None, disponivel=None, raca_id=None,foto=None):
        """Atualiza as informações de um gato existente."""
        gato = CasoUsoGato.buscar_gato_por_id(gato_id)
        if not gato:
            raise ValueError("Gato não encontrado.")
        gato.nome = nome
        gato.sexo = sexo
        gato.cor = cor
        gato.dataNascimento = data_nascimento
        gato.descricao = descricao
        gato.disponivel = disponivel
        # Só atualiza a foto se uma nova foi fornecida
        if foto is not None:
            gato.foto = foto
        try:
            gato.raca = Raca.objects.get(id=raca_id)
        except Raca.DoesNotExist:
            raise ValueError("Raça não encontrada.")
        try:
            gato.full_clean()
        except ValidationError as e:
            raise e
        gato.save()
        return gato
    @staticmethod
    def excluir_gato(gato_id):
        """Exclui um gato do banco de dados."""
        gato = CasoUsoGato.buscar_gato_por_id(gato_id)
        if not gato:
            raise ValueError("Gato não encontrado.")
        gato.delete()
        return True
