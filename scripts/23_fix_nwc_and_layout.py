import os
import json
import shutil
import copy

def run():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pages_dir = os.path.join(base_dir, 'financial-report.Report', 'definition', 'pages')
    page_name = 'efa57c1d47d99221ed42'
    page_dir = os.path.join(pages_dir, page_name)
    visuals_dir = os.path.join(page_dir, 'visuals')

    print("=" * 80)
    print("1. REPARACION DEL ENLACE DE DATOS DE NWC")
    print("=" * 80)

    dso_id = 'f1a2b3c4d5e6f7a8b9c0'
    nwc_id = 'e1f2a3b4c5d6e7f8a9b0'

    dso_file = os.path.join(visuals_dir, dso_id, 'visual.json')
    nwc_file = os.path.join(visuals_dir, nwc_id, 'visual.json')

    # Backup NWC file
    shutil.copy2(nwc_file, nwc_file + '.bak')
    print(f"Respaldo creado: {nwc_file}.bak")

    with open(dso_file, 'r', encoding='utf-8') as f:
        dso_json = json.load(f)

    with open(nwc_file, 'r', encoding='utf-8') as f:
        nwc_json = json.load(f)

    # Extract query block from DSO and clone it
    dso_query = copy.deepcopy(dso_json['visual']['query'])

    # Serialize to string and replace Days_Sales_Outstanding_DSO with Net_Working_Capital
    query_str = json.dumps(dso_query)
    query_str = query_str.replace('Days_Sales_Outstanding_DSO', 'Net_Working_Capital')
    nwc_query = json.loads(query_str)

    # Apply to NWC
    nwc_json['visual']['query'] = nwc_query
    nwc_json['visual']['visualType'] = 'lineChart'

    # Ensure title is 'Net Working Capital (NWC) Trend'
    try:
        nwc_json['visual']['visualContainerObjects']['title'][0]['properties']['text'] = {
            'expr': {'Literal': {'Value': "'Net Working Capital (NWC) Trend'"}}
        }
    except Exception as e:
        print(f"Warning setting title: {e}")

    print("Enlace de datos de NWC reparado exitosamente a partir de DSO.")

    print("\n" + "=" * 80)
    print("2. NORMALIZACION DE COORDENADAS Y DISTRIBUCION EN CANVAS (1280 x 720 px)")
    print("=" * 80)

    # Definicion de coordenadas exactas solicitadas
    layout_spec = {
        # Barra lateral de filtros (x: 15, width: 150)
        '87d58b08d606a6296250': {'name': 'Fiscal Year (Slicer)', 'x': 15, 'y': 15, 'width': 150, 'height': 75},
        '498dc5024d2b7056954b': {'name': 'Month (Slicer)', 'x': 15, 'y': 95, 'width': 150, 'height': 260},
        'b3c4d5e6f7a8b9c0d1e2': {'name': 'Legal Entity (Slicer)', 'x': 15, 'y': 365, 'width': 150, 'height': 160},
        'c4d5e6f7a8b9c0d1e2f3': {'name': 'Currency (Slicer)', 'x': 15, 'y': 535, 'width': 150, 'height': 155},

        # Banda Superior de KPIs (y: 15, height: 95)
        '20fcda46b974d9788c63': {'name': 'Net Revenue (KPI)', 'x': 180, 'y': 15, 'width': 260, 'height': 95},
        '8b1acb8f7e534cbec6bb': {'name': 'Gross Margin (%) (KPI)', 'x': 455, 'y': 15, 'width': 260, 'height': 95},
        'a0f69fb2e8c09e5a2d66': {'name': 'EBITDA Margin (%) (KPI)', 'x': 730, 'y': 15, 'width': 260, 'height': 95},
        'c0f28e700405676dc12e': {'name': 'Operating Free Cash Flow (KPI)', 'x': 1005, 'y': 15, 'width': 260, 'height': 95},

        # Mitad Izquierda
        '48b6570e4d31ad0ed09a': {'name': 'Summary by Account Category (Matrix)', 'x': 180, 'y': 125, 'width': 535, 'height': 565},

        # Mitad Derecha
        'd1e2f3a4b5c6d7e8f9a0': {'name': 'Waterfall Bridge (Waterfall)', 'x': 730, 'y': 125, 'width': 535, 'height': 275},
        'e1f2a3b4c5d6e7f8a9b0': {'name': 'NWC Trend (LineChart)', 'x': 730, 'y': 415, 'width': 535, 'height': 135},
        'f1a2b3c4d5e6f7a8b9c0': {'name': 'DSO Trend (LineChart)', 'x': 730, 'y': 555, 'width': 535, 'height': 135},
    }

    # Also update page.json canvas size to 1280x720
    page_json_file = os.path.join(page_dir, 'page.json')
    if os.path.isfile(page_json_file):
        shutil.copy2(page_json_file, page_json_file + '.bak')
        with open(page_json_file, 'r', encoding='utf-8') as f:
            pdata = json.load(f)
        pdata['width'] = 1280
        pdata['height'] = 720
        with open(page_json_file, 'w', encoding='utf-8') as f:
            json.dump(pdata, f, indent=2)
        print(f"Canvas page.json normalizado a 1280 x 720 px (Respaldo: {page_json_file}.bak)")

    modified_files = []

    print(f"\n{'Visual ID':<22} | {'Nombre':<35} | {'X':>5} | {'Y':>5} | {'Ancho':>5} | {'Alto':>5}")
    print("-" * 88)

    for vid, spec in layout_spec.items():
        v_file = os.path.join(visuals_dir, vid, 'visual.json')
        if not os.path.isfile(v_file):
            print(f"ERROR: Archivo no encontrado: {v_file}")
            continue

        # Load file (if it's nwc_json, use the already modified object)
        if vid == nwc_id:
            v_json = nwc_json
        else:
            with open(v_file, 'r', encoding='utf-8') as f:
                v_json = json.load(f)

        # Create backup if not already done
        bak_file = v_file + '.bak'
        if not os.path.exists(bak_file) and vid != nwc_id:
            shutil.copy2(v_file, bak_file)

        # Update position
        if 'position' not in v_json:
            v_json['position'] = {}
        v_json['position']['x'] = spec['x']
        v_json['position']['y'] = spec['y']
        v_json['position']['width'] = spec['width']
        v_json['position']['height'] = spec['height']

        # Save file
        with open(v_file, 'w', encoding='utf-8') as f:
            json.dump(v_json, f, indent=2)

        modified_files.append((vid, v_file, spec))
        print(f"{vid:<22} | {spec['name']:<35} | {spec['x']:>5} | {spec['y']:>5} | {spec['width']:>5} | {spec['height']:>5}")

    print("\n" + "=" * 80)
    print("3. VALIDACION DE SINTAXIS JSON Y CONFIRMACION")
    print("=" * 80)

    all_valid = True
    for vid, v_file, spec in modified_files:
        try:
            with open(v_file, 'r', encoding='utf-8') as f:
                parsed = json.load(f)
            # Verify position matches
            p = parsed['position']
            assert p['x'] == spec['x'] and p['y'] == spec['y'] and p['width'] == spec['width'] and p['height'] == spec['height']
            print(f"OK [Sintaxis JSON Valida]: {vid} ({spec['name']})")
        except Exception as e:
            print(f"FAIL: {vid} - {e}")
            all_valid = False

    # Check NWC specific validation
    with open(nwc_file, 'r', encoding='utf-8') as f:
        nwc_val = json.load(f)
    assert nwc_val['visual']['visualType'] == 'lineChart', "NWC visualType no es lineChart"
    query_dump = json.dumps(nwc_val['visual']['query'])
    assert 'Net_Working_Capital' in query_dump, "NWC no contiene Net_Working_Capital"
    assert 'Days_Sales_Outstanding_DSO' not in query_dump, "NWC aun contiene Days_Sales_Outstanding_DSO"
    print("OK [NWC Data Binding]: visualType 'lineChart' y medida 'Net_Working_Capital' verificados correctamente.")

    if all_valid:
        print("\nTODOS LOS ARCHIVOS VISUAL.JSON FUERON CORREGIDOS Y VALIDADOS CON EXITO.")

if __name__ == '__main__':
    run()
