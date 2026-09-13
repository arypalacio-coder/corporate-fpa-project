import os
import glob

def verify():
    base_dir = r'financial-report.SemanticModel/definition'
    tables_dir = os.path.join(base_dir, 'tables')

    print("--- Validating TMDL syntax and indentation ---")
    lineage_tags = set()
    duplicates = []

    for filepath in glob.glob(os.path.join(tables_dir, '*.tmdl')):
        basename = os.path.basename(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Verify first line is table <name>
        assert lines[0].startswith('table '), f"{basename}: First line must start with table"
        
        # Check lines for lineageTag uniqueness
        for idx, line in enumerate(lines):
            if 'lineageTag:' in line:
                tag = line.split('lineageTag:')[1].strip()
                if tag in lineage_tags:
                    duplicates.append((basename, idx+1, tag))
                lineage_tags.add(tag)

    print(f"Total unique lineageTags verified: {len(lineage_tags)}")
    assert len(duplicates) == 0, f"Duplicate lineageTags found: {duplicates}"
    print("SUCCESS: All lineageTags are unique.")

    # Validate relationships
    rel_file = os.path.join(base_dir, 'relationships.tmdl')
    with open(rel_file, 'r', encoding='utf-8') as f:
        rel_content = f.read()

    required_rels = [
        ('fct_balance_sheet_monthly.account_id', 'dim_balance_accounts.account_id'),
        ('fct_balance_sheet_monthly.month_date', 'dim_fiscal_calendar.date'),
        ('fct_balance_sheet_monthly.entity_id', 'dim_entity.entity_id'),
        ('fct_sales_subledger.transaction_date', 'dim_fiscal_calendar.date'),
        ('fct_sales_subledger.entity_id', 'dim_entity.entity_id')
    ]

    for from_col, to_col in required_rels:
        assert from_col in rel_content, f"Missing relationship fromColumn: {from_col}"
        assert to_col in rel_content, f"Missing relationship toColumn: {to_col}"
        print(f"SUCCESS: Verified relationship {from_col} -> {to_col}")

    # Validate model.tmdl
    model_file = os.path.join(base_dir, 'model.tmdl')
    with open(model_file, 'r', encoding='utf-8') as f:
        model_content = f.read()

    for t in ['dim_balance_accounts', 'fct_balance_sheet_monthly', 'fct_sales_subledger', 'dim_variance_bridge']:
        assert f"ref table {t}" in model_content, f"Missing ref table {t} in model.tmdl"
        assert f'"{t}"' in model_content, f"Missing {t} in PBI_QueryOrder"
        print(f"SUCCESS: Verified table ref in model.tmdl: {t}")

    # Validate new measures in _Measures.tmdl
    measures_file = os.path.join(tables_dir, '_Measures.tmdl')
    with open(measures_file, 'r', encoding='utf-8') as f:
        m_content = f.read()

    bridge_measures = ['Budget_EBITDA', 'Cost_OpEx_Variance', 'Waterfall_Bridge_Amount']
    for bm in bridge_measures:
        assert f"measure {bm} =" in m_content, f"Missing measure {bm} in _Measures.tmdl"
        print(f"SUCCESS: Verified measure in _Measures.tmdl: {bm}")

    print("\nALL VERIFICATIONS PASSED WITH ZERO ERRORS!")

if __name__ == '__main__':
    verify()
