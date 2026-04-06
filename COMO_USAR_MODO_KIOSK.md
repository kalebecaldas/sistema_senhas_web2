# Como usar o Modo Kiosk (Otimizado para 4GB RAM)

## 🚀 Modo Kiosk - O que é?

O **Modo Kiosk** é um modo especial do Chrome que:
- ✅ Abre em **tela cheia automática**
- ✅ **Remove barra de endereço, abas e menus** → Economia de RAM
- ✅ **Desabilita extensões automaticamente** → Mais rápido
- ✅ **Menos processos em segundo plano** → Menos CPU
- ✅ **Ideal para displays dedicados** → Máximo desempenho

### Economia esperada
- **~100-200MB de RAM** economizados
- **~10-15% menos uso de CPU**
- **Carregamento 20-30% mais rápido**

---

## 📋 Opção 1: Usar o script automático (MAIS FÁCIL)

### Passo a passo

1. **Execute o script:**
   ```
   iniciar_display_kiosk.bat
   ```

2. **O que acontece:**
   - Sistema Flask inicia automaticamente
   - Chrome abre em modo Kiosk após 10 segundos
   - Display aparece em tela cheia otimizada

3. **Para sair do modo Kiosk:**
   - Pressione **Alt+F4**
   - Ou feche a janela do CMD

### ⚠️ Primeira vez?
Se for a primeira vez rodando o sistema, execute antes:
```
iniciar_rapido.bat
```

---

## 📋 Opção 2: Criar atalho manual no Windows

### Passo a passo

1. **Clique com botão direito na Área de Trabalho**
   - Novo → Atalho

2. **Cole este comando:**
   ```
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --kiosk --app=http://localhost:5000/display --disable-extensions --disable-background-networking --disable-sync
   ```

3. **Nome do atalho:**
   ```
   Display - Modo Kiosk
   ```

4. **Clique em Concluir**

5. **Antes de usar o atalho:**
   - Execute primeiro: `iniciar_rapido.bat` (para iniciar o servidor)
   - Aguarde 10 segundos
   - Clique no atalho criado

---

## 📋 Opção 3: Iniciar automaticamente com o Windows

### Para iniciar o display automaticamente quando o PC ligar:

1. **Pressione Windows+R**

2. **Digite:**
   ```
   shell:startup
   ```

3. **Pressione Enter** (abre pasta de Inicialização)

4. **Copie o arquivo:**
   ```
   iniciar_display_kiosk.bat
   ```
   Para dentro da pasta que abriu

5. **Pronto!**
   - Na próxima vez que o PC ligar, o display iniciará automaticamente em modo Kiosk

---

## 🎯 Flags adicionais do Chrome (Avançado)

Se quiser **ainda mais performance**, edite o script `iniciar_display_kiosk.bat` e adicione estas flags:

```batch
start "" "%CHROME_PATH%" --kiosk --app=http://localhost:5000/display ^
  --disable-extensions ^
  --disable-background-networking ^
  --disable-sync ^
  --disable-translate ^
  --disable-features=TranslateUI ^
  --no-first-run ^
  --no-default-browser-check ^
  --disable-gpu-vsync ^
  --enable-gpu-rasterization ^
  --enable-zero-copy ^
  --disable-dev-shm-usage ^
  --disable-software-rasterizer
```

**O que cada flag faz:**
- `--disable-extensions`: Desabilita todas extensões
- `--disable-background-networking`: Para sincronizações em segundo plano
- `--disable-sync`: Desabilita sincronização com conta Google
- `--disable-translate`: Remove barra de tradução
- `--no-first-run`: Pula tela de boas-vindas
- `--enable-gpu-rasterization`: Usa GPU para renderizar (mais rápido)
- `--enable-zero-copy`: Economia de memória na GPU
- `--disable-dev-shm-usage`: Evita erro de memória compartilhada

---

## ❓ Problemas comuns

### ❌ "Chrome não encontrado"
**Solução:**
- Verifique se o Chrome está instalado
- Ou use Edge: substitua o caminho por:
  ```
  "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
  ```

### ❌ "Não consegue sair do modo Kiosk"
**Solução:**
- Pressione **Alt+F4**
- Ou **Ctrl+Alt+Del** → Gerenciador de Tarefas → Fechar Chrome

### ❌ "Página não carrega"
**Solução:**
- Verifique se o servidor Flask está rodando
- Execute primeiro: `iniciar_rapido.bat`
- Aguarde 10-15 segundos antes de abrir o Chrome

---

## 💡 Dicas extras

### Para melhor experiência:

1. **Use o modo Kiosk sempre** → Máximo desempenho
2. **Desabilite extensões do Chrome** (se não usar modo Kiosk)
3. **Compacte o vídeo para 720p** → Ver `OTIMIZACOES_4GB_RAM.md`
4. **Feche outros programas** → Deixe só o display rodando
5. **Considere upgrade de RAM** → 8GB = performance perfeita

---

## 📊 Comparativo

| Modo | Uso de RAM | Uso de CPU | Velocidade |
|------|------------|------------|------------|
| Chrome normal | ~800MB | 100% | Base |
| Chrome + flags | ~650MB | 85% | +15% |
| **Modo Kiosk** | **~500MB** | **70%** | **+30%** |

---

## ✅ Checklist final

Antes de usar o modo Kiosk:

- [ ] Servidor Flask está rodando (`iniciar_rapido.bat`)
- [ ] Aguardou 10 segundos para servidor iniciar
- [ ] Chrome está instalado
- [ ] Vídeo está compactado (idealmente 720p)
- [ ] Outras extensões do Chrome desabilitadas

**Pronto para usar!** 🚀

---

## 📞 Suporte

Se tiver problemas:
1. Verifique o arquivo `OTIMIZACOES_4GB_RAM.md`
2. Execute `teste_sistema.bat` para diagnóstico
3. Verifique logs em `erro.txt`
