from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required,user_passes_test, permission_required
from adocato.services.casousogato import CasoUsoGato
from adocato.services.casousoadotante import CasoUsoAdotante
from adocato.services.casousocoordenador import CasoUsoCoordenador
from adocato.services.casousoraca import CasoUsoRaca
from adocato.utils import GerenciadorMensagens, Utilitaria, GerenciadorSessaoUsuario
from adocato.models import Gato
from django.contrib.auth import authenticate, login,logout





def eh_adotante(user):
    """Verifica se o usuário é um adotante."""
    adotante = CasoUsoAdotante.buscar_adotante_por_id(user.id)
   
    return adotante is not None

def eh_coordenador(user):
    """Verifica se o usuário é um coordenador."""
    coordenador = CasoUsoCoordenador.buscar_coordenador_por_id(user.id)
    return coordenador is not None

def eh_administrador(user):
    """Verifica se o usuário é um administrador."""
    return user.is_superuser

def index(request):

    return render(request, 'adocato/index.html')

#@user_passes_test(eh_coordenador)
def salvar_gato(request, gato_id=None):
    if not eh_coordenador(request.user):
        GerenciadorMensagens.processar_erros_validacao(request, ValidationError("Você não é um coordenador."))
        return redirect('adocato:login')
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

@user_passes_test(eh_coordenador)
def listar_racas(request):
    """Lista todas as raças disponíveis."""
    racas = CasoUsoRaca.listar_racas()
    return render(request, 'adocato/raca/lista.html', {'racas': racas})

@login_required
def perfil_usuario(request):
    """
    Exemplo de view que utiliza as informações do usuário disponíveis globalmente.
    """
    # As informações do usuário estão automaticamente disponíveis no template
    # através do context processor
    return render(request, 'adocato/perfil.html')

def listar_gatos_disponiveis(request):
    """Lista todos os gatos disponíveis para adoção."""
    nome = request.GET.get('nome')
    raca_nome = request.GET.get('raca')
    gatos = CasoUsoGato.buscar_gatos_disponiveis(nome=nome, raca_nome=raca_nome)
    return render(request, 'adocato/gato/lista_disponiveis.html', {'gatos': gatos})

#Esse controle é o mais simples, porém não é possível customizar o retorno
@permission_required('adocato.pode_deletar_gato',raise_exception=True)
def excluir_gato(request, gato_id):
    """Exclui um gato do banco de dados."""

    
    """
    # Opção com customização de mensagem de erro e redirecionamento de erro
    if not request.user.has_perm('adocato.pode_deletar_gato'):
        GerenciadorMensagens.processar_erros_validacao(request, ValidationError("Você não tem permissão para excluir gatos."))
        return redirect('adocato:listar_gatos')
    
    """

    gato = CasoUsoGato.buscar_gato_por_id(gato_id)
    if gato:
        gato.delete()
        GerenciadorMensagens.processar_mensagem(request, "Gato excluído com sucesso!")
    else:
        GerenciadorMensagens.processar_mensagem(request, "Gato não encontrado.")
    return redirect('adocato:listar_gatos')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'adocato/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Força a determinação do tipo de usuário na sessão
            GerenciadorSessaoUsuario.determinar_tipo_usuario(request)
            return redirect('adocato:index')
        else:
            GerenciadorMensagens.processar_erros_validacao(request, ValidationError("Usuário ou senha inválidos."))
            return render(request, 'adocato/login.html')

@login_required
def logout_view(request):
    # Limpa as informações da sessão antes do logout
    GerenciadorSessaoUsuario.limpar_sessao_usuario(request)
    logout(request)
    return redirect('adocato:login')