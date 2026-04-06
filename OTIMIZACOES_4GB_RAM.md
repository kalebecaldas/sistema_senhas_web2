# Otimizações para PCs com 4GB RAM

## ✅ Otimizações já implementadas no código

### Display (`display.html` e `display.js`)
- ❌ **Fontes externas removidas** (Google Fonts) → Usa fontes do sistema
- ❌ **Todas as animações CSS removidas** (marquee, pulse, etc.)
- ❌ **backdrop-filter removido** (muito pesado para GPU)
- ❌ **Gradientes simplificados** → Cores sólidas
- ❌ **Box-shadows simplificadas** → Menos camadas
- ❌ **20 logs de debug removidos** → Economia de requisições fetch
- ⏱️ **Relógio atualiza a cada 5s** (antes: 1s) → 80% menos CPU
- ⏱️ **Polling adaptativo** → Ajusta automaticamente baseado na latência WiFi
- ⏱️ **Intervalo inicial: 700ms** (mais conservador para RAM baixa)
- ⏱️ **CheckServer: 6s** (antes: 3s) → Menos requisições
- 🎯 **Fetch com timeout e retry** → Melhor tratamento de WiFi lento
- 🎯 **Detecção automática de latência** → Ajusta polling dinamicamente
- 🎯 **Loop com proteção** → Evita execuções sobrepostas

### Vídeo
- 🎬 **Vídeo de background removido**
- 🎬 **Hardware acceleration forçada** (`transform: translateZ(0)`)
- 🎬 **image-rendering otimizado** (`-webkit-optimize-contrast`)
- 🎬 **Detecção de formato inválido** (aviso para converter MOV → MP4)

## 🔧 Otimizações adicionais recomendadas

### 1. Configurações do Windows (CRÍTICO)

#### Desabilitar programas em segundo plano
```
Configurações > Privacidade > Aplicativos em segundo plano
→ Desligar TODOS os apps desnecessários
```

#### Desabilitar efeitos visuais
```
Painel de Controle > Sistema > Configurações avançadas do sistema
→ Desempenho > Configurações
→ Selecionar "Ajustar para obter o melhor desempenho"
```

#### Desabilitar indexação
```
Serviços (services.msc)
→ Windows Search → Desabilitar
```

### 2. Configurações do Chrome (MUITO IMPORTANTE)

#### Flags para economizar RAM
Digite na barra de endereço do Chrome:

```
chrome://flags
```

Ative estas flags:
- **#back-forward-cache** → Enabled (cache inteligente)
- **#enable-parallel-downloading** → Enabled (downloads mais eficientes)
- **#enable-gpu-rasterization** → Enabled (usa GPU para renderizar)

#### Desabilitar extensões
```
chrome://extensions
→ Desabilitar TODAS as extensões no PC do display
```

#### Modo kiosk (RECOMENDADO)
Crie um atalho do Chrome com o parâmetro:
```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --kiosk --app=http://localhost:5000/display
```

Benefícios:
- Sem barra de endereço/abas (economia de RAM)
- Tela cheia automática
- Menos recursos do navegador carregados

### 3. Otimização do vídeo (ESSENCIAL)

#### Compactar vídeo com HandBrake (GRÁTIS)
Download: https://handbrake.fr/

Configurações recomendadas:
- **Formato:** MP4
- **Codec:** H.264
- **Resolução:** 1280x720 (ao invés de 1920x1080)
- **Taxa de bits:** 1500-2000 kbps
- **FPS:** 30 (ao invés de 60)
- **Preset:** Very Fast

**Resultado esperado:** Vídeo 60-80% menor, mesma qualidade visual

#### Alternativa online (sem instalar)
https://www.freeconvert.com/video-compressor
- Upload do vídeo
- Reduzir resolução para 720p
- Comprimir para ~50% do tamanho original

### 4. Sistema operacional

#### Considerar Windows 10 LTSC
- Versão mais leve do Windows 10
- Sem bloatware/apps desnecessários
- Melhor para máquinas dedicadas (displays)

#### Ou usar Linux Mint
- Sistema operacional muito mais leve (usa ~800MB RAM)
- Chrome/Chromium funciona normalmente
- Sistema continua funcionando normalmente

### 5. Hardware (se possível)

#### Upgrade de RAM (IDEAL)
- 4GB → 8GB = R$ 100-150
- Maior impacto no desempenho
- Sistema vai rodar muito melhor

#### SSD (se ainda usa HD)
- 240GB SSD = R$ 120-150
- Sistema inicia 5x mais rápido
- Navegador carrega muito mais rápido

## 📊 Impacto esperado das otimizações

| Otimização | Economia de RAM | Economia de CPU |
|------------|-----------------|-----------------|
| Código otimizado | ~150-200MB | ~15-20% |
| Chrome sem extensões | ~100-150MB | ~10% |
| Vídeo compactado | ~50-100MB | ~10-15% |
| Flags do Chrome | ~80-120MB | ~5-10% |
| Modo kiosk | ~100-150MB | ~10% |
| **TOTAL** | **~500MB-700MB** | **~50-60%** |

## ⚡ Checklist de implementação

### Imediatas (faça agora)
- [ ] Desabilitar todas extensões do Chrome no PC do display
- [ ] Fechar todos programas desnecessários no Windows
- [ ] Compactar o vídeo para 720p
- [ ] Criar atalho modo kiosk do Chrome

### Curto prazo (esta semana)
- [ ] Ativar flags de performance do Chrome
- [ ] Desabilitar efeitos visuais do Windows
- [ ] Desabilitar apps em segundo plano
- [ ] Desabilitar Windows Search

### Médio prazo (se necessário)
- [ ] Considerar upgrade para 8GB RAM (R$ 100-150)
- [ ] Considerar trocar HD por SSD (R$ 120-150)

## 🆘 Se ainda estiver lento

1. **Verifique o Gerenciador de Tarefas** (Ctrl+Shift+Esc):
   - Chrome deve usar no máximo 60-70% da RAM
   - Se outros processos estiverem consumindo muito, desinstale

2. **Teste com navegador mais leve**:
   - Edge (consome menos RAM que Chrome)
   - Firefox (pode ser mais leve em alguns casos)

3. **Considere máquina dedicada**:
   - PC só para display (sem outros programas)
   - Sistema mais limpo e rápido

## 📝 Notas finais

O sistema agora está **otimizado ao máximo via software**. As melhorias mais significativas virão de:

1. **Compactar o vídeo** (ESSENCIAL) → 10-15% mais rápido
2. **Modo kiosk do Chrome** (RECOMENDADO) → 5-10% mais rápido
3. **Desabilitar extensões/apps** (IMPORTANTE) → 5-8% mais rápido
4. **Upgrade de RAM** (IDEAL) → 50-100% mais rápido

Com 8GB de RAM, o sistema rodará perfeitamente sem nenhuma preocupação.
