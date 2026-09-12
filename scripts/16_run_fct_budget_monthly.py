import os
import duckdb

DB_PATH = os.path.join("data", "database", "financial_fpa.duckdb")
SQL_PATH = os.path.join("sql", "11_fct_budget_allocations_monthly.sql")

def ejecutar_fct_budget_monthly():
    print(f"Conectando a DuckDB en: {DB_PATH}")
    con = duckdb.connect(DB_PATH)

    print(f"Leyendo script SQL desde: {SQL_PATH}")
    with open(SQL_PATH, "r", encoding="utf-8") as file:
        query_sql = file.read()

    print("Construyendo tabla de hechos de Presupuesto Mensual (fct_budget_allocations_monthly)...")
    con.execute(query_sql)

    total_filas = con.execute("SELECT count(*) FROM fct_budget_allocations_monthly").fetchone()[0]
    print(f"-> Tabla 'fct_budget_allocations_monthly' creada exitosamente con {total_filas:,} asignaciones presupuestarias.\n")

    print("Muestra de metas presupuestarias mensuales:")
    muestra = con.execute("""
        SELECT 
            budget_month,
            account_id,
            cost_center_id,
            budgeted_amount
        FROM fct_budget_allocations_monthly
        ORDER BY budget_month DESC, account_id ASC
        LIMIT 5;
    """).fetchall()

    print(f"{'Mes Presupuesto':<16} | {'Cuenta':<8} | {'CC':<5} | {'Monto Presupuestado ($)':>25}")
    print("-" * 62)
    for row in muestra:
        mes = str(row[0])
        acc = str(row[1])
        cc = str(row[2])
        bgt = f"${row[3]:>20,.2f}"
        print(f"{mes:<16} | {acc:<8} | {cc:<5} | {bgt}")

    con.close()
    print("\nTabla de hechos presupuestaria validada correctamente.")

if __name__ == "__main__":
    ejecutar_fct_budget_monthly()