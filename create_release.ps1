# 📦 Skrypt automatycznego tworzenia Release
# Wersja: 1.0
# Autor: Auto-generated

param(
    [string]$Version = "5.2.0",
    [string]$Message = "Release v5.2.0 - Auto-Update Ready"
)

Write-Host "🚀 Automatyczne tworzenie Release v$Version" -ForegroundColor Cyan
Write-Host "=" -ForegroundColor Gray -NoNewline; Write-Host ("=" * 60) -ForegroundColor Gray

# Funkcja sprawdzająca czy polecenie istnieje
function Test-Command {
    param($Command)
    $null -ne (Get-Command $Command -ErrorAction SilentlyContinue)
}

# Krok 1: Sprawdź czy jesteś w repozytorium git
Write-Host "`n📂 Krok 1: Sprawdzanie repozytorium Git..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    Write-Host "❌ Błąd: To nie jest repozytorium Git!" -ForegroundColor Red
    Write-Host "   Wykonaj: git init" -ForegroundColor Gray
    exit 1
}
Write-Host "✅ Repozytorium Git znalezione" -ForegroundColor Green

# Krok 2: Sprawdź czy są niezatwierdzone zmiany
Write-Host "`n📝 Krok 2: Sprawdzanie statusu Git..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "⚠️  Znaleziono niezatwierdzone zmiany:" -ForegroundColor Yellow
    git status --short

    $response = Read-Host "`nCzy chcesz je zatwierdzić? (t/n)"
    if ($response -eq "t" -or $response -eq "T" -or $response -eq "y" -or $response -eq "Y") {
        Write-Host "`n📦 Dodawanie plików..." -ForegroundColor Cyan
        git add .

        Write-Host "💾 Zatwierdzanie zmian..." -ForegroundColor Cyan
        git commit -m $Message

        Write-Host "✅ Zmiany zatwierdzone" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Kontynuowanie bez zatwierdzania zmian..." -ForegroundColor Yellow
    }
} else {
    Write-Host "✅ Brak niezatwierdzonych zmian" -ForegroundColor Green
}

# Krok 3: Wypychanie zmian
Write-Host "`n🔄 Krok 3: Wypychanie zmian do GitHub..." -ForegroundColor Yellow
$response = Read-Host "Czy chcesz wypchnąć zmiany do GitHub? (t/n)"
if ($response -eq "t" -or $response -eq "T" -or $response -eq "y" -or $response -eq "Y") {
    Write-Host "📤 Wypychanie..." -ForegroundColor Cyan
    git push origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Zmiany wypchnięte" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Błąd wypychania. Kontynuowanie..." -ForegroundColor Yellow
    }
} else {
    Write-Host "⏭️  Pominięto wypychanie" -ForegroundColor Gray
}

# Krok 4: Tworzenie tagu
Write-Host "`n🏷️  Krok 4: Tworzenie tagu v$Version..." -ForegroundColor Yellow

# Sprawdź czy tag już istnieje
$tagExists = git tag -l "v$Version"
if ($tagExists) {
    Write-Host "⚠️  Tag v$Version już istnieje!" -ForegroundColor Yellow
    $response = Read-Host "Czy chcesz go usunąć i utworzyć ponownie? (t/n)"
    if ($response -eq "t" -or $response -eq "T" -or $response -eq "y" -or $response -eq "Y") {
        Write-Host "🗑️  Usuwanie lokalnego tagu..." -ForegroundColor Cyan
        git tag -d "v$Version"

        Write-Host "🗑️  Usuwanie zdalnego tagu..." -ForegroundColor Cyan
        git push origin ":refs/tags/v$Version" 2>$null
    } else {
        Write-Host "❌ Anulowano. Tag już istnieje." -ForegroundColor Red
        exit 1
    }
}

Write-Host "🏷️  Tworzenie tagu v$Version..." -ForegroundColor Cyan
git tag -a "v$Version" -m $Message

Write-Host "📤 Wypychanie tagu do GitHub..." -ForegroundColor Cyan
git push origin "v$Version"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Tag v$Version utworzony i wypchnięty" -ForegroundColor Green
} else {
    Write-Host "❌ Błąd wypychania tagu" -ForegroundColor Red
    exit 1
}

# Krok 5: Sprawdź czy GitHub CLI jest zainstalowane
Write-Host "`n🔧 Krok 5: Sprawdzanie GitHub CLI..." -ForegroundColor Yellow
if (Test-Command "gh") {
    Write-Host "✅ GitHub CLI znalezione" -ForegroundColor Green

    $response = Read-Host "`nCzy chcesz utworzyć Release przez GitHub CLI? (t/n)"
    if ($response -eq "t" -or $response -eq "T" -or $response -eq "y" -or $response -eq "Y") {
        Write-Host "`n📦 Tworzenie Release v$Version..." -ForegroundColor Cyan

        $releaseNotes = @"
# 🚀 Aktualizator Strony v$Version

## ✨ Co nowego w wersji $Version

### 🔄 Auto-Update System
- ✅ Automatyczne sprawdzanie aktualizacji z GitHub
- ✅ Pobieranie i instalacja nowych wersji
- ✅ Backup przed aktualizacją
- ✅ Rollback w przypadku błędu
- ✅ Powiadomienia o dostępnych aktualizacjach

### 🐛 Poprawki
- ✅ Naprawiono błąd 404 przy sprawdzaniu aktualizacji
- ✅ Poprawiono ścieżkę repozytorium GitHub (IgorStarega/aplikacja-szpont)
- ✅ Dodano obsługę tagów wersji

### 📊 Funkcje istniejące
- ⚡ **Batch Processing** - 3x szybsze przetwarzanie
- 💾 **Smart Caching** - 60% oszczędności czasu
- 📊 **Analytics** - statystyki i raporty (Excel/PDF)
- 📅 **Scheduler** - harmonogram automatycznych aktualizacji
- 💬 **Notifications** - Slack, Discord
- 🌐 **Web Dashboard** - Flask + REST API
- 🐳 **Docker** - gotowy do deployment

---

**Full Changelog**: https://github.com/IgorStarega/aplikacja-szpont/commits/v$Version
"@

        gh release create "v$Version" `
            --title "v$Version - Auto-Update Ready" `
            --notes $releaseNotes `
            --latest

        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n✅ Release v$Version utworzony pomyślnie!" -ForegroundColor Green
            Write-Host "`n🔗 Link: https://github.com/IgorStarega/aplikacja-szpont/releases/tag/v$Version" -ForegroundColor Cyan
        } else {
            Write-Host "`n❌ Błąd tworzenia Release" -ForegroundColor Red
            Write-Host "   Możesz utworzyć go ręcznie przez interfejs GitHub" -ForegroundColor Gray
        }
    } else {
        Write-Host "⏭️  Pominięto tworzenie Release" -ForegroundColor Gray
    }
} else {
    Write-Host "⚠️  GitHub CLI nie jest zainstalowane" -ForegroundColor Yellow
    Write-Host "   Możesz je zainstalować z: https://cli.github.com/" -ForegroundColor Gray
    Write-Host "   Lub utworzyć Release ręcznie przez interfejs GitHub" -ForegroundColor Gray
}

# Krok 6: Weryfikacja
Write-Host "`n✅ Krok 6: Weryfikacja..." -ForegroundColor Yellow
Write-Host "`n🔍 Sprawdzanie API GitHub..." -ForegroundColor Cyan

try {
    $apiUrl = "https://api.github.com/repos/IgorStarega/aplikacja-szpont/releases/latest"
    Write-Host "   URL: $apiUrl" -ForegroundColor Gray

    $response = Invoke-RestMethod -Uri $apiUrl -ErrorAction Stop

    Write-Host "`n✅ Release znaleziony!" -ForegroundColor Green
    Write-Host "   Tag: $($response.tag_name)" -ForegroundColor Cyan
    Write-Host "   Nazwa: $($response.name)" -ForegroundColor Cyan
    Write-Host "   Data: $($response.published_at)" -ForegroundColor Cyan
    Write-Host "   URL: $($response.html_url)" -ForegroundColor Cyan
} catch {
    Write-Host "`n⚠️  Nie można znaleźć release przez API" -ForegroundColor Yellow
    Write-Host "   To może być normalne - poczekaj 1-2 minuty i spróbuj ponownie" -ForegroundColor Gray
    Write-Host "   Lub sprawdź: https://github.com/IgorStarega/aplikacja-szpont/releases" -ForegroundColor Gray
}

# Podsumowanie
Write-Host "`n" -NoNewline
Write-Host "=" -ForegroundColor Gray -NoNewline; Write-Host ("=" * 60) -ForegroundColor Gray
Write-Host "🎉 Proces zakończony!" -ForegroundColor Green
Write-Host "=" -ForegroundColor Gray -NoNewline; Write-Host ("=" * 60) -ForegroundColor Gray

Write-Host "`n📝 Następne kroki:" -ForegroundColor Cyan
Write-Host "   1. Sprawdź release: https://github.com/IgorStarega/aplikacja-szpont/releases" -ForegroundColor White
Write-Host "   2. Uruchom aplikację i sprawdź czy auto-update działa" -ForegroundColor White
Write-Host "   3. W razie problemów sprawdź: create_release.md" -ForegroundColor White

Write-Host "`n✨ Gotowe! Aplikacja jest teraz gotowa do automatycznych aktualizacji." -ForegroundColor Green

