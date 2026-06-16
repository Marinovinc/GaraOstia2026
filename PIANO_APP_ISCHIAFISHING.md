# PIANO TECNICO — App ASD IschiaFishing ("Fronte del Tevere")

**Data:** 2026-06-14
**Stato:** PIANO PRE-SVILUPPO — in attesa di approvazione (nessun codice scritto)
**Cartella progetto:** `D:\Dev\Clorofilla` (estende il mockup esistente `index.html`)
**Host designato:** 192.168.1.74 (Windows, presviluppo, raggiungibile, always-on)
**Tipo:** progetto personale/associativo (ASD IschiaFishing) — **separato dal sistema ERP Unitec**

> Convenzione onestà dati: **[CONF]** confermato da codice/fonte reale · **[CALC]** derivato/stimato · **[ASS]** assunzione da verificare.

---

## AGGIORNAMENTO 2026-06-16 — NUOVO CAMPO GARA (capitolato ufficiale)

Il capitolato `Campo Gara OSTIA.pdf` ha cambiato il campo: ora **quadrilatero a 4 vertici**, spostato a SW su acqua profonda (fondali 673-1014 m), NON piu' il pentagono off-foce.
- V1: 41.70370, 12.00272  (N 41 42.222' E 012 00.163')
- V2: 41.53707, 12.09808  (N 41 32.224' E 012 05.885')
- V3: 41.47762, 11.88478  (N 41 28.657' E 011 53.087')
- V4: 41.63045, 11.77377  (N 41 37.827' E 011 46.426')

**Impatto (onesto):**
- AMP Tor Paterno e' ora **fuori dal campo** (resta solo riferimento).
- Hotspot alpha/beta/gamma, deriva del fronte Tevere, rotta manche e previsione erano derivati sul **VECCHIO campo off-foce** -> **DA RIVERIFICARE**: il nuovo campo e' offshore/profondo, scenario diverso (piu' tipo scarpata/1000m, meno guidato dal pennacchio).
- Intel flotta (chartplotter, 16/06): trainano la batimetrica **~148 m off Porto di Roma**, mare 11.3 C, tonni/totano (barca 41.6731 N 12.0970 E confermata; waypoint nominati stimati da foto, in attesa export esatto).
- Aggiornati: campo_gara.geojson/.js, index.html (centro app), prepare_snapshot/basemap (bbox), tile rigenerati (basemap 39 + snapshot 19). Video `generate_manche_video.py` = DA RIFARE (nuova strategia).

---

## 1. OBIETTIVO

App web mobile-first che, **la sera prima di una gara di traina d'altura**, aiuta a:
1. **Localizzare il fronte del Tevere** (la color-line dove l'acqua fertile/torbida del fiume incontra il blu) con dati satellitari di clorofilla, torbidità e temperatura.
2. **Stimare la deriva del fronte** nella finestra di gara (08:00-15:30) combinando vento + portata fiume + marea.
3. **Decidere la rotta**, trainando sul **lato blu** del fronte.

**Gara target:** 62° Campionato Italiano Traina d'Altura, Roma-Ostia, **26-27 giugno 2026**. Finestra 08:00-15:30 (start 08:00-08:30, 7h).

> **Nota di coerenza:** il documento `PROGETTO_CLOROFILLA.md` aveva "generalizzato" l'app togliendo il contesto gara. Questo piano **re-introduce** il contesto IschiaFishing/Roma-Ostia richiesto dal committente, **mantenendo** il motore clorofilla generico già costruito. Il motore dati resta riusabile ovunque; sopra ci montiamo i layer e le viste specifici della gara.

---

## 2. STATO ATTUALE — cosa c'è già [CONF, da `index.html` testato]

Il mockup `D:\Dev\Clorofilla\index.html` è un'app **Leaflet client-only funzionante** (testata Playwright, 24/24 tile satellitari caricati):

- Mappa base multipla (CartoDB scuro / ESRI satellite / OSM).
- Overlay clorofilla multi-prodotto: PACE globale (GIBS WMS) + Med L4 gapfree / L3 / HR 100m (Copernicus teroWmts).
- **Valore puntuale al click** (mg/m³) via GetFeatureInfo sui prodotti Med.
- Selettore data + bottoni rapidi (Oggi/Ieri/-2/-3/-7g), normalizzazione mensile per HR.
- Legenda scala jet, geolocalizzazione, layout responsive desktop/iPhone.
- Funzioni riusabili: `PRODUCTS` (catalogo), `buildWmtsTemplate()`, GetFeatureInfo parser, `esc()` anti-XSS, `getTimeStr()`.

**Punto chiave [CONF]:** tile WMTS Copernicus + GetFeatureInfo + GIBS PACE funzionano **SENZA login/token** (nessuna credenziale nel sorgente). L'account serve **solo** per il download NetCDF (Toolbox) → snapshot offline + analisi numeriche.

---

## 3. DECISIONI CONFERMATE

| Tema | Decisione |
|---|---|
| Stack frontend | HTML + Leaflet, **PWA** installabile, offline-first |
| Host / backend | **1.74** (Windows): job Python notturno + pulsante "prepara snapshot ora" |
| Variabile MVP | **Clorofilla gap-free Copernicus L4 (1km daily)** sul campo gara |
| Distribuzione | Privata ASD/club (**non-commerciale**) — tutti i tier gratuiti OK |
| Base codice | Estende `D:\Dev\Clorofilla\index.html` (no rewrite) |

**Vincolo non-commerciale [CONF]:** Open-Meteo è gratis solo per uso non-commerciale (limiti 10k/giorno, 600/min). Da rivedere solo se un giorno l'app diventa pubblica/monetizzata.

---

## 4. FONTI DATI — readiness verificata (giugno 2026)

**Tutte gratuite.** Differenza = attrito (account, formato, parsing).

| Fonte | Cosa dà | Auth | Formato | Pronta | Note |
|---|---|---|---|---|---|
| Copernicus teroWmts | Tile CHL/SST + valore al click | **Nessuna** (tile pubblici) | PNG / XML | **SI, già in uso** | Limiti rate non documentati → cache lato server |
| Copernicus Marine Toolbox | NetCDF grezzo (snapshot offline, medie, storico) | Account gratuito | NetCDF/Zarr | Sì (dopo registrazione) | `pip install copernicusmarine`; no limite size |
| NASA PACE via GIBS | Tile CHL globali | **Nessuna** | PNG | **SI, già in uso** | Niente GetFeatureInfo (solo visuale) |
| NASA PACE NetCDF | Valori CHL numerici | Earthdata gratuito | NetCDF | Sì (opzionale) | `earthaccess`; solo se serve PACE numerico |
| Open-Meteo Forecast | Vento orario (16gg) | **Nessuna** | JSON | **SI** | Per vista movimento fronte |
| Open-Meteo Historical | Vento storico ERA5 (dal 1940) | **Nessuna** | JSON | **SI** | Proxy ERA5 senza GRIB → per vista previsione |
| Open-Meteo Marine | Onde/correnti/SST | **Nessuna** | JSON | Sì | Caveat costiero: "non per navigazione" |
| GloFAS (EWDS) | Portata Tevere (m³/s) | Account EWDS + token | GRIB/NetCDF | Moderata | Migrato CDS→EWDS nel 2026 |
| Idrometro Ripetta (Prot. Civ. Lazio) | Livello Tevere real-time (m) | Nessuna | HTML (scraping) | Bassa | Locale, 15 min, ma niente API pulita |
| ERA5 via CDS | Vento storico grezzo | Account CDS + token | GRIB/NetCDF | Sì | **Ridondante** con Open-Meteo Historical |

**Prodotti Copernicus consigliati [CONF dal codice + verifica]:**
- CHL daily gap-free → `OCEANCOLOUR_MED_BGC_L4_NRT_009_142` / `cmems_obs-oc_med_bgc-plankton_nrt_l4-gapfree-multi-1km_P1D` — **layer base MVP**.
- CHL daily osservato (buchi nuvole) → `OCEANCOLOUR_MED_BGC_L3_NRT_009_141`.
- CHL/TUR/SPM 100m costa → `OCEANCOLOUR_MED_BGC_HR_L4_NRT_009_211` (mensile) — **unica fonte torbidità/SPM** sul pennacchio.
- SST gap-free → da verificare quale dei due risponde: `SST_MED_SST_L4_NRT_OBSERVATIONS_010_004` (research) vs `SST_MED_PHY_SUBSKIN_L4_NRT_010_036` (già nel codice). **[ASS] da testare il primo carico tile.**

**Caveat onesti [CONF]:**
- "Tempo reale" = **near-real-time giornaliero**, non al minuto. Mostrare sempre data del dato.
- L3 ha buchi nuvole → default su L4 gapfree.
- Prodotti `MED` coprono **solo Mediterraneo** (il campo gara è dentro: OK).
- CHL costiero alla foce = acqua Caso-2 (sedimenti/CDOM) → valore **relativo**, non assoluto.

---

## 5. COSTANTI GEOGRAFICHE [CONF dal brief] — convertite in gradi decimali

**Pentagono campo gara** (lat, lon):
- A: 41.7367, 12.1000  (41°44.2'N 12°06.0'E)
- B: 41.6350, 11.7167  (41°38.1'N 11°43.0'E)
- C: 41.3583, 11.9167  (41°21.5'N 11°55.0'E)
- D: 41.5500, 12.3333  (41°33.0'N 12°20.0'E)
- E: 41.6917, 12.2167  (41°41.5'N 12°13.0'E)

**AMP Secche di Tor Paterno — ZONA DIVIETO** (buffer 500 m da applicare):
- 41.6217, 12.3417  (41°37.3'N 12°20.5'E)
- 41.6000, 12.3650  (41°36.0'N 12°21.9'E)
- 41.5750, 12.3250  (41°34.5'N 12°19.5'E)
- 41.5967, 12.3000  (41°35.8'N 12°18.0'E)

**Hotspot** — coordinate **recuperate dal tool sperimentale 2 giugno [ARCHIVE — DA RIVALIDARE]** (coerenti con le profondità del brief):
- alpha `[41.60, 12.00]` — drop-off nord, ~390 m, 11 nm da Ostia
- beta  `[41.45, 11.82]` — scarpata, ~920 m (brief: 924 m), 22 nm
- gamma `[41.40, 11.88]` — banco sud, ~895 m

**Canyon SW D1-D5** [ARCHIVE — da DEM, da rivalidare]: D1 `[41.396,11.933]` 896m · D2 `[41.386,11.941]` 881m · D3 `[41.461,11.922]` 986m · D4 `[41.581,11.810]` 1017m · D5 `[41.483,11.904]` 969m.

**Punti fissi** [valori vecchio tool — DA CONFERMARE]:
- **CONFLITTO partenza:** brief dice *"porto di Ostia"*; vecchio tool dice **`Porto Fiumicino (START)` `[41.7700, 12.2150]`**. → **da decidere con l'utente**.
- Foce Tevere `[41.7378, 12.2333]` (**Fiumara Grande** + **Canale di Fiumicino**)
- Lido di Ostia `[41.7330, 12.2800]`
- Isobate **200 m** e **1000 m** (da sorgente batimetrica — vedi `D:\Dev\BathymetryExplorer`)

**`front_data.json` [ARCHIVE]:** deriva storica del fronte già calcolata per gara 26-27/6 (08:00→15:30, step 30', offset E/N + 34 segmenti). Candidato riuso diretto per viste 2-3, **da rivalidare** (fase sperimentale).

> Questi diventano un file `campo_gara.geojson` (pentagono, AMP+buffer, hotspot, foce, porti, isobate, rotta consigliata) caricato come layer fissi sovrapponibili con controllo opacità.

---

## 6. ARCHITETTURA

**Modello ibrido: client-only PWA (cuore) + backend Python minimo su 1.74 (solo snapshot/analisi).**

```
┌──────────────────────── CLIENT (PWA, gira su iPhone, offline-capable) ────────────────────────┐
│  index.html + app.js + sw.js (service worker) + manifest.webmanifest                            │
│                                                                                                  │
│  VISTA 1 MAPPA          VISTA 2 MOVIMENTO FRONTE       VISTA 3 PREVISIONE GARA                   │
│  - overlay CHL/TUR/     - deriva taglio blu/verde      - proiezione statistica ERA5 2020-25      │
│    SPM/SST (WMTS/WMS)      08:00->15:30 step 30'         per i giorni gara                        │
│  - layer campo_gara     - vento(Open-Meteo)+marea+      - vento medio orario + deriva risultante  │
│    .geojson + opacità      portata(GloFAS)             - portata Tevere reale (GloFAS)            │
│  - valore al click      - output: ZONA + tolleranza   - etichetta "STIMA, non previsione certa"  │
│  - data/zona selector     (non una linea esatta)                                                  │
│                                                                                                  │
│  Cache offline: snapshot del giorno (tile pre-renderizzati + JSON vento/portata + geojson)       │
└───────────────┬───────────────────────────────────────────────────┬──────────────────────────┘
                │ live: HTTPS dirette (no auth)                       │ offline: legge /snapshot/YYYY-MM-DD/
                ▼                                                     ▼
   Copernicus teroWmts · NASA GIBS · Open-Meteo            File statici serviti da IIS su 1.74
                                                                      ▲
┌─────────────────── BACKEND su 1.74 (Python, solo prep, NON in tempo reale) ──────────┐
│  prepare_snapshot.py  (Task Scheduler notturno + lancio manuale)                       │
│   1. copernicusmarine subset -> NetCDF CHL/SST bbox campo gara (giorno)                 │
│   2. pre-render tile PNG per z6-z11 sul bbox (riuso generate_chl_video.py)              │
│   3. fetch Open-Meteo vento orario (forecast + ieri) -> JSON                            │
│   4. fetch GloFAS portata Tevere -> JSON  [fase avanzata]                               │
│   5. scrive /snapshot/YYYY-MM-DD/ (tiles, wind.json, discharge.json, manifest.json)     │
│   Credenziali Copernicus: SOLO qui (~/.copernicusmarine), MAI nel client               │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

**Razionale:**
- Il **client-only** resta il cuore (riusa il mockup, gira su iPhone, niente server in mare).
- Il **backend su 1.74** serve unicamente a **preparare lo snapshot offline** e (fasi avanzate) le analisi che i tile pubblici non danno. In mare l'app non chiama il backend: legge i file statici dello snapshot.
- IIS su 1.74 serve sia l'app sia la cartella `/snapshot/` (verificare IIS/PHP/Python presenti — primo task di setup).

---

## 7. LE 3 VISTE — dettaglio funzionale

### Vista 1 — MAPPA (estende il mockup)
- Selettore **prodotto** (L4 gapfree / L3 / HR 100m / PACE / SST) e **variabile** (CHL/TUR/SPM/SST).
- **Layer fissi** sovrapponibili da `campo_gara.geojson` con **controllo opacità** ciascuno: pentagono campo, hotspot α/β/γ, AMP Tor Paterno (rosso, divieto + buffer 500m), foce Tevere, porto Fiumicino, isobate 200/1000m, rotta consigliata.
- Selettore **data** e **zona** (zoom rapido al campo gara / foce / hotspot).
- **Valore al click** (mg/m³, già funzionante).
- Indicatore evidente **data del dato** mostrato.

### Vista 2 — MOVIMENTO FRONTE
- Input: un giorno scelto.
- Modello [CALC]: stima deriva del taglio blu/verde **08:00→15:30 a passi di 30'** combinando:
  - vento (Open-Meteo orario) → componente di trasporto superficiale (regola ~3% del vento + deflessione [ASS, da tarare]),
  - marea (tabelle/ARPA o calcolo armonico [ASS]),
  - portata Tevere (GloFAS) → spinta del pennacchio.
- Output: **ZONA dove cercare il fronte con tolleranza** (poligono/ellisse di incertezza), **non** una linea esatta. Animazione a step.
- Riuso del **marching squares** del vecchio tool per disegnare il gradiente CHL come proxy del fronte.

### Vista 3 — PREVISIONE GARA
- Proiezione **statistica** da ERA5 2020-2025 (via Open-Meteo Historical) per gli stessi giorni/orari (26-27 giugno).
- Output: vento medio orario atteso + deriva risultante; portata Tevere da GloFAS reale.
- **Etichetta chiara**: "STIMA statistica con tolleranza — NON previsione certa".

---

## 8. STRATEGIA OFFLINE (vincolo barca)

- **PWA**: `manifest.webmanifest` + `sw.js` (service worker) → installabile su iPhone, asset (Leaflet incluso, da inlineare/bundlare) in cache.
- **Snapshot del giorno**: la sera prima, `prepare_snapshot.py` genera `/snapshot/YYYY-MM-DD/` con tile PNG pre-renderizzati (z6-z11 sul campo gara), `wind.json`, `discharge.json`, `campo_gara.geojson`, `manifest.json` (data, prodotti, bbox).
- L'app, se offline o se l'utente preme "modalità barca", legge dallo snapshot invece che dai WMTS live.
- Leaflet via CDN va **inlineato** per il vero offline (oggi è da `unpkg`).

---

## 9. SICUREZZA

- Credenziali Copernicus **solo lato backend 1.74** (`~/.copernicusmarine` o env), **mai** nel client/HTML.
- `esc()` anti-XSS già presente sui valori dei servizi esterni → mantenere su ogni output.
- **CORS** [ASS]: GetFeatureInfo da `file://` potrebbe essere bloccato → servire l'app da IIS su 1.74 (web server locale) risolve. Da verificare al primo test browser reale.
- Nessun dato personale raccolto; geolocalizzazione solo client-side.

---

## 10. PIANO A FASI (MVP-first)

**Fase 0 — Setup & registrazioni** *(in corso)*
- [ ] Registrazione **Copernicus Marine** (utente fa, link fornito).
- [ ] Verifica su 1.74: IIS, PHP, Python 3.x; install `copernicusmarine`, `xarray`, `cfgrib`, `netCDF4`.
- [ ] Pubblicazione cartella app + `/snapshot/` su IIS 1.74.
- **Deliverable:** ambiente pronto, 1 tile Copernicus verificato da 1.74.

**Fase 1 — MVP gara (1 variabile, 1 prodotto, campo gara, snapshot del giorno)**
- [ ] Estendere `index.html`: default **MED_L4 gapfree** centrato sul **pentagono campo gara**.
- [ ] Creare `campo_gara.geojson` (pentagono + AMP+buffer + foce + porti) e caricarlo come layer con opacità.
- [ ] PWA base (manifest + service worker) + Leaflet inlineato.
- [ ] `prepare_snapshot.py` minimo: tile CHL del giorno + geojson → `/snapshot/`.
- [ ] Pulsante "modalità barca" (legge snapshot).
- **Deliverable:** app installabile su iPhone che mostra CHL sul campo gara, valore al click, e funziona offline con lo snapshot della sera prima. **Criterio:** test reale su telefono + un giorno di snapshot.

**Fase 2 — Multi-variabile + layer completi**
- [ ] Aggiungere TUR/SPM (HR 100m), SST (verificare dataset), selettore variabile.
- [ ] Completare `campo_gara.geojson`: hotspot α/β/γ, isobate 200/1000m, rotta consigliata.
- [ ] Slider temporale ultimi N giorni.
- **Deliverable:** mappa completa come da brief vista 1.

**Fase 3 — Vista Movimento Fronte**
- [ ] Integrare Open-Meteo vento; modello deriva 30' con zona+tolleranza; marching squares gradiente.
- [ ] (Opz.) GloFAS portata Tevere → registrazione EWDS.
- **Deliverable:** vista 2 funzionante con zona di ricerca fronte.

**Fase 4 — Vista Previsione Gara**
- [ ] Open-Meteo Historical (ERA5) 2020-25 per 26-27 giugno; statistiche vento + deriva; etichetta stima.
- **Deliverable:** vista 3 funzionante.

**Fase 5 — Rifinitura**
- [ ] Backend snapshot completo (CHL+SST+vento+portata), automazione Task Scheduler notturna su 1.74.
- [ ] Export punto/area (CSV/KML), punti preferiti, PACE numerico (Earthdata) se serve.

---

## 11. RISCHI E MITIGAZIONI

| Rischio | Mitigazione |
|---|---|
| CORS GetFeatureInfo da file:// | Servire app da IIS 1.74; verificare al primo test browser |
| Dataset SST sbagliato/non risponde | Testare entrambi gli ID al carico tile, tenere quello vivo |
| Buchi nuvole sul giorno gara | Default L4 gapfree + fallback giorno precedente + PACE |
| Modello deriva fronte impreciso | Output come ZONA+tolleranza, mai linea esatta; tarare coefficienti |
| Rate limit WMTS pubblici (non documentato) | Pre-render tile nello snapshot, non martellare live |
| 1.74 instabile (incidente riavvii noto) | Snapshot è file statico: se 1.74 cade, l'app offline continua |
| Leaflet via CDN = serve rete | Inlineare la libreria in Fase 1 |

---

## 12. PROSSIMI PASSI IMMEDIATI (dopo approvazione)

1. Utente: registrazione Copernicus Marine.
2. Io: verifica ambiente 1.74 (IIS/PHP/Python) + install tooling Python.
3. Io: Fase 1 — estensione mockup con campo gara + PWA + snapshot minimo.

**Riferimenti:**
- `D:\Dev\Clorofilla\index.html` — **base app VIVA** (14 giu), motore clorofilla corrente.
- `C:\Users\marin\Downloads\copernicus_roma\Fronte_Tevere_SQUADRA.html` — **ARCHIVIO sperimentale (2 giu), SUPERATO** per i layer clorofilla. Usare SOLO per estrarre/rivalidare geometria gara (hotspot, canyon, punti) e logica marching squares. Esiste in 3 copie identiche (anche in `D:\Dev\Forio_2026\html_originali\` e `D:\claude_handoff\outbox\Roma_pesca_campionato_2026\`). **Nessuna versione più recente.**
- `C:\Users\marin\Downloads\copernicus_roma\front_data.json` — deriva storica gara già calcolata [ARCHIVE].
- `C:\Users\marin\Downloads\copernicus_roma\generate_chl_video.py` — rendering tile/scala colore (per pre-render snapshot).
- `C:\Users\marin\Downloads\copernicus_roma\om_wind.json` / `om_marine.json` / `om_flood.json` — esempi cache Open-Meteo vento/onde/portata.
- `D:\Dev\BathymetryExplorer\index.html` — isobate/batimetria.
