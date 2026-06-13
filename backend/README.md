# Backend - Observatório de Violência contra Mulheres no ES

Este é o backend da aplicação, responsável por conectar ao banco de dados Supabase, processar as consultas, gerar análises estatísticas e gráficos dinâmicos usando Python.

## Principais Funcionalidades
- **Conexão com Supabase**: Consome views pré-calculadas de dados criminais reais do Espírito Santo.
- **Geração de Gráficos (Data Science)**: Utiliza `pandas`, `matplotlib` e `seaborn` para gerar gráficos diretamente no backend (retornados como `image/png`).
- **Machine Learning**: Conta com um módulo de IA usando `scikit-learn` que aplica Regressão Linear com *One-Hot Encoding* para capturar sazonalidade mensal e prever cenários futuros interativos.

## Tecnologias Utilizadas
- **FastAPI**: Framework web de alta performance.
- **Uvicorn**: Servidor ASGI.
- **Pandas, Matplotlib e Seaborn**: Para tratamento e plotagem de dados.
- **Scikit-Learn**: Para os algoritmos preditivos (Machine Learning).

## Instalação e Execução

1. Crie e ative um ambiente virtual Python.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure as variáveis de ambiente (adicione seu `.env` com a url e key do Supabase).
4. Inicie o servidor:
   ```bash
   python -m uvicorn app.main:app --port 8000
   ```

Opcionalmente, inicie através dos scripts na raiz do projeto (`start.ps1` ou `start.bat`).

## Estrutura de Endpoints
- `/analise/incidencias-hora`: Gráficos de barra por hora do dia.
- `/analise/incidencias-hora-local`: Gráficos de barras por hora filtrados por local.
- `/analise/incidencias-ano`: Gráfico de linha demonstrando a progressão anual.
- `/analise/incidencias-mes-ano`: Gráfico de barra interativo exibindo dados de um ano selecionado.
- `/analise/previsao-dados` e `/analise/previsao-chart`: Geração interativa de previsões de Machine Learning baseadas nos anos.
