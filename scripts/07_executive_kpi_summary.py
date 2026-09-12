import os
import duckdb

CSV_PATH = os.path.join("data", "exports", "fpa_income_statement_mart.csv").replace("\\", "/")

def generar_resumen_ejecutivo():
    print(f"Leyendo dataset maestro desde: {CSV_PATH}...\n")
    con = duckdb.connect()

    # 1. Mediana y percentiles de rentabilidad del mercado
    benchmark_query = f"""
        SELECT 
            COUNT(*) AS total_empresas_analizadas,
            ROUND(MEDIAN(gross_margin_pct), 2) AS mediana_margen_bruto,
            ROUND(MEDIAN(operating_margin_pct), 2) AS mediana_margen_operativo,
            ROUND(QUANTILE_CONT(operating_margin_pct, 0.75), 2) AS cuartil_superior_op_margin,
            ROUND(MEDIAN(net_margin_pct), 2) AS mediana_margen_neto
        FROM read_csv_auto('{CSV_PATH}')
        WHERE qtrs = 1 
          AND total_revenue >= 100000000; -- Empresas con ingresos > $100M USD
    """
    benchmarks = con.execute(benchmark_query).fetchone()

    print("=" * 65)
    print("      BENCHMARK DE RENTABILIDAD CORPORATIVA (Q3 2024)")
    print("=" * 65)
    print(f"Empresas analizadas (Ingresos > $100M): {benchmarks[0]:,}")
    print(f"Mediana Margen Bruto:                 {benchmarks[1]}%")
    print(f"Mediana Margen Operativo:             {benchmarks[2]}%")
    print(f"Top 25% Margen Operativo (P75):       {benchmarks[3]}%")
    print(f"Mediana Margen Neto:                  {benchmarks[4]}%")
    print("=" * 65 + "\n")

    # 2. Líderes de eficiencia operativa (Ingresos > $5B USD)
    top_eficiencia_query = f"""
        SELECT 
            entity_name,
            total_revenue,
            operating_margin_pct,
            net_margin_pct
        FROM read_csv_auto('{CSV_PATH}')
        WHERE qtrs = 1 
          AND total_revenue >= 5000000000 -- Ingresos superiores a $5B USD
        ORDER BY operating_margin_pct DESC
        LIMIT 7;
    """
    top_eficiencia = con.execute(top_eficiencia_query).fetchall()

    print("TOP EMPRESAS DE ALTA CAPITALIZACIÓN POR MARGEN OPERATIVO:")
    print(f"{'Empresa':<32} | {'Ingresos (USD)':>15} | {'Op Margin':>10} | {'Net Margin':>10}")
    print("-" * 75)
    for row in top_eficiencia:
        nombre = row[0][:30]
        rev = f"${row[1]:,.0f}"
        op_mgn = f"{row[2]}%"
        net_mgn = f"{row[3]}%"
        print(f"{nombre:<32} | {rev:>15} | {op_mgn:>10} | {net_mgn:>10}")
    print("-" * 75)

    con.close()

if __name__ == "__main__":
    generar_resumen_ejecutivo()