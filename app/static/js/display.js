let ultimaVersao = null;

document.addEventListener('DOMContentLoaded', () => {
  const { ultimaChamadaUrl, filaJsonUrl } = window.DISPLAY_CONFIG;

  let lastCall = { id: null, ts: 0 };
  let isOverlayShowing = false;
  const callQueue = [];
  let firstRun = true;

  function atualizarHora() {
    const horaElement = document.getElementById('hora');
    if (horaElement) {
      horaElement.textContent = new Date().toLocaleTimeString('pt-BR', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
      });
    }
  }

  async function falarComAzure(texto) {
    try {
      const res = await fetch(`/tts_audio?texto=${encodeURIComponent(texto)}`);
      if (!res.ok) {
        console.error('Erro TTS:', res.status, res.statusText);
        return;
      }
      const blob = await res.blob();
      const audio = new Audio(URL.createObjectURL(blob));
      audio.volume = 0.8; // Volume um pouco menor para melhor qualidade
      await audio.play();
    } catch (err) {
      console.error('Erro TTS:', err);
    }
  }

  function mostrarOverlay({ guiche, senha }) {
    isOverlayShowing = true;

    const isNum = /^\d+$/.test(guiche);
    const label = isNum ? 'GUICHÊ' : 'DESTINO';
    const div = document.getElementById('senha-chamada');
    
    // Layout melhorado para o overlay
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
          animation: pulse 1s infinite;
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
          animation: pulse 1s infinite;
        ">${senha}</div>
      </div>`;
    
    // Aplica cor de destaque configurável
    const root = document.documentElement;
    root.style.setProperty('--destaque-senha', window.DISPLAY_CONFIG.destaqueSenha || '#2196f3');

    div.classList.add('show');
    
    // Som de notificação
    new Audio('/static/audio/beep.mp3').play().catch(() => {});

    // TTS após 1 segundo
    setTimeout(() => {
      const prefixo = isNum ? 'ao guichê' : 'a';
      const spelled = senha.replace(/(\D+)(\d+)/, '$1 $2').split('').join(' ');
      const msg = /^[A-Za-z]+$/.test(senha)
        ? `${senha}, dirija-se ${prefixo} ${guiche}`
        : `Senha ${spelled}, dirija-se ${prefixo} ${guiche}`;
      falarComAzure(msg);
    }, 1000);

    // Esconder após 5 segundos
    setTimeout(() => {
      div.classList.remove('show');
      isOverlayShowing = false;
      if (callQueue.length) {
        const next = callQueue.shift();
        mostrarOverlay(next);
      }
    }, 5000);
  }

  function criarSenhaElement(senha, isUltima = false) {
    const el = document.createElement('div');
    el.className = isUltima ? 'senha-item ultima' : 'senha-item';
    
    // Exibe senha e guichê lado a lado
    el.innerHTML = `
      <span class="senha-label">${senha.senha_completa}</span>
      <span class="guiche-label">Guichê ${senha.guiche || '-'}</span>
    `;
    if (isUltima) {
      el.style.animation = 'slideInFromTop 0.5s ease-out';
    }
    return el;
  }

  async function loop() {
    try {
      const [rLista, rUltima] = await Promise.all([
        fetch(filaJsonUrl),
        fetch(ultimaChamadaUrl)
      ]);

      if (rLista.ok) {
        const dados = await rLista.json();
        if (dados.versao === ultimaVersao) return;
        ultimaVersao = dados.versao;
        const chamadas = dados.senhas || dados;

        const col = document.getElementById('lista-senhas');
        if (!col) return;

        // Calcular quantas senhas cabem na tela
        const containerHeight = col.offsetHeight;
        const itemHeight = 120; // Altura aproximada de cada item
        const maxItems = Math.floor((containerHeight - 100) / itemHeight); // -100 para o título

        col.innerHTML = '';
        
        // Adicionar senhas
        chamadas.slice(0, maxItems).forEach((s, i) => {
          const el = criarSenhaElement(s, i === 0);
          col.append(el);
        });

        // Adicionar mensagem se não há senhas
        if (chamadas.length === 0) {
          const emptyEl = document.createElement('div');
          emptyEl.className = 'senha-item';
          emptyEl.style.opacity = '0.6';
          emptyEl.style.fontStyle = 'italic';
          emptyEl.textContent = 'Nenhuma senha aguardando';
          col.append(emptyEl);
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
              lastCall = { id: u.id, ts };
              if (isOverlayShowing) {
                callQueue.push(u);
              } else {
                mostrarOverlay(u);
              }
            }
          }
        }
      }
    } catch (err) {
      console.error('Erro no loop de atualização:', err);
    }
  }

  // Adicionar CSS para animações
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideInFromTop {
      0% {
        opacity: 0;
        transform: translateY(-20px);
      }
      100% {
        opacity: 1;
        transform: translateY(0);
      }
    }
    
    @keyframes pulse {
      0%, 100% {
        transform: scale(1);
      }
      50% {
        transform: scale(1.05);
      }
    }
  `;
  document.head.appendChild(style);

  // Inicializar
  atualizarHora();
  setInterval(atualizarHora, 1000); // Atualizar a cada segundo para mostrar segundos
  loop();
  setInterval(loop, 2000);
});
