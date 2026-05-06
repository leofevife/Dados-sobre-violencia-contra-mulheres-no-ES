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

    <v-row justify="center" v-if="!loading && tables.length === 0">
      <v-col cols="12" lg="10" xl="8">
        <v-alert type="warning" border="start" variant="tonal" class="mb-4">
          Nenhuma tabela encontrada no banco.
        </v-alert>
      </v-col>
    </v-row>

    <v-row justify="center" v-for="tableName in visibleTables" :key="tableName" class="mb-10">
      <v-col cols="12" lg="10" xl="8">
        <v-card elevation="6" rounded="xl" class="overflow-hidden">
          <v-card-title class="d-flex justify-space-between align-center bg-primary px-6 py-4">
            <span class="text-h5 font-weight-medium">{{ tableName }}</span>
            <!-- <v-chip color="primary" variant="elevated" size="small" class="font-weight-bold">
              Linhas: {{ tableData[tableName]?.length ?? 0 }}
            </v-chip> -->
          </v-card-title>

          <v-card-text v-if="tableData[tableName]?.length === 0" class="text-center py-10 text-medium-emphasis">
            A tabela não possui registros visíveis ou não foi possível carregar dados.
          </v-card-text>

          <v-data-table v-else :headers="getHeaders(tableName)" :items="filteredData[tableName]" :items-per-page="10"
            :items-per-page-options="[10, 25, 50, 100, 500]" hover class="text-center">
            <template v-for="header in getHeaders(tableName)" :key="`header-${header.value}`"
              v-slot:[`header.${header.value}`]="{ column }">
              <div class="d-flex align-center justify-center py-3 text-no-wrap" style="min-width: max-content;">
                <span class="font-weight-bold text-uppercase text-caption">{{ column.title }}</span>
                <v-menu :close-on-content-click="false" location="bottom">
                  <template v-slot:activator="{ props }">
                    <v-icon
                      v-bind="props"
                      size="small"
                      class="ml-1 cursor-pointer"
                      :color="getFilters(tableName)[column.value] ? 'primary' : undefined"
                    >
                      mdi-filter-variant
                    </v-icon>
                  </template>
                  <v-card min-width="200" class="pa-2">
                    <v-text-field
                      v-model="getFilters(tableName)[column.value]"
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

            <template v-for="header in getHeaders(tableName)" :key="`item-${header.value}`"
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

const knownTables = ['FEMINICIDIO', 'VIOLENCIA_GERAL']
const tableData = ref<Record<string, TableRow[]>>({})
const filters = ref<Record<string, Record<string, string>>>({})
const loading = ref(false)
const error = ref('')
const tables = computed(() => knownTables)
const apiBase = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

const fetchJson = async <T>(path: string): Promise<T> => {
  const response = await fetch(`${apiBase}${path}`)
  if (!response.ok) {
    const text = await response.text()
    throw new Error(text || 'Falha ao buscar dados')
  }
  return response.json()
}

const loadTables = async () => {
  loading.value = true
  error.value = ''

  try {
    await Promise.all(
      knownTables.map(async (tableName) => {
        const tableResult = await fetchJson<{ success: boolean; rows: TableRow[] }>(`/cloudflare/table/${encodeURIComponent(tableName)}`)
        tableData.value[tableName] = tableResult.rows ?? []
      })
    )
  } catch (err: unknown) {
    error.value = err instanceof Error ? err.message : 'Erro desconhecido ao carregar tabelas.'
  } finally {
    loading.value = false
  }
}

const visibleTables = computed(() => knownTables)

const getHeaders = (tableName: string) => {
  const rows = tableData.value[tableName] ?? []
  if (rows.length === 0) return []
  return Object.keys(rows[0]).map(key => ({
    title: key,
    align: 'center',
    key: key,
    value: key
  }))
}

const getFilters = (tableName: string) => {
  if (!filters.value[tableName]) {
    filters.value[tableName] = {}
  }
  return filters.value[tableName]
}

const filteredData = computed(() => {
  const result: Record<string, TableRow[]> = {}
  for (const tableName of knownTables) {
    const data = tableData.value[tableName] ?? []
    const tableFilters = filters.value[tableName] ?? {}
    result[tableName] = data.filter(row => {
      return Object.entries(tableFilters).every(([key, filterValue]) => {
        if (!filterValue) return true
        const rowValue = String(row[key] ?? '').toLowerCase()
        return rowValue.includes(filterValue.toLowerCase())
      })
    })
  }
  return result
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

onMounted(loadTables)
</script>
