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

    <v-row justify="center" v-if="!loading && tableData.length === 0">
      <v-col cols="12" lg="10" xl="8">
        <v-alert type="warning" border="start" variant="tonal" class="mb-4">
          Nenhuma tabela encontrada no banco.
        </v-alert>
      </v-col>
    </v-row>

    <v-row justify="center" v-if="!loading && tableData.length > 0" class="mb-10">
      <v-col cols="12" lg="10" xl="8">
        <v-card elevation="6" rounded="xl" class="overflow-hidden">
          <v-card-title class="d-flex justify-space-between align-center bg-primary px-6 py-4">
            <span class="text-h5 font-weight-medium">VIOLÊNCIA GERAL</span>
          </v-card-title>

          <v-data-table :headers="headers" :items="filteredData" :items-per-page="10"
            :items-per-page-options="[10, 25, 50, 100, 500]" hover class="text-center">
            <template v-for="header in headers" :key="`header-${header.value}`"
              v-slot:[`header.${header.value}`]="{ column }">
              <div class="d-flex align-center justify-center py-3 text-no-wrap" style="min-width: max-content;">
                <span class="font-weight-bold text-uppercase text-caption">{{ column.title }}</span>
                <v-menu :close-on-content-click="false" location="bottom">
                  <template v-slot:activator="{ props }">
                    <v-icon
                      v-bind="props"
                      size="small"
                      class="ml-1 cursor-pointer"
                      :color="filters[column.value] ? 'primary' : undefined"
                    >
                      mdi-filter-variant
                    </v-icon>
                  </template>
                  <v-card min-width="200" class="pa-2">
                    <v-text-field
                      v-model="filters[column.value]"
                      density="compact"
                      variant="outlined"
                      hide-details
                      placeholder="Filtrar..."
                      prepend-inner-icon="mdi-magnify"
                      clearable
                      autofocus
                    ></v-text-field>
                  </v-card>
                </v-menu>
              </div>
            </template>

            <template v-for="header in headers" :key="`item-${header.value}`"
              v-slot:[`item.${header.value}`]="{ item }">
              <div class="text-center">
                {{ formatValue(item[header.value]) }}
              </div>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue'

type TableRow = Record<string, unknown>

const tableName = 'VIOLENCIA_GERAL'
const tableData = ref<TableRow[]>([])
const filters = ref<Record<string, string>>({})
const loading = ref(false)
const error = ref('')
const apiBase = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

const fetchJson = async <T>(path: string): Promise<T> => {
  const response = await fetch(`${apiBase}${path}`)
  if (!response.ok) {
    const text = await response.text()
    throw new Error(text || 'Falha ao buscar dados')
  }
  return response.json()
}

const loadTable = async () => {
  loading.value = true
  error.value = ''

  try {
    const tableResult = await fetchJson<{ success: boolean; rows: TableRow[] }>(`/cloudflare/table/${encodeURIComponent(tableName)}`)
    tableData.value = tableResult.rows ?? []
  } catch (err: unknown) {
    error.value = err instanceof Error ? err.message : 'Erro desconhecido ao carregar tabela.'
  } finally {
    loading.value = false
  }
}

const headers = computed(() => {
  if (tableData.value.length === 0) return []
  return Object.keys(tableData.value[0]).map(key => ({
    title: key,
    align: 'center',
    key: key,
    value: key
  }))
})

const filteredData = computed(() => {
  return tableData.value.filter(row => {
    return Object.entries(filters.value).every(([key, filterValue]) => {
      if (!filterValue) return true
      const rowValue = String(row[key] ?? '').toLowerCase()
      return rowValue.includes(filterValue.toLowerCase())
    })
  })
})

const formatValue = (value: unknown) => {
  if (value === null || value === undefined) {
    return '-'
  }
  if (typeof value === 'object') {
    return JSON.stringify(value)
  }
  return String(value)
}

onMounted(loadTable)
</script>
