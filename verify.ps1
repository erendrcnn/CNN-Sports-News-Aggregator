# Verification Script
# Run this to verify the application setup

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "CNN Sports News Aggregator - Verification" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$allPassed = $true

# Check 1: Docker
Write-Host "1. Checking Docker..." -ForegroundColor Yellow
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "   ✓ Docker is installed" -ForegroundColor Green
} else {
    Write-Host "   ✗ Docker is NOT installed" -ForegroundColor Red
    $allPassed = $false
}

# Check 2: Docker Compose
Write-Host "2. Checking Docker Compose..." -ForegroundColor Yellow
if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
    Write-Host "   ✓ Docker Compose is installed" -ForegroundColor Green
} else {
    Write-Host "   ✗ Docker Compose is NOT installed" -ForegroundColor Red
    $allPassed = $false
}

# Check 3: Project files
Write-Host "3. Checking project files..." -ForegroundColor Yellow
$requiredFiles = @(
    "docker-compose.yml",
    "README.md",
    ".gitignore",
    ".env.example",
    "backend\requirements.txt",
    "backend\manage.py",
    "backend\config\settings.py",
    "backend\news\models.py",
    "backend\news\views.py",
    "backend\news\services.py",
    "frontend\package.json",
    "frontend\src\App.js",
    "frontend\src\services\newsApi.js"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "   ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "   ✗ $file (MISSING)" -ForegroundColor Red
        $missingFiles += $file
        $allPassed = $false
    }
}

# Check 4: Environment file
Write-Host "4. Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   ✓ .env file exists" -ForegroundColor Green
} else {
    Write-Host "   ⚠ .env file not found (will use .env.example)" -ForegroundColor Yellow
}

# Check 5: Docker services status
Write-Host "5. Checking Docker services..." -ForegroundColor Yellow
$running = docker-compose ps --services --filter "status=running" 2>$null
if ($running) {
    Write-Host "   ✓ Services are running:" -ForegroundColor Green
    foreach ($service in $running) {
        Write-Host "     - $service" -ForegroundColor Cyan
    }
} else {
    Write-Host "   ⚠ No services are running (run 'docker-compose up' to start)" -ForegroundColor Yellow
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
if ($allPassed) {
    Write-Host "VERIFICATION PASSED ✓" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Cyan
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Run: docker-compose up --build" -ForegroundColor White
    Write-Host "2. Access Frontend: http://localhost:3000" -ForegroundColor White
    Write-Host "3. Access API: http://localhost:8000/api" -ForegroundColor White
} else {
    Write-Host "VERIFICATION FAILED ✗" -ForegroundColor Red
    Write-Host "========================================`n" -ForegroundColor Cyan
    Write-Host "Please fix the issues above before running the application." -ForegroundColor Yellow
    if ($missingFiles.Count -gt 0) {
        Write-Host "`nMissing files:" -ForegroundColor Red
        foreach ($file in $missingFiles) {
            Write-Host "  - $file" -ForegroundColor Red
        }
    }
}

Write-Host ""
