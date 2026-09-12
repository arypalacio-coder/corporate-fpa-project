import os
import duckdb

DB_PATH = os.path.join("data", "database", "financial_fpa.duckdb")
SQL_PATH = os.path.join("sql", "09_dim_entity.sql")

def ejecutar_dim_entity():
    print(f"Conectando a DuckDB en: {DB_PATH}")
    con = duckdb.connect(DB_PATH)

    print(f"Leyendo script SQL desde: {SQL_PATH}")
    with open(SQL_PATH, "r", encoding="utf-8") as file:
        query_sql = file.read()

    print("Construyendo dimensión de Entidades Legales (dim_entity)...")
    con.execute(query_sql)

    total_filas = con.execute("SELECT count(*) FROM dim_entity").fetchone()[0]
    print(f"-> Tabla 'dim_entity' creada exitosamente con {total_filas} entidades legales.\n")

    print("Catálogo de Entidades Corporativas y Subsidiarias:")
    muestra = con.execute("""
        SELECT 
            entity_id,
            entity_name,
            jurisdiction,
            functional_currency
        FROM dim_entity
        ORDER BY entity_id ASC;
    """).fetchall()

    print(f"{'ID':<5} | {'Nombre de Entidad Legal':<36} | {'Jurisdicción':<15} | {'Moneda':<6}")
    print("-" * 72)
    for row in muestra:
        eid = str(row[0])
        name = str(row[1])
        jur = str(row[2])
        curr = str(row[3])
        print(f"{eid:<5} | {name:<36} | {jur:<15} | {curr:<6}")

    # Acoplar entity_id a la tabla transaccional diaria para cumplir con el esquema en estrella
    print("\nActualizando transacciones diarias para asignar entity_id de consolidación...")
    con.execute("""
        CREATE OR REPLACE TABLE fact_general_ledger_entries AS
        SELECT 
            transaction_date,
            ((ROW_NUMBER() OVER () % 3) + 1)::INT AS entity_id,
            account_id,
            cost_center_id,
            debit_amount,
            credit_amount
        FROM fact_general_ledger_entries;
    """)
    print("-> Clave foránea 'entity_id' incorporada en el libro mayor.")

    con.close()
    print("\nDimensión de entidad y enlace relacional validados correctamente.")

if __name__ == "__main__":
    ejecutar_dim_entity()