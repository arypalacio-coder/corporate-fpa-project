import os, csv

print("=== 1. VERIFICACION DE FORMATO DE FECHAS ===")
cal_path = os.path.join("Data", "dim_fiscal_calendar.csv")
if not os.path.exists(cal_path):
    cal_path = os.path.join("Data", "exports", "dim_fiscal_calendar.csv")

bs_path = os.path.join("Data", "exports", "fct_balance_sheet_monthly.csv")

with open(bs_path, "r", encoding="utf-8") as f:
    bs_dates = set(row["month_date"] for row in csv.DictReader(f))

with open(cal_path, "r", encoding="utf-8") as f:
    cal_rows = list(csv.DictReader(f))
    cal_dates = set(row["date"] for row in cal_rows)
    cal_ym = set(row.get("year_month", "") for row in cal_rows)

print(f"Fechas en Balance Sheet: {sorted(list(bs_dates))[:3]} ... (Total: {len(bs_dates)})")
print(f"Fechas en Calendario:    {sorted(list(cal_dates))[:3]} ... (Total: {len(cal_dates)})")
coincidencias = bs_dates.intersection(cal_dates)
print(f"Coincidencias exactas de fecha entre Balance y Calendario: {len(coincidencias)} de {len(bs_dates)}")

print("\n=== 2. VERIFICACION dim_balance_accounts ===")
acc_path = os.path.join("Data", "dim_balance_accounts.csv")
if not os.path.exists(acc_path):
    acc_path = os.path.join("Data", "exports", "dim_balance_accounts.csv")

if os.path.exists(acc_path):
    with open(acc_path, "r", encoding="utf-8") as f:
        print("Cuentas presentes en dim_balance_accounts:")
        for r in csv.DictReader(f):
            if r.get("account_id") in ["120", "130", "210", "220"]:
                print(f"  ID: {r.get('account_id')} | Nombre: {r.get('account_name', r.get('name', ''))}")
else:
    print(f"No se encontro archivo de cuentas en {acc_path}")
