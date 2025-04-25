// ✅ Lógica da página de prioridade de senhas
window.inicializarPrioridadeSenhas = function () {
  function atualizarVisibilidadeCampos() {
    const tipo = document.querySelector('input[name="tipo_prioridade"]:checked')?.value;

    document.getElementById('campo-intercalamento')?.classList.toggle('d-none', tipo !== 'intercalamento');
    document.getElementById('campo-peso')?.classList.toggle('d-none', tipo !== 'peso');
    document.getElementById('campo-alternancia')?.classList.toggle('d-none', tipo !== 'alternancia');
  }

  atualizarVisibilidadeCampos();

  document.querySelectorAll('input[name="tipo_prioridade"]').forEach(el => {
    el.addEventListener('change', atualizarVisibilidadeCampos);
  });

  // Tooltips Bootstrap
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
    new bootstrap.Tooltip(el);
  });

  // Validação de aviso visual para intercalamento >= 4
  const intercalamentoInput = document.getElementById('intercalamento_valor');
  const aviso = document.getElementById('aviso-nao-recomendado');
  if (intercalamentoInput && aviso) {
    intercalamentoInput.addEventListener('input', () => {
      const valor = parseInt(intercalamentoInput.value);
      aviso.classList.toggle('d-none', isNaN(valor) || valor < 4);
    });
  }
};

// ✅ Executa na carga inicial (F5 ou acesso direto)
document.addEventListener("DOMContentLoaded", () => {
  if (typeof inicializarPrioridadeSenhas === 'function') {
    inicializarPrioridadeSenhas();
  }
});
