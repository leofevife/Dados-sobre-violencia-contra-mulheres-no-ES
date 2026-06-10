<template>
  <v-container fluid class="px-md-10 py-8 mt-16">
    <v-row justify="center" v-if="error">
      <v-col cols="12" lg="10" xl="8">
        <v-alert type="error" border="start" variant="tonal" class="mb-4">
          {{ error }}
        </v-alert>
      </v-col>
    </v-row>

    <v-row justify="center" v-if="loading">
      <v-col cols="12" lg="10" xl="8">
        <v-progress-linear indeterminate color="primary" rounded class="mb-4"></v-progress-linear>
      </v-col>
    </v-row>

    <v-row justify="center" v-if="!loading && !error">
      <v-col cols="12" lg="10" xl="8">
        <v-card elevation="6" rounded="xl" class="overflow-hidden">
          <v-card-title class="d-flex justify-space-between align-center bg-primary px-6 py-4">
            <span class="text-h5 font-weight-medium">Incidências por Faixa Etária</span>
          </v-card-title>

          <v-card-text class="d-flex justify-center pa-6">
            <img
              :src="chartUrl"
              alt="Gráfico de incidências por faixa etária"
              style="max-width: 100%; height: auto; border-radius: 8px;"
            />
          </v-card-text>

          <v-divider></v-divider>

          <v-card-text class="px-6 pb-6 pt-10">
            <h3 style="font-size: 2rem; font-weight: 800; margin-top: 32px; margin-bottom: 24px; text-align: center;">Análise e Problematização dos Dados</h3>
            <p class="text-body-1 mb-4 text-justify">
              O gráfico acima revela que a faixa etária <strong>adulta</strong> concentra a esmagadora maioria das incidências de violência contra a mulher, representando mais de 84% do total de registros com 120.345 ocorrências. Esse dado reflete a realidade de que mulheres em idade produtiva e em relações afetivas são as principais vítimas, frequentemente expostas à violência doméstica e íntima durante os anos de maior convivência com parceiros.
            </p>
            <p class="text-body-1 mb-4 text-justify">
              A população <strong>idosa</strong> aparece como o segundo grupo mais afetado, com 8.364 registros. A violência contra mulheres idosas frequentemente envolve negligência, abuso patrimonial e agressões praticadas por familiares ou cuidadores, cenário agravado pela dependência física e emocional que muitas dessas mulheres vivenciam.
            </p>
            <p class="text-body-1 mb-4 text-justify">
              As faixas <strong>adolescente</strong> (6.581) e <strong>criança</strong> (3.916) somadas representam mais de 10.000 vítimas menores de idade, um dado alarmante que evidencia a vulnerabilidade de meninas e jovens dentro de seus próprios ambientes familiares. Casos envolvendo crianças e adolescentes frequentemente incluem abuso sexual, violência física e psicológica, e demandam atenção especial das redes de proteção.
            </p>
            <p class="text-body-1 mb-4 text-justify">
              Por fim, os 3.492 registros classificados como <strong>ignorado</strong> apontam para uma fragilidade no processo de coleta de dados. A ausência dessa informação pode dificultar a elaboração de políticas públicas direcionadas e reforça a necessidade de aprimoramento nos protocolos de registro das ocorrências.
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'

const loading = ref(false)
const error = ref('')
const apiBase = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
const chartUrl = ref('')

const loadChart = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch(`${apiBase}/analise/faixa-etaria`)
    if (!response.ok) {
      throw new Error('Falha ao carregar gráfico')
    }
    const blob = await response.blob()
    chartUrl.value = URL.createObjectURL(blob)
  } catch (err: unknown) {
    error.value = err instanceof Error ? err.message : 'Erro desconhecido ao carregar gráfico.'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadChart()
})
</script>
