$pbi = Get-Process PBIDesktop -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $pbi) { Write-Output "PBIDesktop no esta en ejecucion."; exit }

$pbiDir = Split-Path -Parent $pbi.Path
$adomdDll = Get-ChildItem -Path $pbiDir -Filter "Microsoft.AnalysisServices.AdomdClient.dll" -Recurse | Select-Object -First 1

if (-not $adomdDll) {
    # Busqueda exhaustiva en la carpeta contenedora
    $parentDir = Split-Path -Parent $pbiDir
    $adomdDll = Get-ChildItem -Path $parentDir -Filter "Microsoft.AnalysisServices.AdomdClient.dll" -Recurse | Select-Object -First 1
}

Write-Output "DLL detectada: $($adomdDll.FullName)"
[System.Reflection.Assembly]::LoadFrom($adomdDll.FullName) | Out-Null

$msmdsrv = Get-Process msmdsrv -ErrorAction SilentlyContinue | Select-Object -First 1
$port = (Get-NetTCPConnection -OwningProcess $msmdsrv.Id -State Listen | Select-Object -ExpandProperty LocalPort -First 1)

$connStr = "Data Source=localhost:$port;"
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection($connStr)
$conn.Open()

# 1. Conteo de filas
$cmd = $conn.CreateCommand()
$cmd.CommandText = "EVALUATE ROW('Fact_Rows', COUNTROWS(fct_balance_sheet_monthly), 'Dim_Cal_Rows', COUNTROWS(dim_fiscal_calendar), 'Dim_Acc_Rows', COUNTROWS(dim_balance_accounts))"
$reader = $cmd.ExecuteReader()
$dt = New-Object System.Data.DataTable
$dt.Load($reader)
Write-Output "=== 1. CONTEO DE FILAS EN MEMORIA ==="
$dt | Format-Table -AutoSize | Out-String | Write-Output

# 2. Evaluacion de la medida NWC
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
$reader2 = $cmd2.ExecuteReader()
$dt2 = New-Object System.Data.DataTable
$dt2.Load($reader2)
Write-Output "=== 2. VALORES NWC POR MES 2024 ==="
$dt2 | Format-Table -AutoSize | Out-String | Write-Output

$conn.Close()
