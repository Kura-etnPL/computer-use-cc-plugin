$ErrorActionPreference = "Stop"

$pluginRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$mcpServer = Join-Path $pluginRoot "scripts\mcp_server.py"

$python = $null
if ($env:COMPUTER_USE_PYTHON -and (Test-Path $env:COMPUTER_USE_PYTHON)) {
    $python = $env:COMPUTER_USE_PYTHON
}

if (-not $python) {
    $pluginVenvPython = Join-Path $pluginRoot ".venv\Scripts\python.exe"
    if (Test-Path $pluginVenvPython) {
        $python = $pluginVenvPython
    }
}

if (-not $python) {
    $pythonCmd = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($pythonCmd) {
        $python = $pythonCmd.Source
    }
}

if (-not $python) {
    $pyCmd = Get-Command py.exe -ErrorAction SilentlyContinue
    if ($pyCmd) {
        & $pyCmd.Source -3 $mcpServer
        exit $LASTEXITCODE
    }
}

if (-not $python) {
    Write-Error "No Python interpreter found. Set COMPUTER_USE_PYTHON or create .venv in the plugin root."
    exit 1
}

& $python $mcpServer
exit $LASTEXITCODE
