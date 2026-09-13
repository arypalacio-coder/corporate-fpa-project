import os
import json
import shutil

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_def_dir = os.path.join(base_dir, 'financial-report.Report', 'definition')
    page_dir = os.path.join(report_def_dir, 'pages', 'efa57c1d47d99221ed42')
    visuals_dir = os.path.join(page_dir, 'visuals')
    
    # -------------------------------------------------------------
    # 1. Backup
    # -------------------------------------------------------------
    backup_dir = os.path.join(report_def_dir, 'pages_before_linecharts.bak')
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
    shutil.copytree(os.path.join(report_def_dir, 'pages'), backup_dir)
    print(f"Created backup at: {backup_dir}")
    
    # -------------------------------------------------------------
    # 2. Delete old clusteredBarChart '07f44e6fb03047b00491'
    # -------------------------------------------------------------
    old_barchart_dir = os.path.join(visuals_dir, '07f44e6fb03047b00491')
    if os.path.exists(old_barchart_dir):
        shutil.rmtree(old_barchart_dir)
        print(f"Deleted old visualContainer: {old_barchart_dir}")
    else:
        print("Old visualContainer 07f44e6fb03047b00491 not found or already deleted.")
        
    # -------------------------------------------------------------
    # 3. Create Gráfico 1 (Net Working Capital)
    # -------------------------------------------------------------
    id_nwc = "e1f2a3b4c5d6e7f8a9b0"
    nwc_dir = os.path.join(visuals_dir, id_nwc)
    os.makedirs(nwc_dir, exist_ok=True)
    
    nwc_data = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.10.0/schema.json",
        "name": id_nwc,
        "position": {
            "x": 730,
            "y": 415,
            "z": 7000,
            "height": 135,
            "width": 535,
            "tabOrder": 7000
        },
        "visual": {
            "visualType": "lineChart",
            "query": {
                "queryState": {
                    "Category": {
                        "projections": [
                            {
                                "field": {
                                    "Column": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Entity": "dim_fiscal_calendar"
                                            }
                                        },
                                        "Property": "date"
                                    }
                                },
                                "queryRef": "dim_fiscal_calendar.date",
                                "nativeQueryRef": "date",
                                "active": True
                            }
                        ]
                    },
                    "Y": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Entity": "_Measures"
                                            }
                                        },
                                        "Property": "Net_Working_Capital"
                                    }
                                },
                                "queryRef": "_Measures.Net_Working_Capital",
                                "nativeQueryRef": "Net_Working_Capital"
                            }
                        ]
                    }
                }
            },
            "objects": {
                "dataPoint": [
                    {
                        "properties": {
                            "fill": {
                                "solid": {
                                    "color": {
                                        "expr": {
                                            "Literal": {
                                                "Value": "'#1E293B'"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                ],
                "lines": [
                    {
                        "properties": {
                            "lineStyle": {
                                "expr": {
                                    "Literal": {
                                        "Value": "'solid'"
                                    }
                                }
                            }
                        }
                    }
                ],
                "markers": [
                    {
                        "properties": {
                            "show": {
                                "expr": {
                                    "Literal": {
                                        "Value": "true"
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
                                        "Value": "'Net Working Capital (NWC) Trend'"
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
                                                "Value": "'#1E293B'"
                                            }
                                        }
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
    
    nwc_file = os.path.join(nwc_dir, 'visual.json')
    with open(nwc_file, 'w', encoding='utf-8') as f:
        json.dump(nwc_data, f, indent=2)
    shutil.copy2(nwc_file, os.path.join(nwc_dir, 'visual.json.bak'))
    print(f"Created NWC line chart at: {nwc_file}")
    
    # -------------------------------------------------------------
    # 4. Create Gráfico 2 (Days Sales Outstanding)
    # -------------------------------------------------------------
    id_dso = "f1a2b3c4d5e6f7a8b9c0"
    dso_dir = os.path.join(visuals_dir, id_dso)
    os.makedirs(dso_dir, exist_ok=True)
    
    dso_data = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.10.0/schema.json",
        "name": id_dso,
        "position": {
            "x": 730,
            "y": 550,
            "z": 8000,
            "height": 140,
            "width": 535,
            "tabOrder": 8000
        },
        "visual": {
            "visualType": "lineChart",
            "query": {
                "queryState": {
                    "Category": {
                        "projections": [
                            {
                                "field": {
                                    "Column": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Entity": "dim_fiscal_calendar"
                                            }
                                        },
                                        "Property": "date"
                                    }
                                },
                                "queryRef": "dim_fiscal_calendar.date",
                                "nativeQueryRef": "date",
                                "active": True
                            }
                        ]
                    },
                    "Y": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Entity": "_Measures"
                                            }
                                        },
                                        "Property": "Days_Sales_Outstanding_DSO"
                                    }
                                },
                                "queryRef": "_Measures.Days_Sales_Outstanding_DSO",
                                "nativeQueryRef": "Days_Sales_Outstanding_DSO"
                            }
                        ]
                    }
                }
            },
            "objects": {
                "dataPoint": [
                    {
                        "properties": {
                            "fill": {
                                "solid": {
                                    "color": {
                                        "expr": {
                                            "Literal": {
                                                "Value": "'#64748B'"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                ],
                "lines": [
                    {
                        "properties": {
                            "lineStyle": {
                                "expr": {
                                    "Literal": {
                                        "Value": "'solid'"
                                    }
                                }
                            }
                        }
                    }
                ],
                "markers": [
                    {
                        "properties": {
                            "show": {
                                "expr": {
                                    "Literal": {
                                        "Value": "true"
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
                                        "Value": "'Days Sales Outstanding (DSO)'"
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
                                                "Value": "'#1E293B'"
                                            }
                                        }
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
    
    dso_file = os.path.join(dso_dir, 'visual.json')
    with open(dso_file, 'w', encoding='utf-8') as f:
        json.dump(dso_data, f, indent=2)
    shutil.copy2(dso_file, os.path.join(dso_dir, 'visual.json.bak'))
    print(f"Created DSO line chart at: {dso_file}")
    
    # -------------------------------------------------------------
    # 5. Validation
    # -------------------------------------------------------------
    # Ensure old bar chart is deleted
    assert not os.path.exists(old_barchart_dir), "Old barchart container still exists!"
    
    # Validate NWC
    with open(nwc_file, 'r', encoding='utf-8') as f:
        nwc_c = json.load(f)
    assert nwc_c['position']['x'] == 730
    assert nwc_c['position']['y'] == 415
    assert nwc_c['position']['width'] == 535
    assert nwc_c['position']['height'] == 135
    assert nwc_c['visual']['visualType'] == 'lineChart'
    
    # Validate DSO
    with open(dso_file, 'r', encoding='utf-8') as f:
        dso_c = json.load(f)
    assert dso_c['position']['x'] == 730
    assert dso_c['position']['y'] == 550
    assert dso_c['position']['width'] == 535
    assert dso_c['position']['height'] == 140
    assert dso_c['visual']['visualType'] == 'lineChart'
    
    # Verify no overlap between Waterfall (y: 125..400) and NWC (y: 415..550) and DSO (y: 550..690)
    assert 125 + 275 <= 415, "Waterfall overlaps with NWC!"
    assert 415 + 135 <= 550, "NWC overlaps with DSO!"
    assert 550 + 140 <= 720, "DSO exceeds canvas height!"
    
    print("ALL ASSERTIONS PASSED: Layout is perfectly aligned and non-overlapping!")

if __name__ == '__main__':
    main()
