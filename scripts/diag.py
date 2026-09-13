import os

rel_path = "financial-report.SemanticModel/definition/relationships.tmdl"
print("=== RELACIONES fct_balance_sheet_monthly ===")
if os.path.exists(rel_path):
    with open(rel_path, "r", encoding="utf-8") as f:
        content = f.read()
    for block in content.split("relationship "):
        if "fct_balance_sheet_monthly" in block:
            print("relationship " + block.strip() + "\n---")

bs_table = "financial-report.SemanticModel/definition/tables/fct_balance_sheet_monthly.tmdl"
print("\n=== ESQUEMA fct_balance_sheet_monthly.tmdl ===")
if os.path.exists(bs_table):
    with open(bs_table, "r", encoding="utf-8") as f:
        for line in f:
            if any(k in line for k in ["column ", "dataType:"]):
                print(line.rstrip())

measures_path = "financial-report.SemanticModel/definition/tables/_Measures.tmdl"
print("\n=== MEDIDA Net_Working_Capital ===")
if os.path.exists(measures_path):
    with open(measures_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    cap = False
    for line in lines:
        if "measure Net_Working_Capital" in line:
            cap = True
        elif cap and line.strip().startswith("measure "):
            break
        if cap:
            print(line.rstrip())
