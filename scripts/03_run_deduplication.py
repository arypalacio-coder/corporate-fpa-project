import os
import duckdb

DB_PATH = os.path.join("data", "database", "financial_fpa.duckdb")
SQL_PATH = os.path.join("sql", "01_int_deduplicated_facts.sql")

def ejecutar_transformacion():
    print(f"Conectando a la base de datos en: {DB_PATH}")
    con = duckdb.connect(DB_PATH)

    print(f"Leyendo script SQL desde: {SQL_PATH}")
    with open(SQL_PATH, "r", encoding="utf-8") as file:
        query_sql = file.read()

    print("Ejecutando deduplicación y aislamiento de versiones auditadas...")
    con.execute(query_sql)

    total_filas = con.execute("SELECT count(*) FROM int_deduplicated_facts").fetchone()[0]
    print(f"-> Tabla 'int_deduplicated_facts' creada exitosamente con {total_filas:,} registros únicos.")

    con.close()
    print("Transformación finalizada correctamente.")

if __name__ == "__main__":
    ejecutar_transformacion()