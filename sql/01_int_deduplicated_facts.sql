-- Detección y aislamiento de la última versión contable válida reportada
-- Elimina duplicados de enmiendas (10-K/A) conservando la versión auditada más reciente

CREATE OR REPLACE TABLE int_deduplicated_facts AS
WITH audited_statement_deduplication AS (
    SELECT 
        s.cik,
        s.name AS entity_name,
        s.adsh,
        s.period AS fiscal_period_end,
        s.filed AS filed_date,
        n.tag,
        n.version,
        n.ddate AS fact_end_date,
        n.qtrs,
        n.uom,
        n.value AS raw_financial_amount,
        ROW_NUMBER() OVER (
            PARTITION BY s.cik, n.tag, n.ddate, n.qtrs 
            ORDER BY s.filed DESC, s.adsh DESC
        ) AS amendment_recency_rank
    FROM stg_sec_submissions s
    INNER JOIN stg_sec_numbers n 
        ON s.adsh = n.adsh
    WHERE n.uom = 'USD'
      AND n.qtrs IN (1, 4)
)
SELECT 
    cik,
    entity_name,
    tag,
    fiscal_period_end,
    fact_end_date,
    qtrs,
    raw_financial_amount
FROM audited_statement_deduplication
WHERE amendment_recency_rank = 1;