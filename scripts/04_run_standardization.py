import os
import duckdb

DB_PATH = os.path.join("data", "database", "financial_fpa.duckdb")
SQL_PATH = os.path.join("sql", "02_int_standardized_metrics.sql")

def ejecutar_estandarizacion():
    print(f"Conectando a la base de datos en: {DB_PATH}")
    con = duckdb.connect(DB_PATH)

    print(f"Leyendo script SQL desde: {SQL_PATH}")
    with open(SQL_PATH, "r", encoding="utf-8") as file:
        query_sql = file.read()

    print("Ejecutando estandarización de métricas contables...")
    con.execute(query_sql)

    total_filas = con.execute("SELECT count(*) FROM int_standardized_metrics").fetchone()[0]
    print(f"-> Tabla 'int_standardized_metrics' creada exitosamente con {total_filas:,} registros.\n")

    print("Distribución por métrica estandarizada:")
    metricas = con.execute("""
        SELECT standard_metric, count(*) 
        FROM int_standardized_metrics 
        GROUP BY standard_metric 
        ORDER BY count(*) DESC
    """).fetchall()

    for metrica, total in metricas:
        print(f"  - {metrica}: {total:,}")

    con.close()
    print("\nEstandarización finalizada correctamente.")

if __name__ == "__main__":
    ejecutar_estandarizacion()