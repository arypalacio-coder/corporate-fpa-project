import os
import duckdb

DB_PATH = os.path.join("data", "database", "financial_fpa.duckdb")
OUTPUT_DIR = os.path.join("data", "exports")
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "fpa_income_statement_mart.csv").replace("\\", "/")

def exportar_mart():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Conectando a DuckDB en: {DB_PATH}")
    con = duckdb.connect(DB_PATH)

    print(f"Exportando 'mart_income_statement' hacia: {OUTPUT_CSV}")
    con.execute(f"""
        COPY (
            SELECT * 
            FROM mart_income_statement 
            ORDER BY fact_end_date DESC, total_revenue DESC
        ) TO '{OUTPUT_CSV}' (HEADER, DELIMITER ',');
    """)

    filas_exportadas = con.execute("SELECT count(*) FROM mart_income_statement").fetchone()[0]
    print(f"-> Archivo generado exitosamente con {filas_exportadas:,} filas listas para análisis.")

    con.close()

if __name__ == "__main__":
    exportar_mart()