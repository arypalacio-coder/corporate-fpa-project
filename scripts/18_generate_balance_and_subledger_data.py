"""
Script to generate:
1. dim_balance_accounts.csv
2. fct_balance_sheet_monthly.csv
3. fct_sales_subledger.csv

Reconciled with existing GL and Budget facts for 2023 and 2024.
"""

import os
import csv
import math
from collections import defaultdict

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    exports_dir = os.path.join(base_dir, 'Data', 'exports')
    os.makedirs(exports_dir, exist_ok=True)
    
    # ---------------------------------------------------------
    # 1. Generate dim_balance_accounts.csv
    # ---------------------------------------------------------
    dim_balance_file = os.path.join(exports_dir, 'dim_balance_accounts.csv')
    balance_accounts = [
        {
            'account_id': 110,
            'account_name': 'Cash and Cash Equivalents',
            'balance_category': 'Cash & Equivalents',
            'financial_statement_class': 'Asset'
        },
        {
            'account_id': 120,
            'account_name': 'Accounts Receivable',
            'balance_category': 'Receivables',
            'financial_statement_class': 'Asset'
        },
        {
            'account_id': 130,
            'account_name': 'Inventory',
            'balance_category': 'Inventory',
            'financial_statement_class': 'Asset'
        },
        {
            'account_id': 210,
            'account_name': 'Accounts Payable',
            'balance_category': 'Payables',
            'financial_statement_class': 'Liability'
        },
        {
            'account_id': 220,
            'account_name': 'Accrued Operating Liabilities',
            'balance_category': 'Accrued Expenses',
            'financial_statement_class': 'Liability'
        }
    ]
    
    with open(dim_balance_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['account_id', 'account_name', 'balance_category', 'financial_statement_class'])
        writer.writeheader()
        writer.writerows(balance_accounts)
    print(f"Created: {dim_balance_file} with {len(balance_accounts)} records.")
    
    # ---------------------------------------------------------
    # 2. Read GL data to calibrate Balance Sheet & Subledger
    # ---------------------------------------------------------
    gl_file = os.path.join(exports_dir, 'fct_general_ledger_daily.csv')
    with open(gl_file, 'r', encoding='utf-8') as f:
        gl_rows = list(csv.DictReader(f))
        
    rev_by_me = defaultdict(float)
    cogs_by_me = defaultdict(float)
    opex_by_me = defaultdict(float)
    
    for r in gl_rows:
        ym = r['transaction_date'][:7] + '-01'
        ent = int(r['entity_id'])
        acc = int(r['account_id'])
        amt = float(r['net_amount'])
        if acc in (100, 101):
            rev_by_me[(ym, ent)] += amt
        elif acc == 102:
            cogs_by_me[(ym, ent)] += amt
        elif acc in (103, 104):
            opex_by_me[(ym, ent)] += amt
            
    months = sorted(list(set(k[0] for k in rev_by_me.keys())))
    entities = [1, 2, 3]
    
    # ---------------------------------------------------------
    # 3. Generate fct_balance_sheet_monthly.csv
    # ---------------------------------------------------------
    fct_bs_file = os.path.join(exports_dir, 'fct_balance_sheet_monthly.csv')
    bs_rows = []
    dso_values = []
    
    for idx, m in enumerate(months):
        for e in entities:
            rev = rev_by_me[(m, e)]
            cogs = cogs_by_me[(m, e)]
            opex = opex_by_me[(m, e)]
            
            # DSO calibrated strictly between 40 and 60 days (avg ~48 days)
            dso_target = 48.0 + 5.0 * math.sin((idx + e) * 0.7)
            ar_balance = round(rev * (dso_target / 30.0), 2)
            actual_dso = (ar_balance / rev) * 30.0
            dso_values.append(actual_dso)
            
            # Inventory consistent with COGS (DSI ~52 days)
            dsi_target = 52.0 + 6.0 * math.cos((idx + e) * 0.5)
            inv_balance = round(cogs * (dsi_target / 30.0), 2)
            
            # Cash & Cash Equivalents: buffer of ~1.85x monthly outflows + reserve
            cash_balance = round((cogs + opex) * 1.85 + 5000.0, 2)
            
            # Accounts Payable: DPO ~36 days of COGS
            dpo_target = 36.0 + 4.0 * math.sin((idx * 2 + e) * 0.4)
            ap_balance = round(cogs * (dpo_target / 30.0), 2)
            
            # Accrued Liabilities: ~21 days of OpEx
            accrued_target = 21.0 + 3.0 * math.cos((idx + e * 2) * 0.6)
            accrued_balance = round(opex * (accrued_target / 30.0), 2)
            
            bs_rows.append({'month_date': m, 'entity_id': e, 'account_id': 110, 'ending_balance': f"{cash_balance:.2f}"})
            bs_rows.append({'month_date': m, 'entity_id': e, 'account_id': 120, 'ending_balance': f"{ar_balance:.2f}"})
            bs_rows.append({'month_date': m, 'entity_id': e, 'account_id': 130, 'ending_balance': f"{inv_balance:.2f}"})
            bs_rows.append({'month_date': m, 'entity_id': e, 'account_id': 210, 'ending_balance': f"{ap_balance:.2f}"})
            bs_rows.append({'month_date': m, 'entity_id': e, 'account_id': 220, 'ending_balance': f"{accrued_balance:.2f}"})
            
    with open(fct_bs_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['month_date', 'entity_id', 'account_id', 'ending_balance'])
        writer.writeheader()
        writer.writerows(bs_rows)
        
    print(f"Created: {fct_bs_file} with {len(bs_rows)} records.")
    print(f"DSO verified: min={min(dso_values):.2f}, max={max(dso_values):.2f}, avg={sum(dso_values)/len(dso_values):.2f}")
    assert all(40.0 <= d <= 60.0 for d in dso_values), "DSO out of bounds!"

    # ---------------------------------------------------------
    # 4. Generate fct_sales_subledger.csv
    # ---------------------------------------------------------
    fct_sales_file = os.path.join(exports_dir, 'fct_sales_subledger.csv')
    
    catalog = {
        '100': [
            (101, 'Enterprise Analytics Platform', 2500.00),
            (102, 'Data Integration Engine', 1200.00),
            (103, 'Cloud Connector License', 400.00),
        ],
        '101': [
            (201, 'Implementation & Onboarding', 1800.00),
            (202, 'Managed Support Plan', 900.00),
            (203, 'Custom BI Consulting', 300.00),
        ]
    }
    
    rev_rows = [r for r in gl_rows if r['account_id'] in ('100', '101')]
    subledger_rows = []
    
    for idx, r in enumerate(rev_rows):
        dt = r['transaction_date']
        ent = int(r['entity_id'])
        acc = r['account_id']
        target_amt = float(r['net_amount'])
        target_cents = int(round(target_amt * 100))
        skus = catalog[acc]
        
        # Select rotation of SKUs
        if idx % 3 == 0:
            s0, s1 = skus[0], skus[1]
            w0 = 0.60
        elif idx % 3 == 1:
            s0, s1 = skus[1], skus[2]
            w0 = 0.65
        else:
            s0, s1 = skus[0], skus[2]
            w0 = 0.70
            
        p_b_0 = s0[2]
        p_b_1 = s1[2]
        
        units_0 = max(1, int(round((target_cents * w0 / 100.0) / p_b_0)))
        raw_cents_0 = int(round(target_cents * w0))
        # Ensure cents_0 is exactly divisible by units_0 so unit price has clean 2 decimals
        cents_0 = raw_cents_0 - (raw_cents_0 % units_0)
        cents_1 = target_cents - cents_0
        
        # units_1 is set to 1 so cents_1 % 1 == 0 is always exact
        units_1 = 1
        
        p_a_0 = round((cents_0 // units_0) / 100.0, 2)
        p_a_1 = round(cents_1 / 100.0, 2)
        
        b_units_0 = max(1, int(round(target_cents * w0 / 100.0 / p_b_0)))
        b_units_1 = max(1, int(round((target_cents - target_cents * w0) / 100.0 / p_b_1)))
        
        row0 = {
            'transaction_date': dt,
            'entity_id': ent,
            'sku_id': s0[0],
            'product_name': s0[1],
            'units_sold': units_0,
            'actual_unit_price': f"{p_a_0:.2f}",
            'budget_unit_price': f"{p_b_0:.2f}",
            'budget_units': b_units_0
        }
        row1 = {
            'transaction_date': dt,
            'entity_id': ent,
            'sku_id': s1[0],
            'product_name': s1[1],
            'units_sold': units_1,
            'actual_unit_price': f"{p_a_1:.2f}",
            'budget_unit_price': f"{p_b_1:.2f}",
            'budget_units': b_units_1
        }
        
        # Validate exact cent match on each transaction
        assert round(units_0 * p_a_0 + units_1 * p_a_1, 2) == target_amt
        subledger_rows.extend([row0, row1])
        
    with open(fct_sales_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['transaction_date', 'entity_id', 'sku_id', 'product_name', 'units_sold', 'actual_unit_price', 'budget_unit_price', 'budget_units']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(subledger_rows)
        
    total_sub_rev = round(sum(int(r['units_sold']) * float(r['actual_unit_price']) for r in subledger_rows), 2)
    total_gl_rev = round(sum(float(r['net_amount']) for r in rev_rows), 2)
    
    print(f"Created: {fct_sales_file} with {len(subledger_rows)} records.")
    print(f"Total Subledger Revenue: ${total_sub_rev:,.2f}")
    print(f"Total GL Revenue:        ${total_gl_rev:,.2f}")
    assert total_sub_rev == total_gl_rev, f"Revenue mismatch: {total_sub_rev} vs {total_gl_rev}"
    print("All reconciliations passed successfully!")

if __name__ == '__main__':
    main()
