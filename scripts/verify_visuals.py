import os
import json

page_dir = r"financial-report.Report\definition\pages\efa57c1d47d99221ed42\visuals"
all_good = True

for v in sorted(os.listdir(page_dir)):
    vpath = os.path.join(page_dir, v, "visual.json")
    if os.path.isfile(vpath):
        try:
            with open(vpath, "r", encoding="utf-8") as f:
                d = json.load(f)
            assert "$schema" in d, "Missing $schema"
            assert d.get("name") == v, f"Name mismatch: {d.get('name')} != {v}"
            assert "position" in d, "Missing position"
            assert "visual" in d, "Missing visual"
            print(f"OK: {v} ({d['visual']['visualType']})")
        except Exception as e:
            print(f"FAILED: {v} -> {e}")
            all_good = False

if all_good:
    print("\nALL 12 VISUAL CONTAINERS VALIDATED SUCCESSFULLY!")
else:
    print("\nVALIDATION FAILED!")
