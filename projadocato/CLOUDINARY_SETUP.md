# Configuração do Cloudinary para Media Files

Este documento explica como configurar o Cloudinary para armazenamento de arquivos de media em produção.

## 1. Por que usar Cloudinary?

O Render.com não fornece armazenamento persistente de arquivos de media (fotos, documentos). Sempre que a aplicação é redeploy, os arquivos enviados pelos usuários são perdidos. O Cloudinary resolve isso oferecendo:

- ✅ **Gratuito**: 25 créditos/mês (suficiente para projetos pequenos/médios)
- ✅ **CDN Global**: Entrega rápida de imagens em qualquer lugar do mundo
- ✅ **Otimização automática**: Compressão e redimensionamento automático
- ✅ **Transformações**: Resize, crop, filtros em tempo real
- ✅ **Backup seguro**: Seus arquivos ficam seguros na nuvem

## 2. Configuração no Cloudinary

### 2.1. Criar conta no Cloudinary
1. Acesse [cloudinary.com](https://cloudinary.com)
2. Clique em "Sign Up Free"
3. Preencha os dados e confirme o email
4. Acesse o Dashboard

### 2.2. Obter credenciais
No Dashboard do Cloudinary, você encontrará:
```
Cloud name: your-cloud-name
API Key: 123456789012345
API Secret: AbCdEfGhIjKlMnOpQrStUvWxYz
```

## 3. Configuração no Render.com

### 3.1. Adicionar variáveis de ambiente
No painel do Render.com, vá em Settings > Environment e adicione:

```bash
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=AbCdEfGhIjKlMnOpQrStUvWxYz
```

**IMPORTANTE**: 
- Substitua pelos seus valores reais
- Nunca comite essas credenciais no código
- Use apenas as variáveis de ambiente

### 3.2. Redeploy da aplicação
Após adicionar as variáveis:
1. Clique em "Manual Deploy" no Render.com
2. Aguarde o deploy finalizar
3. Teste o upload de arquivos

## 4. Como funciona

### 4.1. Desenvolvimento (local)
- Usa `ImageField` e `FileField` normais
- Arquivos salvos em `media/gatos/` e `media/documentos/`
- Funciona como sempre funcionou

### 4.2. Produção (Render.com)
- Usa `CloudinaryField` automaticamente
- Arquivos salvos no Cloudinary
- URLs automáticas do CDN
- Organização em pastas: `adocato/gatos/` e `adocato/documentos/`

### 4.3. Migração automática
O código detecta automaticamente o ambiente:
```python
# Em models.py
foto = get_image_field(upload_to='gatos/', blank=True, null=True)
arquivo = get_file_field(upload_to='documentos/', verbose_name="Arquivo")
```

## 5. Funcionalidades extras

### 5.1. URLs de imagem otimizadas
```python
# No template, a URL da imagem já vem otimizada
{{ gato.foto.url }}  # https://res.cloudinary.com/your-cloud/image/upload/v123/adocato/gatos/foto.jpg
```

### 5.2. Transformações em tempo real
Você pode redimensionar imagens na URL:
```python
# Redimensionar para 300x200
{{ gato.foto.url|add:"?w_300,h_200,c_fill" }}
```

### 5.3. Formatos automáticos
O Cloudinary entrega automaticamente:
- WebP para navegadores modernos
- JPEG otimizado para navegadores antigos
- Compressão inteligente

## 6. Monitoramento

### 6.1. Verificar uso
No Dashboard do Cloudinary você pode ver:
- Quantos arquivos estão armazenados
- Bandwidth utilizado
- Transformações realizadas
- Créditos restantes

### 6.2. Limites gratuitos
Plano gratuito inclui:
- 25 créditos/mês
- 25GB de armazenamento
- 25GB de bandwidth
- Transformações básicas

## 7. Troubleshooting

### 7.1. Upload não funciona
```bash
# Verificar se as variáveis estão configuradas
python manage.py shell
>>> import os
>>> print(os.environ.get('CLOUDINARY_CLOUD_NAME'))
>>> print(os.environ.get('CLOUDINARY_API_KEY'))
>>> print(os.environ.get('CLOUDINARY_API_SECRET'))
```

### 7.2. Imagens não aparecem
- Verificar as URLs no admin
- Verificar se as imagens estão no Cloudinary Dashboard
- Verificar logs no Render.com

### 7.3. Migração de arquivos existentes
Se você já tem arquivos no sistema local:
```python
# Script para migrar arquivos existentes (executar uma vez)
python manage.py shell
>>> from adocato.models import Gato
>>> for gato in Gato.objects.filter(foto__isnull=False):
...     print(f"Migrando foto do {gato.nome}")
...     # O Cloudinary vai fazer upload automático na próxima edição
```

## 8. Backup e segurança

### 8.1. Backup automático
- Cloudinary mantém backup automático
- Histórico de versões disponível
- Recuperação via API

### 8.2. Segurança
- URLs assinadas para arquivos privados
- Controle de acesso por pasta
- Logs de acesso disponíveis

---

**Resumo**: Após configurar as 3 variáveis de ambiente no Render.com, sua aplicação automaticamente usará o Cloudinary em produção, mantendo compatibilidade total com o desenvolvimento local. Não é necessário alterar templates ou views existentes.
