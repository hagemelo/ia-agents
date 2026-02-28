# Perf Lens

Serviço de **análise de desempenho** que compara o resultado de uma bateria de testes com um histórico de execuções e identifica se o desempenho atual está melhor ou pior que a baseline, usando agentes de IA orquestrados.

## O que faz

- Lê uma **bateria de teste** atual (`bateria-teste-1.csv`) e o **histórico** de baterias (`history.csv`).
- Usa um **orquestrador** que coordena três agentes:
  - **Suite Analyst** – analisa a bateria atual e extrai o melhor resultado (vazão, latência, taxa de erro).
  - **Baseline Analyst** – escolhe a melhor execução no histórico como baseline.
  - **Suite Evaluator** – compara o resultado da bateria atual com a baseline e devolve a avaliação.
- Expõe um endpoint REST para disparar a análise.

Critérios de “melhor” desempenho: **latência ≤ 400 ms**, **taxa de erro ≤ 0,3%** e **maior vazão possível**.

## Estrutura

```
perf-lens/
├── src/
│   ├── main.py                 # FastAPI app
│   ├── orchestrator.py         # Orquestrador dos agentes
│   ├── baseline_analyst.py     # Agente que define a baseline
│   ├── suite_analyst.py        # Agente que analisa a bateria atual
│   ├── suite_evaluator.py      # Agente que compara com a baseline
│   ├── perf_lens_controller.py # Endpoint /perf-lens/analyze-performance
│   ├── perf_lens_service.py    # Serviço que chama o orquestrador
│   ├── health_controller.py    # Health check
│   ├── assessment.py           # Modelo de saída (Assessment)
│   └── perf_data.py            # Modelo de dados (PerfData)
├── recursos/
│   ├── bateria-teste-1.csv     # Bateria a ser analisada
│   └── history.csv            # Histórico de baterias (baseline)
├── tests/
│   ├── baseline_analyst_test.py
│   └── suite_analyst_test.py
└── .env                        # Chaves de API (não versionar)
```

## Pré-requisitos

- Python 3.x
- Variáveis de ambiente no `.env`:
  - `OPENAI_API_KEY` – usado pelo orquestrador e pelo Baseline Analyst
  - `GOOGLE_API_KEY` – usado pelo Suite Analyst (Gemini)

## Execução

### API (FastAPI)

Na raiz do projeto `perf-lens`:

```bash
cd perf-lens
# Ajuste o PYTHONPATH para incluir src (ou instale o pacote no modo editável)
uvicorn src.main:app --reload
```

Endpoint de análise:

```http
POST /perf-lens/analyze-performance
```

Resposta: JSON no formato `Assessment` (avaliação, baseline e resultado da suite).

Health check:

```http
GET /health/live
```

### Testes

A partir da pasta `perf-lens` (raiz do projeto), com `src` e `tests` no path:

```bash
cd perf-lens
python -m pytest tests/ -v
```

Ou com `unittest`:

```bash
cd perf-lens
python -m unittest discover -s tests -p "*_test.py" -v
```

Para um arquivo específico (executando de dentro de `tests/` e com a raiz no path):

```bash
cd perf-lens/tests
python -m unittest baseline_analyst_test -v
python -m unittest suite_analyst_test -v
```

## Dados de entrada (CSV)

Os arquivos em `recursos/` devem ter colunas como: **data da execução**, **vazão**, **latência**, **taxa de erro**. O orquestrador lê esses CSVs e repassa o conteúdo em texto para os agentes.
