<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app color="surface">
      <v-list-item
        class="bg-primary text-black px-6 elevation-3"
        height="64"
        style="position: relative; z-index: 10;"
      >
        <template v-slot:title>
          <span class="font-weight-bold">Painel de Dados</span>
        </template>
        <template v-slot:subtitle>
          <span class="text-black font-weight-medium" style="opacity: 0.8">Menu de Navegação</span>
        </template>
        <template v-slot:append>
          <img src="../assets/fitaRoxa.png" alt="Fita Roxa" width="25" height="20" style="object-fit: contain; margin-right: 10px;" />
        </template>
      </v-list-item>

      <v-list density="compact" nav class="px-4 py-4">
        <v-list-item prepend-icon="mdi-home" title="Página Inicial" to="/" @click="drawer = false"></v-list-item>
        
        <v-list-subheader>Tabelas de Dados</v-list-subheader>
        <v-list-item prepend-icon="mdi-table-multiple" title="Violência Geral" to="/violencia-geral" @click="drawer = false"></v-list-item>

        <v-list-subheader>Análises</v-list-subheader>
        <v-list-item prepend-icon="mdi-chart-line" title="Incidências por Hora" to="/analise-incidencias-hora" @click="drawer = false"></v-list-item>

      </v-list>
    </v-navigation-drawer>

    <v-app-bar color="primary" elevation="3">
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
    </v-app-bar>

    <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 64px; display: flex; align-items: center; justify-content: center; pointer-events: none; z-index: 2000;">
      <span class="font-weight-bold text-black" style="font-size: 1.25rem;">
        Dados sobre violência contra mulheres no ES
      </span>
    </div>

    <v-main class="bg-white">
      <slot />
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const drawer = ref(true)
</script>

<style>
.v-select .v-field .v-field__input input {
  opacity: 0 !important;
}
</style>
