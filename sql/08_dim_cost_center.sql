-- Dimensión: Centros de Costo (dim_cost_center)
-- Habilita la segmentación de costos y el control presupuestario funcional
CREATE OR REPLACE TABLE dim_cost_center AS
SELECT * FROM (
    VALUES 
        (10, 'Operations & Engineering', 'OPR', 'Operations'),
        (11, 'Sales & Commercial Operations', 'SLS', 'Commercial'),
        (12, 'Corporate & General Admin', 'ADM', 'Administration')
) AS t(cost_center_id, cost_center_name, cost_center_code, department_group);