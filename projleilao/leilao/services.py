from .models import Leilao
class LeilaoService:
    @staticmethod
    def listar_leiloes():
        return Leilao.objects.all()
