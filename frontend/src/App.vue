<template>
  <div class="interface-grid">
    <!-- Sidebar com a Logo da FAESA -->
    <Sidebar @navegar="mudarTela" />

    <main class="data-viewport">
      <header class="header-monitor">
        <h1>Painel de Monitoramento da Violência Contra a Mulher</h1>
        <!-- Comentário removido conforme solicitado -->
      </header>

      <section class="container-central">
        <MapaDashboard :tela="telaAtiva" />
      </section>

      <footer class="shelf-dashboard">
        <div class="metrics-grid">
          <div class="metrica-card alert">
            <div class="topo-metrica">⚠️ <strong>Média Anual de Ocorrências: 1.632</strong></div>
            <p class="legenda-metrica">Dados baseados em séries históricas anuais</p>
          </div>
          <div class="metrica-card">
            <div class="topo-metrica">📍 <strong>Cidade Crítica (Histórico): Serra</strong></div>
            <p class="legenda-metrica">Base de microdados SSP-ES</p>
          </div>
          <div class="metrica-card">
            <div class="topo-metrica">🔮 <strong>Predição de Risco: Alto</strong></div>
            <p class="legenda-metrica">Região Noroeste - Média de anos</p>
          </div>
        </div>

        <div class="memorial-info">
          <h3>Contextualização Academicamente Sóbria e Memorial de Dados</h3>
          <p>Análise baseada em microdados reais da Secretaria de Segurança Pública do ES para o Projeto Integrador 2026.</p>
          <span class="pi-stamp">FAESA 2026</span>
        </div>
      </footer>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Sidebar from './components/Sidebar.vue';
import MapaDashboard from './components/MapaDashboard.vue';

const telaAtiva = ref('metrica1');

const mudarTela = (novaTela) => {
  telaAtiva.value = novaTela;
};
</script>

<style>
/* Mantendo o estilo de grid travado para preencher o notebook */
* { margin: 0; padding: 0; box-sizing: border-box; }
body, html { width: 100vw; height: 100vh; background: #1a1d21; overflow: hidden; font-family: sans-serif; }

.interface-grid {
  display: grid;
  grid-template-columns: 280px 1fr;
  width: 100vw;
  height: 100vh;
}

.data-viewport {
  display: flex;
  flex-direction: column;
  padding: 30px;
  height: 100vh;
}

.header-monitor h1 { color: #f0f6fc; font-size: 1.8rem; margin-bottom: 20px; }

.container-central { flex: 1; margin-bottom: 20px; border-radius: 12px; border: 1px solid rgba(240,246,252,0.1); background: #0d1117; }

.metrics-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 20px; }
.metrica-card { background: #22272e; border: 1px solid rgba(240,246,252,0.1); padding: 15px; border-radius: 10px; }
.metrica-card.alert { border-bottom: 3px solid #da3633; }
.topo-metrica strong { color: #f0f6fc; }
.legenda-metrica { font-size: 13px; color: #768390; margin-top: 5px; }

.memorial-info { background: rgba(34, 39, 46, 0.6); padding: 20px; border-radius: 10px; position: relative; }
.pi-stamp { position: absolute; right: 20px; bottom: 15px; font-weight: bold; opacity: 0.2; }
</style>