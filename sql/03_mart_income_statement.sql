-- Capa de Presentación: Data Mart con reglas de auditoría contable FP&A
CREATE OR REPLACE TABLE mart_income_statement AS
WITH pivoted_metrics AS (
    SELECT 
        cik,
        entity_name,
        fact_end_date,
        qtrs,
        MAX(CASE WHEN standard_metric = 'Total Revenue' THEN amount END) AS total_revenue,
        MAX(CASE WHEN standard_metric = 'Cost of Goods Sold' THEN amount END) AS cogs,
        MAX(CASE WHEN standard_metric = 'Gross Profit' THEN amount END) AS gross_profit,
        MAX(CASE WHEN standard_metric = 'Operating Income' THEN amount END) AS operating_income,
        MAX(CASE WHEN standard_metric = 'Net Income' THEN amount END) AS net_income
    FROM int_standardized_metrics
    GROUP BY cik, entity_name, fact_end_date, qtrs
),
ranked_entities AS (
    SELECT 
        cik,
        entity_name,
        fact_end_date,
        qtrs,
        total_revenue,
        cogs,
        COALESCE(gross_profit, total_revenue - cogs) AS gross_profit,
        operating_income,
        net_income,
        ROUND((COALESCE(gross_profit, total_revenue - cogs) / NULLIF(total_revenue, 0)) * 100, 2) AS gross_margin_pct,
        ROUND((operating_income / NULLIF(total_revenue, 0)) * 100, 2) AS operating_margin_pct,
        ROUND((net_income / NULLIF(total_revenue, 0)) * 100, 2) AS net_margin_pct,
        -- Prioriza el reporte consolidado principal por empresa en cada fecha
        ROW_NUMBER() OVER (
            PARTITION BY entity_name, fact_end_date 
            ORDER BY total_revenue DESC
        ) AS entity_rank
    FROM pivoted_metrics
    WHERE total_revenue IS NOT NULL 
      AND total_revenue > 0
)
SELECT 
    cik,
    entity_name,
    fact_end_date,
    qtrs,
    total_revenue,
    cogs,
    gross_profit,
    operating_income,
    net_income,
    gross_margin_pct,
    operating_margin_pct,
    net_margin_pct
FROM ranked_entities
WHERE entity_rank = 1
  AND operating_margin_pct BETWEEN -100.0 AND 100.0;