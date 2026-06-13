# Frontend - Observatório de Violência contra Mulheres no ES

Este é o frontend da aplicação web interativa projetada para expor e analisar os dados estatísticos criminais das ocorrências contra a mulher no estado do Espírito Santo, consumidos diretamente do nosso Backend/Supabase.

## Principais Funcionalidades
- **Dashboard Estatístico Completo**: Layout limpo, responsivo e moderno seguindo padrões do Material Design.
- **Gráficos e Visualização de Dados**: Integração com endpoints do FastAPI que geram imagens gráficas (plotadas via seaborn no backend) apresentadas de forma interativa.
- **Previsões de Inteligência Artificial**: Uma tela específica capaz de interagir com o modelo preditivo do backend, oferecendo opções para que o usuário informe anos hipotéticos e visualize a curva estatística gerada pelo modelo de Machine Learning (Regressão Linear com análise de Sazonalidade Mensal).
- **Filtros e Menus**: Seções interativas de consulta por horários, por locais específicos do crime, ou recortes anuais.

## Tecnologias Utilizadas
- **Vue 3**: Framework progressivo adotado para construção da UI.
- **Vuetify 3**: Biblioteca robusta de componentes de UI (Material Design).
- **Vite**: Bundler super veloz para desenvolvimento.
- **TypeScript**: Adição de tipagem forte e maior segurança e escalabilidade.
- **Vue Router**: Sistema de roteamento embutido para navegação fluida em Single Page Application.

## Estrutura Principal
- `src/components/MainLayout.vue`: Estrutura do esqueleto do painel administrativo.
- `src/pages/`: Contém as visões principais (Análise por Hora, por Tipo de Local, por Ano, e módulo de Machine Learning).
- `src/router/`: Configurações das rotas interativas para o painel lateral.

## Instalação e Execução

Utilize o gerenciador de pacotes **yarn** ou **npm** para começar:

```bash
# 1. Instalar dependências
npm install
# ou yarn install

# 2. Subir servidor de desenvolvimento
npm run dev
# ou yarn dev
```

*Nota: Para garantir o total funcionamento das análises locais e predições interativas (Machine Learning), o servidor FastAPI contido na pasta `/backend` também deverá estar rodando na porta `8000` (ou estar configurado na variável `.env` apropriada).*
