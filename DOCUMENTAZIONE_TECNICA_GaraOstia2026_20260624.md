# DOCUMENTAZIONE TECNICA — Guida di bordo GaraOstia2026

**Versione:** 1.0 · **Data:** 2026-06-24 · **Ultimo commit:** `b619e7c`
**Scopo:** riferimento tecnico completo per continuare il lavoro sulla guida `GUIDA_RAPIDA_BARCA.html` (proiezioni, coordinate, metodi, fonti, deploy).
**Natura:** progetto pesca personale, **separato dall'ERP Unitec** (nessun database aziendale coinvolto).

---

## 1. Infrastruttura e file

| Elemento | Valore |
|---|---|
| Deliverable | `D:\Dev\GaraOstia2026\GUIDA_RAPIDA_BARCA.html` (~822 KB) |
| Copia WhatsApp | `C:\Users\marin\Downloads\Guida_Rapida_Ostia_2026.html` |
| Repo (cartella = clone) | `Marinovinc/GaraOstia2026` |
| Live (GitHub Pages) | `https://marinovinc.github.io/GaraOstia2026/GUIDA_RAPIDA_BARCA.html` |

> NON committare `ROTTA_A_LA_MIGLIORE.html` / `ROTTA_A_LA_MIGLIORE.pdf` / `img/`: sono di una **sessione parallela**. Committare SOLO `GUIDA_RAPIDA_BARCA.html` e i `.md` di documentazione.

**Toolchain:**
- PowerShell (Windows) per file/git; PSSession non serve (deploy via git push).
- Python `C:\Python313\python.exe` con **PIL** (downscale/encode foto) e **Playwright** (render headless Chromium per verifica).
- `git` / `gh` (autenticato come `Marinovinc`).

**Deploy:** la cartella `D:\Dev\GaraOstia2026` E' il clone del repo → `git add GUIDA_RAPIDA_BARCA.html; git commit; git push` → Pages ribuilda in ~1 min. Dopo ogni push, allineare la copia WhatsApp in Downloads.

**Nessun database / backend:** la guida e' HTML statico self-contained. I "dati" sono coordinate hard-coded (proiettate) e immagini base64 incorporate. Le sole "connessioni" esterne sono nelle **app companion** (Clorofilla Live: Copernicus Marine WMTS + NASA GIBS WMS, **pubblici senza login** — vedi `progetto-clorofilla-app`).

---

## 2. Pattern di editing (CRITICO)

La guida e' un HTML grande con **diversi blocchi SVG su righe singole lunghissime** (es. la riga della Rotta A). Conseguenze:
- Il tool **Edit fallisce spesso** ("String to replace not found" per whitespace invisibile; "File has been modified since read"). 
- **Soluzione adottata:** piccoli script Python che fanno `html.replace(a, b)` con **ancora univoca**, **guardia di idempotenza** (`if b in html: skip`) e controllo `if a not in html: errore`. Esempi usati in sessione: `_redraw.py` (ridisegno Sez. IV), `_silvio.py` (overlay Sez. IV), `_silvioroutes.py` (overlay 4 cartine, scoping a `#s4`), `_step.py` (testo Rotta A). Tutti rimossi a fine task (temporanei).

**Workflow obbligatorio per ogni modifica:** backup timestamped → modifica → render Playwright + screenshot → verifica visiva → (se ok) cancella backup. Per inserire overlay in UNO solo degli SVG omonimi, **scopare la regione** tra due marcatori di sezione (es. `<section id="s4">` … `<section id="s5">`).

---

## 3. Struttura della guida

`<head>`: CSS con variabili (`--ink`, `--ink-3`, ecc.), **font embeddati base64** (Fraunces serif titoli, Public Sans testo, IBM Plex Mono coordinate; subset latino). Classi chiave: `.sec-head`/`.sec-num`, `.lead`, `.call` (callout; `.call.info` variante), `.mono` (coordinate), `.rmap` (wrapper cartina con **batimetria reale come background CSS**), `.toc-card`, `.colophon`.

Sezioni e ancore:
| # | id | Titolo |
|---|---|---|
| I | s1 | Colpo d'occhio (mini-mappa + 3 spot) |
| II | s2 | Le due partite |
| III | s3 | I tre segnali sovrapposti (color line / SST / drop-off) |
| IV | s3t | **La foce del Tevere e la clorofilla** (+ confronto Silvio) |
| V | s4 | Le rotte A/B/C (mappa generale + 3 cartine + passo-passo) |
| VI | s5 | Tecnica di traina (esche, galleria foto reali) |
| VII | s6 | Punteggio e marea |
| VIII | s7 | Campo e regole |
| IX | s8 | App a bordo + documenti |

> Nota: gli **id** non sono stati rinumerati quando ho inserito la Sez. IV (id `s3t`); solo i **numeri romani visualizzati** e il TOC sono stati spostati V→IX. Quindi id `s4` = sezione visualizzata **V** (rotte), ecc. I link TOC puntano agli id, quindi funzionano.

---

## 4. Proiezioni cartografiche (il cuore tecnico)

Tutte le cartine usano una **proiezione equirettangolare affine**, con la batimetria reale come sfondo e gli elementi vettoriali (poligono campo, rotte, marker) sovrapposti in SVG `preserveAspectRatio="none"`.

### 4.1 Cartine rotte e overlay (viewBox 584×540)
Crop di riferimento: **lon 11.74–12.13 (Δ0.39°)**, **lat 41.45–41.72 (Δ0.27°)**, immagine 584×540.
```
X(lon) = (lon - 11.74) / 0.39 * 584   = (lon - 11.74) * 1497.44
Y(lat) = (41.72 - lat) / 0.27 * 540    = (41.72 - lat) * 2000
```
Verifiche:
- V1 (12.00272, 41.70370) → (393.4, 32.6) ✓ (combacia col poligono nei sorgenti)
- V2 (12.09808, 41.53707) → (536.1, 365.8) ✓
- check-point Silvio (11.9998, 41.6938) → (389.0, 52.4)
- zona Silvio (11.95, 41.66) → (314.5, 120.0)

### 4.2 Cartina Sez. IV (viewBox 830×600)
**Stessa affine** + **shift Y +90** per far entrare la foce del Tevere (che e' a N/E del crop rotte):
```
X(lon) = (lon - 11.74) * 1497.44
Y(lat) = (41.72 - lat) * 2000 + 90
```
Verifiche:
- V1 (12.00272, 41.70370) → (393.4, 122.6)
- foce Tevere/Ostia (12.243, 41.745) → (753, 40)
- spot tonni "PESCA QUI" (11.990, 41.675) → (374, 180)
- check-point Silvio (11.9998, 41.6938) → (389, 142)
- zona Silvio (11.95, 41.66) → (314, 210)

Costante utile (distanze): 1° lat = 111,1 km; 1° lon @ 41,7°N = **83,2 km** (= 111,32·cos41,7°). 60 nm/° lat; ~44,8 nm/° lon.

---

## 5. Coordinate e fonti (tabella di riferimento)

Legenda fonti: **[DEM]** batimetria/modello quota · **[GP]** `gara_plan.js` · **[GJ]** `campo_gara.geojson` · **[MIS]** misurato/letto · **[PLOT]** plotter Garmin di Silvio · **[CALC]** calcolato · **[ASS]** assunto/concettuale.

| Punto | Lat | Lon | Quota | Fonte |
|---|---|---|---|---|
| V1 (NE) | 41.70370 | 12.00272 | — | [GJ] |
| V2 (SE) | 41.53707 | 12.09808 | — | [GJ] |
| V3 (SW) | 41.47762 | 11.88478 | — | [GJ] |
| V4 (NW) | 41.63045 | 11.77377 | — | [GJ] |
| Partenza Ostia | 41.7450 | 12.2430 | — | [GJ] |
| Tonni in-campo ("PESCA QUI") | 41.675 | 11.990 | ~470–590 m | [GP] |
| Banco | 41.554 | 11.861 | ~717 m | [GP][DEM] |
| Spada (muro) | 41.530 | 11.873 | ~924 m | [GP][DEM] |
| α (alfa, drop-off) | ~41.60 | ~12.00 | −393 m | [DEM] |
| β (beta) | 41.531 | 11.873 | −924 m | [DEM] |
| Canyon D1–D5 SW | 41.39–41.58 | 11.81–11.94 | −881…−1017 m | [DEM] |
| **Check-point Silvio** | **41.6938** | **11.9998** | **~466 m** | **[MIS]** ("VEDI Portolano") |
| **Zona cattura Silvio** | **≈41.66** | **≈11.95** | **>700 m** (789/827/901) | **[PLOT]** (segno largo) |
| Break Rotta A (= A2) | 41.6559 | 11.9627 | −696 m | [DEM] (briefing) |
| Solunare manche 1 | — | — | 09:22–11:22 | [CALC][GP] |
| Solunare manche 2 | — | — | 10:09–12:09 | [CALC][GP] |

**Parametri ambientali (sere prima, Copernicus CMEMS):**
- 22/6: CHL mediana 0.041 mg/m³; SST mediana 25.50 °C; **banda fredda** 25.42 °C @ 41.614/12.050 (−0.08 °C); **fronte CHL max** grad 0.012 @ 41.671/11.979; corrente 0.05 kn → 235°.
- 21/6: banda fredda 25.46 °C @ 41.671/11.907 (−0.12 °C); fronte CHL max grad 0.005 @ 41.643/11.907.
- Risoluzioni: CHL 1 km, **SST ~6 km (grossolana)**, corrente 4 km.

---

## 6. Sez. IV — costruzione SVG

`<svg viewBox="0 0 830 600">`. Ordine di disegno (z implicito): mare blu `#3f6f9c` → poligono **verde** (NE del fronte) → pennacchio Tevere (ellissi) → **terra/costa** (poligono `#cabf94`, approssimata [ASS]) → foce Tevere (cerchio + label) → **fronte di clorofilla** [ASS] (linea cyan `#13c0d4` da (207,0) a (765,600), parallela alla costa, passante per lo spot 374,180) → label VERDE/BLU → **poligono campo reale** (bianco + navy dashed) → vertici V1–V4 (mono) → CAMPO GARA → **stella PESCA QUI** (374,180) → vento/Nord.
**Overlay Silvio** (gruppo finale): connettore tratteggiato (374,180)↔(314,210) "~3,7 km · +200 m"; **check-point** cerchio giallo `#E6B800` + X a (389,142); **fascia rossa** `#E03020` (alone bianco) da (284,92) a (344,148) con label "ZONA SILVIO >700 m".

Didascalia: dichiara cosa e' **reale** (poligono, foce, spot 41.675/11.990) vs **approssimato** (costa) vs **concettuale** (fronte) → rimanda a Clorofilla Live (Sez. IX) per il fronte reale del giorno.

---

## 7. Sez. V — rotte e overlay Silvio

4 SVG `viewBox 0 0 584 540` (mappa generale A/B/C + Rotta A/B/C), con `.rmap` background batimetrico. Ogni rotta = polilinea + cerchi numerati. La **mappa NON contiene `<image>`**: la batimetria e' background CSS della classe `.rmap`.

**Overlay Silvio (4 cartine):** gruppo iniettato prima di ogni `</svg>` della sezione `#s4`: fascia rossa `#E03020` (alone bianco) da (284,92) a (344,148) ≈ centro zona (314,120), + label "ZONA SILVIO / >700 m (Silvio)". Il **check-point e' stato omesso qui** (affollava la Rotta C, tutta nell'angolo NE); resta solo sulla Sez. IV.

**Rotta A — break ~700 m:** lo step `09:03 (41.675/11.990) → 09:47 (41.620/11.910)` (SW 227°, 4.9 nm) ora dichiara il passaggio sul punto `41.656/11.963` (~696 m, ≈09:18) = convergenza drop-off + fronte CHL + banda fredda; "tieni giu' l'affondata, cerca color line/acqua fredda lungo il break". Il punto cade **sulla polilinea tra il punto-mappa 3 (tonni) e 4** → nessun cerchio aggiunto, numerazione 1–8 e mappa invariate. La fascia rossa gia' presente lo mostra.

**Giustificazione statistica (perche' SI):** la zona ~41.66/11.95 e' sorretta da: (a) **scarpata fissa ~700 m** [DEM] = segnale drop-off; (b) **fronte CHL** misurato vicino (41.671/11.979 il 22/6); (c) **banda fredda** vicina (41.671/11.907 il 21/6); (d) letteratura PMC (fronte+shelfbreak+ore diurne). L'ancora e' la **struttura** (non si muove); fronte e banda fredda oscillano di km → cercarli lungo il break. **Il segno di Silvio e' largo**: non usato come coordinata puntuale.

---

## 8. Foto esche reali

Galleria in Sez. VI (5 foto): estratte da `D:\claude_handoff\outbox\Roma_pesca_campionato_2026\Briefing_tattico_Roma_2026.pdf` (pag. 5–6: Halco Laser Pro 160 viola, Laser Pro coral, Rapala X-Rap Magnum, skirted/konahead) + **polpetto** scaricato da `maremossoforzasette.it` (incorporato base64, credito + link). Cartella foto: `esche_foto/`. Distanze traina verificate: minnow Halco LP160 ~40 m (C2/C6), LP190 ~60 m (C3/C5), skirted/konahead ~90 m shotgun (C4), flat piombate 15–25 m (C1/C7), affondata 2×500 g ~11 m sul muro.

---

## 9. App e documenti collegati

- **Clorofilla Live** — `https://marinovinc.github.io/ClorofillaLive/` (cartella `D:\Dev\ClorofillaLive`). Leaflet + Copernicus WMTS (`teroWmts`, CHL L4/L3/HR, SST) + NASA GIBS PACE + EMODnet batimetria + SSHA. Vedi `progetto-clorofilla-app`.
- **CampoGara3D** — `https://marinovinc.github.io/CampoGara3D/` (cartella `D:\Dev\CampoGara3D`). Plotly 3D self-contained, **PWA offline** (`_make_pwa.py`, cache `campo3d-v3`).
- **GaraForio2026** — `https://marinovinc.github.io/GaraForio2026/` (modello catch-led, tracking GPS, percorso animato: pattern riusabili).
- **Handover sessione:** `HANDOVER_SESSIONE_GaraOstia2026_20260624.md`.

---

## 10. Riferimenti incrociati (cartella fonti Roma)

`D:\claude_handoff\outbox\Roma_pesca_campionato_2026\`:
- `Note di Silvio Riccardi.txt` — memo vocale (garbled) che rimanda a `Zone Catture Ostia 2026.jpeg`.
- `SCHEDA_RIFERIMENTO_21-06-2026_GIORNO_VERITA.md` — **fonte della coordinata check-point** (41.6938/11.9998, 466 m) e della zona rossa (>700 m, ~3–5 km SW).
- `REPORT_sera_prima_2026-06-21.md` / `_22.md` — CHL/SST/banda fredda/fronte (vedi §5).
- `BRIEFING_ROTTE_OSTIA_2026.md` — waypoint A1–A5 / B1–B5 / C1–C5 con quote DEM (A2 = break 41.6559/11.9627, −696 m).
- `DOCUMENTAZIONE_TECNICA_roma2026_20260602.md` — fisica del fronte, dataset Copernicus/ERA5/GloFAS/DEM, α/β/D1–D5, vertici campo.
- `Briefing_tattico_Roma_2026.pdf` — **foto esche reali** (pag. 5–6).
- `routine_sera_prima.py` — script da rilanciare la sera prima per i parametri aggiornati.
