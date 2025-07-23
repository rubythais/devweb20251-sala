"""
Views baseadas em classes (Class-Based Views - CBVs) para operações relacionadas aos gatos.

CONCEITOS FUNDAMENTAIS SOBRE CLASS-BASED VIEWS (CBVs):

1. O QUE SÃO CBVs?
   - São uma alternativa às function-based views (FBVs) tradicionais do Django
   - Usam programação orientada a objetos para organizar melhor o código
   - Oferecem maior reutilização através de herança e mixins
   - Seguem o princípio DRY (Don't Repeat Yourself)

2. VANTAGENS DAS CBVs:
   - Código mais organizado e reutilizável
   - Separação clara de responsabilidades por método HTTP (GET, POST, etc.)
   - Herança permite compartilhar funcionalidades entre views
   - Mixins oferecem funcionalidades modulares (autenticação, permissões, etc.)

3. PRINCIPAIS CLASSES GENÉRICAS:
   - View: Classe base mais simples, requer implementação manual dos métodos
   - TemplateView: Para renderizar templates simples
   - ListView: Para listar objetos de um modelo
   - DetailView: Para exibir detalhes de um objeto específico
   - CreateView/UpdateView: Para formulários de criação/edição
   - DeleteView: Para exclusão de objetos

4. MIXINS IMPORTANTES:
   - LoginRequiredMixin: Requer que o usuário esteja logado
   - PermissionRequiredMixin: Verifica permissões específicas
   - UserPassesTestMixin: Permite testes customizados de acesso
"""

from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic import View, ListView, TemplateView
from django.urls import reverse_lazy
from adocato.services.casousogato import CasoUsoGato
from adocato.services.casousoadotante import CasoUsoAdotante
from adocato.services.casousocoordenador import CasoUsoCoordenador
from adocato.utils import GerenciadorMensagens, Utilitaria
from adocato.models import Gato
from adocato.views.mixins import PerfilCoordenadorMixin


class SalvarGatoView(PerfilCoordenadorMixin, View):
    """
    EXEMPLO DE VIEW BASEADA EM CLASSE USANDO 'View' GENÉRICA
    
    CONCEITOS DEMONSTRADOS:
    1. HERANÇA MÚLTIPLA: Esta classe herda de PerfilCoordenadorMixin e View
    2. MIXIN: PerfilCoordenadorMixin adiciona funcionalidade de controle de acesso
    3. VIEW GENÉRICA: 'View' é a classe base mais simples do Django
    4. SEPARAÇÃO POR MÉTODO HTTP: GET e POST são tratados em métodos separados
    
    FUNCIONAMENTO:
    - PerfilCoordenadorMixin: Garante que apenas coordenadores acessem esta view
    - View: Classe base que permite implementação customizada dos métodos HTTP
    - get(): Chamado automaticamente em requisições GET (exibir formulário)
    - post(): Chamado automaticamente em requisições POST (processar formulário)
    
    VANTAGENS DESTA ABORDAGEM:
    - Separação clara entre exibição e processamento do formulário
    - Reutilização do controle de acesso através do mixin
    - Código mais organizado que uma function-based view equivalente
    """
    
    def get(self, request, gato_id=None):
        """
        MÉTODO GET - EXIBIR FORMULÁRIO
        
        Este método é chamado automaticamente pelo Django quando a view
        recebe uma requisição HTTP GET. É equivalente a verificar:
        if request.method == 'GET': em uma function-based view.
        
        PARÂMETROS:
        - request: Objeto HttpRequest com dados da requisição
        - gato_id: Parâmetro opcional da URL para edição de gato existente
        """
        if gato_id:
            # Modo edição: busca gato existente
            gato = CasoUsoGato.buscar_gato_por_id(gato_id)
        else:
            # Modo criação: gato = None
            gato = None
        
        # Busca todas as raças para popular o select do formulário
        racas = CasoUsoGato.listar_racas()
        
        # Renderiza o template com os dados necessários
        return render(request, 'adocato/gato/form.html', {'gato': gato, 'racas': racas})
    
    def post(self, request, gato_id=None):
        """
        MÉTODO POST - PROCESSAR FORMULÁRIO
        
        Este método é chamado automaticamente pelo Django quando a view
        recebe uma requisição HTTP POST. É equivalente a verificar:
        if request.method == 'POST': em uma function-based view.
        
        VANTAGEM: Separação clara de responsabilidades entre GET e POST
        """
        # Extrai dados do formulário enviado
        nome = request.POST.get('nome')
        raca_id = request.POST.get('raca')
        data_nascimento = request.POST.get('data_nascimento')
        descricao = request.POST.get('descricao')
        cor = request.POST.get('cor')
        foto = request.FILES.get('foto')  # Para arquivos usa request.FILES
        sexo = request.POST.get('sexo')
        disponivel = request.POST.get('disponivel') == 'on'  # Checkbox
        
        try:
            if gato_id:
                # MODO EDIÇÃO: Atualiza gato existente
                gato = CasoUsoGato.atualizar_gato(
                    gato_id=gato_id, 
                    nome=nome, 
                    raca_id=raca_id,
                    cor=cor, 
                    data_nascimento=data_nascimento, 
                    descricao=descricao, 
                    foto=foto, 
                    sexo=sexo, 
                    disponivel=disponivel
                )
            else:
                # MODO CRIAÇÃO: Cria novo gato
                gato = CasoUsoGato.cadastrar_gato(
                    nome=nome, 
                    raca_id=raca_id,
                    cor=cor, 
                    data_nascimento=data_nascimento, 
                    descricao=descricao, 
                    foto=foto, 
                    sexo=sexo, 
                    disponivel=disponivel
                )
            
            # Sucesso: Adiciona mensagem e redireciona
            GerenciadorMensagens.processar_mensagem(request, "Gato salvo com sucesso!")
            return redirect('adocato:listar_gatos')
            
        except ValidationError as e:
            # TRATAMENTO DE ERROS: Preserva dados do formulário e exibe erros
            GerenciadorMensagens.processar_erros_validacao(request, e)

            # Busca gato existente para preservar dados não alterados (como foto)
            gato_existente = None
            if gato_id:
                gato_existente = CasoUsoGato.buscar_gato_por_id(gato_id)

            # Reconstrói objeto gato para o template (sem salvar no banco)
            gato = Gato(
                id=gato_id,
                nome=nome,
                raca_id=raca_id, 
                cor=cor, 
                dataNascimento=Utilitaria.conversor_data(data_nascimento), 
                descricao=descricao, 
                sexo=sexo, 
                disponivel=disponivel
            )
            
            # Preserva foto existente se não há nova foto
            if gato_existente and not foto:
                gato.foto = gato_existente.foto
            
            racas = CasoUsoGato.listar_racas()
            
            # Contexto para re-renderizar o formulário com erros
            context = {
                'gato': gato, 
                'racas': racas,
                'foto_enviada': foto.name if foto else None,
            }
            return render(request, 'adocato/gato/form.html', context)


class ListarGatosView(ListView):
    """
    EXEMPLO DE VIEW BASEADA EM CLASSE USANDO 'ListView' GENÉRICA
    
    CONCEITOS DEMONSTRADOS:
    1. VIEW GENÉRICA: ListView é especializada para listar objetos
    2. CONVENÇÕES: O Django automatiza muito do trabalho através de convenções
    3. CUSTOMIZAÇÃO: Podemos sobrescrever métodos para comportamento específico
    
    FUNCIONAMENTO AUTOMÁTICO DA ListView:
    - Automaticamente renderiza uma lista de objetos
    - Cria paginação automaticamente (se configurada)
    - Disponibiliza a lista no template com o nome definido em context_object_name
    - Procura automaticamente pelo template baseado no nome do modelo (se não especificado)
    
    ATRIBUTOS IMPORTANTES:
    - template_name: Especifica qual template usar
    - context_object_name: Nome da variável no template (padrão seria 'object_list')
    - model: Modelo a ser listado (alternativa ao get_queryset)
    - paginate_by: Número de itens por página
    
    MÉTODOS QUE PODEM SER SOBRESCRITOS:
    - get_queryset(): Customiza quais objetos serão listados
    - get_context_data(): Adiciona dados extras ao contexto do template
    """
    
    # Define o template a ser usado (obrigatório se não seguir convenção)
    template_name = 'adocato/gato/lista.html'
    
    # Nome da variável que conterá a lista no template
    # Sem isso, seria 'object_list' (nome padrão do Django)
    context_object_name = 'gatos'

    paginate_by = 2  # Define o número de gatos por página
    
    def get_queryset(self):
        """
        MÉTODO CUSTOMIZADO PARA DEFINIR QUAIS OBJETOS LISTAR
        
        Este método é chamado automaticamente pela ListView para
        determinar quais objetos devem ser incluídos na listagem.
        
        VANTAGEM: Permite filtros dinâmicos baseados em parâmetros GET
        
        RETORNO: Deve retornar uma QuerySet ou lista de objetos
        """
        # Obtém parâmetros de filtro da URL (?nome=...&raca=...)
        nome = self.request.GET.get('nome')
        raca_nome = self.request.GET.get('raca')
        
        # Usa o serviço para buscar gatos com filtros opcionais
        return CasoUsoGato.buscar_gatos(nome=nome, raca_nome=raca_nome)


class ListarGatosDisponiveisView(ListView):
    """
    SEGUNDA ListView - DEMONSTRA REUTILIZAÇÃO E ESPECIALIZAÇÃO
    
    CONCEITOS DEMONSTRADOS:
    1. REUTILIZAÇÃO: Mesma estrutura da ListView anterior
    2. ESPECIALIZAÇÃO: Comportamento ligeiramente diferente (apenas gatos disponíveis)
    3. TEMPLATE DIFERENTE: Cada view pode usar seu próprio template
    
    DIFERENÇAS EM RELAÇÃO À ListarGatosView:
    - Template diferente (lista_disponiveis.html vs lista.html)
    - Lógica de busca diferente (apenas gatos disponíveis)
    - Mesmo padrão de filtros por parâmetros GET
    """
    
    template_name = 'adocato/gato/lista_disponiveis.html'
    context_object_name = 'gatos'
    
    def get_queryset(self):
        """
        QUERYSET ESPECIALIZADO - APENAS GATOS DISPONÍVEIS
        
        Demonstra como a mesma estrutura (ListView) pode ser
        reutilizada para necessidades ligeiramente diferentes.
        """
        nome = self.request.GET.get('nome')
        raca_nome = self.request.GET.get('raca')
        
        # Chama método específico que retorna apenas gatos disponíveis
        return CasoUsoGato.buscar_gatos_disponiveis(nome=nome, raca_nome=raca_nome)


class ExcluirGatoView(PermissionRequiredMixin, View):
    """
    EXEMPLO DE VIEW COM MIXIN DE PERMISSÕES
    
    CONCEITOS DEMONSTRADOS:
    1. MIXIN DE PERMISSÕES: PermissionRequiredMixin verifica permissões automaticamente
    2. CONTROLE DE ACESSO: Usuário deve ter permissão específica para acessar
    3. TRATAMENTO DE ERROS: raise_exception controla como erros são tratados
    4. FLEXIBILIDADE: Suporta GET e POST para compatibilidade
    
    FUNCIONAMENTO DO PermissionRequiredMixin:
    - Verifica automaticamente se o usuário tem a permissão especificada
    - Se não tiver, pode lançar exceção (403) ou redirecionar para login
    - Executa a verificação ANTES dos métodos get() ou post()
    
    ATRIBUTOS DO MIXIN:
    - permission_required: Nome da permissão necessária
    - raise_exception: Se True, lança 403; se False, redireciona para login
    - login_url: URL para redirecionamento (se raise_exception=False)
    """
    
    # CONFIGURAÇÃO DE PERMISSÕES
    permission_required = 'adocato.pode_deletar_gato'  # Permissão necessária
    raise_exception = True  # Lança 403 Forbidden se não tiver permissão
    
    def post(self, request, gato_id):
        """
        MÉTODO POST - EXCLUSÃO SEGURA
        
        POST é o método HTTP correto para operações que modificam dados.
        DELETE seria mais semântico, mas nem todos os browsers suportam.
        
        FLUXO DE EXECUÇÃO:
        1. PermissionRequiredMixin verifica permissão automaticamente
        2. Se aprovado, este método é executado
        3. Se negado, exceção 403 é lançada (raise_exception=True)
        """
        gato = CasoUsoGato.buscar_gato_por_id(gato_id)
        
        if gato:
            gato.delete()
            GerenciadorMensagens.processar_mensagem(request, "Gato excluído com sucesso!")
        else:
            GerenciadorMensagens.processar_mensagem(request, "Gato não encontrado.")
        
        # Redireciona para lista após exclusão
        return redirect('adocato:listar_gatos')
    
    def get(self, request, gato_id):
        """
        MÉTODO GET - COMPATIBILIDADE
        
        Permite exclusão via GET para manter compatibilidade com links simples.
        
        ATENÇÃO: Em aplicações reais, operações destrutivas deveriam
        usar apenas POST/DELETE por questões de segurança (CSRF, etc.)
        """
        return self.post(request, gato_id)


# ============================================================================
# RESUMO DIDÁTICO - COMPARAÇÃO FBV vs CBV
# ============================================================================

"""
COMPARAÇÃO: FUNCTION-BASED VIEW vs CLASS-BASED VIEW

FUNCTION-BASED VIEW (Abordagem tradicional):
```python
@user_passes_test(eh_coordenador)
def salvar_gato(request, gato_id=None):
    if request.method == 'GET':
        # lógica para GET
        return render(...)
    elif request.method == 'POST':
        # lógica para POST
        return redirect(...)
```

CLASS-BASED VIEW (Abordagem orientada a objetos):
```python
class SalvarGatoView(PerfilCoordenadorMixin, View):
    def get(self, request, gato_id=None):
        # lógica para GET
        return render(...)
    
    def post(self, request, gato_id=None):
        # lógica para POST
        return redirect(...)
```

VANTAGENS DAS CBVs:
1. SEPARAÇÃO: Cada método HTTP tem seu próprio método na classe
2. REUTILIZAÇÃO: Mixins permitem compartilhar funcionalidades
3. HERANÇA: Classes podem herdar comportamentos de outras classes
4. ORGANIZAÇÃO: Código fica mais estruturado e legível
5. DJANGO GENÉRICO: Views como ListView automatizam tarefas comuns

QUANDO USAR CADA ABORDAGEM:
- FBVs: Para lógica simples e específica
- CBVs: Para funcionalidades que se beneficiam de herança e reutilização
- Views Genéricas: Para operações CRUD padrão (Create, Read, Update, Delete)

CONFIGURAÇÃO NO urls.py:
- FBV: path('url/', minha_view, name='nome')
- CBV: path('url/', MinhaView.as_view(), name='nome')
"""
