path = "financial-report.SemanticModel/definition/relationships.tmdl"

with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Eliminar el bloque de relacion que vincula dim_fiscal_calendar.year_month con LocalDateTable
import re
pattern = r"relationship [a-f0-9\-]+\s+fromColumn:\s*dim_fiscal_calendar\.year_month\s+toColumn:\s*LocalDateTable_[^\n]+\s+isActive:\s*true\s*"
new_text = re.sub(pattern, "", text)

# Si el patron anterior no lo capturo por variacion de espacios, buscar por bloques
if new_text == text:
    blocks = text.split("relationship ")
    kept = []
    for b in blocks:
        if "fromColumn: dim_fiscal_calendar.year_month" in b and "LocalDateTable" in b:
            continue
        kept.append(b)
    new_text = "relationship ".join(kept)

with open(path, "w", encoding="utf-8") as f:
    f.write(new_text)

print("RELACION_HUERFANA_ELIMINADA_OK")
