-- Dimensión: Calendario Fiscal Maestro (dim_fiscal_calendar)
-- Provee claves temporales para transacciones diarias y presupuestos mensuales
CREATE OR REPLACE TABLE dim_fiscal_calendar AS
WITH date_series AS (
    SELECT unnest(generate_series(DATE '2023-01-01', DATE '2024-12-31', INTERVAL 1 DAY))::DATE AS full_date
)
SELECT 
    full_date AS date,
    DATE_TRUNC('month', full_date)::DATE AS first_day_of_month,
    EXTRACT(YEAR FROM full_date)::INT AS year,
    EXTRACT(MONTH FROM full_date)::INT AS month_number,
    STRFTIME(full_date, '%B') AS month_name,
    'Q' || EXTRACT(QUARTER FROM full_date)::VARCHAR AS quarter,
    STRFTIME(full_date, '%Y-%m') AS year_month
FROM date_series;