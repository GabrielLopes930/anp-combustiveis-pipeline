from datetime import timedelta

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

with DAG(
    dag_id="anp_precos",
    schedule="0 6 * * 1",
    start_date=pendulum.datetime(2026, 10, 1, tz="America/Sao_Paulo"),
    catchup=False,
    max_active_runs=1,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["anp"],
) as dag:
    baixar = BashOperator(
        task_id="baixar_arquivos",
        bash_command="cd /opt/airflow && python ingestion/download.py",
    )

    carregar = BashOperator(
        task_id="carregar_bronze",
        bash_command="cd /opt/airflow && python ingestion/load_bronze.py",
    )

    baixar >> carregar