path = "financial-report.SemanticModel/definition/tables/_Measures.tmdl"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False

for line in lines:
    if line.strip().startswith("measure Net_Working_Capital"):
        skip = True
        new_lines.append("\tmeasure Net_Working_Capital =\n")
        new_lines.append("\t\tCALCULATE(\n")
        new_lines.append("\t\t\tSUM(fct_balance_sheet_monthly[ending_balance]),\n")
        new_lines.append("\t\t\tdim_balance_accounts[account_id] IN {120, 130}\n")
        new_lines.append("\t\t) - CALCULATE(\n")
        new_lines.append("\t\t\tSUM(fct_balance_sheet_monthly[ending_balance]),\n")
        new_lines.append("\t\t\tdim_balance_accounts[account_id] IN {210, 220}\n")
        new_lines.append("\t\t)\n")
    elif skip:
        if line.strip().startswith("formatString:") or line.strip().startswith("lineageTag:") or line.strip().startswith("measure ") or (not line.startswith("\t\t") and not line.startswith(" ") and line.strip()):
            skip = False
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("TMDL_OK")
