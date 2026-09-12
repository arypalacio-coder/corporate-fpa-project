import os

translations = {
    "Ingresos Reales": "Net Revenue",
    "Gastos Operativos (OPEX)": "Operating Expenses (OPEX)",
    "Variación Presupuestaria ($)": "Budget Variance ($)",
    "Variación Presupuestaria (%)": "Budget Variance (%)",
    "Ejecución Presupuestaria Mensual: Real vs Presupuesto": "Monthly Budget Performance: Actual vs Budget",
    "Resumen por Categoría Contable": "Summary by Account Category",
    "Variación Presupuestaria por Departamento": "Budget Variance by Department"
}

target_dir = os.path.join("financial-report.Report", "definition", "pages")

for root, _, files in os.walk(target_dir):
    for file in files:
        if file.endswith("visual.json"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            modified = False
            for es, en in translations.items():
                if es in content:
                    content = content.replace(es, en)
                    modified = True
            if modified:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Modificado: {path}")

print("Traducción completada.")