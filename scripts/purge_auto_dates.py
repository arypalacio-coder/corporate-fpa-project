import os, re

base_dir = "financial-report.SemanticModel/definition"
rels_path = os.path.join(base_dir, "relationships.tmdl")
cal_path = os.path.join(base_dir, "tables", "dim_fiscal_calendar.tmdl")
model_path = os.path.join(base_dir, "model.tmdl")
tables_dir = os.path.join(base_dir, "tables")

# 1. Limpiar relationships.tmdl
if os.path.exists(rels_path):
    with open(rels_path, "r", encoding="utf-8") as f:
        rels_text = f.read()
    
    blocks = rels_text.split("relationship ")
    kept_blocks = []
    for b in blocks:
        if "LocalDateTable" in b:
            continue
        kept_blocks.append(b)
    
    new_rels = "relationship ".join(kept_blocks)
    with open(rels_path, "w", encoding="utf-8") as f:
        f.write(new_rels)

# 2. Limpiar dim_fiscal_calendar.tmdl (eliminar todas las variaciones)
if os.path.exists(cal_path):
    with open(cal_path, "r", encoding="utf-8") as f:
        cal_text = f.read()
    
    # Patrón para capturar y eliminar bloques de 'variation'
    cal_text = re.sub(r'\t+variation \w+[\s\S]*?defaultHierarchy:[^\n]+\n', '', cal_text)
    with open(cal_path, "w", encoding="utf-8") as f:
        f.write(cal_text)

# 3. Limpiar model.tmdl
if os.path.exists(model_path):
    with open(model_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    clean_lines = [l for l in lines if "LocalDateTable_" not in l]
    with open(model_path, "w", encoding="utf-8") as f:
        f.writelines(clean_lines)

# 4. Eliminar archivos LocalDateTable
deleted = 0
if os.path.exists(tables_dir):
    for f_name in os.listdir(tables_dir):
        if f_name.startswith("LocalDateTable_"):
            os.remove(os.path.join(tables_dir, f_name))
            deleted += 1

print(f"PURGA_COMPLETA_OK. Tablas locales eliminadas: {deleted}")
