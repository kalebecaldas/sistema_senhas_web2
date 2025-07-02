{% extends "base.html" %}
{% block head_extra %}
  <link rel="stylesheet" href="{{ url_for('static', filename='css/prioridade_senhas.css') }}?v=1">
{% endblock %}
{% block title %}Prioridade de Senhas{% endblock %}

{% block content %}
<div class="container">
  <h2 class="mb-4">Configuração da Lógica de Prioridade</h2>

  <form method="POST" action="{{ url_for('main.salvar_prioridade') }}">
    <div class="form-group mb-4">
      <label class="form-label d-block">Escolha a lógica de chamada de senhas:</label>

      <!-- Intercalamento Fixo -->
      <div class="mb-4 p-3 border rounded bg-light">
        <div class="form-check">
          <input class="form-check-input" type="radio" name="tipo_prioridade" id="intercalamento" value="intercalamento" {% if config.tipo_prioridade == 'intercalamento' %}checked{% endif %}>
          <label class="form-check-label fs-5" for="intercalamento">Intercalamento Fixo</label>
        </div>
        <div class="ms-4 mt-2 small text-muted">
          <p><strong>O que é:</strong> Chama 1 senha preferencial a cada N senhas normais.</p>
          <p><strong>Ideal:</strong> Fluxos regulares com proporção próxima entre pacientes preferenciais e normais.</p>
          <p><strong>Recomendado:</strong> 1 senha preferencial a cada 2 ou 3 normais.</p>
        </div>
      </div>

      <!-- Sistema de Peso -->
      <div class="mb-4 p-3 border rounded bg-light">
        <div class="form-check">
          <input class="form-check-input" type="radio" name="tipo_prioridade" id="peso" value="peso" {% if config.tipo_prioridade == 'peso' %}checked{% endif %}>
          <label class="form-check-label fs-5" for="peso">Sistema de Peso</label>
        </div>
        <div class="ms-4 mt-2 small text-muted">
          <p><strong>O que é:</strong> Cada tipo de senha recebe um peso. Quanto maior o peso, maior a chance de ser chamada.</p>
          <p><strong>Ideal:</strong> Situações com muitos preferenciais em relação aos normais.</p>
          <p><strong>Recomendado:</strong> Peso 3 para preferenciais e peso 1 para normais.</p>
        </div>
      </div>

      <!-- Alternância Dinâmica -->
      <div class="mb-4 p-3 border rounded bg-light">
        <div class="form-check">
          <input class="form-check-input" type="radio" name="tipo_prioridade" id="alternancia" value="alternancia" {% if config.tipo_prioridade == 'alternancia' %}checked{% endif %}>
          <label class="form-check-label fs-5" for="alternancia">Alternância Dinâmica</label>
        </div>
        <div class="ms-4 mt-2 small text-muted">
          <p><strong>O que é:</strong> Alterna entre preferenciais e normais com base no tempo de espera médio.</p>
          <p><strong>Ideal:</strong> Ambientes com variação imprevisível de fluxo.</p>
          <p><strong>Recomendado:</strong> Tolerância de 5 a 10 minutos de espera máxima para preferenciais.</p>
        </div>
      </div>
    </div>

    <!-- Intercalamento fixo -->
    <div id="campo-intercalamento" class="mb-4 d-none">
      <label for="intercalamento_valor" class="form-label">Chamar 1 senha preferencial a cada quantas senhas normais?</label>
      <input type="number" class="form-control" id="intercalamento_valor" name="intercalamento_valor" min="1" max="3" value="{{ config.intercalamento_valor or 2 }}">
      <div class="form-text text-danger d-none" id="aviso-nao-recomendado">Valor 4 ou maior não recomendado. Isso pode comprometer o tempo de espera dos preferenciais.</div>
    </div>

    <!-- Sistema de Peso -->
    <div id="campo-peso" class="row g-3 mb-4 d-none">
      <div class="col-md-6">
        <label for="peso_normal" class="form-label">Peso para senhas normais:</label>
        <input type="number" class="form-control" id="peso_normal" name="peso_normal" min="1" value="{{ config.peso_normal or 1 }}">
      </div>
      <div class="col-md-6">
        <label for="peso_preferencial" class="form-label">Peso para senhas preferenciais:</label>
        <input type="number" class="form-control" id="peso_preferencial" name="peso_preferencial" min="1" value="{{ config.peso_preferencial or 3 }}">
      </div>
    </div>

    <!-- Alternância dinâmica -->
    <div id="campo-alternancia" class="mb-4 d-none">
      <label for="tolerancia_minutos" class="form-label">Tolerância máxima de espera para preferenciais (em minutos):</label>
      <input type="number" class="form-control" id="tolerancia_minutos" name="tolerancia_minutos" min="1" value="{{ config.tolerancia_minutos or 5 }}">
    </div>

    <div class="mt-4">
      <button type="submit" class="btn btn-primary">Salvar Prioridade</button>
    </div>
  </form>
</div>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/prioridade_senhas.js') }}?v=1"></script>
{% endblock %}
