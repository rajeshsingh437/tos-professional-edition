<#
.SYNOPSIS
    AEGIS Environment Activator & Runner using uv
.DESCRIPTION
    Automatically activates the uv virtual environment (.venv) for this project.
    Optionally runs the application if -Run switch is passed.
.EXAMPLE
    .\start.ps1
    .\start.ps1 -Run
#>
param(
    [switch]$Run,
    [string]$Module = "app.main"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Check and activate .venv
if (Test-Path "$scriptDir\.venv\Scripts\Activate.ps1") {
    & "$scriptDir\.venv\Scripts\Activate.ps1"
    Write-Host "[AEGIS] uv virtual environment (.venv) activated. Python version: 3.14.7" -ForegroundColor Green
} else {
    Write-Host "[AEGIS] .venv not found. Running 'uv sync' to create it..." -ForegroundColor Yellow
    uv sync
    if (Test-Path "$scriptDir\.venv\Scripts\Activate.ps1") {
        & "$scriptDir\.venv\Scripts\Activate.ps1"
        Write-Host "[AEGIS] uv virtual environment created and activated." -ForegroundColor Green
    } else {
        Write-Error "[AEGIS] Failed to activate .venv."
        exit 1
    }
}

if ($Run) {
    Write-Host "[AEGIS] Launching $Module..." -ForegroundColor Cyan
    python -m $Module
}
