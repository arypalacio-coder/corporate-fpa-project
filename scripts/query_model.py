import subprocess

ps_script = """
$p = (Get-Process msmdsrv | Select-Object -First 1).Id
$port = (Get-NetTCPConnection -OwningProcess $p -State Listen | Select-Object -ExpandProperty LocalPort -First 1)
Write-Output "PORT:$port"

$connStr = "Provider=MSOLAP;Data Source=localhost:$port;Initial Catalog='';"
$conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
$conn.Open()

# 1. Contar filas cargadas en memoria
$cmd1 = $conn.CreateCommand()
$cmd1.CommandText = "EVALUATE ROW('Filas_Fact', COUNTROWS(fct_balance_sheet_monthly), 'Filas_Calendario', COUNTROWS(dim_fiscal_calendar))"
$adapter1 = New-Object System.Data.OleDb.OleDbDataAdapter($cmd1)
$ds1 = New-Object System.Data.DataSet
$adapter1.Fill($ds1) | Out-Null
$ds1.Tables[0] | Format-Table -AutoSize | Out-String | Write-Output

# 2. Evaluar NWC agrupado por anio y mes
$cmd2 = $conn.CreateCommand()
$cmd2.CommandText = "EVALUATE SUMMARIZECOLUMNS(dim_fiscal_calendar[year], dim_fiscal_calendar[year_month], 'NWC', [Net_Working_Capital])"
$adapter2 = New-Object System.Data.OleDb.OleDbDataAdapter($cmd2)
$ds2 = New-Object System.Data.DataSet
$adapter2.Fill($ds2) | Out-Null
$ds2.Tables[0] | Format-Table -AutoSize | Out-String | Write-Output

$conn.Close()
"""

res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("STDERR:\n" + res.stderr)
