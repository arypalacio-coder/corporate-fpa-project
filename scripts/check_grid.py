import os
import json

page_dir = r"financial-report.Report\definition\pages\efa57c1d47d99221ed42\visuals"
items = []

for v in os.listdir(page_dir):
    vpath = os.path.join(page_dir, v, "visual.json")
    if os.path.isfile(vpath):
        with open(vpath, "r", encoding="utf-8") as f:
            d = json.load(f)
        pos = d.get("position", {})
        vtype = d.get("visual", {}).get("visualType", "unknown")
        title = "None"
        vco = d.get("visual", {}).get("visualContainerObjects", {})
        if "title" in vco and len(vco["title"]) > 0:
            title = vco["title"][0].get("properties", {}).get("text", {}).get("expr", {}).get("Literal", {}).get("Value", "None")
        items.append((pos.get("x", 0), pos.get("y", 0), pos.get("width", 0), pos.get("height", 0), v, vtype, title))

items.sort(key=lambda item: (item[0], item[1]))
print(f"{'x':>5} {'y':>5} {'w':>5} {'h':>5} | {'Type':<15} | {'Title':<38} | ID")
print("-" * 95)
for x, y, w, h, v, vtype, title in items:
    print(f"{x:>5} {y:>5} {w:>5} {h:>5} | {vtype:<15} | {title:<38} | {v}")
