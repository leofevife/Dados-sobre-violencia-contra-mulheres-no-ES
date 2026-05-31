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
            <span class="text-h5 font-weight-medium">Incidências por Hora</span>
          </v-card-title>

          <v-card-text class="d-flex justify-center pa-6">
            <img
              :src="chartUrl"
              alt="Gráfico de incidências por hora"
              style="max-width: 100%; height: auto; border-radius: 8px;"
            />
          </v-card-text>

          <v-divider></v-divider>

          <v-card-text class="px-6 pb-6 pt-10">
            <h3 style="font-size: 2rem; font-weight: 800; margin-top: 32px; margin-bottom: 24px; text-align: center;">Análise e Problematização dos Dados</h3>
            <p class="text-body-1 mb-4 text-justify">
              O gráfico acima apresenta a distribuição das incidências de violência contra a mulher ao longo das 24 horas do dia. É possível observar que os registros atingem seus maiores volumes no período noturno, com pico entre 19h e 21h, ultrapassando 280 ocorrências, enquanto as menores quantidades se concentram na madrugada, entre 4h e 5h. Durante o dia, há uma elevação gradual a partir das 8h, com valores expressivos entre 10h e 16h. Compreender em quais horários essas ocorrências se intensificam é um passo importante, mas para uma análise mais completa é fundamental também investigar onde esses crimes acontecem, o que será explorado a seguir.
            </p>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-title class="d-flex justify-space-between align-center bg-primary px-6 py-4">
            <span class="text-h5 font-weight-medium">Top 10 Locais com Mais Incidências</span>
          </v-card-title>

          <v-card-text class="d-flex justify-center pa-6">
            <v-progress-circular v-if="loadingTreemap" indeterminate color="primary"></v-progress-circular>
            <img
              v-else-if="treemapUrl"
              :src="treemapUrl"
              alt="Treemap dos 10 locais com mais incidências"
              style="max-width: 100%; height: auto; border-radius: 8px;"
            />
            <v-alert v-else-if="errorTreemap" type="error" border="start" variant="tonal">
              {{ errorTreemap }}
            </v-alert>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-text class="px-6 pb-6 pt-10">
            <h3 style="font-size: 2rem; font-weight: 800; margin-top: 32px; margin-bottom: 24px; text-align: center;">Análise e Problematização dos Dados</h3>
            <p class="text-body-1 mb-4 text-justify">
              O treemap acima evidencia que a <strong>residência</strong> é, disparadamente, o local com maior número de incidências de violência contra a mulher, concentrando 2.662 registros. Esse dado reforça o que estudos e pesquisas já apontam: a violência contra a mulher é predominantemente <strong>doméstica e íntima</strong>. O lar, que deveria ser um espaço de segurança, torna-se o principal cenário de agressões, frequentemente perpetradas por companheiros, ex-companheiros ou familiares. Fatores como dependência financeira, medo de retaliação, presença de filhos e a naturalização da violência no ambiente privado contribuem para que essas situações se perpetuem dentro de casa.
            </p>
            <p class="text-body-1 mb-4 text-justify">
              A <strong>via pública</strong> aparece como o segundo local mais recorrente, com 2.004 ocorrências, o que indica que a violência contra a mulher não se limita ao espaço doméstico. Assédio, perseguição (<em>stalking</em>) e agressões em espaços abertos revelam a dimensão estrutural do problema, evidenciando que a insegurança feminina permeia tanto o ambiente privado quanto o público.
            </p>
            <p class="text-body-1 mb-4 text-justify">
              Outro ponto que merece atenção crítica é o <strong>ambiente web</strong>, que registra 1.482 incidências. Embora esse número já seja significativo, ele está longe de representar a totalidade dos crimes virtuais contra a mulher. A realidade é que a <strong>subnotificação nesse tipo de crime é altíssima</strong>: muitas vítimas de pornografia não consensual, cyberstalking, ameaças online e assédio virtual sequer registram ocorrência, seja por desconhecimento de que tais atos constituem crime, pela dificuldade de reunir provas digitais, ou pela descrença de que as autoridades serão capazes de investigar e punir os agressores. Portanto, os dados de ambiente web representam apenas a ponta do iceberg de um fenômeno muito mais amplo.
            </p>
            <p class="text-body-1 mb-4 text-justify">
              Locais como <strong>comércio</strong>, <strong>escola</strong> e <strong>hospital</strong> também figuram no ranking, demonstrando que a violência contra a mulher atravessa todos os espaços de convivência social. A presença de hospitais na lista pode indicar, inclusive, casos em que a própria vítima busca atendimento médico e, nesse momento, a violência é identificada ou registrada. A diversidade de locais reforça a necessidade de políticas públicas transversais, que não se restrinjam ao enfrentamento da violência doméstica, mas que contemplem a proteção da mulher em todos os ambientes onde ela circula.
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

const loadingTreemap = ref(false)
const errorTreemap = ref('')
const treemapUrl = ref('')

const loadChart = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch(`${apiBase}/analise/incidencias-hora`)
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

const loadTreemap = async () => {
  loadingTreemap.value = true
  errorTreemap.value = ''

  try {
    const response = await fetch(`${apiBase}/analise/treemap-tipo-local`)
    if (!response.ok) {
      throw new Error('Falha ao carregar treemap')
    }
    const blob = await response.blob()
    treemapUrl.value = URL.createObjectURL(blob)
  } catch (err: unknown) {
    errorTreemap.value = err instanceof Error ? err.message : 'Erro desconhecido ao carregar treemap.'
  } finally {
    loadingTreemap.value = false
  }
}

onMounted(async () => {
  await loadChart()
  await loadTreemap()
})
</script>
