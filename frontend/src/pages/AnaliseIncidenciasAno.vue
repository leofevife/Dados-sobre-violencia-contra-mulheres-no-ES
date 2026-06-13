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
            <span class="text-h5 font-weight-medium">Incidências por Ano</span>
          </v-card-title>

          <v-card-text class="d-flex justify-center pa-6">
            <img
              :src="chartUrl"
              alt="Gráfico de incidências por ano"
              style="max-width: 100%; height: auto; border-radius: 8px;"
            />
          </v-card-text>

          <v-divider></v-divider>

          <v-card-text class="px-6 pb-6 pt-10">
            <h3 style="font-size: 2rem; font-weight: 800; margin-top: 32px; margin-bottom: 24px; text-align: center;">Análise e Problematização dos Dados</h3>
            <p class="text-body-1 mb-4 text-justify">
              O gráfico de linha acima apresenta a evolução temporal das ocorrências de violência contra a mulher no Espírito Santo de 2022 a 2025. Nota-se um crescimento contínuo de registros no primeiro triênio analisado: partindo de 22.156 ocorrências em 2022, subindo para 23.831 em 2023, e atingindo seu ápice histórico em 2024, com 25.534 registros. Esse aumento expressivo de aproximadamente 15% em dois anos sinaliza um cenário preocupante de exposição ao risco, mas também aponta para o fortalecimento da rede de apoio e para a maior conscientização das vítimas, que passaram a denunciar e registrar as agressões com maior frequência em canais públicos e digitais.
            </p>
            <p class="text-body-1 mb-4 text-justify">
              Já em 2025, os registros apresentam uma queda acentuada, retornando ao patamar de 22.142 ocorrências. Embora essa redução possa sugerir um efeito positivo das campanhas preventivas, do endurecimento das penas e da aplicação mais ágil de medidas protetivas de urgência, ela deve ser interpretada com cautela. Flutuações acentuadas em dados criminais muitas vezes escondem barreiras de notificação ou instabilidades nos fluxos de tabulação de dados entre órgãos públicos. Portanto, a diminuição de registros em 2025 reforça a necessidade de contínua vigilância, aprimoramento dos canais de escuta e fortalecimento do policiamento preventivo para garantir que a redução seja um reflexo de uma queda real da violência e não de uma elevação da subnotificação.
            </p>
          </v-card-text>
          
          <v-divider></v-divider>

          <v-card-text class="px-6 pb-6 pt-10">
            <div class="mx-auto" style="max-width: 320px; width: 100%;">
              <span class="text-subtitle-2 mb-2 d-block font-weight-medium text-grey-darken-2 text-center">Selecione o Ano</span>
              <v-select
                v-model="selectedAno"
                :items="anosDisponiveis"
                variant="outlined"
                density="compact"
                hide-details
                bg-color="surface"
                class="elevation-2 rounded-lg"
                style="width: 100%;"
                @update:model-value="loadMesChart"
              ></v-select>
            </div>
            
            <div v-if="loadingMes" class="d-flex justify-center my-4">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
            </div>
            <div v-else-if="errorMes">
              <v-alert type="error" border="start" variant="tonal" class="mb-4 mt-4">
                {{ errorMes }}
              </v-alert>
            </div>
            <div v-else-if="mesChartUrl" class="d-flex flex-column align-center mt-4">
              <img
                :src="mesChartUrl"
                alt="Gráfico de incidências por mês"
                style="max-width: 100%; height: auto; border-radius: 8px;"
              />
            </div>
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
const apiBase = import.meta.env.VITE_API_BASE_URL ?? ''
const chartUrl = ref('')

const anosDisponiveis = ref<number[]>([])
const selectedAno = ref<number | null>(null)
const loadingMes = ref(false)
const errorMes = ref('')
const mesChartUrl = ref('')

const loadChart = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch(`${apiBase}/analise/incidencias-ano`)
    if (!response.ok) {
      throw new Error('Falha ao carregar gráfico por ano')
    }
    const blob = await response.blob()
    chartUrl.value = URL.createObjectURL(blob)
  } catch (err: unknown) {
    error.value = err instanceof Error ? err.message : 'Erro desconhecido ao carregar gráfico.'
  } finally {
    loading.value = false
  }
}

const loadAnosDisponiveis = async () => {
  try {
    const response = await fetch(`${apiBase}/analise/anos-disponiveis`)
    if (!response.ok) throw new Error('Falha ao carregar anos disponíveis')
    const data = await response.json()
    if (data.success && data.anos) {
      anosDisponiveis.value = data.anos
      if (anosDisponiveis.value.length > 0) {
        selectedAno.value = anosDisponiveis.value[0]
        await loadMesChart(selectedAno.value)
      }
    }
  } catch (err: unknown) {
    console.error(err)
  }
}

const loadMesChart = async (ano: number) => {
  if (!ano) return
  loadingMes.value = true
  errorMes.value = ''
  
  try {
    const response = await fetch(`${apiBase}/analise/incidencias-mes-ano?ano=${ano}`)
    if (!response.ok) throw new Error('Falha ao carregar gráfico do mês')
    const blob = await response.blob()
    mesChartUrl.value = URL.createObjectURL(blob)
  } catch (err: unknown) {
    errorMes.value = err instanceof Error ? err.message : 'Erro desconhecido ao carregar gráfico do mês.'
  } finally {
    loadingMes.value = false
  }
}

onMounted(async () => {
  await loadChart()
  await loadAnosDisponiveis()
})
</script>
