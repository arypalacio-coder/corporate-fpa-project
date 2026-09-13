path = "financial-report.SemanticModel/definition/tables/dim_fiscal_calendar.tmdl"

with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Corregir la declaracion de la columna year_month a string
import re
text = re.sub(
    r'(column year_month[\s\S]*?dataType:\s*)dateTime[\s\S]*?(annotation UnderlyingDateTimeDataType = Date)?',
    r'\1string',
    text
)

# 2. Corregir la transformacion M en la particion
text = text.replace('{"year_month", type date}', '{"year_month", type text}')

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("CALENDARIO_CORREGIDO_OK")
