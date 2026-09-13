import os, csv

cal_path = os.path.join("Data", "dim_fiscal_calendar.csv")
if not os.path.exists(cal_path):
    cal_path = os.path.join("Data", "exports", "dim_fiscal_calendar.csv")

with open(cal_path, "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    print("Primeras 3 filas de dim_fiscal_calendar:")
    for i, row in enumerate(r):
        if i < 3:
            print(f"  date: '{row.get('date')}' | first_day_of_month: '{row.get('first_day_of_month')}' | year_month: '{row.get('year_month')}'")
