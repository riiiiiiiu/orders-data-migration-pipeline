
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR = "/usr/local/airflow/include/project"
DBT_DIR = f"{PROJECT_DIR}/orders_dbt"
DBT_PROFILES_DIR = f"{PROJECT_DIR}/dbt_config"

with DAG(
    dag_id="orders_data_migration_pipeline",
    description="Orchestrate the orders migration pipeline with Python, DuckDB, and dbt",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["data-engineering", "dbt", "duckdb"],
) as dag:

    check_project_files = BashOperator(
        task_id="check_project_files",
        bash_command=(
            f"test -f {PROJECT_DIR}/incremental_load.py && "
            f"test -f {PROJECT_DIR}/sync_customers.py && "
            f"test -f {PROJECT_DIR}/warehouse.duckdb && "
            f"test -f {DBT_PROFILES_DIR}/profiles.yml && "
            "echo 'Project files found successfully'"
        ),
    )

    sync_customers = BashOperator(
        task_id="sync_customers",
        bash_command=f"cd {PROJECT_DIR} && python sync_customers.py",
    )

    incremental_load = BashOperator(
        task_id="incremental_load",
        bash_command=f"cd {PROJECT_DIR} && python incremental_load.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            f"export DBT_PROFILES_DIR={DBT_PROFILES_DIR} && "
            f"dbt run --project-dir {DBT_DIR}"
        ),
    )

    dbt_snapshot = BashOperator(
        task_id="dbt_snapshot",
        bash_command=(
            f"export DBT_PROFILES_DIR={DBT_PROFILES_DIR} && "
            f"dbt snapshot --project-dir {DBT_DIR}"
        ),
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            f"export DBT_PROFILES_DIR={DBT_PROFILES_DIR} && "
            f"dbt test --project-dir {DBT_DIR}"
        ),
    )

    validate_sales = BashOperator(
        task_id="validate_sales",
        bash_command=f"cd {PROJECT_DIR} && python check_sales.py",
    )

    validate_customer_sales = BashOperator(
        task_id="validate_customer_sales",
        bash_command=f"cd {PROJECT_DIR} && python check_customer_sales.py",
    )

    check_project_files >> sync_customers
    sync_customers >> incremental_load
    incremental_load >> dbt_run

    dbt_run >> dbt_snapshot >> dbt_test
    dbt_test >> validate_sales >> validate_customer_sales
