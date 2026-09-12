import os
import duckdb

DB_PATH = os.path.join("data", "database", "financial_fpa.duckdb")

def generar_tablas_gl_y_presupuesto():
    print(f"Conectando a DuckDB en: {DB_PATH}")
    con = duckdb.connect(DB_PATH)

    print("Creando tabla de transacciones diarias del Libro Mayor (fact_general_ledger_entries)...")
    con.execute("""
        CREATE OR REPLACE TABLE fact_general_ledger_entries AS
        WITH fechas AS (
            SELECT unnest(generate_series(DATE '2023-01-01', DATE '2024-12-31', INTERVAL 1 DAY))::DATE AS d
        ),
        indexadas AS (
            SELECT 
                d AS transaction_date,
                ROW_NUMBER() OVER () AS idx
            FROM fechas
        )
        SELECT 
            transaction_date,
            ((idx % 5) + 100)::INT AS account_id,
            ((idx % 3) + 10)::INT AS cost_center_id,
            ROUND(random() * 5000 + 1000, 2) AS debit_amount,
            ROUND(random() * 500, 2) AS credit_amount
        FROM indexadas;
    """)

    print("Creando tabla de asignaciones de presupuesto mensual (fact_budget_allocations)...")
    con.execute("""
        CREATE OR REPLACE TABLE fact_budget_allocations AS
        WITH meses AS (
            SELECT unnest(generate_series(DATE '2023-01-01', DATE '2024-12-01', INTERVAL 1 MONTH))::DATE AS budget_month
        ),
        cuentas AS (
            SELECT unnest([100, 101, 102, 103, 104]) AS account_id
        ),
        centros AS (
            SELECT unnest([10, 11, 12]) AS cost_center_id
        )
        SELECT 
            m.budget_month,
            c.account_id,
            cc.cost_center_id,
            ROUND(random() * 80000 + 50000, 2) AS budgeted_amount
        FROM meses m
        CROSS JOIN cuentas c
        CROSS JOIN centros cc;
    """)

    gl_count = con.execute("SELECT count(*) FROM fact_general_ledger_entries").fetchone()[0]
    bgt_count = con.execute("SELECT count(*) FROM fact_budget_allocations").fetchone()[0]

    print(f"-> 'fact_general_ledger_entries' creada con {gl_count:,} asientos diarios.")
    print(f"-> 'fact_budget_allocations' creada con {bgt_count:,} registros de presupuesto mensual.")

    con.close()
    print("\nEstructura transaccional y presupuestaria lista.")

if __name__ == "__main__":
    generar_tablas_gl_y_presupuesto()