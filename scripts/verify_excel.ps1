param([string]$WorkbookPath = "")
# Yêu cầu Windows và Microsoft Excel. Chỉ mở một phiên riêng, đọc file, không lưu.
$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($WorkbookPath)) {
    $WorkbookPath = Join-Path $repoRoot "excel/mo_hinh_dinh_phi.xlsx"
}
$WorkbookPath = (Resolve-Path -LiteralPath $WorkbookPath).Path
$assumptions = Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $repoRoot "data/assumptions.json") | ConvertFrom-Json
$scenarios = Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $repoRoot "data/scenarios.json") | ConvertFrom-Json
$mortality = @(Import-Csv -Encoding UTF8 -LiteralPath (Join-Path $repoRoot "data/mortality.csv"))
if ($mortality.Count -ne 20) { throw "Excel đang hỗ trợ bảng nguồn 20 tuổi; giữ cấu trúc hoặc mở rộng công thức." }
$stream = New-Object System.IO.MemoryStream
foreach ($name in @("assumptions.json", "mortality.csv", "scenarios.json")) {
    $bytes = [Text.Encoding]::UTF8.GetBytes($name)
    $stream.Write($bytes, 0, $bytes.Length)
    $bytes = [IO.File]::ReadAllBytes((Join-Path $repoRoot ("data/"+$name)))
    $stream.Write($bytes, 0, $bytes.Length)
}
$sha = [Security.Cryptography.SHA256]::Create()
$inputHash = ([BitConverter]::ToString($sha.ComputeHash($stream.ToArray()))).Replace("-","").ToLower()
$stream.Dispose()
$sha.Dispose()
$fields = @("year","age","qx_base","qx","inforce_boy","deaths","lapses","inforce_eoy",
 "df_boy","df_eoy","pv_exposure","commission_rate","pv_commission_factor","claims",
 "acquisition_expense","maintenance_expense","pv_claims","pv_acquisition","pv_maintenance",
 "annual_premium","premium_cashflow","commission","net_cashflow","pv_premium","pv_commission","pv_profit")
$inputMap = @{
 issue_age="B8"; term="B9"; sum_assured="B10"; initial_policies="B11"; target_margin="B13";
 lapse_rate="B14"; discount_rate="B15"; acquisition_expense="B16"; maintenance_expense="B17";
 expense_inflation="B18"; first_commission="B19"; renewal_commission="B20"
}
function Numeric($cell) {
    $text = [string]$cell.Text
    if ($text.StartsWith("#") -or $text -eq "n.a." -or $null -eq $cell.Value2) {
        throw ("Excel không có kết quả số tại "+$cell.Address()+": "+$text)
    }
    return ([double]$cell.Value2).ToString("R", [Globalization.CultureInfo]::InvariantCulture)
}
$excel = $null
$book = $null
try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $book = $excel.Workbooks.Open($WorkbookPath, 0, $true)
    $inputSheet = $book.Worksheets.Item("Giả định")
    $summary = $book.Worksheets.Item("Tổng quan")
    $build = $book.Worksheets.Item("Mô hình")
    foreach ($key in $inputMap.Keys) { $inputSheet.Range($inputMap[$key]).Value2 = [double]$assumptions.$key }
    for ($i=0; $i -lt $mortality.Count; $i++) {
        $inputSheet.Cells.Item(31+$i,1).Value2 = [double]$mortality[$i].age
        $inputSheet.Cells.Item(31+$i,2).Value2 = [double]$mortality[$i].qx
    }
    foreach ($s in $scenarios) {
        $row = 14+[int]$s.id
        $inputSheet.Cells.Item($row,6).Value2 = [string]$s.name
        $inputSheet.Cells.Item($row,7).Value2 = [double]$s.mortality_multiplier
        $inputSheet.Cells.Item($row,8).Value2 = [double]$s.lapse_multiplier
        $inputSheet.Cells.Item($row,9).Value2 = [double]$s.expense_multiplier
        $inputSheet.Cells.Item($row,10).Value2 = [double]$s.discount_shift
    }
    $inputSheet.Range("B5").Value2 = 1
    $inputSheet.Range("B21").ClearContents() | Out-Null
    $excel.CalculateFullRebuild()
    $basePremium = [double]$summary.Range("B6").Value2
    $inputSheet.Range("B21").Value2 = $basePremium
    $annual = [Collections.Generic.List[object]]::new()
    $results = [Collections.Generic.List[object]]::new()
    foreach ($s in $scenarios) {
        $inputSheet.Range("B5").Value2 = [double]$s.id
        $excel.CalculateFullRebuild()
        $result = [ordered]@{
            scenario_id=[int]$s.id; scenario_name=[string]$s.name;
            required_premium=(Numeric $summary.Range("B6"));
            annual_premium=(Numeric $summary.Range("B7"));
            pv_premium=(Numeric $summary.Range("B8"));
            pv_claims=(Numeric $summary.Range("B9"));
            pv_expenses=(Numeric $summary.Range("B10"));
            pv_commission=(Numeric $summary.Range("B11"));
            pv_profit=(Numeric $summary.Range("B12"));
            profit_margin=(Numeric $summary.Range("B13"));
            closing_inforce=(Numeric $summary.Range("B14"))
        }
        $results.Add([pscustomobject]$result)
        for($t=1; $t -le [int]$assumptions.term; $t++){
            $row = [ordered]@{scenario_id=[int]$s.id}
            for($col=1; $col -le 26; $col++){
                $row[$fields[$col-1]] = Numeric $build.Cells.Item(6+$t,$col)
            }
            $annual.Add([pscustomobject]$row)
        }
    }
    $results | Export-Csv -LiteralPath (Join-Path $repoRoot "results/excel_scenarios.csv") -NoTypeInformation -Encoding utf8
    ConvertTo-Json -InputObject @($results.ToArray()) -Depth 4 | Set-Content -LiteralPath (Join-Path $repoRoot "results/excel_capture.json") -Encoding utf8
    $annual | Export-Csv -LiteralPath (Join-Path $repoRoot "results/excel_annual.csv") -NoTypeInformation -Encoding utf8
    [ordered]@{
        input_sha256=$inputHash
        workbook_sha256=(Get-FileHash -LiteralPath $WorkbookPath -Algorithm SHA256).Hash.ToLower()
        engine="Microsoft Excel"
        excel_version=[string]$excel.Version
        fixed_premium=$basePremium
        mode="recalculated_from_current_json_csv_in_read_only_workbook"
    } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $repoRoot "results/excel_manifest.json") -Encoding utf8
    Write-Output "Excel recalculated 6 scenarios. Run: python scripts/reconcile.py"
} finally {
    if ($null -ne $book) { $book.Close($false) }
    if ($null -ne $excel) { $excel.Quit() }
    if ($null -ne $book) { [Runtime.InteropServices.Marshal]::ReleaseComObject($book) | Out-Null }
    if ($null -ne $excel) { [Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null }
}
