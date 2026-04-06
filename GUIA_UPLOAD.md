# 📹 Guia de Upload de Vídeos e Imagens

## 🎯 Limites de Upload

### Tamanho Máximo
- **Limite atual:** 500 MB por arquivo
- **Recomendado para vídeos:** até 200 MB para melhor performance
- **Recomendado para imagens:** até 5 MB

### Formatos Suportados

#### Vídeos
- ✅ MP4 (recomendado)
- ✅ AVI
- ✅ MOV
- ✅ WEBM
- ✅ MKV

#### Imagens (Logo)
- ✅ PNG (recomendado para logos)
- ✅ JPG/JPEG
- ✅ GIF

---

## 🚀 Como Fazer Upload

### 1. Acessar Configurações
1. Faça login como administrador
2. Vá para **Editar Telas** no menu
3. Role até a seção de upload

### 2. Upload de Vídeo de Fundo
1. Clique em **"Escolher arquivo"** na seção de vídeo
2. Selecione seu vídeo (máx. 500 MB)
3. Aguarde o upload completar
4. Clique em **"Salvar Configurações"**

### 3. Upload de Logo
1. Clique em **"Escolher arquivo"** na seção de logo
2. Selecione sua imagem (PNG recomendado)
3. Clique em **"Salvar Configurações"**

---

## ⚠️ Solução de Problemas

### Erro: "Request Entity Too Large"

**Causa:** O arquivo excede o limite de 500 MB

**Solução:**
1. **Comprimir o vídeo:**
   - Use ferramentas online como [HandBrake](https://handbrake.fr/)
   - Reduza a resolução (1080p → 720p)
   - Ajuste a taxa de bits (bitrate)

2. **Converter para formato mais eficiente:**
   - MP4 com codec H.264 é o mais eficiente
   - Use ferramentas como VLC ou FFmpeg

### Erro: "Formato de vídeo inválido"

**Causa:** Extensão do arquivo não suportada

**Solução:**
- Converta o vídeo para MP4, AVI, MOV, WEBM ou MKV
- Use ferramentas de conversão online ou VLC

### Vídeo não aparece no display

**Possíveis causas:**
1. O vídeo ainda está sendo processado
2. Formato incompatível com o navegador
3. Caminho do arquivo incorreto

**Solução:**
1. Recarregue a página do display (F5)
2. Verifique se o vídeo está em formato MP4
3. Verifique os logs do servidor

---

## 💡 Dicas de Otimização

### Para Vídeos de Fundo

1. **Resolução ideal:** 1920x1080 (Full HD)
2. **Taxa de bits:** 2-5 Mbps
3. **Codec:** H.264 (MP4)
4. **Duração:** 30 segundos a 2 minutos (em loop)
5. **Sem áudio:** Remove o áudio para reduzir tamanho

### Para Logos

1. **Formato:** PNG com fundo transparente
2. **Resolução:** 512x512 ou 1024x1024 pixels
3. **Tamanho:** Menos de 500 KB
4. **Cores:** Use cores sólidas para melhor visualização

---

## 🔧 Compressão de Vídeo

### Usando HandBrake (Gratuito)

1. **Download:** [handbrake.fr](https://handbrake.fr/)
2. **Abra seu vídeo** no HandBrake
3. **Configurações recomendadas:**
   - Preset: "Fast 1080p30"
   - Format: MP4
   - Video Codec: H.264
   - Framerate: 30 FPS
   - Quality: RF 22-24
4. **Clique em "Start"**

### Usando FFmpeg (Linha de Comando)

```bash
# Comprimir vídeo mantendo qualidade razoável
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k output.mp4

# Reduzir resolução para 720p
ffmpeg -i input.mp4 -vf scale=1280:720 -c:v libx264 -crf 23 output.mp4

# Remover áudio
ffmpeg -i input.mp4 -c:v copy -an output.mp4
```

### Ferramentas Online

- **CloudConvert:** [cloudconvert.com](https://cloudconvert.com/)
- **Online-Convert:** [online-convert.com](https://www.online-convert.com/)
- **FreeConvert:** [freeconvert.com](https://www.freeconvert.com/)

---

## 📊 Tabela de Referência

| Resolução | Taxa de Bits | Tamanho (1 min) | Qualidade |
|-----------|--------------|-----------------|-----------|
| 4K (3840x2160) | 20-50 Mbps | 150-375 MB | Excelente |
| 1080p | 5-10 Mbps | 37-75 MB | Ótima |
| 720p | 2.5-5 Mbps | 18-37 MB | Boa |
| 480p | 1-2 Mbps | 7-15 MB | Aceitável |

---

## 🆘 Suporte Técnico

### Verificar Logs do Servidor

Se o upload falhar, verifique os logs no terminal onde o servidor está rodando:

```bash
# Os erros aparecerão no terminal
# Procure por mensagens como:
# "Erro ao salvar vídeo: ..."
# "Erro detalhado ao salvar vídeo: ..."
```

### Informações Úteis para Debug

Ao reportar problemas, inclua:
- Tamanho do arquivo
- Formato/extensão
- Mensagem de erro exata
- Sistema operacional
- Navegador utilizado

---

## 📝 Checklist de Upload

Antes de fazer upload, verifique:

- [ ] Arquivo tem menos de 500 MB
- [ ] Formato é suportado (MP4, AVI, MOV, WEBM, MKV)
- [ ] Vídeo está em boa qualidade
- [ ] Você está logado como administrador
- [ ] Conexão com internet está estável
- [ ] Há espaço suficiente no servidor

---

## 🎨 Recomendações de Design

### Vídeos de Fundo
- Use vídeos sutis que não distraiam
- Prefira movimentos lentos
- Evite cores muito vibrantes
- Teste em diferentes tamanhos de tela

### Logos
- Mantenha simples e legível
- Use alto contraste
- Teste em fundo escuro e claro
- Certifique-se de que está centralizado

---

## 🔄 Atualizações Futuras

Recursos planejados:
- [ ] Preview antes do upload
- [ ] Barra de progresso de upload
- [ ] Compressão automática no servidor
- [ ] Suporte para múltiplos vídeos
- [ ] Galeria de vídeos pré-configurados
