// static/js/painel.js

window.inicializarPainel = function() {
  let dadosFila = [];
  const guicheInput      = document.getElementById('guiche');
  const btnPersonalizada = document.getElementById('btn-personalizada');
  const btnUltima        = document.getElementById('btn-ultima');
  const btnProxima       = document.getElementById('btn-proxima');
  const tbody            = document.getElementById('fila-corpo');
  const painelRoot       = document.getElementById('painel-root');
  const usuarioId        = parseInt(painelRoot.dataset.usuarioId || '0', 10);

  if (!guicheInput || !btnPersonalizada || !btnUltima || !btnProxima || !tbody) {
    console.warn('⚠️ Elementos do painel não encontrados.');
    return;
  }

  // ─── Função de exibir toast ───────────────────────────────────────────────────
  function flashToast(msg, type = 'info') {
    const container = document.getElementById('notification-container');
    if (!container) return console.warn('Notification container não encontrado');
    const notif = document.createElement('div');
    notif.className = `alert alert-${type} alert-dismissible fade show`;
    notif.role = 'alert';
    notif.innerHTML = `
      ${msg}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    container.appendChild(notif);
    // auto-dismiss após 4s
    setTimeout(() => {
      notif.classList.remove('show');
      notif.addEventListener('transitionend', () => notif.remove());
      notif.classList.add('hide');
    }, 4000);
  }

  // ─── Estado do guichê ─────────────────────────────────────────────────────────
  function atualizarEstadoGuiche() {
    const ok = guicheInput.value.trim() !== '';
    btnPersonalizada.disabled = !ok;
    btnUltima.disabled        = !ok;
    btnProxima.disabled       = !ok;
    if (ok) sessionStorage.setItem('guiche', guicheInput.value.trim());
  }

  // inicializa guichê salvo
  guicheInput.value = sessionStorage.getItem('guiche') || '';
  guicheInput.addEventListener('input', atualizarEstadoGuiche);
  atualizarEstadoGuiche();

  // ─── Chama a API de ação ─────────────────────────────────────────────────────
  async function executarAcao(payload) {
    try {
      const res  = await fetch('/api/painel_action', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });
      const json = await res.json();
      if (!res.ok || !json.success) throw new Error(json.message || 'Erro desconhecido');
      flashToast(json.message, 'success');
      await atualizarFila();
    } catch (err) {
      console.error(err);
      flashToast(err.message, 'danger');
    }
  }

  // ─── Botões de ação ───────────────────────────────────────────────────────────
  btnPersonalizada.addEventListener('click', () => {
    const texto  = document.getElementById('texto_personalizado').value.trim();
    const guiche = guicheInput.value.trim();
    if (!texto || !guiche) return flashToast('Preencha o texto e o guichê', 'warning');
    executarAcao({ acao: 'personalizada', texto_personalizado: texto, guiche });
  });

  btnUltima.addEventListener('click', () => {
    const rech   = JSON.parse(sessionStorage.getItem('rechamada_info') || 'null');
    const guiche = guicheInput.value.trim();
    if (!rech || !rech.id) return flashToast('Nenhuma senha para rechamar', 'warning');
    executarAcao({ acao: 'rechamar', rechamar_id: rech.id, guiche });
  });

  btnProxima.addEventListener('click', () => {
    const guiche = guicheInput.value.trim();
    if (!guiche) return flashToast('Informe o número do guichê', 'warning');
    executarAcao({ acao: 'proxima', guiche });
  });

  // ─── Atualiza tabela de fila ─────────────────────────────────────────────────
  async function atualizarFila() {
    try {
      const res   = await fetch('/painel_fila_json');
      if (!res.ok) throw new Error('Resposta inválida da API');
      const dados = await res.json();
      // só re-render se mudou
      if (JSON.stringify(dadosFila) === JSON.stringify(dados)) return;
      dadosFila = dados;

      // salva última rechamada
      const chamadas = dados.filter(s => s.chamado);
      if (chamadas.length) {
        const u = chamadas.sort((a,b) => new Date(b.chamado_em) - new Date(a.chamado_em))[0];
        sessionStorage.setItem(
          'rechamada_info',
          JSON.stringify({ id: u.id, guiche: guicheInput.value.trim() })
        );
      }

      // renderiza linhas
      tbody.innerHTML = '';
      dados.forEach(s => {
        const tr = document.createElement('tr');

        const tdSenha = document.createElement('td');
        tdSenha.textContent = s.senha_completa;
        tdSenha.className   = 'fw-bold';
        tr.appendChild(tdSenha);

        const tdStatus = document.createElement('td');
        tdStatus.innerHTML = s.chamado
          ? '<span class="badge bg-success">Chamado</span>'
          : '<span class="badge bg-secondary">Aguardando</span>';
        tr.appendChild(tdStatus);

        const tdAcao = document.createElement('td');
        if (s.chamado) {
          const btn = document.createElement('button');
          btn.type        = 'button';
          btn.className   = 'btn btn-secondary btn-sm';
          btn.textContent = 'Rechamar';
          btn.onclick     = () => executarAcao({
            acao: 'rechamar',
            rechamar_id: s.id,
            guiche: guicheInput.value.trim()
          });
          tdAcao.appendChild(btn);
        }
        tr.appendChild(tdAcao);

        tbody.appendChild(tr);
      });
    } catch (e) {
      console.error(e);
    }
  }

  // ─── Inicialização ───────────────────────────────────────────────────────────
  atualizarFila();
  setInterval(atualizarFila, 3000);
};
