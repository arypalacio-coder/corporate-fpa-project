-- Capa Marts: Hechos Diarios del Libro Mayor (fct_general_ledger_daily)
-- Integra transacciones diarias con claves foráneas hacia las dimensiones conformadas
CREATE OR REPLACE TABLE fct_general_ledger_daily AS
SELECT 
    transaction_date,
    entity_id,
    account_id,
    cost_center_id,
    debit_amount,
    credit_amount,
    ROUND(debit_amount - credit_amount, 2) AS net_amount
FROM fact_general_ledger_entries;