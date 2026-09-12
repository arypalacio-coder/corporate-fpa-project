CREATE OR REPLACE TABLE int_standardized_metrics AS
SELECT 
    cik,
    entity_name,
    fiscal_period_end,
    fact_end_date,
    qtrs,
    CASE 
        WHEN tag IN ('Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax', 'SalesRevenueNet') 
            THEN 'Total Revenue'
        WHEN tag IN ('CostOfGoodsAndServicesSold', 'CostOfRevenue') 
            THEN 'Cost of Goods Sold'
        WHEN tag IN ('GrossProfit') 
            THEN 'Gross Profit'
        WHEN tag IN ('OperatingIncomeLoss') 
            THEN 'Operating Income'
        WHEN tag IN ('NetIncomeLoss') 
            THEN 'Net Income'
        WHEN tag IN ('Assets') 
            THEN 'Total Assets'
        WHEN tag IN ('Liabilities') 
            THEN 'Total Liabilities'
        WHEN tag IN ('StockholdersEquity') 
            THEN 'Stockholders Equity'
        ELSE NULL 
    END AS standard_metric,
    raw_financial_amount AS amount
FROM int_deduplicated_facts
WHERE standard_metric IS NOT NULL;