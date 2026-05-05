<template>
  <div class="map-wrapper">
    <div class="map-overlay">ESPÍRITO SANTO // CAMADA_CALOR</div>
    <div class="map-placeholder">
      <p>Área pronta para renderização de microdados.</p>
    </div>
  </div>
</template>

<style scoped>
.map-wrapper {
  width: 100%;
  height: 100%;
  background: #0d1117;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
.map-overlay {
  position: absolute;
  top: 15px;
  left: 15px;
  background: rgba(0,0,0,0.8);
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 10px;
  color: #da3633;
  font-weight: bold;
}
.map-placeholder { color: #30363d; font-size: 14px; }
</style>