# Pipeline de Preços de Combustíveis (ANP)

> **Status:** em desenvolvimento

Pipeline de dados que coleta os preços de combustíveis publicados semanalmente pela ANP
e os organiza em uma arquitetura medallion (bronze, silver e gold) para análise.

**Pergunta de negócio:** como o preço de gasolina e etanol varia por região, estado,
município e bandeira ao longo do tempo, e onde o etanol compensa mais que a gasolina?

## Stack

Python · PostgreSQL · Docker Compose · Apache Airflow · dbt (planejado)

## Como funciona

1. Uma DAG do Airflow roda toda segunda-feira às 6h (horário de Brasília).
2. A primeira tarefa baixa os arquivos mensais da ANP e o arquivo das últimas 4 semanas,
   que é atualizado semanalmente.
3. A segunda tarefa carrega os arquivos na camada **bronze** do Postgres, sem alterar o
   conteúdo, com colunas de controle (arquivo de origem e data de carga).

As camadas **silver** (dados limpos e deduplicados) e **gold** (star schema) serão
construídas com dbt.

## Status

- [x] Ingestão: download dos arquivos da ANP e carga na camada bronze, de forma idempotente
- [x] Infraestrutura: Postgres e Airflow rodando via Docker Compose
- [x] Orquestração: DAG semanal no Airflow com carga incremental
- [ ] Transformação: camadas silver e gold com dbt (star schema)
- [ ] Qualidade de dados e dashboard

## Como rodar

Pré-requisito: Docker.

```bash
git clone https://github.com/GabrielLopes930/anp-combustiveis-pipeline.git
cd anp-combustiveis-pipeline
cp .env.example .env   # preencha com suas credenciais
docker compose up -d --build
```

Depois, acesse o Airflow em http://localhost:8080 com o usuário e a senha definidos em
`AIRFLOW_ADMIN_USER` e `AIRFLOW_ADMIN_PASSWORD`, ative a DAG `anp_precos` e acione uma
execução manual.

## Decisões técnicas

- **Bronze com todas as colunas como texto:** a carga nunca falha por um valor fora do
  padrão vindo da ANP. A conversão de tipos fica para a silver.
- **Idempotência:** rodar o pipeline várias vezes não duplica dados. O download pula
  arquivos já baixados, e a carga apaga e reinsere cada arquivo dentro de uma transação.
- **Sem execuções simultâneas:** a DAG usa `max_active_runs=1`. Duas execuções em paralelo
  chegaram a duplicar dados durante o desenvolvimento, porque a idempotência não protege
  contra concorrência.
- **Arquivo semanal guardado por data:** o arquivo das últimas 4 semanas da ANP sempre tem
  o mesmo link, então cada download é salvo com a data no nome. As semanas se sobrepõem
  entre si e com os arquivos mensais; a deduplicação será feita na silver.
- **LocalExecutor no Airflow:** para um projeto local, ele dispensa Redis e workers Celery,
  reduzindo de 7 para 4 os containers do Airflow.

## Próximos passos

- Camadas silver e gold com dbt
- Carregar na bronze apenas os arquivos ainda não processados
- Usar a data da execução do Airflow no nome do arquivo semanal

## Fonte dos dados

[Série Histórica de Preços de Combustíveis e de GLP — ANP](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis)