import os
import duckdb

DB_PATH = os.path.join("data", "database", "financial_fpa.duckdb")
SQL_PATH = os.path.join("sql", "08_dim_cost_center.sql")

def ejecutar_dim_cost_center():
    print(f"Conectando a DuckDB en: {DB_PATH}")
    con = duckdb.connect(DB_PATH)

    print(f"Leyendo script SQL desde: {SQL_PATH}")
    with open(SQL_PATH, "r", encoding="utf-8") as file:
        query_sql = file.read()

    print("Construyendo dimensión de Centros de Costo (dim_cost_center)...")
    con.execute(query_sql)

    total_filas = con.execute("SELECT count(*) FROM dim_cost_center").fetchone()[0]
    print(f"-> Tabla 'dim_cost_center' creada exitosamente con {total_filas} centros de costo.\n")

    print("Catálogo de Centros de Costo:")
    muestra = con.execute("""
        SELECT 
            cost_center_id,
            cost_center_name,
            cost_center_code,
            department_group
        FROM dim_cost_center
        ORDER BY cost_center_id ASC;
    """).fetchall()

    print(f"{'ID':<5} | {'Nombre Centro de Costo':<32} | {'Código':<8} | {'Grupo Departamental':<20}")
    print("-" * 75)
    for row in muestra:
        cid = str(row[0])
        name = str(row[1])
        code = str(row[2])
        group = str(row[3])
        print(f"{cid:<5} | {name:<32} | {code:<8} | {group:<20}")

    con.close()
    print("\nDimensión de centros de costo validada correctamente.")

if __name__ == "__main__":
    ejecutar_dim_cost_center()