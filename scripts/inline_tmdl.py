path = "financial-report.SemanticModel/definition/tables/_Measures.tmdl"

with open(path, "r", encoding="utf-8") as f:
    text = f.read()

import re
# Reemplaza completamente el bloque de Net_Working_Capital por una definicion en una sola linea
pattern = r"(\tmeasure Net_Working_Capital\s*=)[\s\S]*?(?=\t\tformatString:)"
replacement = r"\1 CALCULATE(SUM(fct_balance_sheet_monthly[ending_balance]), dim_balance_accounts[account_id] IN {120, 130}) - CALCULATE(SUM(fct_balance_sheet_monthly[ending_balance]), dim_balance_accounts[account_id] IN {210, 220})\n"

text = re.sub(pattern, replacement, text)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("MEDIDA_EN_LINEA_UNICA_OK")
