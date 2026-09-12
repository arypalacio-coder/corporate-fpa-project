import os
import duckdb

DB_PATH = os.path.join("data", "database", "financial_fpa.duckdb")
SQL_PATH = os.path.join("sql", "10_fct_general_ledger_daily.sql")

def ejecutar_fct_gl_daily():
    print(f"Conectando a DuckDB en: {DB_PATH}")
    con = duckdb.connect(DB_PATH)

    print(f"Leyendo script SQL desde: {SQL_PATH}")
    with open(SQL_PATH, "r", encoding="utf-8") as file:
        query_sql = file.read()

    print("Construyendo tabla de hechos diaria del Libro Mayor (fct_general_ledger_daily)...")
    con.execute(query_sql)

    total_filas = con.execute("SELECT count(*) FROM fct_general_ledger_daily").fetchone()[0]
    print(f"-> Tabla 'fct_general_ledger_daily' creada exitosamente con {total_filas:,} asientos diarios.\n")

    print("Muestra de transacciones diarias del Libro Mayor:")
    muestra = con.execute("""
        SELECT 
            transaction_date,
            entity_id,
            account_id,
            cost_center_id,
            debit_amount,
            credit_amount,
            net_amount
        FROM fct_general_ledger_daily
        ORDER BY transaction_date DESC, account_id ASC
        LIMIT 5;
    """).fetchall()

    print(f"{'Fecha':<12} | {'Entidad':<8} | {'Cuenta':<8} | {'CC':<5} | {'Débito ($)':>12} | {'Crédito ($)':>12} | {'Neto ($)':>12}")
    print("-" * 85)
    for row in muestra:
        fecha = str(row[0])
        ent = str(row[1])
        acc = str(row[2])
        cc = str(row[3])
        deb = f"${row[4]:>10,.2f}"
        crd = f"${row[5]:>10,.2f}"
        net = f"${row[6]:>10,.2f}"
        print(f"{fecha:<12} | {ent:<8} | {acc:<8} | {cc:<5} | {deb} | {crd} | {net}")

    con.close()
    print("\nTabla de hechos diaria validada correctamente.")

if __name__ == "__main__":
    ejecutar_fct_gl_daily()