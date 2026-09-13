import os

print("=== 1. PROPIEDADES DE LA RELACION fct_balance_sheet_monthly -> dim_fiscal_calendar ===")
rel_file = "financial-report.SemanticModel/definition/relationships.tmdl"
with open(rel_file, "r", encoding="utf-8") as f:
    rels = f.read().split("relationship ")

for r in rels:
    if "fct_balance_sheet_monthly.month_date" in r:
        print("relationship " + r.strip())

print("\n=== 2. CONSULTA M (PARTICION) fct_balance_sheet_monthly.tmdl ===")
tbl_file = "financial-report.SemanticModel/definition/tables/fct_balance_sheet_monthly.tmdl"
with open(tbl_file, "r", encoding="utf-8") as f:
    print(f.read())
