# IFT3295 - TP1 - Creation du venv et installation des dependances (Windows).
#
# Usage (PowerShell) :
#   .\setup.ps1        -> cree le venv (.venv) et installe les dependances
#   . .\setup.ps1      -> en plus, active le venv dans votre session
#
# Si PowerShell bloque l'execution de scripts :
#   powershell -ExecutionPolicy Bypass -File .\setup.ps1
#
# Apres l'execution, activez le venv avant de rouler le TP :
#   .\.venv\Scripts\Activate.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# 1) Python present ? (py launcher en priorite, puis python)
$py = "py"
if (-not (Get-Command $py -ErrorAction SilentlyContinue)) { $py = "python" }
if (-not (Get-Command $py -ErrorAction SilentlyContinue)) {
    Write-Error "Python introuvable - installez Python 3.10 ou plus recent depuis python.org (cochez 'Add python.exe to PATH'), voir README.md section 2."
}

# 2) Version >= 3.10 (les annotations de type du TP l'exigent).
& $py -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Python 3.10+ requis. Version trouvee : $(& $py --version 2>&1). Installez une version recente (voir README.md section 2)."
}

# 3) Creation du venv (une seule fois).
if (Test-Path ".venv") {
    Write-Host "venv deja present : .venv"
} else {
    & $py -m venv .venv
    Write-Host "venv cree : .venv"
}

# 4) Installation des dependances (via le python du venv).
if (Test-Path ".venv/bin/python") { $vpy = ".venv/bin/python" }
else { $vpy = ".venv/Scripts/python.exe" }
& $vpy -m pip install -q -r requirements.txt
Write-Host "dependances installees."

# 5) Activation : efficace seulement si le script est SOURCE (". .\setup.ps1").
if ($MyInvocation.InvocationName -eq ".") {
    if (Test-Path ".venv/Scripts/Activate.ps1") { & ".venv/Scripts/Activate.ps1" }
    elseif (Test-Path ".venv/bin/Activate.ps1") { & ".venv/bin/Activate.ps1" }
    Write-Host "venv active dans cette session."
} else {
    Write-Host ""
    Write-Host "Pour activer le venv dans votre session :"
    Write-Host "  Windows (PowerShell) : .\.venv\Scripts\Activate.ps1"
    Write-Host "  macOS/Linux (bash)   : source .venv/bin/activate"
    Write-Host "(ou relancez ce script en le sourcant : . .\setup.ps1)"
}
