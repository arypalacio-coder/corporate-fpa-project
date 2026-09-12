-- Desacumulación aritmética del cuarto trimestre y análisis de variaciones temporales
CREATE OR REPLACE TABLE int_quarterly_time_series AS
WITH isolated_quarterly_series AS (  
    SELECT   
        cik,  
        tag,  
        fact_end_date,  
        EXTRACT(YEAR FROM fact_end_date) AS fiscal_year,  
        qtrs,  
        raw_financial_amount,  
        CASE   
            WHEN qtrs = 1 THEN raw_financial_amount  
            WHEN qtrs = 4 THEN raw_financial_amount - COALESCE(  
                SUM(raw_financial_amount) OVER (  
                    PARTITION BY cik, tag, EXTRACT(YEAR FROM fact_end_date)   
                    ORDER BY fact_end_date   
                    ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING  
                ), 0)  
        END AS isolated_quarter_amount  
    FROM int_deduplicated_facts  
    WHERE tag IN ('Revenues', 'CostOfGoodsAndServicesSold', 'OperatingIncomeLoss', 'NetIncomeLoss')  
),  
temporal_window_metrics AS (  
    SELECT   
        cik,  
        tag,  
        fact_end_date,  
        fiscal_year,  
        isolated_quarter_amount,  
        LAG(isolated_quarter_amount, 1) OVER (  
            PARTITION BY cik, tag   
            ORDER BY fact_end_date  
        ) AS prior_quarter_amount,  
        LAG(isolated_quarter_amount, 4) OVER (  
            PARTITION BY cik, tag   
            ORDER BY fact_end_date  
        ) AS prior_year_quarter_amount,  
        SUM(isolated_quarter_amount) OVER (  
            PARTITION BY cik, tag   
            ORDER BY fact_end_date   
            ROWS BETWEEN 3 PRECEDING AND CURRENT ROW  
        ) AS trailing_twelve_months_sum  
    FROM isolated_quarterly_series  
)  
SELECT   
    cik,  
    tag,  
    fact_end_date,  
    isolated_quarter_amount AS actual_quarterly_value,  
    prior_quarter_amount,  
    prior_year_quarter_amount,  
    trailing_twelve_months_sum AS ttm_amount,  
    ROUND(  
        ((isolated_quarter_amount - prior_quarter_amount) /   
        NULLIF(ABS(prior_quarter_amount), 0)) * 100, 2  
    ) AS qoq_growth_percentage,  
    ROUND(  
        ((isolated_quarter_amount - prior_year_quarter_amount) /   
        NULLIF(ABS(prior_year_quarter_amount), 0)) * 100, 2  
    ) AS yoy_growth_percentage  
FROM temporal_window_metrics;