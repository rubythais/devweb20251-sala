from .models import Leilao,ItemLeilao
class LeilaoService:
    @staticmethod
    def listar_leiloes():
        return Leilao.objects.all()
    @staticmethod
    def listar_itensLeilao(leilao_id,titulo=None):
        if titulo:
            leilao=Leilao.objects.get(id=leilao_id)
            #itensLeilao=ItemLeilao.objects.filter(leilao__id=leilao_id,titulo__icontains=titulo)
            return leilao.itensLeilao.filter(titulo__icontains=titulo)
        return Leilao.objects.get(id=leilao_id).itensLeilao.all()