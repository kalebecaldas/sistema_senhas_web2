let ultimaVersao = null;

// static/js/painel.js
window.inicializarPainel = function() {
  if (!document.getElementById('painel-root')) return;   // ✅ EVITA ERRO FORA DO PAINEL

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

  // ─── Estado do guichê ─────────────────────────────────────────────────────────
  function atualizarEstadoGuiche() {
    const ok = SistemaUtils.Validators.isValidGuiche(guicheInput.value);
    btnPersonalizada.disabled = !ok;
    btnUltima.disabled        = !ok;
    btnProxima.disabled       = !ok;
    if (ok) SistemaUtils.SessionManager.setGuiche(guicheInput.value);
  }

  // inicializa guichê salvo
  guicheInput.value = SistemaUtils.SessionManager.getGuiche();
  guicheInput.addEventListener('input', atualizarEstadoGuiche);
  atualizarEstadoGuiche();

  // ─── Chama a API de ação ─────────────────────────────────────────────────────
  async function executarAcao(payload) {
    try {
      const json = await SistemaUtils.ApiUtils.postJson('/api/painel_action', payload);
      if (!json.success) {
        throw new Error(json.message || json.error || 'Erro desconhecido');
      }
      SistemaUtils.toastManager.success(json.message);
      await atualizarFila();
    } catch (err) {
      console.error(err);
      SistemaUtils.toastManager.error(err.message);
    }
  }

  // ─── Botões de ação ───────────────────────────────────────────────────────────
  btnPersonalizada.addEventListener('click', () => {
    const texto  = document.getElementById('texto_personalizado').value.trim();
    const guiche = guicheInput.value.trim();
    if (!texto || !guiche) return SistemaUtils.toastManager.warning('Preencha o texto e o guichê');
    executarAcao({ acao: 'personalizada', texto_personalizado: texto, guiche });
  });

  btnUltima.addEventListener('click', () => {
    const rech   = SistemaUtils.SessionManager.getRechamadaInfo();
    const guiche = guicheInput.value.trim();
    if (!rech || !rech.id) return SistemaUtils.toastManager.warning('Nenhuma senha para rechamar');
    executarAcao({ acao: 'rechamar', rechamar_id: rech.id, guiche });
  });

  btnProxima.addEventListener('click', () => {
    const guiche = guicheInput.value.trim();
    if (!guiche) return SistemaUtils.toastManager.warning('Informe o número do guichê');
    executarAcao({ acao: 'proxima', guiche });
  });

  // ─── Atualiza tabela de fila ─────────────────────────────────────────────────
  async function atualizarFila() {
    try {
      const dados = await SistemaUtils.ApiUtils.getJson('/painel_fila_json');

      // Verifica se houve mudança com base no conteúdo
      const versaoAtual = JSON.stringify(dados);
      if (JSON.stringify(dadosFila) === versaoAtual) return;
      dadosFila = dados;

      // salva última rechamada
      const chamadas = dados.filter(s => s.chamado);
      if (chamadas.length) {
        const u = chamadas.sort((a,b) => new Date(b.chamado_em) - new Date(a.chamado_em))[0];
        SistemaUtils.SessionManager.setRechamadaInfo({ 
          id: u.id, 
          guiche: guicheInput.value.trim() 
        });
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
  setInterval(atualizarFila, SISTEMA_CONFIG.INTERVALO_ATUALIZACAO);
};
