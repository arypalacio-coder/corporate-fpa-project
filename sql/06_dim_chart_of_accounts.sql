-- Dimensión: Catálogo Maestro de Cuentas (dim_chart_of_accounts)
-- Incluye jerarquía contable multinivel (Parent-Child) y polaridad de presentación
CREATE OR REPLACE TABLE dim_chart_of_accounts AS
SELECT * FROM (
    VALUES 
        -- Nivel 1: Raíz
        (1, 'Total P&L', NULL::INT, 'Consolidated P&L', 1),
        
        -- Nivel 2: Agrupaciones intermedias
        (10, 'Gross Margin Summary', 1, 'Operating Performance', 1),
        (20, 'Operating Expenses (OPEX)', 1, 'Operating Performance', -1),
        
        -- Nivel 3: Cuentas operativas asignadas en el Libro Mayor
        (100, 'Product Revenue', 10, 'Revenues', 1),
        (101, 'Services Revenue', 10, 'Revenues', 1),
        (102, 'Direct Cost of Goods Sold', 10, 'Cost of Goods Sold', -1),
        (103, 'Research & Development (R&D)', 20, 'Operating Expenses', -1),
        (104, 'Selling, General & Administrative (SG&A)', 20, 'Operating Expenses', -1)
) AS t(account_id, account_name, parent_account_id, account_category, display_polarity_factor);