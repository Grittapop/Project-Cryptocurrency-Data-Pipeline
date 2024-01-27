from datetime import timedelta

from airflow import DAG
from airflow.operators.email import EmailOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils import timezone

from etl import (
    _fetch_ohlcv,
    _download_file,
    _load_data_into_database,
)


default_args = {
    "owner": "stellar",
    "email": ["stellar@dataengineer.io"],
    "start_date": timezone.datetime(2023, 5, 1),
    "retries": 3,
    "retry_delay": timedelta(minutes=3),
}
with DAG(
    "cryptocurrency_data_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
) as dag:

    t1 = PythonOperator(
        task_id="fetch_ohlcv",
        python_callable=_fetch_ohlcv,
    )

    t2 = PythonOperator(
        task_id="download_file",
        python_callable=_download_file,
    )

    t3 = PostgresOperator(
        task_id="create_import_table",
        postgres_conn_id="postgres",
        sql="""
            CREATE TABLE IF NOT EXISTS cryptocurrency_import (
                timestamp BIGINT,
                open FLOAT,
                highest FLOAT,
                lowest FLOAT,
                closing FLOAT,
                volume FLOAT
            )
        """,
    )

    t4 = PythonOperator(
        task_id="load_data_into_database",
        python_callable=_load_data_into_database,

    )

    t5 = PostgresOperator(
        task_id="create_final_table",
        postgres_conn_id="postgres",
        sql="""
            CREATE TABLE IF NOT EXISTS cryptocurrency (
                timestamp BIGINT PRIMARY KEY,
                open FLOAT,
                highest FLOAT,
                lowest FLOAT,
                closing FLOAT,
                volume FLOAT
            )
        """,
    )

    t6 = PostgresOperator(
        task_id="merge_import_into_final_table",
        postgres_conn_id="postgres",
        sql="""
            INSERT INTO cryptocurrency (
                timestamp,
                open,
                highest,
                lowest,
                closing,
                volume
            )
            SELECT
                timestamp,
                open,
                highest,
                lowest,
                closing,
                volume
            FROM
                cryptocurrency_import
            ON CONFLICT (timestamp)
            DO UPDATE SET
                open = EXCLUDED.open,
                highest = EXCLUDED.highest,
                lowest = EXCLUDED.lowest,
                closing = EXCLUDED.closing,
                volume = EXCLUDED.volume
        """,
    )

    t7 = PostgresOperator(
        task_id="clear_import_table",
        postgres_conn_id="postgres",
        sql="""
            DELETE FROM cryptocurrency_import
        """,
    )

    t8 = EmailOperator(
        task_id="notify",
        to=["stellar@dataengineer.io"],
        subject="Loaded data into database successfully on {{ ds }}",
        html_content="Your pipeline has loaded data into database successfully",
    )

    t1 >> t2 >> t3 >> t4 >> t5 >> t6 >> t7 >> t8
