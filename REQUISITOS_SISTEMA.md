# Requisitos de Sistema - Sistema de Senhas

## 💾 Requisitos de Memória RAM

### Mínimo (Funcional, mas pode ser lento)
- **4GB RAM total**
- **~1.5-2GB disponível** para o sistema
- Sistema pode ficar lento, especialmente com Chrome

### Recomendado (Ideal)
- **8GB RAM total**
- **~3-4GB disponível** para o sistema
- Roda perfeitamente, sem travamentos

### Ótimo (Máximo desempenho)
- **16GB RAM total**
- **~6-8GB disponível** para o sistema
- Sobra memória para outros programas

---

## 📊 Uso de Memória por Componente

### 1. Sistema Operacional (Windows 10/11)
| Componente | Uso de RAM |
|------------|------------|
| Windows 10/11 base | ~1.5-2GB |
| Serviços essenciais | ~300-500MB |
| **Total Windows** | **~1.8-2.5GB** |

### 2. Backend Flask (Python)
| Componente | Uso de RAM |
|------------|------------|
| Python runtime | ~50-80MB |
| Flask framework | ~20-30MB |
| SQLAlchemy (ORM) | ~30-50MB |
| Dependências (Azure TTS, etc) | ~50-100MB |
| Banco SQLite (em memória) | ~10-30MB |
| **Total Backend** | **~160-290MB** |

### 3. Navegador (Chrome/Edge)
| Modo | Uso de RAM |
|------|------------|
| Chrome normal | ~600-800MB |
| Chrome modo Kiosk | ~400-600MB |
| Edge normal | ~500-700MB |
| Edge modo Kiosk | ~350-500MB |
| **Total Navegador** | **~350-800MB** |

### 4. Vídeo (se houver)
| Resolução | Uso de RAM |
|-----------|------------|
| 720p (1280x720) | ~50-100MB |
| 1080p (1920x1080) | ~100-200MB |
| 4K (3840x2160) | ~300-500MB |

### 5. Outros Processos
| Componente | Uso de RAM |
|------------|------------|
| Antivírus | ~50-150MB |
| Outros programas | ~100-300MB |
| **Total Outros** | **~150-450MB** |

---

## 📈 Uso Total de Memória

### Cenário 1: PC Dedicado (Só Display)
```
Windows:            ~2.0GB
Backend Flask:      ~0.2GB
Chrome Kiosk:       ~0.5GB
Vídeo 720p:         ~0.1GB
Outros (mínimo):    ~0.2GB
─────────────────────────────
TOTAL:              ~3.0GB
```

**Recomendação:** **4GB RAM** (sobra 1GB de margem)

### Cenário 2: PC Compartilhado (Display + Outros Apps)
```
Windows:            ~2.0GB
Backend Flask:      ~0.2GB
Chrome normal:      ~0.7GB
Vídeo 1080p:        ~0.2GB
Outros programas:   ~0.5GB
─────────────────────────────
TOTAL:              ~3.6GB
```

**Recomendação:** **8GB RAM** (sobra 4.4GB de margem)

### Cenário 3: PC com Muitos Programas
```
Windows:            ~2.5GB
Backend Flask:      ~0.3GB
Chrome normal:      ~0.8GB
Vídeo 1080p:        ~0.2GB
Outros programas:   ~1.0GB
─────────────────────────────
TOTAL:              ~4.8GB
```

**Recomendação:** **8GB RAM mínimo** ou **16GB RAM** ideal

---

## 🖥️ Requisitos Completos do Sistema

### Processador (CPU)
- **Mínimo:** Intel Core i3 / AMD A6 (2 núcleos)
- **Recomendado:** Intel Core i5 / AMD Ryzen 3 (4 núcleos)
- **Ótimo:** Intel Core i7 / AMD Ryzen 5 (6+ núcleos)

### Armazenamento
- **Mínimo:** 10GB livres (sistema + banco de dados)
- **Recomendado:** 20GB livres (com backups)
- **Ideal:** SSD (sistema inicia 5x mais rápido)

### Sistema Operacional
- **Windows 10/11** (64-bit)
- **Linux** (Ubuntu 20.04+, Debian 11+)
- **macOS** (10.15+)

### Conexão
- **WiFi ou Ethernet** (recomendado: Ethernet para menor latência)
- **Largura de banda:** Mínimo 1 Mbps (recomendado: 5+ Mbps)

---

## ⚡ Otimizações para Reduzir Uso de RAM

### 1. Modo Kiosk (ECONOMIA: ~200MB)
```batch
iniciar_display_kiosk.bat
```
- Remove barra de endereço, abas, menus
- Desabilita extensões automaticamente

### 2. Compactar Vídeo (ECONOMIA: ~50-100MB)
- Converter para 720p ao invés de 1080p
- Usar codec H.264
- Taxa de bits: 1500-2000 kbps

### 3. Desabilitar Programas Desnecessários (ECONOMIA: ~200-500MB)
```
Configurações > Aplicativos > Inicialização
→ Desabilitar programas que não precisa
```

### 4. Usar Edge ao invés de Chrome (ECONOMIA: ~100-200MB)
- Edge geralmente usa menos RAM que Chrome
- Funciona igual para o display

### 5. Desabilitar Antivírus Temporariamente (ECONOMIA: ~50-150MB)
- Apenas se o PC for dedicado ao display
- ⚠️ **Cuidado:** Só faça isso se tiver certeza que o PC está seguro

---

## 📊 Comparativo: Antes vs Depois das Otimizações

| Item | Antes | Depois | Economia |
|------|-------|--------|----------|
| Chrome normal | ~800MB | - | - |
| Chrome Kiosk | - | ~500MB | **-300MB** |
| Vídeo 1080p | ~200MB | - | - |
| Vídeo 720p | - | ~100MB | **-100MB** |
| Código otimizado | ~50MB | ~30MB | **-20MB** |
| **TOTAL** | **~1.0GB** | **~630MB** | **-370MB** |

---

## 🎯 Recomendações por Cenário

### PC Dedicado (Só Display)
- **RAM:** 4GB mínimo, 8GB recomendado
- **CPU:** Qualquer processador moderno (2015+)
- **Armazenamento:** 20GB livres
- **Conexão:** Ethernet (melhor) ou WiFi estável

### PC Compartilhado (Display + Outros)
- **RAM:** 8GB mínimo, 16GB recomendado
- **CPU:** Intel i5 / AMD Ryzen 3 ou superior
- **Armazenamento:** 50GB livres
- **Conexão:** Ethernet ou WiFi 5GHz

### PC com Muitos Programas
- **RAM:** 16GB recomendado
- **CPU:** Intel i7 / AMD Ryzen 5 ou superior
- **Armazenamento:** SSD 256GB+
- **Conexão:** Ethernet obrigatório

---

## 🔍 Como Verificar Uso de Memória

### Windows
1. Pressione **Ctrl+Shift+Esc** (Gerenciador de Tarefas)
2. Aba **Desempenho** → **Memória**
3. Veja:
   - **Em uso:** Quanto está sendo usado
   - **Disponível:** Quanto está livre
   - **Committed:** Total comprometido

### Durante o Uso do Sistema
1. Abra o Gerenciador de Tarefas
2. Vá em **Detalhes**
3. Ordene por **Memória**
4. Veja:
   - **chrome.exe** ou **msedge.exe** → Navegador
   - **python.exe** → Backend Flask
   - **Total** → Soma de tudo

---

## ⚠️ Sinais de Pouca RAM

Se o sistema estiver com pouca RAM, você verá:
- ❌ Sistema **travando** ou **lento**
- ❌ Chrome **congelando** ou **fechando sozinho**
- ❌ Mensagem "**Memória insuficiente**"
- ❌ Display **não atualizando** corretamente
- ❌ Vídeo **travando** ou **sem som**

### Solução Imediata
1. Feche outros programas
2. Reinicie o navegador
3. Use modo Kiosk
4. Compacte o vídeo

### Solução Definitiva
- **Upgrade de RAM** (4GB → 8GB = R$ 100-150)

---

## 💡 Dicas Finais

### Para Máxima Economia de RAM:
1. ✅ Use **modo Kiosk** sempre
2. ✅ **Compacte vídeo** para 720p
3. ✅ **Feche outros programas** no PC do display
4. ✅ **Desabilite extensões** do navegador
5. ✅ Use **Edge** ao invés de Chrome (se possível)

### Para Melhor Performance:
1. ✅ **8GB RAM** mínimo
2. ✅ **SSD** ao invés de HD
3. ✅ **Ethernet** ao invés de WiFi
4. ✅ **PC dedicado** só para display

---

## 📝 Resumo Executivo

| RAM Total | Status | Recomendação |
|-----------|--------|--------------|
| **4GB** | ⚠️ Funciona, mas pode ser lento | Use modo Kiosk + vídeo 720p |
| **8GB** | ✅ Ideal | Roda perfeitamente |
| **16GB** | 🚀 Excelente | Sobra memória para tudo |

**Para deixar rodando 24/7 no PC do display:**
- **Mínimo:** 4GB RAM (com otimizações)
- **Recomendado:** 8GB RAM (sem preocupações)
- **Ideal:** 16GB RAM (máximo desempenho)

---

## 🔧 Script de Verificação

Crie um arquivo `verificar_ram.bat`:

```batch
@echo off
echo ========================================
echo   VERIFICACAO DE MEMORIA RAM
echo ========================================
echo.
wmic OS get TotalVisibleMemorySize,FreePhysicalMemory /format:list
echo.
echo ========================================
pause
```

Execute para ver quanto de RAM está disponível.

---

**Conclusão:** Com as otimizações implementadas, o sistema roda bem em **4GB RAM**, mas **8GB é o ideal** para deixar rodando 24/7 sem preocupações! 🚀
