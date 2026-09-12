-- Reconciliación estructural de granularidades asimétricas (Real Diario vs Presupuesto Mensual)
CREATE OR REPLACE TABLE int_budget_vs_actual_monthly_bridge AS  
WITH date_spine_monthly AS (  
    SELECT   
        DATE_TRUNC('month', d)::DATE AS reporting_month  
    FROM (
        SELECT unnest(generate_series(DATE '2023-01-01', DATE '2024-12-31', INTERVAL 1 MONTH)) AS d
    )  
),  
aggregated_actual_transactions AS (  
    SELECT   
        DATE_TRUNC('month', transaction_date)::DATE AS reporting_month,  
        account_id,  
        cost_center_id,  
        SUM(debit_amount - credit_amount) AS net_actual_movement  
    FROM fact_general_ledger_entries  
    GROUP BY 1, 2, 3  
),  
unified_performance_mart AS (  
    SELECT   
        ds.reporting_month,  
        COALESCE(act.account_id, bgt.account_id) AS account_id,  
        COALESCE(act.cost_center_id, bgt.cost_center_id) AS cost_center_id,  
        COALESCE(act.net_actual_movement, 0.0) AS actual_amount,  
        COALESCE(bgt.budgeted_amount, 0.0) AS budget_amount  
    FROM date_spine_monthly ds  
    LEFT JOIN aggregated_actual_transactions act   
        ON ds.reporting_month = act.reporting_month  
    FULL OUTER JOIN fact_budget_allocations bgt   
        ON ds.reporting_month = bgt.budget_month   
       AND act.account_id = bgt.account_id   
       AND act.cost_center_id = bgt.cost_center_id  
)  
SELECT   
    reporting_month,  
    account_id,  
    cost_center_id,  
    ROUND(actual_amount, 2) AS actual_amount,  
    ROUND(budget_amount, 2) AS budget_amount,  
    ROUND((actual_amount - budget_amount), 2) AS budget_variance_absolute,  
    CASE   
        WHEN budget_amount = 0 THEN NULL  
        ELSE ROUND(((actual_amount - budget_amount) / ABS(budget_amount)) * 100, 2)  
    END AS budget_variance_percentage  
FROM unified_performance_mart;