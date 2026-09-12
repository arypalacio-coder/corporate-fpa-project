import os
import duckdb

DB_PATH = os.path.join("data", "database", "financial_fpa.duckdb")
SQL_PATH = os.path.join("sql", "04_int_quarterly_time_series.sql")

def ejecutar_series_de_tiempo():
    print(f"Conectando a DuckDB en: {DB_PATH}")
    con = duckdb.connect(DB_PATH)

    print("Convirtiendo fact_end_date a formato DATE nativo...")
    con.execute("""
        CREATE OR REPLACE TABLE int_deduplicated_facts AS 
        SELECT 
            cik,
            entity_name,
            tag,
            fiscal_period_end,
            CASE 
                WHEN fact_end_date IS NOT NULL AND length(fact_end_date::VARCHAR) >= 8 THEN
                    MAKE_DATE(
                        SUBSTR(fact_end_date::VARCHAR, 1, 4)::INT,
                        SUBSTR(fact_end_date::VARCHAR, 5, 2)::INT,
                        SUBSTR(fact_end_date::VARCHAR, 7, 2)::INT
                    )
                ELSE NULL 
            END AS fact_end_date,
            qtrs,
            raw_financial_amount
        FROM int_deduplicated_facts;
    """)

    print(f"Leyendo consulta de series de tiempo desde: {SQL_PATH}")
    with open(SQL_PATH, "r", encoding="utf-8") as file:
        query_sql = file.read()

    print("Calculando desacumulación del 4to trimestre, métricas TTM, QoQ y YoY...")
    con.execute(query_sql)

    total_filas = con.execute("SELECT count(*) FROM int_quarterly_time_series").fetchone()[0]
    print(f"-> Tabla 'int_quarterly_time_series' creada exitosamente con {total_filas:,} registros.\n")

    print("Muestra de análisis temporal para Revenues (Top registros):")
    muestra = con.execute("""
        SELECT 
            cik, 
            tag, 
            fact_end_date, 
            actual_quarterly_value, 
            ttm_amount, 
            qoq_growth_percentage, 
            yoy_growth_percentage
        FROM int_quarterly_time_series
        WHERE tag = 'Revenues'
          AND actual_quarterly_value IS NOT NULL
          AND fact_end_date IS NOT NULL
        ORDER BY fact_end_date DESC, actual_quarterly_value DESC
        LIMIT 5;
    """).fetchall()

    for row in muestra:
        cik = str(row[0])
        fecha = str(row[2])
        trimestre = f"${row[3]:>14,.0f}" if row[3] is not None else " " * 15
        ttm = f"${row[4]:>15,.0f}" if row[4] is not None else "            N/A"
        qoq = f"{row[5]:>6.2f}%" if row[5] is not None else "   N/A"
        yoy = f"{row[6]:>6.2f}%" if row[6] is not None else "   N/A"
        print(f"CIK: {cik:<10} | Fecha: {fecha} | Trimestre: {trimestre} | TTM: {ttm} | QoQ: {qoq} | YoY: {yoy}")

    con.close()
    print("\nProcesamiento de series de tiempo completado con éxito.")

if __name__ == "__main__":
    ejecutar_series_de_tiempo()