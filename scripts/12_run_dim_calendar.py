import os
import duckdb

DB_PATH = os.path.join("data", "database", "financial_fpa.duckdb")
SQL_PATH = os.path.join("sql", "07_dim_fiscal_calendar.sql")

def ejecutar_dim_calendar():
    print(f"Conectando a DuckDB en: {DB_PATH}")
    con = duckdb.connect(DB_PATH)

    print(f"Leyendo script SQL desde: {SQL_PATH}")
    with open(SQL_PATH, "r", encoding="utf-8") as file:
        query_sql = file.read()

    print("Construyendo dimensión del Calendario Fiscal (dim_fiscal_calendar)...")
    con.execute(query_sql)

    total_filas = con.execute("SELECT count(*) FROM dim_fiscal_calendar").fetchone()[0]
    print(f"-> Tabla 'dim_fiscal_calendar' creada exitosamente con {total_filas:,} días calendario.\n")

    print("Muestra de estructura temporal:")
    muestra = con.execute("""
        SELECT 
            date,
            first_day_of_month,
            year,
            month_number,
            month_name,
            quarter,
            year_month
        FROM dim_fiscal_calendar
        WHERE date IN (DATE '2023-01-01', DATE '2023-01-15', DATE '2024-06-30', DATE '2024-12-31')
        ORDER BY date ASC;
    """).fetchall()

    print(f"{'Date':<12} | {'First Day Month':<16} | {'Año':<5} | {'Mes #':<6} | {'Nombre':<12} | {'Q':<4} | {'Año-Mes':<8}")
    print("-" * 80)
    for row in muestra:
        d = str(row[0])
        fd = str(row[1])
        y = str(row[2])
        m_num = str(row[3])
        m_name = str(row[4])
        q = str(row[5])
        ym = str(row[6])
        print(f"{d:<12} | {fd:<16} | {y:<5} | {m_num:<6} | {m_name:<12} | {q:<4} | {ym:<8}")

    con.close()
    print("\nDimensión de calendario validada correctamente.")

if __name__ == "__main__":
    ejecutar_dim_calendar()