/**
 * router/index.ts
 *
 * Manual routes for ./src/pages/*.vue
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router'
import PaginaInicial from '@/pages/PaginaInicial.vue'
import TabelaFeminicidio from '@/pages/TabelaFeminicidio.vue'
import TabelaViolenciaGeral from '@/pages/TabelaViolenciaGeral.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: PaginaInicial,
    },
    {
      path: '/feminicidio',
      name: 'Feminicidio',
      component: TabelaFeminicidio,
    },
    {
      path: '/violencia-geral',
      name: 'ViolenciaGeral',
      component: TabelaViolenciaGeral,
    },
  ],
})

export default router
