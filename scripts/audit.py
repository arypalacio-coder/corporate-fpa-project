import os, glob, json, csv
from collections import defaultdict

print("=== AUDITORIA 1: DATOS DE BALANCE SHEET ===")
csv_path = os.path.join("Data", "exports", "fct_balance_sheet_monthly.csv")
if not os.path.exists(csv_path):
    print(f"ERROR: No encontrado {csv_path}")
else:
    balances = defaultdict(lambda: defaultdict(float))
    with open(csv_path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            balances[row["month_date"]][int(row["account_id"])] += float(row["ending_balance"])
    print(f"Meses totales: {len(balances)}")
    for m in sorted(balances.keys()):
        if m.startswith("2024"):
            b = balances[m]
            nwc = (b[120] + b[130]) - (b[210] + b[220])
            print(f"{m} | NWC: ${nwc:,.2f} | AR(120): ${b[120]:,.2f} | Inv(130): ${b[130]:,.2f} | AP(210): ${b[210]:,.2f} | Acc(220): ${b[220]:,.2f}")

print("\n=== AUDITORIA 2: RELACIONES ===")
rel_path = os.path.join("financial-report.SemanticModel", "definition", "relationships.tmdl")
if os.path.exists(rel_path):
    with open(rel_path, "r", encoding="utf-8") as f:
        for line in f:
            if any(k in line for k in ["fct_balance_sheet_monthly", "fct_sales_subledger", "dim_fiscal_calendar"]):
                print(line.strip())

print("\n=== AUDITORIA 3: VISUALES PBIR ===")
for vf in glob.glob("financial-report.Report/definition/pages/**/visual.json", recursive=True):
    if ".bak" in vf: continue
    try:
        with open(vf, "r", encoding="utf-8") as f:
            v = json.load(f)
        vt = v.get("visual", {}).get("visualType", "")
        if vt in ["lineChart", "pivotTable", "waterfallChart"]:
            cid = os.path.basename(os.path.dirname(vf))
            pos = v.get("position", {})
            q = list(v.get("visual", {}).get("query", {}).get("queryState", {}).keys())
            print(f"[{vt}] {cid} | Pos: ({pos.get('x')}, {pos.get('y')}, {pos.get('width')}, {pos.get('height')}) | Roles: {q}")
    except Exception as e:
        print(f"Error en {vf}: {e}")
