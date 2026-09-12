-- Capa Marts: Hechos Mensuales de Presupuesto (fct_budget_allocations_monthly)
-- Modela las asignaciones presupuestarias mensuales articuladas con las dimensiones conformadas
CREATE OR REPLACE TABLE fct_budget_allocations_monthly AS
SELECT 
    budget_month,
    account_id,
    cost_center_id,
    ROUND(budgeted_amount, 2) AS budgeted_amount
FROM fact_budget_allocations;