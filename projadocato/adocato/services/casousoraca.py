from adocato.models import Raca
from django.core.exceptions import ValidationError


class CasoUsoRaca:
    @staticmethod
    def listar_racas():
        """Lista todas as raças cadastradas no banco de dados."""
        return Raca.objects.all().order_by('nome')
    
    @staticmethod
    def buscar_raca_por_id(raca_id):
        """Busca uma raça pelo ID."""
        try:
            return Raca.objects.get(id=raca_id)
        except Raca.DoesNotExist:
            return None
    
    @staticmethod
    def buscar_racas(nome=None):
        """Busca raças com filtro opcional por nome."""
        query = Raca.objects.all()
        
        if nome:
            query = query.filter(nome__icontains=nome)
        
        return query.order_by('nome')
    
    @staticmethod
    def cadastrar_raca(nome):
        """Cadastra uma nova raça no banco de dados."""
        raca = Raca(nome=nome)
        
        try:
            raca.full_clean()
        except ValidationError as e:
            raise e
        
        raca.save()
        return raca
    
    @staticmethod
    def atualizar_raca(raca_id, nome=None):
        """Atualiza as informações de uma raça existente."""
        raca = CasoUsoRaca.buscar_raca_por_id(raca_id)
        if not raca:
            raise ValueError("Raça não encontrada.")
        
        # Atualiza apenas os campos fornecidos
        if nome is not None:
            raca.nome = nome
        
        try:
            raca.full_clean()
        except ValidationError as e:
            raise e
        
        raca.save()
        return raca
    
    @staticmethod
    def excluir_raca(raca_id):
        """Exclui uma raça do banco de dados."""
        raca = CasoUsoRaca.buscar_raca_por_id(raca_id)
        if not raca:
            raise ValueError("Raça não encontrada.")
        
        # Verifica se existem gatos associados a esta raça
        if raca.gatos.exists():
            raise ValueError("Não é possível excluir uma raça que possui gatos associados.")
        
        raca.delete()
        return True
    
