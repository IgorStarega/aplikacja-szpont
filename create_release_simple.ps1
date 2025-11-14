# Skrypt automatycznego tworzenia Release v5.2.0
# Prostsza wersja

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "  Tworzenie Release v5.2.0" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Krok 1: Sprawdz git
Write-Host "[1/6] Sprawdzanie repozytorium Git..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    Write-Host "BLAD: To nie jest repozytorium Git!" -ForegroundColor Red
    exit 1
}
Write-Host "OK - Repozytorium Git znalezione" -ForegroundColor Green
Write-Host ""

# Krok 2: Status git
Write-Host "[2/6] Sprawdzanie statusu Git..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "Znaleziono niezatwierdzone zmiany:" -ForegroundColor Yellow
    git status --short
    Write-Host ""

    $response = Read-Host "Czy zatwierdzic zmiany? (t/n)"
    if ($response -eq "t" -or $response -eq "T") {
        git add .
        git commit -m "Release v5.2.0 - Auto-Update Ready"
        Write-Host "OK - Zmiany zatwierdzone" -ForegroundColor Green
    }
} else {
    Write-Host "OK - Brak niezatwierdzonych zmian" -ForegroundColor Green
}
Write-Host ""

# Krok 3: Push do GitHub
Write-Host "[3/6] Wypychanie zmian do GitHub..." -ForegroundColor Yellow
$response = Read-Host "Czy wypchnac zmiany? (t/n)"
if ($response -eq "t" -or $response -eq "T") {
    git push origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK - Zmiany wypchnięte" -ForegroundColor Green
    } else {
        Write-Host "UWAGA - Blad wypychania" -ForegroundColor Yellow
    }
}
Write-Host ""

# Krok 4: Tworzenie tagu
Write-Host "[4/6] Tworzenie tagu v5.2.0..." -ForegroundColor Yellow
$tagExists = git tag -l "v5.2.0"
if ($tagExists) {
    Write-Host "Tag v5.2.0 juz istnieje!" -ForegroundColor Yellow
    $response = Read-Host "Czy usunac i utworzyc ponownie? (t/n)"
    if ($response -eq "t" -or $response -eq "T") {
        git tag -d "v5.2.0"
        git push origin ":refs/tags/v5.2.0" 2>$null
        Write-Host "Tag usuniety" -ForegroundColor Gray
    } else {
        Write-Host "Anulowano" -ForegroundColor Red
        exit 1
    }
}

git tag -a "v5.2.0" -m "Release v5.2.0 - Auto-Update Ready"
git push origin "v5.2.0"

if ($LASTEXITCODE -eq 0) {
    Write-Host "OK - Tag v5.2.0 utworzony i wypchniety" -ForegroundColor Green
} else {
    Write-Host "BLAD - Nie udalo sie wypchnac tagu" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Krok 5: GitHub CLI
Write-Host "[5/6] Tworzenie Release..." -ForegroundColor Yellow
$ghExists = Get-Command "gh" -ErrorAction SilentlyContinue
if ($ghExists) {
    Write-Host "GitHub CLI znalezione" -ForegroundColor Green

    $response = Read-Host "Czy utworzyc Release przez GitHub CLI? (t/n)"
    if ($response -eq "t" -or $response -eq "T") {
        $notes = "Release v5.2.0 z obsluga automatycznych aktualizacji"

        gh release create "v5.2.0" --title "v5.2.0 - Auto-Update Ready" --notes $notes --latest

        if ($LASTEXITCODE -eq 0) {
            Write-Host "OK - Release utworzony!" -ForegroundColor Green
        } else {
            Write-Host "BLAD - Nie udalo sie utworzyc Release" -ForegroundColor Red
        }
    }
} else {
    Write-Host "GitHub CLI nie jest zainstalowane" -ForegroundColor Yellow
    Write-Host "Zainstaluj z: https://cli.github.com/" -ForegroundColor Gray
    Write-Host "Lub utworz Release recznie:" -ForegroundColor Gray
    Write-Host "  https://github.com/IgorStarega/aplikacja-szpont/releases/new" -ForegroundColor Cyan
}
Write-Host ""

# Krok 6: Weryfikacja
Write-Host "[6/6] Weryfikacja..." -ForegroundColor Yellow
try {
    $apiUrl = "https://api.github.com/repos/IgorStarega/aplikacja-szpont/releases/latest"
    $response = Invoke-RestMethod -Uri $apiUrl -ErrorAction Stop

    Write-Host "OK - Release znaleziony!" -ForegroundColor Green
    Write-Host "  Tag: $($response.tag_name)" -ForegroundColor Cyan
    Write-Host "  Nazwa: $($response.name)" -ForegroundColor Cyan
    Write-Host "  URL: $($response.html_url)" -ForegroundColor Cyan
} catch {
    Write-Host "UWAGA - Release nie jest jeszcze widoczny w API" -ForegroundColor Yellow
    Write-Host "Poczekaj 1-2 minuty i sprawdz:" -ForegroundColor Gray
    Write-Host "  https://github.com/IgorStarega/aplikacja-szpont/releases" -ForegroundColor Cyan
}
Write-Host ""

Write-Host "=======================================" -ForegroundColor Green
Write-Host "  Proces zakonczony!" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green

