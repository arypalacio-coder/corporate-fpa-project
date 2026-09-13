import subprocess, re, urllib.request, xml.etree.ElementTree as ET

# Obtener PID y puerto de msmdsrv
ps_cmd = '$p = (Get-Process msmdsrv | Select-Object -First 1).Id; Get-NetTCPConnection -OwningProcess $p -State Listen | Select-Object -ExpandProperty LocalPort -First 1'
res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
port = res.stdout.strip()
print(f"Puerto detectado: {port}")

def run_dax(query):
    xml_payload = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
      <Body>
        <Execute xmlns="urn:schemas-microsoft-com:xml-analysis">
          <Command>
            <Statement><![CDATA[{query}]]></Statement>
          </Command>
          <Properties>
            <PropertyList>
              <Format>Tabular</Format>
            </PropertyList>
          </Properties>
        </Execute>
      </Body>
    </Envelope>"""
    
    req = urllib.request.Request(f"http://localhost:{port}/xmla", data=xml_payload.encode('utf-8'), headers={'Content-Type': 'text/xml'})
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return str(e)

# 1. Contar filas cargadas en memoria
q1 = "EVALUATE ROW('Fact_Rows', COUNTROWS(fct_balance_sheet_monthly), 'Dim_Cal_Rows', COUNTROWS(dim_fiscal_calendar), 'Dim_Acc_Rows', COUNTROWS(dim_balance_accounts))"
r1 = run_dax(q1)

print("\n=== 1. FILAS EN MEMORIA ===")
rows = re.findall(r'<row>(.*?)</row>', r1)
for r in rows:
    clean = re.sub(r'<.*?>', ' ', r)
    print(" ".join(clean.split()))

# 2. Evaluar NWC y suma de ending_balance por mes en 2024
q2 = 'EVALUATE CALCULATETABLE(SUMMARIZECOLUMNS(dim_fiscal_calendar[year_month], "Suma_Ending", CALCULATE(SUM(fct_balance_sheet_monthly[ending_balance])), "NWC", [Net_Working_Capital]), dim_fiscal_calendar[year] = 2024)'
r2 = run_dax(q2)

print("\n=== 2. EVALUACION NWC 2024 ===")
rows2 = re.findall(r'<row>(.*?)</row>', r2)
if not rows2:
    print("Sin filas retornadas o error XMLA:")
    print(r2[:500])
else:
    for r in rows2:
        clean = re.sub(r'<.*?>', ' | ', r)
        print(" | ".join([c.strip() for c in clean.split('|') if c.strip()]))
