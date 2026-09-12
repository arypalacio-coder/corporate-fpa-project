import os
import duckdb

DB_PATH = os.path.join("data", "database", "financial_fpa.duckdb")
SQL_PATH = os.path.join("sql", "06_dim_chart_of_accounts.sql")

def ejecutar_dim_accounts():
    print(f"Conectando a DuckDB en: {DB_PATH}")
    con = duckdb.connect(DB_PATH)

    print(f"Leyendo script SQL desde: {SQL_PATH}")
    with open(SQL_PATH, "r", encoding="utf-8") as file:
        query_sql = file.read()

    print("Construyendo dimensión maestra del Plan de Cuentas (dim_chart_of_accounts)...")
    con.execute(query_sql)

    total_filas = con.execute("SELECT count(*) FROM dim_chart_of_accounts").fetchone()[0]
    print(f"-> Tabla 'dim_chart_of_accounts' creada exitosamente con {total_filas} cuentas y niveles jerárquicos.\n")

    print("Catálogo Maestro de Cuentas y Factores de Polaridad Contable:")
    muestra = con.execute("""
        SELECT 
            account_id,
            account_name,
            parent_account_id,
            account_category,
            display_polarity_factor
        FROM dim_chart_of_accounts
        ORDER BY account_id ASC;
    """).fetchall()

    print(f"{'ID':<5} | {'Nombre de Cuenta':<38} | {'Parent ID':<10} | {'Categoría':<22} | {'Polaridad':<10}")
    print("-" * 95)
    for row in muestra:
        acc_id = str(row[0])
        name = str(row[1])
        parent = str(row[2]) if row[2] is not None else "ROOT"
        cat = str(row[3])
        pol = f"{row[4]:+d}"
        print(f"{acc_id:<5} | {name:<38} | {parent:<10} | {cat:<22} | {pol:<10}")

    con.close()
    print("\nDimensión contable validada correctamente.")

if __name__ == "__main__":
    ejecutar_dim_accounts()