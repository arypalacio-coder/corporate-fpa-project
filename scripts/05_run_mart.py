import os
import duckdb

DB_PATH = os.path.join("data", "database", "financial_fpa.duckdb")
SQL_PATH = os.path.join("sql", "03_mart_income_statement.sql")

def ejecutar_mart():
    print(f"Conectando a la base de datos en: {DB_PATH}")
    con = duckdb.connect(DB_PATH)

    print(f"Leyendo script SQL desde: {SQL_PATH}")
    with open(SQL_PATH, "r", encoding="utf-8") as file:
        query_sql = file.read()

    print("Generando capa analítica (mart_income_statement)...")
    con.execute(query_sql)

    total_filas = con.execute("SELECT count(*) FROM mart_income_statement").fetchone()[0]
    print(f"-> Tabla 'mart_income_statement' creada exitosamente con {total_filas:,} registros consolidados.\n")

    print("Top 5 empresas por ingresos reportados en el período:")
    muestra = con.execute("""
        SELECT 
            entity_name, 
            fact_end_date, 
            total_revenue, 
            operating_margin_pct, 
            net_margin_pct
        FROM mart_income_statement
        WHERE qtrs = 1
        ORDER BY total_revenue DESC
        LIMIT 5
    """).fetchall()

    for row in muestra:
        print(f"  - {row[0][:30]:<30} | Fecha: {row[1]} | Rev: ${row[2]:>15,.0f} | Op Mgn: {row[3]:>6}% | Net Mgn: {row[4]:>6}%")

    con.close()
    print("\nCálculo de Data Mart finalizado correctamente.")

if __name__ == "__main__":
    ejecutar_mart()