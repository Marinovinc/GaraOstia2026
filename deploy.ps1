# =============================================================================
# deploy.ps1 - Rigenera lo snapshot clorofilla del giorno e pubblica su GitHub Pages
# Uso (la sera prima della gara):
#   .\deploy.ps1                 -> snapshot di IERI (con fallback ai giorni prima)
#   .\deploy.ps1 -Date 2026-06-25
# Risultato: lo snapshot piu' recente disponibile va online; sul telefono apri
# l'app e premi "Prepara offline" su quella data.
# =============================================================================
param([string]$Date = (Get-Date).AddDays(-1).ToString('yyyy-MM-dd'))

$app = 'D:\Dev\IschiaFishing'
$py  = 'C:\Python313\python.exe'
Set-Location $app

function Get-DataCount($txt) {
  if ($txt -match '\((\d+) con dato') { return [int]$matches[1] } else { return -1 }
}

Write-Host "=== Snapshot clorofilla (gap-free) - cerco l'ultima data con dato ===" -ForegroundColor Cyan
$start = [datetime]::ParseExact($Date, 'yyyy-MM-dd', $null)
$used = $null
for ($i = 0; $i -lt 5; $i++) {
  $d = $start.AddDays(-$i).ToString('yyyy-MM-dd')
  Write-Host ("  provo {0} ..." -f $d) -NoNewline
  $out = & $py prepare_snapshot.py $d --zmin 7 --zmax 11 2>&1 | Out-String
  $n = Get-DataCount $out
  Write-Host (" {0} tile con dato" -f $n)
  if ($n -gt 0) { $used = $d; break }
}
if (-not $used) {
  Write-Host "Nessun dato gap-free negli ultimi 5 giorni: il prodotto non e' ancora pronto, riprova piu' tardi." -ForegroundColor Red
  exit 1
}
Write-Host ("Snapshot usato: {0}" -f $used) -ForegroundColor Green

Write-Host "=== Pubblicazione su GitHub Pages ===" -ForegroundColor Cyan
git add -A | Out-Null
$changes = git status --porcelain
if (-not $changes) {
  Write-Host "Niente di nuovo da pubblicare (snapshot gia' online)." -ForegroundColor Yellow
} else {
  git commit -q -m ("deploy: snapshot {0}" -f $used)
  git push -q origin main
  if ($LASTEXITCODE -ne 0) { Write-Host "PUSH FALLITO." -ForegroundColor Red; exit 1 }
  Write-Host "Pubblicato (GitHub Pages si ricostruisce in ~1-2 min)." -ForegroundColor Green
}

Write-Host ""
Write-Host "FATTO." -ForegroundColor Green
Write-Host ("  App:  https://marinovinc.github.io/GaraOstia2026/")
Write-Host ("  Telefono: apri l'app su Wi-Fi, seleziona la data {0}, premi 'Prepara offline'." -f $used)
