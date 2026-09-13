path = "financial-report.SemanticModel/definition/tables/dim_fiscal_calendar.tmdl"
with open(path, "r", encoding="utf-8") as f:
    for line in f:
        if any(k in line for k in ["column date", "dataType:", "UnderlyingDateTimeDataType", "type date", "type datetime"]):
            print(line.rstrip())
