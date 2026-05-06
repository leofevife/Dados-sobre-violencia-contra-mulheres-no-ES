<template>
  <v-app>
    <v-app-bar color="primary" elevation="3">
      <v-app-bar-title class="text-center font-weight-bold text-black w-100">
        Dados sobre violência contra mulheres no ES
      </v-app-bar-title>
    </v-app-bar>

    <v-main class="bg-white">
      <slot />
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
</script>

<style>
.v-select .v-field .v-field__input input {
  opacity: 0 !important;
}
</style>
