import { createRouter, createWebHistory } from 'vue-router'
import PaginaInicial from '@/pages/PaginaInicial.vue'
import TabelaViolenciaGeral from '@/pages/TabelaViolenciaGeral.vue'
import AnaliseIncidenciasHora from '@/pages/AnaliseIncidenciasHora.vue'
import AnaliseIncidenciasFaixaEtaria from '@/pages/AnaliseIncidenciasFaixaEtaria.vue'
import AnaliseIncidenciasAno from '@/pages/AnaliseIncidenciasAno.vue'

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
    {
      path: '/analise-faixa-etaria',
      name: 'AnaliseIncidenciasFaixaEtaria',
      component: AnaliseIncidenciasFaixaEtaria,
    },
    {
      path: '/analise-ano',
      name: 'AnaliseIncidenciasAno',
      component: AnaliseIncidenciasAno,
    },
  ],
})

export default router

