<template>
  <v-footer class="bg-primary pa-0" style="position: fixed; bottom: 0; left: 0; right: 0; z-index: 2000; border-top: 2px solid rgba(0, 0, 0, 0.1);">
    <div style="display: flex; align-items: center; justify-content: space-between; width: 100%; padding: 12px 32px; flex-wrap: nowrap; overflow-x: auto;">
      
      <!-- Lado Esquerdo -->
      <div style="display: flex; align-items: center; gap: 16px; flex-shrink: 0;">
        <a href="https://www.faesa.br" target="_blank" rel="noopener noreferrer" style="display: flex; align-items: center;">
          <img
            src="/logoFaesa.svg"
            alt="Logo FAESA"
            style="height: 32px; width: auto; opacity: 0.85; transition: opacity 0.3s ease;"
            onmouseover="this.style.opacity='1'"
            onmouseout="this.style.opacity='0.85'"
          />
        </a>
        <span class="text-black" style="opacity: 0.5; font-size: 0.75rem; white-space: nowrap;">
          © {{ new Date().getFullYear() }} — Projeto Integrador FAESA
        </span>
      </div>

      <!-- Lado Direito -->
      <div style="display: flex; align-items: center; gap: 12px; flex-shrink: 0;">
        <span class="font-weight-bold text-black" style="font-size: 0.8rem; white-space: nowrap;">
          Contribuidores do Projeto:
        </span>

        <div v-if="loading" style="display: flex; align-items: center; gap: 4px;">
          <v-progress-circular
            indeterminate
            size="14"
            width="2"
            color="black"
          ></v-progress-circular>
          <span class="text-black" style="opacity: 0.6; font-size: 0.7rem;">Carregando...</span>
        </div>

        <div v-else-if="error" class="text-black" style="opacity: 0.6; font-size: 0.7rem;">
          {{ error }}
        </div>

        <div v-else style="display: flex; align-items: center; gap: 6px;">
          <a
            v-for="contributor in contributors"
            :key="contributor.id"
            :href="contributor.html_url"
            target="_blank"
            rel="noopener noreferrer"
            style="text-decoration: none;"
          >
            <v-chip
              variant="outlined"
              color="black"
              size="small"
              class="contributor-chip"
            >
              <template v-slot:prepend>
                <v-avatar start size="20">
                  <v-img :src="contributor.avatar_url" :alt="contributor.login"></v-img>
                </v-avatar>
              </template>
              {{ contributor.login }}
            </v-chip>
          </a>
        </div>
      </div>
      
    </div>
  </v-footer>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'

interface Contributor {
  id: number
  login: string
  avatar_url: string
  html_url: string
  contributions: number
}

const contributors = ref<Contributor[]>([])
const loading = ref(true)
const error = ref('')

const fetchContributors = async () => {
  try {
    const response = await fetch(
      'https://api.github.com/repos/leofevife/Dados-sobre-violencia-contra-mulheres-no-ES/contributors'
    )
    if (!response.ok) throw new Error('Falha ao carregar contribuidores')
    const data: Contributor[] = await response.json()
    contributors.value = data
  } catch (e: any) {
    error.value = 'Não foi possível carregar os contribuidores.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchContributors()
})
</script>

<style scoped>
.contributor-chip {
  transition: all 0.2s ease;
  border-color: rgba(0, 0, 0, 0.3) !important;
}

.contributor-chip:hover {
  background: rgba(0, 0, 0, 0.08) !important;
  border-color: rgba(0, 0, 0, 0.6) !important;
  transform: translateY(-1px);
}
</style>
