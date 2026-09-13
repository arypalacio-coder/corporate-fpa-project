path = "financial-report.SemanticModel/definition/relationships.tmdl"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

print("=== RELACIONES DECLARADAS EN EL MODELO ===")
for block in text.split("relationship "):
    if not block.strip(): continue
    lines = [l.strip() for l in block.strip().splitlines()]
    from_col = [l for l in lines if l.startswith("fromColumn:")]
    to_col = [l for l in lines if l.startswith("toColumn:")]
    is_active = [l for l in lines if l.startswith("isActive:")]
    cross_filter = [l for l in lines if l.startswith("crossFilteringBehavior:")]
    print(f"Relacion: {lines[0]}")
    if from_col: print(f"  {from_col[0]}")
    if to_col:   print(f"  {to_col[0]}")
    if is_active: print(f"  {is_active[0]}")
    else:         print("  isActive: true (por defecto)")
    if cross_filter: print(f"  {cross_filter[0]}")
    print()
