import { createRouter, createWebHistory } from 'vue-router'
import PaginaInicial from '@/pages/PaginaInicial.vue'
import TabelaViolenciaGeral from '@/pages/TabelaViolenciaGeral.vue'
import AnaliseIncidenciasHora from '@/pages/AnaliseIncidenciasHora.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: PaginaInicial,
    },
    {
      path: '/violencia-geral',
      name: 'ViolenciaGeral',
      component: TabelaViolenciaGeral,
    },
    {
      path: '/analise-incidencias-hora',
      name: 'AnaliseIncidenciasHora',
      component: AnaliseIncidenciasHora,
    },
  ],
})

export default router
