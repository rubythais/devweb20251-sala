from django.forms import ValidationError
from django.shortcuts import redirect, render
from adocato.services.casousogato import CasoUsoGato
from adocato.utils import GerenciadorMensagens, Utilitaria
from adocato.models import Gato
def index(request):
    return render(request, 'adocato/index.html')
def salvar_gato(request, gato_id=None):
    """Salva um gato no banco de dados."""
    if request.method == 'GET':
        if gato_id:
            gato = CasoUsoGato.buscar_gato_por_id(gato_id)
        else:
            gato = None
        racas=CasoUsoGato.listar_racas()
        return render(request, 'adocato/gato/form.html', {'gato': gato, 'racas': racas})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        raca_id = request.POST.get('raca')
        data_nascimento = request.POST.get('data_nascimento')
        descricao = request.POST.get('descricao')
        cor= request.POST.get('cor')
        foto = request.FILES.get('foto')
        sexo= request.POST.get('sexo')
        disponivel = request.POST.get('disponivel') == 'on'
        try:
            
            if gato_id:
                # Para edição, passa None se não há nova foto para preservar a existente
                gato=CasoUsoGato.atualizar_gato(gato_id=gato_id, nome=nome, raca_id=raca_id,cor=cor, data_nascimento=data_nascimento, descricao=descricao, foto=foto, sexo=sexo, disponivel=disponivel)
            else:
                gato=CasoUsoGato.cadastrar_gato(nome=nome, raca_id=raca_id,cor=cor, data_nascimento=data_nascimento, descricao=descricao, foto=foto, sexo=sexo, disponivel=disponivel)
            GerenciadorMensagens.processar_mensagem(request, "Gato salvo com sucesso!")
            return redirect('adocato:listar_gatos')
        except ValidationError as e:
            GerenciadorMensagens.processar_erros_validacao(request, e)

            # Busca o gato existente para preservar dados não alterados (como foto)
            gato_existente = None
            if gato_id:
                gato_existente = CasoUsoGato.buscar_gato_por_id(gato_id)

            gato=Gato(id=gato_id,nome=nome,raca_id=raca_id, cor=cor, dataNascimento=Utilitaria.conversor_data(data_nascimento), descricao=descricao, sexo=sexo, disponivel=disponivel) #usado pelo template
            
            # Preserva a foto existente se não há nova foto e está em modo de editar um gato existente
            if gato_existente and not foto:
                gato.foto = gato_existente.foto
            
            racas=CasoUsoGato.listar_racas()
            
            # Prepara o contexto com informações adicionais para preservar dados do formulário
            context = {
                'gato': gato, 
                'racas': racas,
                'foto_enviada': foto.name if foto else None,
            }
            return render(request, 'adocato/gato/form.html', context)
def listar_gatos(request):
    """Lista todos os gatos disponíveis."""
    nome=request.GET.get('nome')
    raca_nome=request.GET.get('raca')
    gatos=CasoUsoGato.buscar_gatos(nome=nome,raca_nome=raca_nome)
    return render(request, 'adocato/gato/lista.html', {'gatos': gatos})
def excluir_gato(request, gato_id):
    """Exclui um gato do banco de dados."""
    gato = CasoUsoGato.buscar_gato_por_id(gato_id)
    if gato:
        gato.delete()
        GerenciadorMensagens.processar_mensagem(request, "Gato excluído com sucesso!")
    else:
        GerenciadorMensagens.processar_mensagem(request, "Gato não encontrado.")
    return redirect('adocato:listar_gatos')