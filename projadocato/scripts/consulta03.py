from adocato.models import Solicitacao

def run():
    solicitacoes = Solicitacao.objects.filter(status__iexact='APROVADA',avaliadores__nome__icontains='A').distinct()
    for solicitacao in solicitacoes:
        print(f"Adotante: {solicitacao.adotante.nome}")
        print(f"Gato: {solicitacao.gato.nome}")
        print(f"Data da Solicitação: {solicitacao.dataSolicitacao}")
        print(f"Status: {solicitacao.status}")
        if solicitacao.recurso:
            print(f"Motivo do Recurso: {solicitacao.recurso}")
    print(f"Total de solicitações aprovadas: {solicitacoes.count()}")