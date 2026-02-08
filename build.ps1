# Stop script on any error
$ErrorActionPreference = "Stop"

# --- Welcome Message ---
Write-Host "XHS-Downloader One-Click Build Script (ASCII Version)" -ForegroundColor Green
Write-Host "-----------------------------------------------------"
Write-Host ""

# --- Step 1: Clean up old build files ---
Write-Host "Step 1: Cleaning up old build artifacts..."
if (Test-Path -Path "build") {
    Remove-Item -Recurse -Force "build"
    Write-Host "  - 'build' directory deleted."
}
if (Test-Path -Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "  - 'dist' directory deleted."
}
if (Test-Path -Path "main.spec") {
    Remove-Item -Force "main.spec"
    Write-Host "  - 'main.spec' file deleted."
}
Write-Host "Cleanup complete."
Write-Host ""

# --- Step 2: Set up virtual environment ---
Write-Host "Step 2: Setting up Python virtual environment..."
if (-not (Test-Path -Path "venv")) {
    Write-Host "  - Creating 'venv' directory..."
    python -m venv venv
    Write-Host "  - Virtual environment created."
} else {
    Write-Host "  - 'venv' directory already exists, skipping creation."
}
Write-Host "Virtual environment setup complete."
Write-Host ""

# --- Step 3: Install dependencies ---
Write-Host "Step 3: Installing dependencies..."
# Use executables from the virtual environment explicitly
$PythonExe = ".\venv\Scripts\python.exe"
& $PythonExe -m pip install --upgrade pip --quiet
& $PythonExe -m pip install -r requirements.txt --quiet
& $PythonExe -m pip install pyinstaller --quiet
Write-Host "All dependencies installed."
Write-Host ""

# --- Step 4: Run PyInstaller to build the executable ---
Write-Host "Step 4: Running PyInstaller..."
$PyInstallerExe = ".\venv\Scripts\pyinstaller.exe"
& $PyInstallerExe --noconfirm `
    --icon=./static/XHS-Downloader.ico `
    --add-data "static:static" `
    --add-data "locale:locale" `
    --collect-all "fastmcp" `
    --hidden-import "rich._unicode_data.unicode17-0-0" `
    --collect-all "fastapi" `
    --copy-metadata "fastmcp" `
    --runtime-hook "./source/expansion/pyi_rth_beartype.py" `
    main.py

Write-Host "PyInstaller build finished."
Write-Host ""

# --- Final Message ---
Write-Host "Script executed successfully!" -ForegroundColor Green
Write-Host "The executable can be found in the 'dist\main' directory."
