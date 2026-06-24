# DOCUMENTAZIONE TECNICA — Rotta A: dossier, scena 3D, GPS, PWA offline

**Data:** 2026-06-24
**Progetto:** Gara di traina d'altura Ostia 2026 (personale, **non ERP**)

---

## 0. Avvertenza onesta su "database e collegamenti"
**Questo progetto non ha alcun database né backend.** È composto da **pagine web statiche** servite da **GitHub Pages**, con **dati incorporati** nei file (JS/JSON inline, batimetria base64 dentro l'HTML). Le uniche "connessioni" reali sono:
- **GitHub Pages** (hosting statico HTTPS) dei due repository;
- **API di geolocalizzazione del browser** (`navigator.geolocation`) per la posizione reale — richiede HTTPS, non è una connessione a un server nostro;
- **Solo nella Leaflet app `GaraOstia2026/index.html`** (usata online per generare la cartina): tile/WMS satellitari di terzi (vedi §9). La **scena 3D e il dossier NON fanno chiamate di rete** (tutto incorporato).

Qualsiasi riferimento a "DB/connessioni" oltre a questi sarebbe inventato.

---

## 1. Architettura
```
GitHub Pages (statico, HTTPS)
├── repo GaraOstia2026  → dossier, PDF, immagini, Leaflet app sorgente cartina
└── repo CampoGara3D    → scena 3D Plotly (online) + PWA offline
Browser del dispositivo → Geolocation API (GPS hardware), Service Worker (cache offline)
```
Nessun server applicativo, nessun database, nessuna autenticazione.

---

## 2. Repository, file principali, deploy
### 2.1 `GaraOstia2026` (D:\Dev\GaraOstia2026)
- `ROTTA_A_LA_MIGLIORE.html` — **dossier** Rotta A (HTML autonomo, font via Google Fonts `@import`, immagini locali in `img/`).
- `ROTTA_A_LA_MIGLIORE.pdf` — versione stampabile/plastificabile.
- `GUIDA_RAPIDA_BARCA.html` — guida originale a 3 rotte (fonte dati waypoint).
- `index.html` — **Leaflet app** (clorofilla/SST + batimetria EMODnet); sorgente della cartina batimetrica.
- Dati app Leaflet: `campo_gara.js`, `isobate.js`, `dropoff.js`, `gara_plan.js`, `front_drift.js`, `chl_field.json`, `front_data.json`, `banco.json`.
- `img/campo_batimetria_rottaA.png` — cartina batimetrica con Rotta A (render Playwright).
- `img/esche/forio/forio_01..11.(png|jpg)` — **11 foto prodotto reali** delle esche + `_sources.json`.
- Script generatori (prefisso `_`, ignorati o di servizio): `_map_shot.py` (render cartina), `_fetch_forio_lures.py` (download foto esche), `_pdf_shot.py` (PDF), `_ios_webkit_test.py` (test mobile).
- `.gitignore` ignora `_*.py`, `_*.png`, `*.BAK_*`, log di sessione.

### 2.2 `CampoGara3D` (D:\Dev\CampoGara3D)
- `index.html` — scena 3D originale (Plotly bundle + batimetria, ~8 MB) — **non** modificata da noi se non come **fonte dati**.
- `ROTTA_A_3D.html` — **scena 3D online** generata da `_build_rotta3d.py`.
- `offline/` — **PWA offline**: `index.html` (scena + registrazione SW), `sw.js`, `manifest.webmanifest`, `icon-192.png`, `icon-512.png`.
- `_build_rotta3d.py` — **generatore** (vedi §5–7).
- `_extract_fig.py` — estrae `data`/`layout` Plotly da `index.html` → `_fig_extracted.json`.
- `_fig_extracted.json` — figura batimetrica estratta (input del generatore).
- `manifest.json`, `sw.js` — PWA della index originale (scope `/CampoGara3D/`, **cache `campo3d-v3`**) — distinta dalla nostra `/offline/`.

### 2.3 Deploy
Entrambi i repo: **GitHub Pages da branch `main`, root**. Push → rebuild ~30–60 s.
Verifica: `curl -s -o /dev/null -w "%{http_code}" <url>`.

---

## 3. Sistema di coordinate (CRITICO)
La scena 3D usa coordinate **chilometriche relative al centro campo**, non lat/lon:
- Centro: `LAT0 = 41.587`, `LON0 = 11.940`.
- `KX = 111.320 * cos(rad(LAT0))` ≈ 83.27 km/grado lon; `KY = 110.574` km/grado lat.
- **x = km Est-Ovest**, **y = km Nord-Sud**, **z = quota in metri** (fondale negativo, **superficie del mare = 0**).
- Conversione: `x = (lon - LON0) * KX`, `y = (lat - LAT0) * KY`.
- `aspectratio` scena: x=2, y=2, z=0.9 (z fortemente compresso).
- Quota barca/rotta in superficie: `ZS = 6.0 m` (appena sopra il pelo, per visibilità).

**Questo identico sistema** è usato sia per disegnare la rotta sia per posizionare il GPS reale: coerenza garantita.

---

## 4. Dati
### 4.1 Rotta A — waypoint (fonte: `GaraOstia2026/gara_plan.js`, route A)
| # | min | lat | lon | nota |
|---|-----|-----|-----|------|
| 1 | 0 | 41.680 | 11.985 | Start NE, cala lo spread (tonni) |
| 2 | 60 | 41.665 | 11.965 | Bordo NE nel solunare |
| 3 | 120 | 41.675 | 11.990 | Angolo NE, primi tonni |
| 4 | 180 | 41.620 | 11.910 | Scende SW verso le strutture |
| 5 | 240 | 41.554 | 11.861 | Banco 717 m (alalunga) |
| 6 | 300 | 41.530 | 11.873 | Drop-off 924 m (spada, stop&go) |
| 7 | 360 | 41.560 | 11.885 | Muri / orlo banco W |
| 8 | 450 | 41.585 | 11.910 | Ultima passata (fino 15:30) |

### 4.2 Spot nominati (per "spot più vicino" nel GPS)
`bordo NE (41.675,11.990)`, `banco 717 m (41.55417,11.86146)`, `drop-off 924 m (41.53021,11.87292)`.

### 4.3 Batimetria
Superficie 3D = griglia **259×365** float64 (x,y,z 2D), estratta da `CampoGara3D/index.html` (figura Plotly). Valori `z` in metri; NaN nei no-data. Origine dati: **EMODnet Bathymetry** (rendering originale dell'app 3D).

### 4.4 Foto esche — provenienza
Scaricate da `C:\Users\marin\Downloads\Briefing_Forio_2026_20.html` (URL prodotto hotlinkati: `halcotackle.com`, `williamson`, `rapala`, `nootica`). Salvate in `img/esche/forio/`. Uso personale di bordo (cataloghi produttori).

---

## 5. Generatore `_build_rotta3d.py` — metodi
- **`decode(v)`** — decodifica i typed-array binari di Plotly (`{dtype,bdata(base64),shape}`) in `numpy` (mappa dtype `f8→<f8`, ecc.).
- **`seabed_z(qx,qy)`** — campionatore **bilineare** della griglia batimetrica; gestisce NaN (media dei vertici validi → fallback finestra 7×7); ritorna `None` se tutto NaN. Assi `xa=SX[0,:]`, `ya=SY[:,0]` riordinati ascendenti.
- **`to_xy(lat,lon)`** — conversione lat/lon→km (vedi §3).
- **`pos_at(t)`** — interpolazione lineare della posizione barca al minuto `t` lungo i waypoint.
- **`hhmm(m)`** — minuti dallo START (08:00) → "HH:MM".
- **Tracce generate**: surface batimetria (0), spot (1–3), campo (4), piano del mare (Mesh3d z=0), Rotta A superficie (oro), scia/barca/beam/eco animati (frame), Rotta A sul fondale (cresce nei frame), waypoint fondale.
- **Animazione**: 31 frame (0→450 min, step 15); `updatemenus` Play/Pausa; `sliders` con label orario.
- **Post-processing HTML**: iniezione meta iOS in `<head>`; UI `<style>/<div>/<script>` prima di `</body>`; iniezione dati `window.__ROUTE__ / __SPOTS__ / __GEO__`.

Output: `ROTTA_A_3D.html` (online) + `offline/` (PWA).

---

## 6. Modulo GPS + correzioni (JS iniettato)
Globali iniettati da Python: `window.__ROUTE__` (waypoint in km+lat/lon), `window.__SPOTS__` (spot in km), `window.__GEO__` (LAT0,LON0,KX,KY,ZS).
- **`toXY(lat,lon)`** — come §3.
- **`nearest(px,py)`** — proiezione del punto su ogni segmento della polilinea (parametro `t` clampato 0–1), ritorna distanza minima (cross-track) e indice segmento.
- **`brgTrue(dx,dy)`** — rotta bussola vera: `atan2(dx_est, dy_nord)` → 0–360°.
- **Logica correzione** (toccando il marker o nel pannello):
  - `xtm = nearest.d * 1000` (m fuori-rotta);
  - target = **prossimo waypoint** = `ROUTE[min(segi+1, n-1)]`; `brg` e `distWp` verso di esso;
  - **tolleranza** (slider, default 50 m): `xtm ≤ TOL` → "IN ROTTA"; altrimenti correzione;
  - **"vira sx/dx"** da `pos.coords.heading` (GPS): `diff = ((brg-heading+540)%360)-180` → dritta se >0, sinistra se <0; **solo se heading disponibile** (in movimento), altrimenti "prua non disponibile";
  - **spot più vicino** per distanza euclidea in km.
- **Posizione reale**: `navigator.geolocation.watchPosition(update, err, {enableHighAccuracy:true})`; marker `scatter3d` verde `#39ff7a` "TU" aggiunto con `Plotly.addTraces` e aggiornato con `Plotly.restyle`.
- **Tap**: `gd.on('plotly_click', …)` confronta `curveNumber` con l'indice del marker reale.
- **Zoom +/−**: scala `scene.camera.eye` rispetto a `center` di fattore 0.8 (avanti) / 1.25 (indietro).
- **UI a scomparsa**: rilevamento touch `matchMedia('(pointer: coarse)')`; `@media(pointer:coarse)` nasconde la **modebar** Plotly; legenda/scala via `Plotly.relayout({showlegend})` + `Plotly.restyle({showscale},[0])`.

**Verifica numerica** (Playwright + geolocation simulata): valori del pannello identici al calcolo Python indipendente (in-rotta e fuori-rotta).
**Limite:** `coords.heading` non simulabile in Playwright → "vira sx/dx" testabile solo su dispositivo reale in movimento.

---

## 7. PWA offline (`CampoGara3D/offline/`)
- **`manifest.webmanifest`**: `start_url ./index.html`, `scope ./`, `display standalone`, icone 192/512, theme `#0d1626`.
- **`sw.js`**: cache **`rotta3d-v1`**, strategia **cache-first**; `install` → `caches.addAll(['./','./index.html','./manifest.webmanifest','./icon-192.png','./icon-512.png'])` (**pre-download**); `activate` → pulizia cache vecchie + `clients.claim()`; `fetch` → cache → rete (e cache della risposta) → fallback `./index.html`.
- **Scope isolato** in `/offline/` per non collidere con il SW della index (`/CampoGara3D/`).
- **Registrazione** iniettata in `offline/index.html`.
- La scena è **autonoma** (0 richieste esterne, verificato): basta cachare `index.html`.

**Uso:** aprire una volta **con rete** (cache ~8 MB) → "Aggiungi a Home" → offline.

---

## 8. Dossier e PDF
- `ROTTA_A_LA_MIGLIORE.html`: HTML semantico, CSS con variabili, **responsive** (`@media max-width:600`, tabelle scrollabili), meta iOS, hero, gallerie esche con badge `1ª·C#` (ordine/canna), tabella assetto, confronto A/B/C.
- **PDF**: `_pdf_shot.py` (Playwright Chromium, `emulate_media('print')`, `print_background=True`, A4). Fix: rimosso `loading="lazy"` + scroll forzato pre-stampa (le immagini lazy non si stampavano).

---

## 9. Connessioni esterne (elenco completo e onesto)
| Risorsa | Dove | Quando |
|---|---|---|
| GitHub Pages | hosting dei 2 repo | sempre (caricamento pagine) |
| Google Fonts (`@import`) | solo `ROTTA_A_LA_MIGLIORE.html` | online; offline ripiega su font di sistema |
| Geolocation API | scena 3D (GPS) | su richiesta utente (HTTPS) |
| EMODnet Bathymetry WMS (`ows.emodnet-bathymetry.eu/wms`) | solo `GaraOstia2026/index.html` (Leaflet) | online, app cartina |
| Copernicus Marine WMTS (`wmts.marine.copernicus.eu`) | solo Leaflet app (CHL/SST) | online |
| NASA GIBS WMS | solo Leaflet app (PACE) | online |
| ESRI World_Imagery tiles | solo Leaflet app (basemap) | online |
| Cataloghi produttori (foto esche) | scaricate **una tantum** in locale | non più necessarie a runtime |

**La scena 3D (`ROTTA_A_3D.html` / `offline/`) non usa nessuna di queste a runtime** (tutto incorporato + Geolocation locale).

---

## 10. Metodologia di test (Playwright)
- **Motore**: Chromium (SW affidabile) e **WebKit** (motore Safari) v26 + device `iPhone 13` / `iPad Pro 11`.
- **Mobile**: misura `scrollWidth` vs `clientWidth` (overflow), conteggio immagini caricate, errori console/page.
- **GPS**: `new_context(geolocation={...}, permissions=['geolocation'])`, confronto `#corrBody` con calcolo Python.
- **Offline**: `python -m http.server --directory`, attesa `serviceWorker.controller` + cache, `context.set_offline(True)`, reload. (SW non funziona su `file://`.)
- **Limite noto**: reload offline su **WebKit headless** dà errore interno di Playwright (non riproduce → da verificare su Safari reale).

---

## 11. Sviluppi futuri possibili
1. **Test su dispositivo iOS reale** (priorità): touch, GPS `heading` per "vira sx/dx", offline su Safari, "Aggiungi a Home". *(richiede solo il telefono)*
2. **Selettore rotte A/B/C** nella scena 3D (i dati B/C esistono in `gara_plan.js`).
3. **Bussola via `DeviceOrientation`** (con permesso iOS) per dare "vira sx/dx" anche da fermo.
4. **Registrazione traccia reale** (breadcrumb GPS) e confronto col piano + esportazione.
5. **Allarme tolleranza** (vibrazione/suono) quando si esce dalla soglia.
6. **Allarme AMP Tor Paterno** (zona vietata) con buffer.
7. **Versioning service worker** + pulsante "Aggiorna dati" (oggi cache `rotta3d-v1` statica).
8. **CHL/SST aggiornata la sera prima** integrata nel 3D (ricampionamento, come fa già la Leaflet app).
9. **Export GPX/KML** della rotta per chartplotter.
10. **ETA al prossimo waypoint** dalla velocità GPS (`coords.speed`).
11. **Modalità notturna/alto contrasto** per uso in plancia.
12. **Riduzione peso** (~8 MB): compressione/lazy della batimetria o tile DEM.
13. **Meteo/vento** (Open-Meteo) integrato nel pannello.
14. **Persistenza preferenze** (tolleranza, ultima vista) in `localStorage`.
15. **Pulsante "Apri in 3D"** dal dossier (aggiunto in questa sessione, vedi guida).

---

## 12. Riferimenti rapidi
- Generatore 3D: `D:\Dev\CampoGara3D\_build_rotta3d.py`
- Estrattore figura: `D:\Dev\CampoGara3D\_extract_fig.py` → `_fig_extracted.json`
- Render cartina: `D:\Dev\GaraOstia2026\_map_shot.py`
- Download foto esche: `D:\Dev\GaraOstia2026\_fetch_forio_lures.py`
- PDF: `D:\Dev\GaraOstia2026\_pdf_shot.py`
- Python: `C:\Python313\python.exe` (plotly 6.8.0, numpy, playwright)
- Handover: `HANDOVER_SESSIONE_rotta_a_dossier_3d_20260624.md`
