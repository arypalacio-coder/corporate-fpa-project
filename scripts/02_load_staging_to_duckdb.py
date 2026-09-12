import os
import duckdb

# Definición de rutas del proyecto
DB_DIR = os.path.join("data", "database")
DB_PATH = os.path.join(DB_DIR, "financial_fpa.duckdb")
RAW_DIR = os.path.join("data", "raw")

def cargar_capa_staging():
    os.makedirs(DB_DIR, exist_ok=True)
    
    print(f"Iniciando conexión con DuckDB en: {DB_PATH}")
    con = duckdb.connect(DB_PATH)

    # Mapeo de tablas de staging y sus respectivos archivos crudos
    archivos_staging = [
        ("stg_sec_submissions", "sub.txt"),
        ("stg_sec_tags", "tag.txt"),
        ("stg_sec_numbers", "num.txt"),
        ("stg_sec_presentation", "pre.txt")
    ]

    for tabla, archivo in archivos_staging:
        ruta_archivo = os.path.join(RAW_DIR, archivo).replace("\\", "/")
        print(f"Cargando {archivo} en la tabla {tabla}...")
        
        # Ingesta directa optimizada para archivos delimitados por tabulaciones
        con.execute(f"""
            CREATE OR REPLACE TABLE {tabla} AS 
            SELECT * FROM read_csv(
                '{ruta_archivo}', 
                delim='\\t', 
                header=True, 
                auto_detect=True,
                ignore_errors=True
            );
        """)
        
        filas = con.execute(f"SELECT count(*) FROM {tabla}").fetchone()[0]
        print(f"-> {tabla} creada exitosamente con {filas:,} registros.")

    con.close()
    print("Carga de la capa de staging finalizada con éxito.")

if __name__ == "__main__":
    cargar_capa_staging()