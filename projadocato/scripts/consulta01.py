from adocato.models import Adotante

def run():
    adotantes=Adotante.objects.filter(solicitacoes_adotante__status__iexact='EM_ANALISE')
    for adotante in adotantes:
        print(f"Adotante: {adotante.nome}")
        print(f"Email: {adotante.email}")
        print(f"Telefone: {adotante.telefone}")
    print(f"Total de adotantes com solicitações em análise: {adotantes.count()}")    