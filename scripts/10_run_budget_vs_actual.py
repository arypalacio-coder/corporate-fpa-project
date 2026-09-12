import os
import duckdb

DB_PATH = os.path.join("data", "database", "financial_fpa.duckdb")
SQL_PATH = os.path.join("sql", "05_int_budget_vs_actual.sql")

def ejecutar_budget_vs_actual():
    print(f"Conectando a DuckDB en: {DB_PATH}")
    con = duckdb.connect(DB_PATH)

    print(f"Leyendo consulta de reconciliación desde: {SQL_PATH}")
    with open(SQL_PATH, "r", encoding="utf-8") as file:
        query_sql = file.read()

    print("Ejecutando reconciliación de granularidades asimétricas (Date Spine & Bridge)...")
    con.execute(query_sql)

    total_filas = con.execute("SELECT count(*) FROM int_budget_vs_actual_monthly_bridge").fetchone()[0]
    print(f"-> Tabla 'int_budget_vs_actual_monthly_bridge' creada exitosamente con {total_filas:,} registros.\n")

    print("Muestra de análisis de variaciones presupuestarias (Budget vs Actual):")
    muestra = con.execute("""
        SELECT 
            reporting_month,
            account_id,
            cost_center_id,
            actual_amount,
            budget_amount,
            budget_variance_absolute,
            budget_variance_percentage
        FROM int_budget_vs_actual_monthly_bridge
        WHERE actual_amount > 0 OR budget_amount > 0
        ORDER BY reporting_month DESC, account_id ASC
        LIMIT 5;
    """).fetchall()

    print(f"{'Mes':<12} | {'Cuenta':<8} | {'CC':<5} | {'Real ($)':>12} | {'Ppto ($)':>12} | {'Var Abs ($)':>12} | {'Var %':>8}")
    print("-" * 80)
    for row in muestra:
        mes = str(row[0])
        acc = str(row[1])
        cc = str(row[2])
        act = f"${row[3]:>10,.2f}"
        bgt = f"${row[4]:>10,.2f}"
        var_abs = f"${row[5]:>10,.2f}"
        var_pct = f"{row[6]:>7.2f}%" if row[6] is not None else "    N/A"
        print(f"{mes:<12} | {acc:<8} | {cc:<5} | {act} | {bgt} | {var_abs} | {var_pct}")

    con.close()
    print("\nReconciliación presupuestaria completada con éxito.")

if __name__ == "__main__":
    ejecutar_budget_vs_actual()