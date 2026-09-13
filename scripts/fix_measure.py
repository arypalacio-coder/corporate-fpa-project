path = "financial-report.SemanticModel/definition/tables/_Measures.tmdl"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

old_measure = """measure Net_Working_Capital =
CALCULATE(
SUM(fct_balance_sheet_monthly[ending_balance]),
fct_balance_sheet_monthly[account_id] IN {120, 130}
) - CALCULATE(
SUM(fct_balance_sheet_monthly[ending_balance]),
fct_balance_sheet_monthly[account_id] IN {210, 220}
)"""

new_measure = """measure Net_Working_Capital =
CALCULATE(
SUM(fct_balance_sheet_monthly[ending_balance]),
dim_balance_accounts[account_id] IN {120, 130}
) - CALCULATE(
SUM(fct_balance_sheet_monthly[ending_balance]),
dim_balance_accounts[account_id] IN {210, 220}
)"""

if old_measure in text:
    text = text.replace(old_measure, new_measure)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Medida Net_Working_Capital actualizada exitosamente en TMDL.")
else:
    # Reemplazo por regex si difiere el espaciado
    import re
    pattern = r"measure Net_Working_Capital\s*=[\s\S]*?formatString:"
    replacement = """measure Net_Working_Capital =
CALCULATE(
SUM(fct_balance_sheet_monthly[ending_balance]),
dim_balance_accounts[account_id] IN {120, 130}
) - CALCULATE(
SUM(fct_balance_sheet_monthly[ending_balance]),
dim_balance_accounts[account_id] IN {210, 220}
)
formatString:"""
    text = re.sub(pattern, replacement, text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Medida Net_Working_Capital actualizada mediante regex en TMDL.")
