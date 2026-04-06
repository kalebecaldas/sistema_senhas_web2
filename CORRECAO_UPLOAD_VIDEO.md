# 🔧 Correção: Upload de Vídeos - Request Entity Too Large

## 📋 Problema Identificado

**Erro:** "Request Entity Too Large"  
**Causa:** O limite de upload estava configurado para apenas 16 MB, insuficiente para vídeos.

---

## ✅ Correções Implementadas

### 1. **Aumento do Limite de Upload** (`app/config.py`)
- **Antes:** 16 MB
- **Depois:** 500 MB
- **Formatos adicionados:** WEBM, MKV

```python
# Configurações de upload
MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'webm', 'mkv'}
```

### 2. **Melhorias na Rota de Upload** (`app/routes.py`)

#### Validações Adicionadas:
- ✅ Verificação de extensão de arquivo
- ✅ Criação automática de diretórios
- ✅ Validação de tamanho após upload
- ✅ Mensagens de erro específicas
- ✅ Logging detalhado para debug

#### Tratamento de Erros:
- ✅ Try-catch robusto
- ✅ Rollback de transação em caso de erro
- ✅ Mensagens amigáveis para o usuário
- ✅ Informação do tamanho do arquivo enviado

### 3. **Melhorias no Script de Inicialização** (`iniciar_sistema.sh`)

#### Novos Recursos:
- ✅ Interface colorida e moderna
- ✅ Verificação de porta em uso
- ✅ Detecção automática de porta disponível
- ✅ Opção de abrir navegador automaticamente
- ✅ Suporte a argumentos de linha de comando

#### Opções Disponíveis:
```bash
./iniciar_sistema.sh              # Inicialização padrão
./iniciar_sistema.sh -b           # Com navegador
./iniciar_sistema.sh -p 8080      # Porta customizada
./iniciar_sistema.sh -a           # Auto-instalar dependências
./iniciar_sistema.sh -h           # Ajuda
```

### 4. **Script de Inicialização Rápida** (`iniciar_rapido.sh`)
- Simplificado para chamar o script principal com flag `-b`
- Abre o navegador automaticamente

---

## 📚 Documentação Criada

### 1. **COMO_INICIAR.md**
- Guia completo de inicialização do sistema
- Todas as opções disponíveis
- Solução de problemas comuns
- Comparação entre os scripts

### 2. **GUIA_UPLOAD.md**
- Limites e formatos suportados
- Como fazer upload
- Solução de problemas
- Dicas de otimização de vídeo
- Ferramentas de compressão
- Checklist de upload

---

## 🚀 Como Usar Agora

### Para Reiniciar o Servidor:

1. **Pare o servidor atual:**
   - Pressione `Ctrl+C` no terminal

2. **Reinicie com as novas configurações:**
   ```bash
   ./iniciar_rapido.sh
   ```

3. **Tente fazer upload do vídeo novamente**

---

## 📊 Limites Atualizados

| Tipo | Limite Anterior | Limite Atual | Formatos |
|------|----------------|--------------|----------|
| **Vídeos** | 16 MB | 500 MB | MP4, AVI, MOV, WEBM, MKV |
| **Imagens** | 16 MB | 500 MB | PNG, JPG, JPEG, GIF |

---

## 💡 Recomendações

### Para Vídeos de Fundo:
- **Tamanho ideal:** 50-200 MB
- **Formato:** MP4 (H.264)
- **Resolução:** 1920x1080 (Full HD)
- **Duração:** 30s - 2min (em loop)

### Se o Vídeo for Muito Grande:
1. Use HandBrake ou FFmpeg para comprimir
2. Reduza a resolução (1080p → 720p)
3. Ajuste a taxa de bits (5-10 Mbps)
4. Remova o áudio se não for necessário

---

## 🔍 Verificação de Funcionamento

### Teste 1: Upload de Vídeo Pequeno
1. Tente fazer upload de um vídeo < 50 MB
2. Deve funcionar sem problemas

### Teste 2: Upload de Vídeo Médio
1. Tente fazer upload de um vídeo entre 50-200 MB
2. Deve funcionar, mas pode demorar um pouco

### Teste 3: Verificar Mensagens
1. Após o upload, você deve ver:
   - "Vídeo enviado com sucesso! (XX.XX MB)"
   - "Configurações salvas com sucesso!"

---

## 🐛 Debug

Se ainda houver problemas:

1. **Verifique os logs no terminal** onde o servidor está rodando
2. **Procure por mensagens** como:
   ```
   Erro detalhado ao salvar vídeo: ...
   ```
3. **Verifique o espaço em disco:**
   ```bash
   df -h
   ```
4. **Verifique permissões da pasta:**
   ```bash
   ls -la app/static/videos/
   ```

---

## 📝 Próximos Passos

1. ✅ Reiniciar o servidor
2. ✅ Testar upload de vídeo
3. ✅ Verificar se o vídeo aparece no display
4. ✅ Ajustar configurações de cores/texto se necessário

---

## 🆘 Suporte

Se o problema persistir:
1. Compartilhe a mensagem de erro completa
2. Informe o tamanho do vídeo
3. Informe o formato do vídeo
4. Compartilhe os logs do terminal
