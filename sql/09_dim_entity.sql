-- Dimensión: Entidades Legales y Subsidiarias (dim_entity)
-- Habilita la consolidación multientidad y análisis segmentado por subsidiaria
CREATE OR REPLACE TABLE dim_entity AS
SELECT * FROM (
    VALUES 
        (1, 'Global Holdings Corp (Parent)', 'US-DELAWARE', 'USD'),
        (2, 'North America Operating Sub LLC', 'US-NEWYORK', 'USD'),
        (3, 'EMEA Commercial Services Ltd', 'UK-LONDON', 'USD')
) AS t(entity_id, entity_name, jurisdiction, functional_currency);