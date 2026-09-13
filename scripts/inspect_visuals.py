import json, glob, os

print("=== 1. CAMPOS ASIGNADOS EN VISUALES DE LINEA ===")
for vf in glob.glob("financial-report.Report/definition/pages/**/visual.json", recursive=True):
    if ".bak" in vf: continue
    try:
        with open(vf, "r", encoding="utf-8") as f:
            v = json.load(f)
        vt = v.get("visual", {}).get("visualType", "")
        if vt == "lineChart":
            cid = os.path.basename(os.path.dirname(vf))
            qs = v.get("visual", {}).get("query", {}).get("queryState", {})
            print(f"\nVisual ID: {cid} (Tipo: {vt})")
            for role, data in qs.items():
                projs = data.get("projections", [])
                for p in projs:
                    print(f"  Rol: {role:<12} | queryRef: {p.get('queryRef')}")
    except Exception as e:
        print(f"Error leyendo {vf}: {e}")

print("\n=== 2. MEDIDA Days_Sales_Outstanding_DSO ===")
meas_path = "financial-report.SemanticModel/definition/tables/_Measures.tmdl"
if os.path.exists(meas_path):
    with open(meas_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    cap = False
    for line in lines:
        if "measure Days_Sales_Outstanding_DSO" in line or "measure 'Days_Sales_Outstanding_DSO'" in line:
            cap = True
        elif cap and line.strip().startswith("measure "):
            break
        if cap:
            print(line.rstrip())
