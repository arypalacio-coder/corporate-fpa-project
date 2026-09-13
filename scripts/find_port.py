import subprocess, re

# Buscar el proceso msmdsrv.exe asociado a Power BI Desktop
cmd = 'Get-Process msmdsrv | Select-Object Id'
res = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
pids = re.findall(r'\d+', res.stdout)

if not pids:
    print("NO_MSMDSRV: Power BI Desktop no parece estar ejecutándose con un modelo abierto.")
else:
    print(f"Instancias de Analysis Services detectadas (PID): {pids}")
    # Obtener el puerto de escucha
    net_cmd = f'Get-NetTCPConnection -OwningProcess {pids[0]} -State Listen | Select-Object -ExpandProperty LocalPort'
    port_res = subprocess.run(["powershell", "-Command", net_cmd], capture_output=True, text=True)
    ports = port_res.strip().split()
    print(f"Puertos locales detectados: {ports}")
