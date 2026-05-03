<template>
  <div class="min-h-screen bg-slate-50 text-slate-900 px-4 py-6">
    <div class="mx-auto max-w-6xl space-y-6">
      <header class="rounded-3xl bg-slate-900 p-6 text-white shadow-lg">
        <h1 class="text-3xl font-semibold">Visualização Cloudflare D1</h1>
        <p class="mt-2 text-slate-300">Mostrando as duas primeiras tabelas disponíveis no banco D1.</p>
      </header>

      <section v-if="error" class="rounded-3xl bg-rose-50 p-6 text-rose-800 shadow-sm">
        <strong>Erro:</strong> {{ error }}
      </section>

      <section v-if="loading" class="rounded-3xl bg-sky-50 p-6 text-sky-800 shadow-sm">
        Carregando tabelas do backend...
      </section>

      <section v-if="!loading && tables.length === 0" class="rounded-3xl bg-amber-50 p-6 text-amber-900 shadow-sm">
        Nenhuma tabela encontrada no banco. Certifique-se de que o backend está rodando e as credenciais estão corretas.
      </section>

      <section v-for="tableName in visibleTables" :key="tableName" class="rounded-3xl bg-white p-6 shadow-sm">
        <div class="mb-4 flex items-center justify-between gap-4">
          <div>
            <h2 class="text-2xl font-semibold text-slate-900">Tabela: {{ tableName }}</h2>
            <p class="mt-1 text-sm text-slate-500">Mostrando até 100 linhas.</p>
          </div>
          <span class="rounded-full bg-slate-100 px-3 py-1 text-sm text-slate-700">Linhas: {{ tableData[tableName]?.length ?? 0 }}</span>
        </div>

        <div v-if="tableData[tableName]?.length === 0" class="rounded-2xl border border-dashed border-slate-300 p-6 text-slate-600">
          A tabela não possui registros visíveis ou não foi possível carregar dados.
        </div>

        <div v-else class="overflow-x-auto">
          <table class="min-w-full border-collapse text-left text-sm">
            <thead>
              <tr class="bg-slate-100 text-slate-700">
                <th v-for="column in columns(tableName)" :key="column" class="px-4 py-3 font-medium uppercase tracking-wide">{{ column }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, rowIndex) in tableData[tableName]" :key="`${tableName}-${rowIndex}`" class="border-b border-slate-200 hover:bg-slate-50">
                <td v-for="column in columns(tableName)" :key="`${tableName}-${rowIndex}-${column}`" class="px-4 py-3 align-top">
                  <pre class="whitespace-pre-wrap text-sm text-slate-800">{{ formatValue(row[column]) }}</pre>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section v-if="tables.length > 2" class="rounded-3xl bg-slate-100 p-6 text-slate-700 shadow-sm">
        Exibindo apenas as duas primeiras tabelas encontradas. Ajuste a seleção no frontend se quiser mostrar tabelas adicionais.
      </section>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue'

type TableRow = Record<string, unknown>

const knownTables = ['FEMINICIDIO', 'VIOLENCIA_GERAL']
const tableData = ref<Record<string, TableRow[]>>({})
const loading = ref(false)
const error = ref('')
const tables = computed(() => knownTables)
const apiBase = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

const fetchJson = async <T >(path: string): Promise<T> => {
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

const columns = (tableName: string): string[] => {
  const rows = tableData.value[tableName] ?? []
  return rows.length > 0 ? Object.keys(rows[0]) : []
}

const formatValue = (value: unknown) => {
  if (value === null || value === undefined) {
    return '-'
  }
  if (typeof value === 'object') {
    return JSON.stringify(value, null, 2)
  }
  return String(value)
}

onMounted(loadTables)
</script>
