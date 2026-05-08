<template>
  <v-container fluid class="px-md-10 py-8 mt-16">
    <v-row justify="center">
      <v-col cols="12" lg="10" xl="8">
        <v-card elevation="6" rounded="xl" class="overflow-hidden">
          <v-card-title class="d-flex justify-space-between align-center bg-primary px-6 py-4">
            <span class="text-h5 font-weight-medium">Análise: Violência por Hora</span>
          </v-card-title>

          <v-card-text class="pa-6">
            <v-row v-if="error">
              <v-col>
                <v-alert type="error" border="start" variant="tonal">
                  {{ error }}
                </v-alert>
              </v-col>
            </v-row>

            <v-row v-if="loading" justify="center" class="my-10">
              <v-col class="text-center">
                <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
                <div class="mt-4 text-medium-emphasis">Carregando dados...</div>
              </v-col>
            </v-row>

            <v-row v-if="!loading && !error && chartData">
              <v-col>
                <div style="height: 400px; position: relative;">
                  <Line :data="chartData" :options="chartOptions" />
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

type RowData = {
  HORA_DIA: string
  TOTAL_OCORRENCIAS: number
}

const loading = ref(false)
const error = ref('')
const tableData = ref<RowData[]>([])

const apiBase = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

const loadData = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await fetch(`${apiBase}/cloudflare/table/VW_VIOLENCIA_POR_HORA`)
    if (!response.ok) {
      throw new Error('Falha ao buscar dados da view VW_VIOLENCIA_POR_HORA')
    }
    const result = await response.json()
    if (result.success && result.rows) {
      // Ordenar por hora, caso o banco não retorne ordenado
      tableData.value = result.rows.sort((a: RowData, b: RowData) => {
        return (a.HORA_DIA || '').localeCompare(b.HORA_DIA || '')
      })
    } else {
      throw new Error('Formato de resposta inválido')
    }
  } catch (err: any) {
    error.value = err.message || 'Erro desconhecido'
  } finally {
    loading.value = false
  }
}

const chartData = computed(() => {
  if (tableData.value.length === 0) return null

  return {
    labels: tableData.value.map(row => row.HORA_DIA),
    datasets: [
      {
        label: 'Total de Ocorrências',
        backgroundColor: '#6200EE',
        borderColor: '#6200EE',
        data: tableData.value.map(row => row.TOTAL_OCORRENCIAS),
        tension: 0.3,
        fill: false
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const,
    },
    title: {
      display: true,
      text: 'Ocorrências Registradas ao Longo do Dia'
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Total de Ocorrências'
      }
    },
    x: {
      title: {
        display: true,
        text: 'Hora do Dia'
      }
    }
  }
}

onMounted(() => {
  loadData()
})
</script>
