# Corporate FP&A Data Modeling & Analytics Engine

An end-to-end corporate Financial Planning & Analysis (FP&A) architecture and reporting pipeline designed to analyze General Ledger (GL) transactions, monthly budget allocations, and performance variances across corporate entities and cost centers.

---

## Architecture & Data Pipeline

1. **Ingestion & Staging:** Structured SQL queries processing financial transaction feeds.
2. **Data Modeling:** Star schema dimensional modeling built on DuckDB/SQL, decoupling transactions into centralized facts and operational dimensions.
3. **Semantic Layer & Analytics:** Power BI project (`.pbip`) utilizing TMDL definitions, standardized financial DAX measures, and structured P&L hierarchy groupings.

---

## Dimensional Model

- **Fact Tables:**
  - `fct_general_ledger_daily`: Granular transactional postings with debit/credit balance mapping.
  - `fct_budget_allocations_monthly`: Corporate planning baselines by cost center and account code.
- **Bridge & Analytics Mart:**
  - `fpa_income_statement_mart`: Pre-aggregated income statement reporting layer.
  - `int_budget_vs_actual_monthly_bridge`: Consolidated variance calculation mart.
- **Dimensions:**
  - `dim_chart_of_accounts`: Master account mapping (Revenue, COGS, OpEx, CapEx).
  - `dim_cost_center`: Functional business units and departmental hierarchy.
  - `dim_entity`: Multi-company legal entity master.
  - `dim_fiscal_calendar`: Fiscal calendar dimension supporting time-intelligence functions.

---

## Power BI Implementation

- **Format:** Git-integrated Power BI Project format (`.pbip` / TMDL).
- **Key DAX Metrics:** Actuals, Budget, Variance ($), Variance (%), Gross Margin, Operating Income, and Rolling Run Rates.
- **Localization:** Standardized corporate English nomenclature across visuals, semantic layers, and field parameters.

---

## Repository Structure

```text
corporate-fpa-project/
├── Data/
│   └── exports/                       # Cleaned dimensional & fact datasets (.csv)
├── docs/                              # Data model and DAX documentation
├── financial-report.Report/           # Visual report definitions (PBIP)
├── financial-report.SemanticModel/    # TMDL semantic model & DAX measures
├── scripts/                           # Python automation & processing scripts
├── sql/                               # SQL transformation & mart queries
├── .gitattributes                     # Language detection overrides
├── .gitignore                         # Build and cache exclusion rules
├── financial-report.pbip              # Power BI Project entry point
├── LICENSE                            # MIT License
└── README.md                          # Project documentation