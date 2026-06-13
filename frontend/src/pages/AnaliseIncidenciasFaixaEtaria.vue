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

          <v-divider></v-divider>

          <v-card-title class="d-flex justify-space-between align-center bg-primary px-6 py-4">
            <span class="text-h5 font-weight-medium">Faixa Etária por Cor de Pele</span>
          </v-card-title>

          <v-card-text class="d-flex justify-center pa-6">
            <v-progress-circular v-if="loadingStacked" indeterminate color="primary"></v-progress-circular>
            <img
              v-else-if="stackedChartUrl"
              :src="stackedChartUrl"
              alt="Gráfico de barras por faixa etária e cor de pele"
              style="max-width: 100%; height: auto; border-radius: 8px;"
            />
            <v-alert v-else-if="errorStacked" type="error" border="start" variant="tonal">
              {{ errorStacked }}
            </v-alert>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-text class="px-6 pb-6 pt-10">
            <h3 style="font-size: 2rem; font-weight: 800; margin-top: 32px; margin-bottom: 24px; text-align: center;">Análise e Problematização — Recorte Racial</h3>
            <p class="text-body-1 mb-4 text-justify">
              Antes de analisar os números, é fundamental compreender uma questão metodológica que impacta diretamente a leitura destes dados. Nos registros da SESP/ES, a classificação de cor de pele utiliza as categorias <strong>PARDA</strong> e <strong>NEGRA</strong> de forma separada. No entanto, o termo "NEGRA" nos dados da SESP corresponde ao que o IBGE classifica como <strong>"preta"</strong> — isto é, pessoas negras retintas, de pele mais escura e fenótipo de ascendência africana mais marcada. Já o <strong>Estatuto da Igualdade Racial (Lei nº 12.288/2010)</strong> e o próprio IBGE definem que a <strong>população negra</strong> é composta pela soma de pessoas que se autodeclaram <strong>pretas e pardas</strong>. Essa distinção é crucial: ao analisar os gráficos acima, "PARDA" e "NEGRA" devem ser lidas como subdivisões da população negra, e não como categorias raciais opostas.
            </p>
            <p class="text-body-1 mb-4 text-justify">
              Quando aplicamos esse critério unificado aos dados, o cenário se transforma drasticamente. Na faixa <strong>adulta</strong> — que o gráfico de pizza mostra concentrar 84% de todas as ocorrências com 120.345 registros —, a soma de pardas (55.459) e negras/pretas (16.689) alcança <strong>72.148 ocorrências</strong>, representando aproximadamente <strong>60% de todos os casos nessa faixa etária</strong>. Esse número supera em quase o dobro as 37.386 ocorrências de mulheres brancas. A mesma proporção se repete entre <strong>adolescentes</strong> (pardas 3.042 + negras 749 = 3.791, contra 1.685 brancas) e entre <strong>crianças</strong> (pardas 1.789 + negras 337 = 2.126, contra 960 brancas). Isso significa que, em todas as faixas etárias, <strong>mulheres negras são vítimas em proporção significativamente maior</strong>.
            </p>
            <p class="text-body-1 mb-4 text-justify">
              Esse padrão não é acidental. Segundo o Censo 2022 do IBGE, pardos (45,3%) e pretos (10,2%) juntos compõem <strong>55,5% da população brasileira</strong>. Porém, nos dados de violência do ES, a população negra (parda + preta) responde por cerca de 60% das ocorrências — uma <strong>sobre-representação</strong> que evidencia o impacto do racismo estrutural. Mulheres negras estão, historicamente, em situações de maior vulnerabilidade socioeconômica, com menor acesso a redes de apoio, moradia segura, emprego formal e assistência jurídica — fatores que as expõem desproporcionalmente a contextos de violência e dificultam a ruptura do ciclo.
            </p>
            <p class="text-body-1 mb-4 text-justify">
              Há ainda a questão do <strong>colorismo</strong>: dentro da própria população negra, mulheres pretas retintas (classificadas como "NEGRA" nos dados da SESP) enfrentam formas mais severas de discriminação do que mulheres pardas de pele mais clara. Embora ambas pertençam à população negra, as experiências de violência podem variar em intensidade e tipo conforme o tom de pele e os traços fenotípicos — um fenômeno que os dados da SESP permitem, ao menos parcialmente, capturar ao manter as categorias separadas.
            </p>
            <p class="text-body-1 mb-4 text-justify">
              Na população <strong>idosa</strong>, chama a atenção que mulheres <strong>brancas</strong> (3.707) superam as pardas (2.879), sendo a única faixa etária em que isso ocorre. Contudo, ao somar pardas e negras/pretas (2.879 + 972 = 3.851), a população negra idosa volta a superar a branca. Uma hipótese para a maior presença de brancas nessa faixa é a maior expectativa de vida associada a melhores condições socioeconômicas, resultando em maior longevidade e, consequentemente, em maior exposição a situações de violência na terceira idade.
            </p>
            <p class="text-body-1 mb-4 text-justify">
              Por fim, a categoria <strong>S/I</strong> (sem informação) apresenta números expressivos em todas as faixas — 6.148 entre adultas e 700 entre adolescentes. A ausência do registro de cor de pele compromete a precisão da análise racial. Quando combinada com os 3.492 registros de faixa etária "ignorado" evidenciados no gráfico de pizza, essa lacuna reforça a necessidade urgente de padronizar e exigir o preenchimento completo nos boletins de ocorrência, garantindo que as políticas públicas de enfrentamento à violência contra a mulher possam ser direcionadas com precisão às populações mais vulnerabilizadas.
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
const apiBase = import.meta.env.VITE_API_BASE_URL ?? ''
const chartUrl = ref('')

const loadingStacked = ref(false)
const errorStacked = ref('')
const stackedChartUrl = ref('')

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

const loadStackedChart = async () => {
  loadingStacked.value = true
  errorStacked.value = ''

  try {
    const response = await fetch(`${apiBase}/analise/faixa-etaria-cor-pele`)
    if (!response.ok) {
      throw new Error('Falha ao carregar gráfico de barras empilhadas')
    }
    const blob = await response.blob()
    stackedChartUrl.value = URL.createObjectURL(blob)
  } catch (err: unknown) {
    errorStacked.value = err instanceof Error ? err.message : 'Erro desconhecido ao carregar gráfico.'
  } finally {
    loadingStacked.value = false
  }
}

onMounted(async () => {
  await loadChart()
  await loadStackedChart()
})
</script>

