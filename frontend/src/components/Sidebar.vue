<template>
  <aside class="sidebar-container">
    <!-- TOPO LIMPO: Título de Métricas como primeiro item -->
    <header class="titulo-sessao">MÉTRICAS</header>
    
    <nav class="botoes-navegacao">
      <button 
        v-for="bt in botoes" 
        :key="bt.id"
        :class="['btn-nav', { ativo: botaoAtivo === bt.id }]"
        @click="clicarBotao(bt.id)"
      >
        {{ bt.label }}
      </button>
    </nav>

    <!-- LOGO DA FAESA NO FINAL (Puxando da pasta public) -->
    <footer class="footer-faesa">
      <img src="/logo-faesa.png" alt="FAESA Centro Universitário" class="faesa-img-final">
    </footer>
  </aside>
</template>

<script setup>
import { ref } from 'vue';

const emit = defineEmits(['navegar']);
const botaoAtivo = ref('metrica1');

// Lista de botões genérica conforme solicitado
const botoes = [
  { id: 'metrica1', label: '📊 MÉTRICA 1' },
  { id: 'metrica2', label: '📊 MÉTRICA 2' },
  { id: 'metrica3', label: '📊 MÉTRICA 3' },
  { id: 'metrica4', label: '📊 MÉTRICA 4' },
  { id: 'metrica5', label: '📊 MÉTRICA 5' },
  { id: 'metrica6', label: '📊 MÉTRICA 6' }
];

const clicarBotao = (id) => {
  botaoAtivo.value = id;
  emit('navegar', id);
};
</script>

<style scoped>
.sidebar-container {
  background-color: #1c2128;
  border-right: 1px solid rgba(240, 246, 252, 0.1);
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.titulo-sessao { 
  padding: 40px 30px 20px; 
  font-size: 11px; 
  font-weight: 800; 
  color: #768390; 
  letter-spacing: 2px; 
}

.botoes-navegacao { 
  display: flex; 
  flex-direction: column; 
  gap: 4px; 
  flex: 1; 
}

.btn-nav {
  background: none; 
  border: none; 
  color: #adbac7; 
  text-align: left;
  padding: 12px 30px; 
  font-size: 13px; 
  cursor: pointer; 
  transition: 0.2s;
  width: 90%; 
  border-radius: 0 25px 25px 0;
}

.btn-nav:hover { 
  background: rgba(255, 255, 255, 0.05); 
  color: #f0f6fc; 
}

.btn-nav.ativo { 
  background: #440c10; 
  color: #f0f6fc; 
  font-weight: bold; 
}

/* ESTILO DA LOGO DA FAESA NO RODAPÉ */
.footer-faesa {
  padding: 30px;
  display: flex;
  justify-content: center;
  border-top: 1px solid rgba(240, 246, 252, 0.1);
}

.faesa-img-final {
  width: 130px; /* Tamanho ajustado para o notebook */
  filter: brightness(0) invert(1); /* Deixa a logo branca */
  opacity: 0.9;
  object-fit: contain;
}
</style>