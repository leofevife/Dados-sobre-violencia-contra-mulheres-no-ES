<template>
  <v-container fluid class="px-md-10 py-8 mt-16 text-center">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="7">
        <h1 class="text-h3 font-weight-bold text-black mb-6">
          Dados que Incomodam, Ações que Transformam
        </h1>

        <div class="text-left text-body-1 text-high-emphasis space-y-4 mb-8">
          <p class="mb-4">
            O Espírito Santo historicamente enfrenta o grave desafio de figurar entre os estados com elevados índices de violência contra a mulher e feminicídio no Brasil. Das periferias da Grande Vitória às áreas rurais e urbanas do interior, a violência de gênero se manifesta como uma realidade estrutural que impacta a vida de milhares de capixabas todos os dias.
          </p>
          <p class="mb-4">
            Para combater esse problema, o primeiro passo é tirá-lo da invisibilidade por meio de dados transparentes e acessíveis. Este projeto tem como objetivo centralizar, tratar e analisar visualmente as informações registradas sobre as ocorrências de violência contra as mulheres no estado.
          </p>
          <p class="mb-4">
            Os dados analisados nesta plataforma foram obtidos junto à SESP (Secretaria de Estado da Segurança Pública e Defesa Social) e abrangem o período de 2022 a 2025, permitindo traçar um diagnóstico temporal da evolução dessas ocorrências e identificar padrões geográficos e demográficos.
          </p>
          <p class="mb-6">
            Acreditamos que a informação estruturada é um instrumento fundamental para a conscientização social, a cobrança por políticas públicas eficientes e o fortalecimento de redes de apoio. Conhecer a realidade dos números e mapear onde a violência se concentra é um passo essencial para que o Espírito Santo avance na garantia de segurança e dignidade para todas as mulheres.
          </p>
        </div>

        <v-divider class="my-6"></v-divider>

        <p class="text-subtitle-1 font-weight-medium text-medium-emphasis">
          Para começar, selecione uma tabela no menu lateral para visualizar os dados.
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
</script>

<style scoped>
.space-y-4 > p {
  margin-bottom: 1rem;
}
</style>