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
              alt="Gráfico de barras dos 10 locais com mais incidências"
              style="max-width: 100%; height: auto; border-radius: 8px;"
            />
            <v-alert v-else-if="errorTreemap" type="error" border="start" variant="tonal">
              {{ errorTreemap }}
            </v-alert>
          </v-card-text>



          <v-divider></v-divider>

          <v-card-text class="px-6 pb-6 pt-10">
            <h3 style="font-size: 2rem; font-weight: 800; margin-bottom: 24px; text-align: center;">Incidências por Hora por Local</h3>
            <v-select
              v-model="selectedLocal"
              :items="locais"
              item-title="local"
              item-value="local"
              label="Selecione o Local"
              variant="outlined"
              @update:model-value="loadLocalChart"
            ></v-select>
            
            <div v-if="loadingLocal" class="d-flex justify-center my-4">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
            </div>
            <div v-else-if="errorLocal">
              <v-alert type="error" border="start" variant="tonal" class="mb-4">
                {{ errorLocal }}
              </v-alert>
            </div>
            <div v-else-if="localChartUrl" class="d-flex flex-column align-center mt-4">
              <img
                :src="localChartUrl"
                alt="Gráfico de incidências por hora no local"
                style="max-width: 100%; height: auto; border-radius: 8px;"
              />
              <p class="text-caption mt-2 text-grey-darken-1 font-weight-bold">
                * {{ selectedLocalData?.ni_count || 0 }} incidência(s) sem horário informado (N/I) neste local.
              </p>
            </div>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-text class="px-6 pb-6 pt-10">
            <h3 style="font-size: 2rem; font-weight: 800; margin-top: 32px; margin-bottom: 24px; text-align: center;">Análise e Problematização dos Dados</h3>
            <p class="text-body-1 mb-4 text-justify">
              O gráfico de barras acima evidencia que a <strong>residência</strong> é, disparadamente, o local com maior número de incidências de violência contra a mulher, concentrando 3.080 registros — mais que o triplo do segundo colocado. Esse dado reforça que a violência contra a mulher é predominantemente <strong>doméstica e íntima</strong>. Ao cruzar essa informação com o gráfico de incidências por hora no local "RESIDÊNCIA", percebemos que os maiores picos ocorrem no período da noite (especialmente entre 19h e 22h) e à meia-noite (0h). Esse padrão horário tem explicação: o período noturno e o início da madrugada geralmente coincidem com o retorno do agressor e da vítima para casa após o expediente. É o momento em que ambos estão no mesmo ambiente privado, isolados da vista pública, o que facilita o ciclo da agressão e dificulta pedidos de socorro. Além disso, fatores como o uso abusivo de álcool (mais comum à noite) e a convivência forçada prolongada no final do dia funcionam como gatilhos para que a violência escale dentro de casa.
            </p>
            <p class="text-body-1 mb-4 text-justify">
              A <strong>via pública</strong> aparece como o segundo local mais recorrente, com 946 ocorrências, indicando que a violência não se limita ao espaço doméstico. Casos de assédio, perseguição (<em>stalking</em>) e agressões físicas em ruas e praças revelam a dimensão estrutural do problema, evidenciando que a insegurança feminina permeia profundamente os espaços abertos e de circulação.
            </p>
            <p class="text-body-1 mb-4 text-justify">
              Outro ponto crítico é o <strong>ambiente web</strong>, com 208 incidências registradas. É vital ressaltar que a <strong>subnotificação de crimes virtuais é massiva</strong>. Muitas vítimas de pornografia não consensual, <em>cyberstalking</em> e assédio online não denunciam por desconhecerem que as práticas configuram crime, por dificuldades técnicas em reunir provas digitais ou pelo medo do julgamento social. Portanto, os dados de ambiente web representam apenas uma pequena fração do real volume de violências no meio digital.
            </p>
            <p class="text-body-1 mb-4 text-justify">
              A presença de locais como <strong>comércio</strong> (184 ocorrências), <strong>hospital</strong> (65) e <strong>escola</strong> (31) no ranking demonstra que a violência atravessa as mais diversas esferas do convívio social. A identificação de casos em hospitais e escolas evidencia a importância desses equipamentos públicos atuarem não apenas no atendimento direto, mas também como portas de entrada cruciais para acolher e encaminhar vítimas que sofrem violência em outros ambientes. A diversidade de cenários reforça a urgência de uma rede de apoio transversal.
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { onMounted, ref, computed } from 'vue'

const loading = ref(false)
const error = ref('')
const apiBase = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
const chartUrl = ref('')

const loadingTreemap = ref(false)
const errorTreemap = ref('')
const treemapUrl = ref('')

interface LocalData {
  local: string
  ni_count: number
}

const locais = ref<LocalData[]>([])
const selectedLocal = ref<string | null>(null)
const selectedLocalData = computed(() => locais.value.find(l => l.local === selectedLocal.value))
const loadingLocal = ref(false)
const errorLocal = ref('')
const localChartUrl = ref('')

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

const loadLocais = async () => {
  try {
    const response = await fetch(`${apiBase}/analise/locais-disponiveis`)
    if (!response.ok) throw new Error('Falha ao carregar locais')
    const data = await response.json()
    if (data.success) {
      locais.value = data.locais
      if (locais.value.length > 0) {
        selectedLocal.value = locais.value[0].local
        await loadLocalChart(selectedLocal.value)
      }
    }
  } catch (err: unknown) {
    console.error(err)
  }
}

const loadLocalChart = async (local: string) => {
  if (!local) return
  loadingLocal.value = true
  errorLocal.value = ''
  
  try {
    const response = await fetch(`${apiBase}/analise/incidencias-hora-local?local=${encodeURIComponent(local)}`)
    if (!response.ok) throw new Error('Falha ao carregar gráfico do local')
    const blob = await response.blob()
    localChartUrl.value = URL.createObjectURL(blob)
  } catch (err: unknown) {
    errorLocal.value = err instanceof Error ? err.message : 'Erro desconhecido ao carregar gráfico do local.'
  } finally {
    loadingLocal.value = false
  }
}

onMounted(async () => {
  await loadChart()
  await loadTreemap()
  await loadLocais()
})
</script>
