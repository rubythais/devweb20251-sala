# Sistema de Gerenciamento de Usuários - Adocato

## Visão Geral

O sistema implementa um gerenciamento inteligente de tipos de usuário (Adotante e Coordenador) com informações armazenadas na sessão para melhor performance e reutilização em todo o projeto.

## Componentes Principais

### 1. GerenciadorSessaoUsuario (utils.py)

Classe responsável por determinar e gerenciar o tipo de usuário na sessão.

#### Métodos principais:
- `determinar_tipo_usuario(request)`: Determina o tipo e armazena na sessão
- `limpar_sessao_usuario(request)`: Remove informações da sessão
- `eh_adotante(request)`: Verifica se é adotante
- `eh_coordenador(request)`: Verifica se é coordenador
- `obter_nome_usuario(request)`: Obtém o nome do usuário

### 2. Context Processor (context_processors.py)

Disponibiliza automaticamente as informações do usuário em todos os templates.

#### Variáveis disponíveis globalmente:
- `tipo_usuario`: 'adotante', 'coordenador', 'indefinido' ou 'anonimo'
- `eh_adotante`: Boolean
- `eh_coordenador`: Boolean
- `usuario_nome`: Nome completo do usuário
- `usuario_id`: ID do usuário
- `usuario_email`: Email do usuário
- `usuario_username`: Username do usuário

## Como Usar

### Em Views

```python
from adocato.utils import GerenciadorSessaoUsuario

def minha_view(request):
    # As informações estão automaticamente disponíveis no template
    # Mas você pode acessar programaticamente se necessário
    info_usuario = GerenciadorSessaoUsuario.determinar_tipo_usuario(request)
    
    if info_usuario['eh_adotante']:
        # Lógica específica para adotante
        pass
    elif info_usuario['eh_coordenador']:
        # Lógica específica para coordenador
        pass
    
    return render(request, 'template.html')
```

### Em Templates

```html
{% if user.is_authenticated %}
    <p>Olá, {{ usuario_nome }}!</p>
    
    {% if eh_adotante %}
        <p>Você é um adotante</p>
        <a href="{% url 'adocato:listar_gatos_disponiveis' %}">Ver Gatos</a>
    {% elif eh_coordenador %}
        <p>Você é um coordenador</p>
        <a href="{% url 'adocato:listar_gatos' %}">Gerenciar Gatos</a>
    {% endif %}
{% else %}
    <p>Faça login para continuar</p>
{% endif %}
```

### Em Decorators

```python
@user_passes_test(eh_coordenador)
def view_apenas_coordenador(request):
    return render(request, 'template.html')
```

## Configuração

### 1. Context Processor registrado em settings.py:
```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'adocato.context_processors.usuario_context',
            ],
        },
    },
]
```

### 2. Importação nas views:
```python
from adocato.utils import GerenciadorSessaoUsuario
```

## Benefícios

1. **Performance**: Informações armazenadas na sessão, evitando consultas desnecessárias ao banco
2. **Reutilização**: Disponível automaticamente em todos os templates
3. **Consistência**: Lógica centralizada para determinação do tipo de usuário
4. **Flexibilidade**: Pode ser usado tanto em views quanto em templates
5. **Manutenibilidade**: Código centralizado facilita manutenção e alterações

## Exemplo de Uso Completo

Veja o template `adocato/perfil.html` para um exemplo completo de como utilizar todas as informações disponíveis.

## Notas Importantes

- As informações são automaticamente limpas no logout
- A sessão é atualizada no login para garantir dados atualizados
- Suporta usuários anônimos e usuários sem tipo definido
- Thread-safe e otimizado para performance
