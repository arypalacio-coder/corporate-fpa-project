$p = (Get-Process msmdsrv -ErrorAction SilentlyContinue | Select-Object -First 1)
if (-not $p) { Write-Output "NO_PROCESS"; exit }

$port = (Get-NetTCPConnection -OwningProcess $p.Id -State Listen | Select-Object -ExpandProperty LocalPort -First 1)
Write-Output "PORT: $port"

# Localizar la DLL nativa de AdomdClient provista por Power BI Desktop
$pbiPath = (Get-Process PBIDesktop -ErrorAction SilentlyContinue | Select-Object -First 1).Path
$dir = [System.IO.Path]::GetDirectoryName($pbiPath)
$dll = Get-ChildItem -Path $dir -Filter "Microsoft.AnalysisServices.AdomdClient.dll" -Recurse | Select-Object -First 1

if (-not $dll) {
    # Buscar en rutas estandar si difiere el binario
    $dll = Get-ChildItem -Path "C:\Program Files\Microsoft Power BI Desktop" -Filter "Microsoft.AnalysisServices.AdomdClient.dll" -Recurse | Select-Object -First 1
}

Write-Output "DLL: $($dll.FullName)"
[System.Reflection.Assembly]::LoadFrom($dll.FullName) | Out-Null

$connStr = "Data Source=localhost:$port;"
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection($connStr)
$conn.Open()

# 1. Conteo de filas en memoria
$cmd = $conn.CreateCommand()
$cmd.CommandText = "EVALUATE ROW('Fact_Rows', COUNTROWS(fct_balance_sheet_monthly), 'Dim_Calendar_Rows', COUNTROWS(dim_fiscal_calendar), 'Dim_Accounts_Rows', COUNTROWS(dim_balance_accounts))"
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$ds = New-Object System.Data.DataSet
$adapter.Fill($ds) | Out-Null
Write-Output "=== 1. FILAS EN MEMORIA ==="
$ds.Tables[0] | Format-Table -AutoSize | Out-String | Write-Output

# 2. Evaluacion directa de Net_Working_Capital para 2024
$cmd2 = $conn.CreateCommand()
$cmd2.CommandText = @"
EVALUATE 
CALCULATETABLE(
    SUMMARIZECOLUMNS(
        dim_fiscal_calendar[year],
        dim_fiscal_calendar[year_month],
        "Ending_Balance_Sum", CALCULATE(SUM(fct_balance_sheet_monthly[ending_balance])),
        "NWC_Valor", [Net_Working_Capital]
    ),
    dim_fiscal_calendar[year] = 2024
)
"@
$adapter2 = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd2)
$ds2 = New-Object System.Data.DataSet
$adapter2.Fill($ds2) | Out-Null
Write-Output "=== 2. EVALUACION NWC POR MES EN 2024 ==="
$ds2.Tables[0] | Format-Table -AutoSize | Out-String | Write-Output

$conn.Close()
