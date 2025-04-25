// static/js/display.js

document.addEventListener('DOMContentLoaded', () => {
  const { ultimaChamadaUrl, filaJsonUrl } = window.DISPLAY_CONFIG;

  let lastCall         = { id: null, ts: 0 };
  let isOverlayShowing = false;
  const callQueue      = [];
  let firstRun         = true; // ignora primeira detecção ao carregar

  // Atualiza o relógio no rodapé
  function atualizarHora() {
    document.getElementById('hora').textContent =
      new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
  }

  // TTS via Azure
  async function falarComAzure(texto) {
    try {
      const res = await fetch(
        `${ultimaChamadaUrl.replace('/ultima_chamada','/tts_audio')}?texto=${encodeURIComponent(texto)}`
      );
      if (!res.ok) return;
      const blob = await res.blob();
      new Audio(URL.createObjectURL(blob)).play();
    } catch (err) {
      console.error('Erro TTS:', err);
    }
  }

  // Exibe overlay de chamada e enfileira próximas
  function mostrarOverlay({ guiche, senha }) {
    isOverlayShowing = true;

    const isNum = /^\d+$/.test(guiche);
    const label = isNum ? 'GUICHÊ' : 'DESTINO';
    const div   = document.getElementById('senha-chamada');
    div.innerHTML = `
      <div>
        <div style="font-size:3rem;">${label}</div>
        <div style="font-size:6rem;font-weight:bold;">${guiche}</div>
        <div style="font-size:3rem;margin-top:2rem;">SENHA</div>
        <div style="font-size:6rem;font-weight:bold;">${senha}</div>
      </div>`;
    div.classList.add('show');
    new Audio('/static/audio/beep.mp3').play();

    // TTS 1s depois
    setTimeout(() => {
      const prefixo = isNum ? 'ao guichê' : 'a';
      const spelled = senha.replace(/(\D+)(\d+)/,'$1 $2').split('').join(' ');
      const msg = /^[A-Za-z]+$/.test(senha)
        ? `${senha}, dirija-se ${prefixo} ${guiche}`
        : `Senha ${spelled}, dirija-se ${prefixo} ${guiche}`;
      falarComAzure(msg);
    }, 1000);

    // Fecha após 5s e processa próxima da fila
    setTimeout(() => {
      div.classList.remove('show');
      isOverlayShowing = false;
      if (callQueue.length) {
        const next = callQueue.shift();
        mostrarOverlay(next);
      }
    }, 5000);
  }

  // Único loop que atualiza lista e checa última chamada
  async function loop() {
    try {
      const [rLista, rUltima] = await Promise.all([
        fetch(filaJsonUrl),
        fetch(ultimaChamadaUrl)
      ]);

      // 1) atualiza coluna lateral
      if (rLista.ok) {
        const dados = await rLista.json();
        const chamadas = dados
          .filter(s => s.chamado)
          .sort((a,b) => new Date(b.chamado_em) - new Date(a.chamado_em));

        const col = document.getElementById('lista-senhas');
        col.innerHTML = '';
        const max = Math.floor(col.offsetHeight / 90);
        chamadas.slice(0, max).forEach((s,i) => {
          const el = document.createElement('div');
          el.className = i===0 ? 'senha-item ultima' : 'senha-item';
          el.textContent = s.senha_completa;
          col.append(el);
        });
      }

      // 2) dispara overlay em chamada ou rechamada
      if (rUltima.ok) {
        const u = await rUltima.json();
        if (u.id) {
          const ts = new Date(u.chamado_em).getTime();
          if (u.id !== lastCall.id || ts > lastCall.ts) {
            // na primeira execução, só registra sem disparar overlay
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

  // Inicialização
  atualizarHora();
  setInterval(atualizarHora, 10000);

  loop();
  setInterval(loop, 2000);
});
