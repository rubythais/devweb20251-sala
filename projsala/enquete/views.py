from django.shortcuts import render

# Create your views here.
votos =[0,0,0,0]
voto1=0
voto2=0
voto3=0
voto4=0
def index(request):
    pergunta="Quanto é 2+2?"
    contexto={'pergunta':pergunta}
    return render(request, 'enquete/index.html',contexto)
def votar(request):
    opcao=int(request.GET.get('opcao'))
    global voto1
    global voto2
    global voto3
    global voto4
    if opcao == 1:
        voto1 += 1
    elif opcao == 2:
        voto2 += 1
    elif opcao == 3:
        voto3 += 1
    elif opcao == 4:
        voto4 += 1
    contexto = {
        'voto1': voto1,
        'voto2': voto2,
        'voto3': voto3,
        'voto4': voto4,
    }
    return render(request, 'enquete/resultado.html', contexto)
