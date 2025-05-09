from django.shortcuts import render

# Create your views here.
pergunta="Quanto é 2+2?"
alternativas=["4","5","6","7"]
votos=[0,0,0,0]
def index(request):
    contexto={'pergunta':pergunta,"alternativas":alternativas,}
    return render(request, 'enquete/index.html',contexto)
def votar(request):
    opcao=int(request.GET.get('opcao'))
    global votos
    votos[opcao-1]+=1
    resultado=zip(alternativas,votos)
    contexto = {
        'resultado': resultado,
        'pergunta': pergunta,
    }
    return render(request, 'enquete/resultado.html', contexto)
