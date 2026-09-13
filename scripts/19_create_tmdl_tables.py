import uuid
import os

def create_tmdls():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tables_dir = os.path.join(base_dir, 'financial-report.SemanticModel', 'definition', 'tables')
    definition_dir = os.path.join(base_dir, 'financial-report.SemanticModel', 'definition')
    
    # -------------------------------------------------------------
    # 1. dim_balance_accounts.tmdl
    # -------------------------------------------------------------
    content_ba = """table dim_balance_accounts
\tlineageTag: __T_BA__

\tcolumn account_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: __C_ACC__
\t\tsummarizeBy: none
\t\tsourceColumn: account_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn account_name
\t\tdataType: string
\t\tlineageTag: __C_NAME__
\t\tsummarizeBy: none
\t\tsourceColumn: account_name

\t\tannotation SummarizationSetBy = Automatic

\tcolumn balance_category
\t\tdataType: string
\t\tlineageTag: __C_CAT__
\t\tsummarizeBy: none
\t\tsourceColumn: balance_category

\t\tannotation SummarizationSetBy = Automatic

\tcolumn financial_statement_class
\t\tdataType: string
\t\tlineageTag: __C_CLASS__
\t\tsummarizeBy: none
\t\tsourceColumn: financial_statement_class

\t\tannotation SummarizationSetBy = Automatic

\tpartition dim_balance_accounts = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t  Origen = Csv.Document(File.Contents("C:\\Users\\Ary Palacios\\Desktop\\corporate-fpa-project\\Data\\exports\\dim_balance_accounts.csv"), [Delimiter = ",", Columns = 4, QuoteStyle = QuoteStyle.None]),
\t\t\t\t  #"Encabezados promovidos" = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
\t\t\t\t  #"Tipo de columna cambiado" = Table.TransformColumnTypes(#"Encabezados promovidos", {{"account_id", Int64.Type}, {"account_name", type text}, {"balance_category", type text}, {"financial_statement_class", type text}}, "es")
\t\t\t\tin
\t\t\t\t  #"Tipo de columna cambiado"

\tannotation PBI_ResultType = Table
"""
    content_ba = content_ba.replace("__T_BA__", str(uuid.uuid4()))
    content_ba = content_ba.replace("__C_ACC__", str(uuid.uuid4()))
    content_ba = content_ba.replace("__C_NAME__", str(uuid.uuid4()))
    content_ba = content_ba.replace("__C_CAT__", str(uuid.uuid4()))
    content_ba = content_ba.replace("__C_CLASS__", str(uuid.uuid4()))
    
    with open(os.path.join(tables_dir, 'dim_balance_accounts.tmdl'), 'w', encoding='utf-8') as f:
        f.write(content_ba)
    print("Created dim_balance_accounts.tmdl")

    # -------------------------------------------------------------
    # 2. fct_balance_sheet_monthly.tmdl
    # -------------------------------------------------------------
    content_bs = """table fct_balance_sheet_monthly
\tlineageTag: __T_BS__

\tcolumn month_date
\t\tdataType: dateTime
\t\tformatString: Long Date
\t\tlineageTag: __C_MDATE__
\t\tsummarizeBy: none
\t\tsourceColumn: month_date

\t\tannotation SummarizationSetBy = Automatic

\t\tannotation UnderlyingDateTimeDataType = Date

\tcolumn entity_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: __C_ENT__
\t\tsummarizeBy: none
\t\tsourceColumn: entity_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn account_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: __C_BS_ACC__
\t\tsummarizeBy: none
\t\tsourceColumn: account_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn ending_balance
\t\tdataType: double
\t\tformatString: \\$#,0.00;(\\$#,0.00);\\$0.00
\t\tlineageTag: __C_BAL__
\t\tsummarizeBy: sum
\t\tsourceColumn: ending_balance

\t\tannotation SummarizationSetBy = Automatic

\tpartition fct_balance_sheet_monthly = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t  Origen = Csv.Document(File.Contents("C:\\Users\\Ary Palacios\\Desktop\\corporate-fpa-project\\Data\\exports\\fct_balance_sheet_monthly.csv"), [Delimiter = ",", Columns = 4, QuoteStyle = QuoteStyle.None]),
\t\t\t\t  #"Encabezados promovidos" = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
\t\t\t\t  #"Tipo de columna cambiado" = Table.TransformColumnTypes(#"Encabezados promovidos", {{"month_date", type date}, {"entity_id", Int64.Type}, {"account_id", Int64.Type}, {"ending_balance", type number}}, "en-US")
\t\t\t\tin
\t\t\t\t  #"Tipo de columna cambiado"

\tannotation PBI_ResultType = Table
"""
    content_bs = content_bs.replace("__T_BS__", str(uuid.uuid4()))
    content_bs = content_bs.replace("__C_MDATE__", str(uuid.uuid4()))
    content_bs = content_bs.replace("__C_ENT__", str(uuid.uuid4()))
    content_bs = content_bs.replace("__C_BS_ACC__", str(uuid.uuid4()))
    content_bs = content_bs.replace("__C_BAL__", str(uuid.uuid4()))
    
    with open(os.path.join(tables_dir, 'fct_balance_sheet_monthly.tmdl'), 'w', encoding='utf-8') as f:
        f.write(content_bs)
    print("Created fct_balance_sheet_monthly.tmdl")

    # -------------------------------------------------------------
    # 3. fct_sales_subledger.tmdl
    # -------------------------------------------------------------
    content_sl = """table fct_sales_subledger
\tlineageTag: __T_SL__

\tcolumn transaction_date
\t\tdataType: dateTime
\t\tformatString: Long Date
\t\tlineageTag: __C_TDATE__
\t\tsummarizeBy: none
\t\tsourceColumn: transaction_date

\t\tannotation SummarizationSetBy = Automatic

\t\tannotation UnderlyingDateTimeDataType = Date

\tcolumn entity_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: __C_SL_ENT__
\t\tsummarizeBy: none
\t\tsourceColumn: entity_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn sku_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: __C_SKU__
\t\tsummarizeBy: none
\t\tsourceColumn: sku_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn product_name
\t\tdataType: string
\t\tlineageTag: __C_PNAME__
\t\tsummarizeBy: none
\t\tsourceColumn: product_name

\t\tannotation SummarizationSetBy = Automatic

\tcolumn units_sold
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: __C_UNITS__
\t\tsummarizeBy: sum
\t\tsourceColumn: units_sold

\t\tannotation SummarizationSetBy = Automatic

\tcolumn actual_unit_price
\t\tdataType: double
\t\tformatString: \\$#,0.00;(\\$#,0.00);\\$0.00
\t\tlineageTag: __C_ACT_P__
\t\tsummarizeBy: sum
\t\tsourceColumn: actual_unit_price

\t\tannotation SummarizationSetBy = Automatic

\tcolumn budget_unit_price
\t\tdataType: double
\t\tformatString: \\$#,0.00;(\\$#,0.00);\\$0.00
\t\tlineageTag: __C_BUD_P__
\t\tsummarizeBy: sum
\t\tsourceColumn: budget_unit_price

\t\tannotation SummarizationSetBy = Automatic

\tcolumn budget_units
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: __C_B_UNITS__
\t\tsummarizeBy: sum
\t\tsourceColumn: budget_units

\t\tannotation SummarizationSetBy = Automatic

\tpartition fct_sales_subledger = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t  Origen = Csv.Document(File.Contents("C:\\Users\\Ary Palacios\\Desktop\\corporate-fpa-project\\Data\\exports\\fct_sales_subledger.csv"), [Delimiter = ",", Columns = 8, QuoteStyle = QuoteStyle.None]),
\t\t\t\t  #"Encabezados promovidos" = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
\t\t\t\t  #"Tipo de columna cambiado" = Table.TransformColumnTypes(#"Encabezados promovidos", {{"transaction_date", type date}, {"entity_id", Int64.Type}, {"sku_id", Int64.Type}, {"product_name", type text}, {"units_sold", Int64.Type}, {"actual_unit_price", type number}, {"budget_unit_price", type number}, {"budget_units", Int64.Type}}}, "en-US")
\t\t\t\tin
\t\t\t\t  #"Tipo de columna cambiado"

\tannotation PBI_ResultType = Table
"""
    content_sl = content_sl.replace("__T_SL__", str(uuid.uuid4()))
    content_sl = content_sl.replace("__C_TDATE__", str(uuid.uuid4()))
    content_sl = content_sl.replace("__C_SL_ENT__", str(uuid.uuid4()))
    content_sl = content_sl.replace("__C_SKU__", str(uuid.uuid4()))
    content_sl = content_sl.replace("__C_PNAME__", str(uuid.uuid4()))
    content_sl = content_sl.replace("__C_UNITS__", str(uuid.uuid4()))
    content_sl = content_sl.replace("__C_ACT_P__", str(uuid.uuid4()))
    content_sl = content_sl.replace("__C_BUD_P__", str(uuid.uuid4()))
    content_sl = content_sl.replace("__C_B_UNITS__", str(uuid.uuid4()))
    
    with open(os.path.join(tables_dir, 'fct_sales_subledger.tmdl'), 'w', encoding='utf-8') as f:
        f.write(content_sl)
    print("Created fct_sales_subledger.tmdl")

    # -------------------------------------------------------------
    # 4. Update relationships.tmdl
    # -------------------------------------------------------------
    rel_path = os.path.join(definition_dir, 'relationships.tmdl')
    with open(rel_path, 'r', encoding='utf-8') as f:
        rel_content = f.read()

    new_relationships = [
        ("fct_balance_sheet_monthly.account_id", "dim_balance_accounts.account_id"),
        ("fct_balance_sheet_monthly.month_date", "dim_fiscal_calendar.date"),
        ("fct_balance_sheet_monthly.entity_id", "dim_entity.entity_id"),
        ("fct_sales_subledger.transaction_date", "dim_fiscal_calendar.date"),
        ("fct_sales_subledger.entity_id", "dim_entity.entity_id"),
    ]

    rel_additions = ""
    for from_col, to_col in new_relationships:
        if from_col not in rel_content:
            rid = str(uuid.uuid4())
            rel_additions += f"\nrelationship {rid}\n\tfromColumn: {from_col}\n\ttoColumn: {to_col}\n"

    if rel_additions:
        with open(rel_path, 'a', encoding='utf-8') as f:
            f.write(rel_additions)
        print("Updated relationships.tmdl with 5 new 1:* relationships")
    else:
        print("Relationships already present in relationships.tmdl")

    # -------------------------------------------------------------
    # 5. Update model.tmdl
    # -------------------------------------------------------------
    model_path = os.path.join(definition_dir, 'model.tmdl')
    with open(model_path, 'r', encoding='utf-8') as f:
        model_lines = f.readlines()

    new_tables = ["dim_balance_accounts", "fct_balance_sheet_monthly", "fct_sales_subledger"]
    existing_text = "".join(model_lines)
    
    refs_to_add = []
    for t in new_tables:
        ref_line = f"ref table {t}\n"
        if f"ref table {t}" not in existing_text:
            refs_to_add.append(ref_line)
            
    new_model_lines = []
    for line in model_lines:
        if "annotation PBI_QueryOrder" in line:
            parts = line.split('=')[1].strip()
            items = [x.strip().strip('"') for x in parts.strip('[]').split(',')]
            for t in new_tables:
                if t not in items:
                    items.append(t)
            formatted_items = ",".join(f'"{x}"' for x in items)
            new_model_lines.append(f"annotation PBI_QueryOrder = [{formatted_items}]\n")
        else:
            new_model_lines.append(line)

    if refs_to_add:
        final_lines = []
        for line in new_model_lines:
            if "ref cultureInfo" in line:
                for r in refs_to_add:
                    final_lines.append(r)
            final_lines.append(line)
        new_model_lines = final_lines

    with open(model_path, 'w', encoding='utf-8') as f:
        f.writelines(new_model_lines)
    print("Updated model.tmdl with new table references and query order")

if __name__ == '__main__':
    create_tmdls()
