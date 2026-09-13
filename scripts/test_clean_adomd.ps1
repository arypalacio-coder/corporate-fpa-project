$ms = Get-Process msmdsrv -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $ms) { Write-Output "msmdsrv no esta en ejecucion."; exit }

$msRoot = Split-Path -Parent (Split-Path -Parent $ms.Path)
$dllFile = Get-ChildItem -Path $msRoot -Filter "Microsoft.AnalysisServices.AdomdClient.dll" -Recurse -ErrorAction SilentlyContinue | 
           Where-Object { $_.FullName -notlike "*\.ni\.*" -and $_.Name -notlike "*.ni.dll" } | 
           Select-Object -First 1

if (-not $dllFile) {
    $pbi = Get-Process PBIDesktop -ErrorAction SilentlyContinue | Select-Object -First 1
    $pbiRoot = Split-Path -Parent $pbi.Path
    $dllFile = Get-ChildItem -Path $pbiRoot -Filter "Microsoft.AnalysisServices.AdomdClient.dll" -Recurse -ErrorAction SilentlyContinue | 
               Where-Object { $_.FullName -notlike "*\.ni\.*" -and $_.Name -notlike "*.ni.dll" } | 
               Select-Object -First 1
}

Write-Output "Ruta DLL limpia: $($dllFile.FullName)"
[System.Reflection.Assembly]::LoadFrom($dllFile.FullName) | Out-Null

$port = (Get-NetTCPConnection -OwningProcess $ms.Id -State Listen | Select-Object -ExpandProperty LocalPort -First 1)

$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:$port;")
$conn.Open()

# 1. Filas cargadas en las tablas
$cmd = $conn.CreateCommand()
$cmd.CommandText = "EVALUATE ROW('Fact_Rows', COUNTROWS(fct_balance_sheet_monthly), 'Dim_Cal_Rows', COUNTROWS(dim_fiscal_calendar), 'Dim_Acc_Rows', COUNTROWS(dim_balance_accounts))"
$r = $cmd.ExecuteReader()
$dt = New-Object System.Data.DataTable
$dt.Load($r)
Write-Output "=== CONTEO DE FILAS EN MEMORIA ==="
$dt | Format-Table -AutoSize | Out-String | Write-Output

# 2. Evaluacion DAX de Net_Working_Capital en 2024
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
