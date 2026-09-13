$pbi = Get-Process PBIDesktop -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $pbi) { Write-Output "PBIDesktop no esta en ejecucion."; exit }

# 1. Obtener la ruta del modulo AdomdClient cargado en memoria por el propio proceso
$mod = $pbi.Modules | Where-Object { $_.ModuleName -like "*AdomdClient*" } | Select-Object -First 1

if (-not $mod) {
    # Buscar en la carpeta donde reside msmdsrv
    $ms = Get-Process msmdsrv -ErrorAction SilentlyContinue | Select-Object -First 1
    $msDir = Split-Path -Parent $ms.Path
    $dllFile = Get-ChildItem -Path (Split-Path -Parent $msDir) -Filter "*AdomdClient*.dll" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    $dllPath = $dllFile.FullName
} else {
    $dllPath = $mod.FileName
}

Write-Output "Ruta DLL: $dllPath"
[System.Reflection.Assembly]::LoadFrom($dllPath) | Out-Null

$msmdsrv = Get-Process msmdsrv -ErrorAction SilentlyContinue | Select-Object -First 1
$port = (Get-NetTCPConnection -OwningProcess $msmdsrv.Id -State Listen | Select-Object -ExpandProperty LocalPort -First 1)

$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:$port;")
$conn.Open()

# 2. Conteo de filas en memoria
$cmd = $conn.CreateCommand()
$cmd.CommandText = "EVALUATE ROW('Fact_Rows', COUNTROWS(fct_balance_sheet_monthly), 'Dim_Cal_Rows', COUNTROWS(dim_fiscal_calendar), 'Dim_Acc_Rows', COUNTROWS(dim_balance_accounts))"
$r = $cmd.ExecuteReader()
$dt = New-Object System.Data.DataTable
$dt.Load($r)
Write-Output "=== CONTEO DE FILAS EN MEMORIA ==="
$dt | Format-Table -AutoSize | Out-String | Write-Output

# 3. Evaluacion de Net_Working_Capital por mes en 2024
$cmd2 = $conn.CreateCommand()
$cmd2.CommandText = @"
EVALUATE 
CALCULATETABLE(
    SUMMARIZECOLUMNS(
        dim_fiscal_calendar[year_month],
        "Ending_Sum", CALCULATE(SUM(fct_balance_sheet_monthly[ending_balance])),
        "NWC", [Net_Working_Capital]
    ),
    dim_fiscal_calendar[year] = 2024
)
"@
$r2 = $cmd2.ExecuteReader()
$dt2 = New-Object System.Data.DataTable
$dt2.Load($r2)
Write-Output "=== VALORES NWC POR MES 2024 ==="
$dt2 | Format-Table -AutoSize | Out-String | Write-Output

$conn.Close()
