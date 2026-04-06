let ultimaVersao = null;

/**
 * Sintetiza o som de chamada de acordo com o tipo configurado.
 * Usa Web Audio API; nenhum arquivo MP3 adicional é necessário.
 */
function tocarSomChamada(tipo) {
  tipo = tipo || 'sino_suave';

  if (tipo === 'beep') {
    new Audio('/static/audio/beep.mp3').play().catch(() => {});
    return;
  }

  const ctx = new (window.AudioContext || window.webkitAudioContext)();

  function pulso(freq, startTime, duration, volume) {
    const osc  = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, startTime);
    gain.gain.setValueAtTime(0, startTime);
    gain.gain.linearRampToValueAtTime(volume, startTime + 0.005);
    gain.gain.exponentialRampToValueAtTime(0.0001, startTime + duration);
    osc.start(startTime);
    osc.stop(startTime + duration + 0.01);
  }

  const now = ctx.currentTime;

  if (tipo === 'sino_suave') {
    // Sino único, suave, 660 Hz, decaimento lento
    pulso(660, now, 1.5, 0.35);
  } else if (tipo === 'duplo') {
    // Dois toques suaves em sequência
    pulso(700, now, 0.9, 0.30);
    pulso(700, now + 0.28, 0.9, 0.28);
  } else if (tipo === 'cristal') {
    // Nota aguda pura, longo fade-out
    pulso(1320, now, 2.0, 0.22);
  } else if (tipo === 'sino_grave') {
    // Tom grave com harmônico suave
    pulso(330, now, 1.8, 0.35);
    pulso(660, now, 1.8, 0.12);
  } else {
    // Fallback: MP3 original
    new Audio('/static/audio/beep.mp3').play().catch(() => {});
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const { ultimaChamadaUrl, filaJsonUrl } = window.DISPLAY_CONFIG;

  let lastCall = { id: null, ts: 0 };
  let isOverlayShowing = false;
  let lastShownCallId = null;
  const callQueue = [];
  let firstRun = true;

  // ========================================
  // Configuração de Vídeo OTIMIZADA (4GB RAM)
  // ========================================
  const mainVideo = document.getElementById('main-video');
  const backgroundVideo = document.getElementById('background-video');
  const unmuteBtn = document.getElementById('unmute-btn');

  let videoMuted = true;

  if (mainVideo) {
    // Configurar volume do vídeo
    mainVideo.volume = 0.3;

    // Otimizações de performance
    mainVideo.style.display = 'block';
    mainVideo.style.width = '100%';
    mainVideo.style.height = '100%';
    mainVideo.style.objectFit = 'contain';
    
    // Forçar aceleração de hardware
    mainVideo.style.transform = 'translateZ(0)';
    
    // Desabilitar vídeo de background
    if (backgroundVideo) {
      backgroundVideo.remove();
    }

    // Detectar orientação do vídeo
    mainVideo.addEventListener('loadedmetadata', () => {
      const videoWidth = mainVideo.videoWidth;
      const videoHeight = mainVideo.videoHeight;
      const isVertical = videoHeight > videoWidth;

      if (videoWidth === 0 || videoHeight === 0) {
        console.warn('⚠️ Vídeo sem dimensões válidas - converta para MP4');
        mainVideo.style.width = '100%';
        mainVideo.style.height = '100%';
        mainVideo.style.objectFit = 'contain';
        return;
      }

      if (isVertical) {
        mainVideo.style.maxWidth = '50%';
        mainVideo.style.maxHeight = '100%';
        mainVideo.style.margin = '0 auto';
      } else {
        mainVideo.style.maxWidth = '100%';
        mainVideo.style.maxHeight = '100%';
      }
    });

    // Detectar erros
    mainVideo.addEventListener('error', (e) => {
      console.error('❌ Erro ao carregar vídeo:', mainVideo.error);
      
      const container = document.getElementById('video-container');
      if (container && mainVideo.error) {
        const errorMsg = mainVideo.error.code === 4 ? 
          'Formato não suportado. Use MP4 (H.264).' :
          'Erro ao carregar vídeo.';
        
        container.innerHTML = `
          <div style="color: white; text-align: center; padding: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⚠️</div>
            <div style="font-size: 1.5rem; margin-bottom: 1rem;">${errorMsg}</div>
            <div style="font-size: 1rem; opacity: 0.7;">
              Converta para MP4 em: <a href="https://cloudconvert.com/mov-to-mp4" target="_blank" style="color: #f43f5e;">CloudConvert</a>
            </div>
          </div>`;
      }
    });

    // Timeout para detectar vídeo travado
    setTimeout(() => {
      if (mainVideo.readyState === 0) {
        console.warn('⚠️ Vídeo não carregou após 5s - possível problema de formato');
      }
    }, 5000);

    // Botão de unmute
    if (unmuteBtn) {
      unmuteBtn.style.display = 'flex';
      unmuteBtn.addEventListener('click', () => {
        mainVideo.muted = false;
        videoMuted = false;
        unmuteBtn.style.display = 'none';
      });
    }
  }

  // ========================================
  // Relógio OTIMIZADO (atualiza a cada 5s ao invés de 1s)
  // ========================================
  function atualizarHora() {
    const now = new Date();
    const clockEl = document.getElementById('clock-time');
    const dateEl = document.getElementById('clock-date');

    if (clockEl) {
      clockEl.textContent = now.toLocaleTimeString('pt-BR', {
        hour: '2-digit',
        minute: '2-digit'
      });
    }

    if (dateEl) {
      dateEl.textContent = now.toLocaleDateString('pt-BR', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
      });
    }
  }

  // ========================================
  // TTS Azure
  // ========================================
  async function falarComAzure(texto) {
    try {
      if (mainVideo) mainVideo.volume = 0.1;

      const res = await fetch(`/tts_audio?texto=${encodeURIComponent(texto)}`);
      if (!res.ok) {
        console.error('Erro TTS:', res.status);
        return;
      }
      const blob = await res.blob();
      const audio = new Audio(URL.createObjectURL(blob));
      audio.volume = 0.8;
      await audio.play();

      audio.addEventListener('ended', () => {
        if (mainVideo) mainVideo.volume = 0.3;
      });
    } catch (err) {
      console.error('Erro TTS:', err);
      if (mainVideo) mainVideo.volume = 0.3;
    }
  }

  // ========================================
  // Overlay de chamada
  // ========================================
  function mostrarOverlay({ guiche, senha, id }) {
    if (id && id === lastShownCallId && isOverlayShowing) {
      console.warn('⚠️ Duplicata prevenida:', id);
      return;
    }
    
    if (id) lastShownCallId = id;
    isOverlayShowing = true;

    const isNum = /^\d+$/.test(guiche);
    const label = isNum ? 'GUICHÊ' : 'DESTINO';
    const div = document.getElementById('senha-chamada');
    
    if (!div) {
      console.error('❌ Elemento #senha-chamada não encontrado');
      return;
    }

    div.innerHTML = `
      <div style="text-align: center; max-width: 90vw;">
        <div style="
          font-size: 4rem; 
          font-weight: 600; 
          color: #fff; 
          text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
          margin-bottom: 1rem;
          opacity: 0.9;
        ">${label}</div>
        <div style="
          font-size: 12rem; 
          font-weight: 900; 
          color: var(--destaque-senha, #2196f3); 
          text-shadow: 0 0 8px var(--destaque-senha, #2196f3);
          margin-bottom: 2rem;
        ">${guiche}</div>
        <div style="
          font-size: 4rem; 
          font-weight: 600; 
          color: #fff; 
          text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
          margin-bottom: 1rem;
          opacity: 0.9;
        ">SENHA</div>
        <div style="
          font-size: 12rem; 
          font-weight: 900; 
          color: var(--destaque-senha, #2196f3); 
          text-shadow: 0 0 8px var(--destaque-senha, #2196f3);
        ">${senha}</div>
      </div>`;

    const root = document.documentElement;
    root.style.setProperty('--destaque-senha', window.DISPLAY_CONFIG.destaqueSenha || '#f43f5e');

    div.classList.add('show');

    // Tocar som de chamada configurado
    tocarSomChamada(window.DISPLAY_CONFIG.somChamada);

    // Falar imediatamente
    const prefixo = isNum ? 'ao guichê' : 'a';
    const spelled = senha.replace(/(\D+)(\d+)/, '$1 $2').split('').join(' ');
    const msg = /^[A-Za-z]+$/.test(senha)
      ? `${senha}, dirija-se ${prefixo} ${guiche}`
      : `Senha ${spelled}, dirija-se ${prefixo} ${guiche}`;
    falarComAzure(msg);

    setTimeout(() => {
      div.classList.remove('show');
      isOverlayShowing = false;
      
      if (callQueue.length) {
        const next = callQueue.shift();
        console.log('📋 Próxima da fila:', next.senha);
        setTimeout(() => {
          mostrarOverlay(next);
        }, 300);
      }
    }, 5000);
  }

  // ========================================
  // Atualizar fila visual
  // ========================================
  function updateQueueDisplay(chamadas) {
    const nowServingNumber = document.getElementById('now-serving-number');
    const nowServingDesk = document.getElementById('now-serving-desk');

    if (chamadas.length > 0) {
      const current = chamadas[0];
      if (nowServingNumber) nowServingNumber.textContent = current.senha_completa;
      if (nowServingDesk) nowServingDesk.textContent = `Guichê ${current.guiche}`;
    } else {
      if (nowServingNumber) nowServingNumber.textContent = '---';
      if (nowServingDesk) nowServingDesk.textContent = '---';
    }

    const recentList = document.getElementById('recent-list');
    if (!recentList) return;
    
    const recentItems = chamadas.slice(1);

    if (recentItems.length === 0) {
      recentList.innerHTML = `
        <div class="empty-state">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
          <span>Aguardando...</span>
        </div>`;
    } else {
      let html = '';
      recentItems.forEach(item => {
        let timeStr = '';
        if (item.chamado_em) {
          try {
            // O backend já envia o horário convertido para o fuso local (Manaus)
            // Apenas formatar como horário local
            const date = new Date(item.chamado_em);
            // Verificar se a data é válida
            if (!isNaN(date.getTime())) {
              // Formatar como horário local (já está no fuso correto)
              timeStr = date.toLocaleTimeString('pt-BR', { 
                hour: '2-digit', 
                minute: '2-digit',
                hour12: false
              });
            }
          } catch (e) {
            console.error('Erro ao formatar horário:', e, item.chamado_em);
          }
        }
        
        html += `
          <div class="recent-item">
            <div>
              <div class="recent-item-senha">${item.senha_completa}</div>
              <div class="recent-item-label">Senha</div>
            </div>
            <div class="recent-item-desk">
              <div class="recent-item-guiche">
                <span class="recent-item-dot"></span>
                <span>Guichê ${item.guiche}</span>
              </div>
              <div class="recent-item-time">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                ${timeStr}
              </div>
            </div>
          </div>`;
      });
      recentList.innerHTML = html;
    }
  }

  // ========================================
  // Sistema de Fetch OTIMIZADO para WiFi
  // ========================================
  let networkLatency = 0;
  let consecutiveSlowRequests = 0;
  let currentPollingInterval = 100; // Intervalo ULTRA RÁPIDO para detecção instantânea
  let fastModeActive = false;
  let fastModeTimeout = null;
  const FAST_MODE_INTERVAL = 50; // Modo ultra rápido - 50ms (20 verificações por segundo)
  const NORMAL_MODE_INTERVAL = 100; // Modo normal ultra rápido - 100ms (10 verificações por segundo)
  const SLOW_MODE_INTERVAL = 500; // Modo lento apenas se WiFi muito lento
  
  async function fetchWithTimeout(url, options = {}, timeout = 3000, retries = 0) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    
    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        const startTime = Date.now();
        const response = await fetch(url, {
          ...options,
          signal: controller.signal,
          cache: 'no-store'
        });
        clearTimeout(timeoutId);
        
        const duration = Date.now() - startTime;
        networkLatency = (networkLatency * 0.7) + (duration * 0.3);
        
        // Detectar WiFi lento (só ativa modo lento se WiFi MUITO lento)
        if (duration > 1000) {
          consecutiveSlowRequests++;
          if (consecutiveSlowRequests > 5 && !fastModeActive) {
            currentPollingInterval = Math.min(SLOW_MODE_INTERVAL, currentPollingInterval + 50);
            console.warn(`⚠️ WiFi muito lento (${duration}ms). Polling: ${currentPollingInterval}ms`);
          }
        } else {
          consecutiveSlowRequests = Math.max(0, consecutiveSlowRequests - 1);
          // Só volta ao normal se não estiver em modo rápido
          if (consecutiveSlowRequests === 0 && !fastModeActive && currentPollingInterval > NORMAL_MODE_INTERVAL) {
            currentPollingInterval = NORMAL_MODE_INTERVAL;
          }
        }
        
        return response;
      } catch (error) {
        clearTimeout(timeoutId);
        
        if (attempt < retries && error.name !== 'AbortError') {
          await new Promise(resolve => setTimeout(resolve, 300 * Math.pow(2, attempt)));
          continue;
        }
        
        throw error;
      }
    }
  }

  // ========================================
  // Loop principal ULTRA OTIMIZADO
  // ========================================
  let loopRunning = false;

  async function loop() {
    if (loopRunning) return;
    
    loopRunning = true;
    
    try {
      const [rLista, rUltima] = await Promise.all([
        fetchWithTimeout(filaJsonUrl, {}, 2000, 0),
        fetchWithTimeout(ultimaChamadaUrl, {}, 2000, 0)
      ]);

      if (rLista.ok) {
        const dados = await rLista.json();
        if (dados.versao !== ultimaVersao || firstRun) {
          ultimaVersao = dados.versao;
          const chamadas = dados.senhas || dados;
          updateQueueDisplay(chamadas);
        }
      }

      if (rUltima.ok) {
        const u = await rUltima.json();
        if (u.id) {
          const ts = new Date(u.chamado_em).getTime();
          
          if (u.id !== lastCall.id || ts > lastCall.ts) {
            if (firstRun) {
              lastCall = { id: u.id, ts };
              firstRun = false;
            } else {
              // NOVA CHAMADA DETECTADA - ATIVAR MODO RÁPIDO
              const isNewCall = u.id !== lastCall.id || ts > lastCall.ts;
              
              if (isNewCall) {
                if (!fastModeActive) {
                  fastModeActive = true;
                  currentPollingInterval = FAST_MODE_INTERVAL;
                  console.log('⚡ Modo rápido ativado para detectar chamadas rapidamente');
                  
                  // Cancelar próximo loop agendado e reagendar imediatamente
                  if (nextLoopTimeout) clearTimeout(nextLoopTimeout);
                  scheduleNextLoop();
                }
                
                // Resetar timeout do modo rápido (estender por mais 5s)
                if (fastModeTimeout) clearTimeout(fastModeTimeout);
                fastModeTimeout = setTimeout(() => {
                  fastModeActive = false;
                  currentPollingInterval = NORMAL_MODE_INTERVAL;
                  console.log('✅ Voltando ao modo normal');
                }, 5000);
              }
              
              lastCall = { id: u.id, ts };
              if (isOverlayShowing) {
                const jaEstaNaFila = callQueue.some(item => item.id === u.id);
                
                if (jaEstaNaFila) {
                  console.log('⚠️ Já na fila:', u.senha);
                } else {
                  console.log('⏳ Adicionando à fila:', u.senha);
                  callQueue.push(u);
                }
              } else {
                console.log('🚀 Mostrando:', u.senha);
                mostrarOverlay(u);
              }
            }
          }
        }
      }
    } catch (err) {
      console.error('Erro no loop:', err);
    } finally {
      loopRunning = false;
    }
  }

  // ========================================
  // Sistema de reconexão
  // ========================================
  const overlay = document.getElementById('reconnect-overlay');
  const videoEl = document.getElementById('main-video');
  let offline = false;

  async function checkServer() {
    try {
      const res = await fetchWithTimeout(window.DISPLAY_CONFIG.pingUrl, {}, 5000, 1);
      if (!res.ok) throw new Error();
      if (offline) {
        overlay.style.display = 'none';
        if (videoEl) videoEl.play();
        offline = false;
      }
    } catch {
      if (!offline) {
        offline = true;
        overlay.style.display = 'flex';
        if (videoEl) videoEl.pause();
      }
    }
  }

  // ========================================
  // Inicialização OTIMIZADA para 4GB RAM
  // ========================================
  atualizarHora();
  setInterval(atualizarHora, 5000); // A cada 5s ao invés de 1s
  
  loop();
  
  // Polling adaptativo com modo rápido
  let nextLoopTimeout = null;
  function scheduleNextLoop() {
    if (nextLoopTimeout) clearTimeout(nextLoopTimeout);
    
    nextLoopTimeout = setTimeout(() => {
      loop().finally(() => {
        scheduleNextLoop();
      });
    }, currentPollingInterval);
  }
  scheduleNextLoop();
  
  setInterval(checkServer, 6000); // Menos frequente
  
  console.log('✅ Sistema iniciado (modo 4GB RAM)');
});
