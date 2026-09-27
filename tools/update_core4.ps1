param(
    [Parameter(Mandatory=$true)]
    [ValidateSet(
        "Architecture",
        "Engineering",
        "Component",
        "NextAction"
    )]
    [string]$Section,

    [Parameter(Mandatory=$true)]
    [string]$Content
)

$root = Split-Path -Parent $PSScriptRoot
$core = Join-Path $root "docs\core\AEGIS_CORE-4.md"

if (-not (Test-Path $core)) {
    throw "AEGIS Core-4 not found: $core"
}

$text = Get-Content $core -Raw

$headers = @{
    Architecture = "# 01 — ARCHITECTURE STATE"
    Engineering  = "# 02 — ENGINEERING STATE"
    Component    = "# 03 — VERIFIED COMPONENT STATE"
    NextAction   = "# 04 — NEXT ACTION / BLOCKERS"
}

$currentHeader = $headers[$Section]
$headerList = $headers.Values

$escapedCurrent = [regex]::Escape($currentHeader)

$nextHeaders = $headerList |
    Where-Object { $_ -ne $currentHeader } |
    ForEach-Object { [regex]::Escape($_) }

$nextPattern = ($nextHeaders -join "|")

if ($nextPattern) {
    $pattern = "(?s)$escapedCurrent.*?(?=$nextPattern|\z)"
} else {
    $pattern = "(?s)$escapedCurrent.*?\z"
}

$newSection = @"
$currentHeader

$Content

"@

if (-not [regex]::IsMatch($text, $pattern)) {
    throw "Could not locate Core-4 section: $Section"
}

$updated = [regex]::Replace(
    $text,
    $pattern,
    [System.Text.RegularExpressions.MatchEvaluator]{
        param($m)
        $newSection
    },
    1
)

Set-Content $core $updated -Encoding UTF8

Write-Host ""
Write-Host "CORE-4 UPDATED" -ForegroundColor Green
Write-Host "Section : $Section"
Write-Host "File    : $core"
Write-Host ""
