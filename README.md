# Orders Data Migration Pipeline

An end-to-end data engineering project that orchestrates data migration, customer synchronization, incremental loading, transformation, snapshotting, and data quality validation using **Python, Apache Airflow, DuckDB, and dbt**.

## Project Overview

This project demonstrates how to build and orchestrate a data pipeline that extracts data from a source database, loads it into a DuckDB warehouse, transforms raw data into analytics-ready models using dbt, and validates the resulting sales data.

Apache Airflow manages the pipeline execution and task dependencies, while Python handles data loading and synchronization.

## Architecture


```flowchart TD
    A["SQLite Source Database"] --> B["Python Data Ingestion"]
    B --> C["DuckDB Data Warehouse"]

    subgraph AIRFLOW["Apache Airflow Orchestration"]
        D["Check Project Files"]
        E["Sync Customers"]
        F["Incremental Load"]
        G["dbt Run"]
        H["dbt Snapshot"]
        I["dbt Test"]
        J["Validate Sales"]
        K["Validate Customer Sales"]

        D --> E --> F --> G --> H --> I --> J --> K
    end

    C --> E
    C --> F
    G --> L["dbt Transformation Models"]

    subgraph DBT["dbt Analytics Layer"]
        L --> M["Staging Models"]
        M --> N["Fact Order Sales"]
        M --> O["Customer Sales Mart"]
        P["Customer Snapshot"]
    end

    H --> P
    N --> I
    O --> I
    I --> Q["Data Quality Validation"]
    Q --> R["Validated Analytics Data"]

    style A fill:#E0F2FE,stroke:#0284C7,color:#0F172A
    style C fill:#DCFCE7,stroke:#16A34A,color:#14532D
    style AIRFLOW fill:#F3E8FF,stroke:#9333EA,color:#581C87
    style DBT fill:#FEF3C7,stroke:#D97706,color:#78350F
    style R fill:#DCFCE7,stroke:#16A34A,color:#14532D
```

## Technology Stack

- **Python** — Data extraction, loading, synchronization, and validation
- **Apache Airflow** — Workflow orchestration and task dependency management
- **DuckDB** — Analytical data warehouse
- **dbt** — SQL-based data transformations, testing, and snapshots
- **SQLite** — Source database
- **Docker / Astro CLI** — Local Airflow development environment
- **Git and GitHub** — Version control and project hosting

## Key Features

- Source data extraction and warehouse loading
- Incremental loading of new orders and order items
- Customer synchronization
- SQL transformations using dbt
- Staging models for customers, products, orders, and order items
- Fact table for order sales
- Customer sales mart for analytics
- Customer history tracking using a dbt snapshot
- Automated dbt data quality tests
- Sales reconciliation and validation
- Airflow orchestration with task dependencies

## Project Structure

```text
orders-data-migration-pipeline/
├── dags/
│   ├── orders_migration_pipeline.py
│   └── exampledag.py
├── include/
│   └── project/
│       ├── dbt_config/
│       │   └── profiles.example.yml
│       ├── orders_dbt/
│       │   ├── models/
│       │   │   ├── stg_customers.sql
│       │   │   ├── stg_products.sql
│       │   │   ├── stg_orders.sql
│       │   │   ├── stg_order_items.sql
│       │   │   ├── fct_order_sales.sql
│       │   │   ├── mart_customer_sales.sql
│       │   │   └── schema.yml
│       │   ├── snapshots/
│       │   │   └── customers_snapshot.sql
│       │   └── dbt_project.yml
│       ├── extract_load.py
│       ├── incremental_load.py
│       ├── sync_customers.py
│       ├── check_sales.py
│       └── check_customer_sales.py
├── tests/
├── Dockerfile
├── packages.txt
├── requirements.txt
├── .dockerignore
└── .gitignore
```

## Pipeline Workflow

The Airflow DAG, `orders_data_migration_pipeline`, executes the following tasks in sequence:

1. **Check project files** — Verify that required scripts, the warehouse, and the dbt profile are present.
2. **Sync customers** — Synchronize customer data with the warehouse.
3. **Incremental load** — Load new orders and order items.
4. **dbt run** — Execute SQL transformations.
5. **dbt snapshot** — Track changes to customer records.
6. **dbt test** — Execute configured data quality tests.
7. **Validate sales** — Check sales fact data and order-level results.
8. **Validate customer sales** — Reconcile customer-level sales metrics.

## Validation Results

The pipeline was successfully executed in the local Airflow environment.

| Validation metric | Result |
|---|---:|
| Customers with orders | 200 |
| Distinct orders | 5,002 |
| Total units purchased | 37,396 |
| Total sales | 4,213,081.29 |
| dbt models created successfully | 8 |
| dbt data tests previously passed | 18 |
| Airflow tasks in successful DAG run | 8 |

The customer sales validation confirmed that the summary and fact data matched for customer counts, distinct orders, total units, and total sales.

## Prerequisites

- Python compatible with your installed Airflow environment
- Docker Desktop
- Astro CLI
- Git
- dbt Core and the dbt-duckdb adapter

Use the project's `requirements.txt` and Astro configuration to determine the exact dependency versions.

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/riiiiiiiu/orders-data-migration-pipeline.git
cd orders-data-migration-pipeline
```

### 2. Start the local Airflow environment

```bash
astro dev start
```

Wait for the Airflow services to become available.

### 3. Prepare the source database and warehouse

The local SQLite and DuckDB database files are intentionally excluded from Git. Prepare them using the project's data-generation and loading scripts, following their intended execution order.

For example, inspect `make_source.py` and `extract_load.py` before running them. The full-refresh loading script may rebuild the warehouse, so do not run it against data you need to preserve.

### 4. Configure dbt

Use `include/project/dbt_config/profiles.example.yml` as a starting template for your local `profiles.yml`.

Ensure the dbt profile name is `orders_dbt` and that the configured DuckDB path points to the warehouse location accessible from the Airflow container.

### 5. Run the Airflow DAG

Open:

```text
http://localhost:8080
```

Find `orders_data_migration_pipeline` and trigger it from the Airflow interface.

### 6. Review the results

Inspect the task logs in Airflow and confirm that the dbt transformations, tests, and Python validation tasks succeed.

## Data and Configuration Notes

- Local `.db`, `.duckdb`, and other database files are excluded from version control.
- The real local dbt profile is excluded; use the example profile as a template.
- Airflow logs, generated dbt artifacts, and local environment files are excluded.
- The source database and warehouse must be prepared locally before the full pipeline can run.

## Future Enhancements

- Add automated scheduling and retry policies.
- Add logging and alerting for pipeline failures.
- Add a larger set of incremental-load and data quality tests.
- Add CI checks for Python code and dbt models.
- Add pipeline monitoring and execution metrics.
- Add automated environment setup and reproducible sample-data generation.

## Author

**Rehan Shaikh**

Aspiring Data Engineer interested in Python, SQL, data pipelines, cloud technologies, and analytics engineering.

## License

No license has been added yet. Contact the repository owner before reusing this project unless a license is added.
