import os

tables_dir = "financial-report.SemanticModel/definition/tables"
orphan_file = "LocalDateTable_9e91bcb1-1d98-4665-86e0-501a6892c112.tmdl"
orphan_path = os.path.join(tables_dir, orphan_file)

if os.path.exists(orphan_path):
    os.remove(orphan_path)
    print(f"ARCHIVO_ELIMINADO: {orphan_file}")
else:
    print(f"NO_EXISTE: {orphan_file}")

model_file = "financial-report.SemanticModel/definition/model.tmdl"
if os.path.exists(model_file):
    with open(model_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    clean_lines = [l for l in lines if "LocalDateTable_9e91bcb1-1d98-4665-86e0-501a6892c112" not in l]
    
    with open(model_file, "w", encoding="utf-8") as f:
        f.writelines(clean_lines)
    print("MODEL_TMDL_ACTUALIZADO_OK")
