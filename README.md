# Corporate FP&A Data & Reporting Architecture

Arquitectura analitica integral para FP&A orientada a la consolidacion contable, modelado dimensional y reportes ejecutivos en Power BI (PBIP + TMDL).

## 1. Arquitectura General

- DuckDB / SQL Data Layer
- Tabular Model (TMDL / PBIP)
- Power BI Executive Dashboard (KPIs, PL Matrix, EBITDA Bridge, NWC y DSO)

## 2. Metricas Core

- Net Working Capital (NWC) con KEEPFILTERS
- Days Sales Outstanding (DSO)
- EBITDA Variance Bridge

## 3. Estructura del Repositorio

- Data/exports/
- financial-report.pbip
- financial-report.Report/
- financial-report.SemanticModel/
- power_bi/templates/
- scripts/
- sql/
- README.md
