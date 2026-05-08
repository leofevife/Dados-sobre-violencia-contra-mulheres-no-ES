<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app color="surface">
      <v-list-item
        class="bg-primary text-black px-6"
        height="64"
      >
        <template v-slot:title>
          <span class="font-weight-bold">Painel de Dados</span>
        </template>
        <template v-slot:subtitle>
          <span class="text-black font-weight-medium" style="opacity: 0.8">Menu de Navegação</span>
        </template>
      </v-list-item>

      <v-divider></v-divider>

      <v-list density="compact" nav class="px-4 py-4">
        <v-list-item prepend-icon="mdi-home" title="Página Inicial" to="/" @click="drawer = false"></v-list-item>
        
        <v-list-subheader>Tabelas de Dados</v-list-subheader>
        <v-list-item prepend-icon="mdi-table" title="Feminicídio" to="/feminicidio" @click="drawer = false"></v-list-item>
        <v-list-item prepend-icon="mdi-table-multiple" title="Violência Geral" to="/violencia-geral" @click="drawer = false"></v-list-item>

        <v-list-subheader class="mt-4">Análises</v-list-subheader>
        <v-list-item prepend-icon="mdi-chart-line" title="Violência por Hora" to="/analise/violencia-por-hora" @click="drawer = false"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar color="primary" elevation="3">
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-app-bar-title class="font-weight-bold text-black">
        Dados sobre violência contra mulheres no ES
      </v-app-bar-title>
    </v-app-bar>

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
