from adocato.models import Gato, Raca # Importando os modelos Gato e Raca
class CasoUsoGato:
    @staticmethod
    def listar_gatos(): 
        """Lista todos os gatos cadastrados no banco de dados."""
        return Gato.objects.all()
    @staticmethod
    def buscar_gato_por_id(gato_id):
        """Busca um gato pelo ID."""
        try:
            return Gato.objects.get(id=gato_id)
        except Gato.DoesNotExist:
            return None
    @staticmethod
    def buscar_gatos_por_nome(nome):
        """Busca gatos pelo nome independente do case."""
        return Gato.objects.filter(nome__icontains=nome)
    
    @staticmethod
    def cadastrar_gato(nome, sexo, cor, data_nascimento, 
                       descricao=None, disponivel=True, raca_id=None):
        """Cadastra um novo gato no banco de dados."""  
        gato = Gato(
            nome=nome,
            sexo=sexo,
            cor=cor,
            dataNascimento=data_nascimento,
            descricao=descricao,
            disponivel=disponivel,
            raca=Raca.objects.get(id=raca_id)
        )
        gato.save()
        return gato
    
    @staticmethod
    def atualizar_gato(gato_id, nome=None, sexo=None, cor=None, 
                       data_nascimento=None, descricao=None, disponivel=None, raca_id=None):
        """Atualiza as informações de um gato existente."""
        gato = CasoUsoGato.buscar_gato_por_id(gato_id)
        gato.nome = nome
        gato.sexo = sexo
        gato.cor = cor
        gato.dataNascimento = data_nascimento
        gato.descricao = descricao
        gato.disponivel = disponivel
        gato.raca = Raca.objects.get(id=raca_id)
        gato.save()
        return gato
    
    @staticmethod
    def excluir_gato(gato_id):
        """Exclui um gato do banco de dados."""
        gato = CasoUsoGato.buscar_gato_por_id(gato_id)
        gato.delete()
        return True