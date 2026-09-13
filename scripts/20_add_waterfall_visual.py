import os
import json
import shutil

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    page_dir = os.path.join(base_dir, 'financial-report.Report', 'definition', 'pages', 'efa57c1d47d99221ed42')
    visuals_dir = os.path.join(page_dir, 'visuals')
    
    # 1. Create backup of page visuals directory
    page_bak_dir = os.path.join(base_dir, 'financial-report.Report', 'definition', 'pages_before_waterfall.bak')
    if os.path.exists(page_bak_dir):
        shutil.rmtree(page_bak_dir)
    shutil.copytree(os.path.join(base_dir, 'financial-report.Report', 'definition', 'pages'), page_bak_dir)
    print(f"Created backup at {page_bak_dir}")
    
    # 2. Define Waterfall Chart visual container
    visual_id = "d1e2f3a4b5c6d7e8f9a0"
    waterfall_dir = os.path.join(visuals_dir, visual_id)
    os.makedirs(waterfall_dir, exist_ok=True)
    
    waterfall_data = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.10.0/schema.json",
        "name": visual_id,
        "position": {
            "x": 730,
            "y": 125,
            "z": 6000,
            "height": 275,
            "width": 535,
            "tabOrder": 6000
        },
        "visual": {
            "visualType": "waterfallChart",
            "query": {
                "queryState": {
                    "Category": {
                        "projections": [
                            {
                                "field": {
                                    "Column": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Entity": "dim_variance_bridge"
                                            }
                                        },
                                        "Property": "Step_Name"
                                    }
                                },
                                "queryRef": "dim_variance_bridge.Step_Name",
                                "nativeQueryRef": "Step_Name",
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
                                        "Property": "Waterfall_Bridge_Amount"
                                    }
                                },
                                "queryRef": "_Measures.Waterfall_Bridge_Amount",
                                "nativeQueryRef": "Waterfall_Bridge_Amount"
                            }
                        ]
                    }
                }
            },
            "objects": {
                "sentimentColors": [
                    {
                        "properties": {
                            "increaseFill": {
                                "solid": {
                                    "color": {
                                        "expr": {
                                            "Literal": {
                                                "Value": "'#10B981'"
                                            }
                                        }
                                    }
                                }
                            },
                            "decreaseFill": {
                                "solid": {
                                    "color": {
                                        "expr": {
                                            "Literal": {
                                                "Value": "'#EF4444'"
                                            }
                                        }
                                    }
                                }
                            },
                            "totalFill": {
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
                "labels": [
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
                                        "Value": "'Variance Bridge: EBITDA Budget to Actual'"
                                    }
                                }
                            },
                            "fontSize": {
                                "expr": {
                                    "Literal": {
                                        "Value": "11D"
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
                ],
                "dropShadow": [
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
                ]
            },
            "drillFilterOtherVisuals": True
        }
    }
    
    visual_json_path = os.path.join(waterfall_dir, 'visual.json')
    with open(visual_json_path, 'w', encoding='utf-8') as f:
        json.dump(waterfall_data, f, indent=2)
    print(f"Created visual.json at {visual_json_path}")
    
    visual_bak_path = os.path.join(waterfall_dir, 'visual.json.bak')
    shutil.copy2(visual_json_path, visual_bak_path)
    print(f"Created visual.json.bak at {visual_bak_path}")
    
    # 3. Validation
    with open(visual_json_path, 'r', encoding='utf-8') as f:
        loaded = json.load(f)
    assert loaded['name'] == visual_id
    assert loaded['visual']['visualType'] == 'waterfallChart'
    assert loaded['position']['x'] == 730
    assert loaded['position']['y'] == 125
    assert loaded['position']['width'] == 535
    assert loaded['position']['height'] == 275
    print("SUCCESS: Waterfall visualContainer validated without errors.")

if __name__ == '__main__':
    main()
