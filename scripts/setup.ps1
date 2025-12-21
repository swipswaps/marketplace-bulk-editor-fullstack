# Marketplace Bulk Editor - Interactive Setup Script (Windows)
# This script guides you through setting up the full Docker backend
# Future: Will include OCR processing capabilities
# Run as Administrator: Right-click PowerShell → Run as Administrator

$ErrorActionPreference = "Stop"

function Write-Step { param($msg) Write-Host "`n==> $msg" -ForegroundColor Blue }
function Write-OK { param($msg) Write-Host "✓ $msg" -ForegroundColor Green }
function Write-Warn { param($msg) Write-Host "⚠ $msg" -ForegroundColor Yellow }
function Write-Err { param($msg) Write-Host "✗ $msg" -ForegroundColor Red }

Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║      Marketplace Bulk Editor - Full Setup Script          ║" -ForegroundColor Green
Write-Host "║   PostgreSQL + Redis + JWT Auth + Backend API             ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green

# Step 1: Check Docker
Write-Step "Step 1/7: Checking Docker installation..."
try {
    $dockerVersion = docker --version
    Write-OK "Docker found: $dockerVersion"
} catch {
    Write-Err "Docker not found!"
    Write-Host ""
    Write-Host "Please install Docker Desktop for Windows:"
    Write-Host "  Download from https://docker.com/products/docker-desktop"
    exit 1
}

# Check Docker is running
Write-Step "Step 2/7: Checking Docker daemon..."
try {
    docker info | Out-Null
    Write-OK "Docker daemon is running"
} catch {
    Write-Err "Docker daemon is not running!"
    Write-Host "Please start Docker Desktop from the Start menu"
    exit 1
}

# Step 3: Check/clone repo
Write-Step "Step 3/7: Checking repository..."
if ((Test-Path "docker-compose.yml") -and (Test-Path "backend/app.py")) {
    Write-OK "Already in marketplace-bulk-editor directory"
    $repoDir = "."
} elseif (Test-Path "marketplace-bulk-editor") {
    Write-OK "Found existing marketplace-bulk-editor directory"
    Set-Location marketplace-bulk-editor
    $repoDir = "marketplace-bulk-editor"
} else {
    Write-Warn "Cloning repository..."
    git clone https://github.com/swipswaps/marketplace-bulk-editor.git
    Set-Location marketplace-bulk-editor
    $repoDir = "marketplace-bulk-editor"
    Write-OK "Repository cloned"
}

# Step 4: Start Docker containers
Write-Step "Step 4/7: Starting Docker containers (this may take 2-5 minutes on first run)..."
Write-Host "    Building backend with PostgreSQL + Redis..."
docker compose up -d --build 2>&1 | ForEach-Object { Write-Host "    $_" }
Write-OK "Containers started"

# Step 5: Wait for backend to initialize
Write-Step "Step 5/7: Waiting for backend to initialize..."
Write-Host "    (Backend initializes database schema on first run)"
$maxWait = 120
$waitCount = 0
$healthy = $false

while ($waitCount -lt $maxWait) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5000/" -UseBasicParsing -TimeoutSec 2
        if ($response.Content -match '"status":"ok"') {
            Write-Host ""
            Write-OK "Backend is healthy!"
            $response.Content | ConvertFrom-Json | ConvertTo-Json
            $healthy = $true
            break
        }
    } catch {
        # Continue waiting
    }
    Write-Host "." -NoNewline
    Start-Sleep -Seconds 2
    $waitCount += 2
}

if (-not $healthy) {
    Write-Err "Backend did not become healthy within ${maxWait}s"
    Write-Host "Check logs with: docker logs marketplace-backend"
    exit 1
}

# Step 6: Install npm dependencies
Write-Step "Step 6/7: Setting up frontend..."
try {
    $npmVersion = npm --version
    Write-OK "npm found: $npmVersion"
    Write-Host "    Installing dependencies..."
    npm install --silent
    Write-OK "Dependencies installed"
} catch {
    Write-Warn "npm not found - please install Node.js 20+ from https://nodejs.org"
    Write-Host ""
    Write-Host "After installing Node.js, run:"
    Write-Host "  cd $repoDir"
    Write-Host "  npm install"
    Write-Host "  npm run dev"
    exit 0
}

# Step 7: Network access and firewall configuration
Write-Step "Step 7/7: Network Access Configuration"
Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    Setup Complete!                        ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Get local IP
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notmatch "Loopback" } | Select-Object -First 1).IPAddress

Write-Host "Access the app:"
Write-Host "  Local:   http://localhost:5173" -ForegroundColor Blue
if ($localIP) {
    Write-Host "  Network: http://${localIP}:5173" -ForegroundColor Blue
}
Write-Host ""

# Check and configure Windows Firewall
Write-Host "Checking Windows Firewall for network access from other devices..."
Write-Host ""

$firewallConfigured = $false

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if ($isAdmin) {
    # Check existing firewall rules
    $frontendRule = Get-NetFirewallRule -DisplayName "Marketplace Editor - Frontend" -ErrorAction SilentlyContinue
    $backendRule = Get-NetFirewallRule -DisplayName "Marketplace Editor - Backend" -ErrorAction SilentlyContinue

    if (-not $frontendRule -or -not $backendRule) {
        Write-Warn "Firewall rules not found"
        Write-Host ""
        Write-Host "    To access this app from phones/tablets/other computers,"
        Write-Host "    ports 5173 (frontend) and 5000 (backend) must be opened."
        Write-Host ""
        $response = Read-Host "    Open firewall ports now? [Y/n]"

        if ($response -eq "" -or $response -eq "Y" -or $response -eq "y") {
            New-NetFirewallRule -DisplayName "Marketplace Editor - Frontend" -Direction Inbound -Protocol TCP -LocalPort 5173 -Action Allow | Out-Null
            New-NetFirewallRule -DisplayName "Marketplace Editor - Backend" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow | Out-Null
            Write-OK "Firewall ports opened (5173, 5000)"
            $firewallConfigured = $true
        } else {
            Write-Host ""
            Write-Warn "Skipped. To enable network access later, run as Administrator:"
            Write-Host "    New-NetFirewallRule -DisplayName 'Marketplace Editor - Frontend' -Direction Inbound -Protocol TCP -LocalPort 5173 -Action Allow" -ForegroundColor Blue
            Write-Host "    New-NetFirewallRule -DisplayName 'Marketplace Editor - Backend' -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow" -ForegroundColor Blue
        }
    } else {
        Write-OK "Firewall rules already configured"
        $firewallConfigured = $true
    }
} else {
    Write-Warn "Not running as Administrator - cannot configure firewall"
    Write-Host ""
    Write-Host "    To enable network access, re-run this script as Administrator:"
    Write-Host "    Right-click PowerShell → Run as Administrator" -ForegroundColor Blue
}

Write-Host ""
if ($firewallConfigured -and $localIP) {
    Write-Host "✓ Network access ready: http://${localIP}:5173" -ForegroundColor Green
}
Write-Host ""
Write-Host "To start the app, run:"
Write-Host "  npm run dev" -ForegroundColor Blue
Write-Host ""
Write-Host "Backend API documentation:"
Write-Host "  http://localhost:5000/" -ForegroundColor Blue
Write-Host ""
$response = Read-Host "Start the app now? [Y/n]"

if ($response -eq "" -or $response -eq "Y" -or $response -eq "y") {
    npm run dev
}

