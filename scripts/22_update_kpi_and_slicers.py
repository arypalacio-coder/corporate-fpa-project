import os
import json
import shutil

BASE_DIR = r"c:\Users\Ary Palacios\Desktop\corporate-fpa-project"
PAGE_DIR = os.path.join(BASE_DIR, r"financial-report.Report\definition\pages\efa57c1d47d99221ed42")
VISUALS_DIR = os.path.join(PAGE_DIR, "visuals")

# 1. Update 4th KPI Card (c0f28e700405676dc12e)
card4_dir = os.path.join(VISUALS_DIR, "c0f28e700405676dc12e")
card4_file = os.path.join(card4_dir, "visual.json")
shutil.copy2(card4_file, card4_file + ".bak")

with open(card4_file, "r", encoding="utf-8") as f:
    card4 = json.load(f)

# Update data binding to Free_Operating_Cash_Flow
card4["visual"]["query"]["queryState"]["Data"]["projections"] = [
    {
        "field": {
            "Measure": {
                "Expression": {
                    "SourceRef": {
                        "Entity": "_Measures"
                    }
                },
                "Property": "Free_Operating_Cash_Flow"
            }
        },
        "queryRef": "_Measures.Free_Operating_Cash_Flow",
        "nativeQueryRef": "Free_Operating_Cash_Flow"
    }
]

card4["visual"]["query"]["sortDefinition"] = {
    "sort": [
        {
            "field": {
                "Measure": {
                    "Expression": {
                        "SourceRef": {
                            "Entity": "_Measures"
                        }
                    },
                    "Property": "Free_Operating_Cash_Flow"
                }
            },
            "direction": "Descending"
        }
    ],
    "isDefaultSort": True
}

# Update title: "OPERATING FREE CASH FLOW", 10pt uppercase, Segoe UI, #64748B
# Background #FFFFFF, border #E2E8F0
card4["visual"]["visualContainerObjects"] = {
    "title": [
        {
            "properties": {
                "text": {
                    "expr": {
                        "Literal": {
                            "Value": "'OPERATING FREE CASH FLOW'"
                        }
                    }
                },
                "fontSize": {
                    "expr": {
                        "Literal": {
                            "Value": "10D"
                        }
                    }
                },
                "fontFamily": {
                    "expr": {
                        "Literal": {
                            "Value": "'Segoe UI'"
                        }
                    }
                },
                "bold": {
                    "expr": {
                        "Literal": {
                            "Value": "true"
                        }
                    }
                },
                "fontColor": {
                    "solid": {
                        "color": {
                            "expr": {
                                "Literal": {
                                    "Value": "'#64748B'"
                                }
                            }
                        }
                    }
                },
                "show": {
                    "expr": {
                        "Literal": {
                            "Value": "true"
                        }
                    }
                }
            }
        }
    ],
    "subTitle": [
        {
            "properties": {
                "show": {
                    "expr": {
                        "Literal": {
                            "Value": "false"
                        }
                    }
                }
            }
        }
    ],
    "background": [
        {
            "properties": {
                "show": {
                    "expr": {
                        "Literal": {
                            "Value": "true"
                        }
                    }
                },
                "color": {
                    "solid": {
                        "color": {
                            "expr": {
                                "Literal": {
                                    "Value": "'#FFFFFF'"
                                }
                            }
                        }
                    }
                },
                "transparency": {
                    "expr": {
                        "Literal": {
                            "Value": "0D"
                        }
                    }
                }
            }
        }
    ],
    "border": [
        {
            "properties": {
                "show": {
                    "expr": {
                        "Literal": {
                            "Value": "true"
                        }
                    }
                },
                "color": {
                    "solid": {
                        "color": {
                            "expr": {
                                "Literal": {
                                    "Value": "'#E2E8F0'"
                                }
                            }
                        }
                    }
                },
                "radius": {
                    "expr": {
                        "Literal": {
                            "Value": "4D"
                        }
                    }
                }
            }
        }
    ]
}

with open(card4_file, "w", encoding="utf-8") as f:
    json.dump(card4, f, indent=2, ensure_ascii=False)
print("Updated Card 4 (Free_Operating_Cash_Flow)")

# 2. Update Slicer 1 - Year (87d58b08d606a6296250)
slicer1_dir = os.path.join(VISUALS_DIR, "87d58b08d606a6296250")
slicer1_file = os.path.join(slicer1_dir, "visual.json")
shutil.copy2(slicer1_file, slicer1_file + ".bak")

with open(slicer1_file, "r", encoding="utf-8") as f:
    slicer1 = json.load(f)

slicer1["position"] = {
    "x": 15,
    "y": 15,
    "z": 0,
    "height": 75,
    "width": 150,
    "tabOrder": 0
}

slicer1["visual"]["visualContainerObjects"] = {
    "title": [
        {
            "properties": {
                "text": {
                    "expr": {
                        "Literal": {
                            "Value": "'Fiscal Year'"
                        }
                    }
                },
                "fontSize": {
                    "expr": {
                        "Literal": {
                            "Value": "9D"
                        }
                    }
                },
                "fontFamily": {
                    "expr": {
                        "Literal": {
                            "Value": "'Segoe UI'"
                        }
                    }
                },
                "bold": {
                    "expr": {
                        "Literal": {
                            "Value": "true"
                        }
                    }
                },
                "fontColor": {
                    "solid": {
                        "color": {
                            "expr": {
                                "Literal": {
                                    "Value": "'#1E293B'"
                                }
                            }
                        }
                    }
                },
                "show": {
                    "expr": {
                        "Literal": {
                            "Value": "true"
                        }
                    }
                }
            }
        }
    ],
    "background": [
        {
            "properties": {
                "show": {
                    "expr": {
                        "Literal": {
                            "Value": "true"
                        }
                    }
                },
                "color": {
                    "solid": {
                        "color": {
                            "expr": {
                                "Literal": {
                                    "Value": "'#FFFFFF'"
                                }
                            }
                        }
                    }
                },
                "transparency": {
                    "expr": {
                        "Literal": {
                            "Value": "0D"
                        }
                    }
                }
            }
        }
    ],
    "border": [
        {
            "properties": {
                "show": {
                    "expr": {
                        "Literal": {
                            "Value": "true"
                        }
                    }
                },
                "color": {
                    "solid": {
                        "color": {
                            "expr": {
                                "Literal": {
                                    "Value": "'#E2E8F0'"
                                }
                            }
                        }
                    }
                },
                "radius": {
                    "expr": {
                        "Literal": {
                            "Value": "4D"
                        }
                    }
                }
            }
        }
    ]
}

if "objects" in slicer1["visual"]:
    slicer1["visual"]["objects"]["items"] = [
        {
            "properties": {
                "textSize": {
                    "expr": {
                        "Literal": {
                            "Value": "9D"
                        }
                    }
                }
            }
        }
    ]

with open(slicer1_file, "w", encoding="utf-8") as f:
    json.dump(slicer1, f, indent=2, ensure_ascii=False)
print("Updated Slicer 1 (Year) position to x:15, y:15, w:150, h:75")

# 3. Update Slicer 2 - Month (498dc5024d2b7056954b)
slicer2_dir = os.path.join(VISUALS_DIR, "498dc5024d2b7056954b")
slicer2_file = os.path.join(slicer2_dir, "visual.json")
shutil.copy2(slicer2_file, slicer2_file + ".bak")

with open(slicer2_file, "r", encoding="utf-8") as f:
    slicer2 = json.load(f)

slicer2["position"] = {
    "x": 15,
    "y": 95,
    "z": 1000,
    "height": 260,
    "width": 150,
    "tabOrder": 1000
}

slicer2["visual"]["visualContainerObjects"] = {
    "title": [
        {
            "properties": {
                "text": {
                    "expr": {
                        "Literal": {
                            "Value": "'Month'"
                        }
                    }
                },
                "fontSize": {
                    "expr": {
                        "Literal": {
                            "Value": "9D"
                        }
                    }
                },
                "fontFamily": {
                    "expr": {
                        "Literal": {
                            "Value": "'Segoe UI'"
                        }
                    }
                },
                "bold": {
                    "expr": {
                        "Literal": {
                            "Value": "true"
                        }
                    }
                },
                "fontColor": {
                    "solid": {
                        "color": {
                            "expr": {
                                "Literal": {
                                    "Value": "'#1E293B'"
                                }
                            }
                        }
                    }
                },
                "show": {
                    "expr": {
                        "Literal": {
                            "Value": "true"
                        }
                    }
                }
            }
        }
    ],
    "subTitle": [
        {
            "properties": {
                "show": {
                    "expr": {
                        "Literal": {
                            "Value": "false"
                        }
                    }
                }
            }
        }
    ],
    "background": [
        {
            "properties": {
                "show": {
                    "expr": {
                        "Literal": {
                            "Value": "true"
                        }
                    }
                },
                "color": {
                    "solid": {
                        "color": {
                            "expr": {
                                "Literal": {
                                    "Value": "'#FFFFFF'"
                                }
                            }
                        }
                    }
                },
                "transparency": {
                    "expr": {
                        "Literal": {
                            "Value": "0D"
                        }
                    }
                }
            }
        }
    ],
    "border": [
        {
            "properties": {
                "show": {
                    "expr": {
                        "Literal": {
                            "Value": "true"
                        }
                    }
                },
                "color": {
                    "solid": {
                        "color": {
                            "expr": {
                                "Literal": {
                                    "Value": "'#E2E8F0'"
                                }
                            }
                        }
                    }
                },
                "radius": {
                    "expr": {
                        "Literal": {
                            "Value": "4D"
                        }
                    }
                }
            }
        }
    ]
}

if "objects" in slicer2["visual"]:
    slicer2["visual"]["objects"]["items"] = [
        {
            "properties": {
                "textSize": {
                    "expr": {
                        "Literal": {
                            "Value": "9D"
                        }
                    }
                }
            }
        }
    ]

with open(slicer2_file, "w", encoding="utf-8") as f:
    json.dump(slicer2, f, indent=2, ensure_ascii=False)
print("Updated Slicer 2 (Month) position to x:15, y:95, w:150, h:260")

# 4. Create Slicer 3 - Legal Entity (b3c4d5e6f7a8b9c0d1e2)
slicer3_id = "b3c4d5e6f7a8b9c0d1e2"
slicer3_dir = os.path.join(VISUALS_DIR, slicer3_id)
os.makedirs(slicer3_dir, exist_ok=True)
slicer3_file = os.path.join(slicer3_dir, "visual.json")

slicer3 = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.10.0/schema.json",
    "name": slicer3_id,
    "position": {
        "x": 15,
        "y": 365,
        "z": 1100,
        "height": 160,
        "width": 150,
        "tabOrder": 1100
    },
    "visual": {
        "visualType": "slicer",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {
                            "field": {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Entity": "dim_entity"
                                        }
                                    },
                                    "Property": "entity_name"
                                }
                            },
                            "queryRef": "dim_entity.entity_name",
                            "nativeQueryRef": "entity_name",
                            "active": True
                        }
                    ]
                }
            }
        },
        "objects": {
            "data": [
                {
                    "properties": {
                        "mode": {
                            "expr": {
                                "Literal": {
                                    "Value": "'Basic'"
                                }
                            }
                        }
                    }
                }
            ],
            "selection": [
                {
                    "properties": {
                        "singleSelect": {
                            "expr": {
                                "Literal": {
                                    "Value": "false"
                                }
                            }
                        },
                        "selectAllCheckboxEnabled": {
                            "expr": {
                                "Literal": {
                                    "Value": "true"
                                }
                            }
                        }
                    }
                }
            ],
            "header": [
                {
                    "properties": {
                        "showRestatement": {
                            "expr": {
                                "Literal": {
                                    "Value": "false"
                                }
                            }
                        },
                        "show": {
                            "expr": {
                                "Literal": {
                                    "Value": "false"
                                }
                            }
                        }
                    }
                }
            ],
            "items": [
                {
                    "properties": {
                        "textSize": {
                            "expr": {
                                "Literal": {
                                    "Value": "9D"
                                }
                            }
                        }
                    }
                }
            ]
        },
        "visualContainerObjects": {
            "title": [
                {
                    "properties": {
                        "text": {
                            "expr": {
                                "Literal": {
                                    "Value": "'Legal Entity'"
                                }
                            }
                        },
                        "fontSize": {
                            "expr": {
                                "Literal": {
                                    "Value": "9D"
                                }
                            }
                        },
                        "fontFamily": {
                            "expr": {
                                "Literal": {
                                    "Value": "'Segoe UI'"
                                }
                            }
                        },
                        "bold": {
                            "expr": {
                                "Literal": {
                                    "Value": "true"
                                }
                            }
                        },
                        "fontColor": {
                            "solid": {
                                "color": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "'#1E293B'"
                                        }
                                    }
                                }
                            }
                        },
                        "show": {
                            "expr": {
                                "Literal": {
                                    "Value": "true"
                                }
                            }
                        }
                    }
                }
            ],
            "subTitle": [
                {
                    "properties": {
                        "show": {
                            "expr": {
                                "Literal": {
                                    "Value": "false"
                                }
                            }
                        }
                    }
                }
            ],
            "background": [
                {
                    "properties": {
                        "show": {
                            "expr": {
                                "Literal": {
                                    "Value": "true"
                                }
                            }
                        },
                        "color": {
                            "solid": {
                                "color": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "'#FFFFFF'"
                                        }
                                    }
                                }
                            }
                        },
                        "transparency": {
                            "expr": {
                                "Literal": {
                                    "Value": "0D"
                                }
                            }
                        }
                    }
                }
            ],
            "border": [
                {
                    "properties": {
                        "show": {
                            "expr": {
                                "Literal": {
                                    "Value": "true"
                                }
                            }
                        },
                        "color": {
                            "solid": {
                                "color": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "'#E2E8F0'"
                                        }
                                    }
                                }
                            }
                        },
                        "radius": {
                            "expr": {
                                "Literal": {
                                    "Value": "4D"
                                }
                            }
                        }
                    }
                }
            ]
        },
        "drillFilterOtherVisuals": True
    }
}

with open(slicer3_file, "w", encoding="utf-8") as f:
    json.dump(slicer3, f, indent=2, ensure_ascii=False)
shutil.copy2(slicer3_file, slicer3_file + ".bak")
print(f"Created Slicer 3 (Legal Entity) at {slicer3_file}")

# 5. Create Slicer 4 - Currency (c4d5e6f7a8b9c0d1e2f3)
slicer4_id = "c4d5e6f7a8b9c0d1e2f3"
slicer4_dir = os.path.join(VISUALS_DIR, slicer4_id)
os.makedirs(slicer4_dir, exist_ok=True)
slicer4_file = os.path.join(slicer4_dir, "visual.json")

slicer4 = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.10.0/schema.json",
    "name": slicer4_id,
    "position": {
        "x": 15,
        "y": 535,
        "z": 1200,
        "height": 155,
        "width": 150,
        "tabOrder": 1200
    },
    "visual": {
        "visualType": "slicer",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {
                            "field": {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Entity": "dim_entity"
                                        }
                                    },
                                    "Property": "functional_currency"
                                }
                            },
                            "queryRef": "dim_entity.functional_currency",
                            "nativeQueryRef": "functional_currency",
                            "active": True
                        }
                    ]
                }
            }
        },
        "objects": {
            "data": [
                {
                    "properties": {
                        "mode": {
                            "expr": {
                                "Literal": {
                                    "Value": "'Basic'"
                                }
                            }
                        }
                    }
                }
            ],
            "selection": [
                {
                    "properties": {
                        "singleSelect": {
                            "expr": {
                                "Literal": {
                                    "Value": "false"
                                }
                            }
                        },
                        "selectAllCheckboxEnabled": {
                            "expr": {
                                "Literal": {
                                    "Value": "true"
                                }
                            }
                        }
                    }
                }
            ],
            "header": [
                {
                    "properties": {
                        "showRestatement": {
                            "expr": {
                                "Literal": {
                                    "Value": "false"
                                }
                            }
                        },
                        "show": {
                            "expr": {
                                "Literal": {
                                    "Value": "false"
                                }
                            }
                        }
                    }
                }
            ],
            "items": [
                {
                    "properties": {
                        "textSize": {
                            "expr": {
                                "Literal": {
                                    "Value": "9D"
                                }
                            }
                        }
                    }
                }
            ]
        },
        "visualContainerObjects": {
            "title": [
                {
                    "properties": {
                        "text": {
                            "expr": {
                                "Literal": {
                                    "Value": "'Currency'"
                                }
                            }
                        },
                        "fontSize": {
                            "expr": {
                                "Literal": {
                                    "Value": "9D"
                                }
                            }
                        },
                        "fontFamily": {
                            "expr": {
                                "Literal": {
                                    "Value": "'Segoe UI'"
                                }
                            }
                        },
                        "bold": {
                            "expr": {
                                "Literal": {
                                    "Value": "true"
                                }
                            }
                        },
                        "fontColor": {
                            "solid": {
                                "color": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "'#1E293B'"
                                        }
                                    }
                                }
                            }
                        },
                        "show": {
                            "expr": {
                                "Literal": {
                                    "Value": "true"
                                }
                            }
                        }
                    }
                }
            ],
            "subTitle": [
                {
                    "properties": {
                        "show": {
                            "expr": {
                                "Literal": {
                                    "Value": "false"
                                }
                            }
                        }
                    }
                }
            ],
            "background": [
                {
                    "properties": {
                        "show": {
                            "expr": {
                                "Literal": {
                                    "Value": "true"
                                }
                            }
                        },
                        "color": {
                            "solid": {
                                "color": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "'#FFFFFF'"
                                        }
                                    }
                                }
                            }
                        },
                        "transparency": {
                            "expr": {
                                "Literal": {
                                    "Value": "0D"
                                }
                            }
                        }
                    }
                }
            ],
            "border": [
                {
                    "properties": {
                        "show": {
                            "expr": {
                                "Literal": {
                                    "Value": "true"
                                }
                            }
                        },
                        "color": {
                            "solid": {
                                "color": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "'#E2E8F0'"
                                        }
                                    }
                                }
                            }
                        },
                        "radius": {
                            "expr": {
                                "Literal": {
                                    "Value": "4D"
                                }
                            }
                        }
                    }
                }
            ]
        },
        "drillFilterOtherVisuals": True
    }
}

with open(slicer4_file, "w", encoding="utf-8") as f:
    json.dump(slicer4, f, indent=2, ensure_ascii=False)
shutil.copy2(slicer4_file, slicer4_file + ".bak")
print(f"Created Slicer 4 (Currency) at {slicer4_file}")
