path = "financial-report.SemanticModel/definition/tables/dim_fiscal_calendar.tmdl"

with open(path, "r", encoding="utf-8") as f:
    text = f.read()

import re
# Eliminar el bloque 'variation Variación' completo bajo la definicion de year_month
pattern = r"(\t+variation Variación[\s\S]*?defaultHierarchy:[^\n]+)"
clean_text = re.sub(pattern, "", text)

with open(path, "w", encoding="utf-8") as f:
    f.write(clean_text)

print("VARIACION_ELIMINADA_OK")
