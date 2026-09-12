import os
import duckdb

DB_PATH = os.path.join("data", "database", "financial_fpa.duckdb")
EXPORT_DIR = os.path.join("data", "exports")

def exportar_capas_bi():
    os.makedirs(EXPORT_DIR, exist_ok=True)
    print(f"Conectando a DuckDB en: {DB_PATH}")
    con = duckdb.connect(DB_PATH)

    tablas = [
        "dim_chart_of_accounts",
        "dim_fiscal_calendar",
        "dim_cost_center",
        "dim_entity",
        "fct_general_ledger_daily",
        "fct_budget_allocations_monthly",
        "int_budget_vs_actual_monthly_bridge"
    ]

    print(f"Iniciando exportación hacia: {EXPORT_DIR}\n")
    for tabla in tablas:
        csv_path = os.path.join(EXPORT_DIR, f"{tabla}.csv").replace("\\", "/")
        con.execute(f"COPY {tabla} TO '{csv_path}' (HEADER, DELIMITER ',');")
        total_filas = con.execute(f"SELECT count(*) FROM {tabla}").fetchone()[0]
        print(f"-> {tabla:<35} exportada ({total_filas:>6,} registros) -> {csv_path}")

    con.close()
    print("\nExportación a capa BI completada exitosamente.")

if __name__ == "__main__":
    exportar_capas_bi()