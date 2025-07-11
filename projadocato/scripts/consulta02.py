from adocato.models import Gato
from datetime import date, timedelta

def run():
    um_ano_atras = date.today() - timedelta(days=365)
    gatos = Gato.objects.filter(dataNascimento__lt=um_ano_atras,disponivel=True)
    for gato in gatos:
        print(f"Gato: {gato.nome}")
        print(f"Raça: {gato.raca.nome}")
        print(f"Idade: {gato.idade} anos")
        print(f"Disponível para adoção: {'Sim' if gato.disponivel else 'Não'}")
    print(f"Total de gatos com mais de 1 ano: {gatos.count()}")