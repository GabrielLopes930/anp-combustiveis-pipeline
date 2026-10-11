# Pipeline de Preços de Combustíveis (ANP)

> **Status:** em desenvolvimento

Pipeline de dados que coleta os preços de combustíveis publicados semanalmente pela ANP
e os organiza em uma arquitetura medallion (bronze, silver e gold) para análise.

**Pergunta de negócio:** como o preço de gasolina e etanol varia por região, estado,
município e bandeira ao longo do tempo, e onde o etanol compensa mais que a gasolina?

## Stack

Python · PostgreSQL · Docker Compose · Apache Airflow · dbt (planejado)

## Status

- [x] Ingestão: download dos arquivos da ANP e carga na camada bronze, de forma idempotente
- [x] Infraestrutura: Postgres e Airflow rodando via Docker Compose
- [ ] Orquestração: DAG semanal no Airflow
- [ ] Transformação: camadas silver e gold com dbt (star schema)
- [ ] Qualidade de dados e dashboard

## Como rodar

Pré-requisitos: Docker e Python 3.12.

```bash
git clone https://github.com/GabrielLopes930/anp-combustiveis-pipeline.git
cd anp-combustiveis-pipeline
cp .env.example .env   # preencha com suas credenciais
docker compose up -d --build
```

Para carregar os dados na camada bronze:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ingestion/download.py
python ingestion/load_bronze.py
```

A interface do Airflow fica em http://localhost:8080.

## Fonte dos dados

[Série Histórica de Preços de Combustíveis e de GLP — ANP](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis)