# HANDOVER SESSIONE — Guida di bordo GaraOstia2026

**Progetto:** guida di bordo dell'equipaggio per il 62° Campionato Italiano Assoluto di Traina d'Altura (ASD IschiaFishing) — Ostia/Roma, manche **ven 26 e sab 27 giugno 2026**.
**Data handover:** 2026-06-24
**Deliverable:** `D:\Dev\GaraOstia2026\GUIDA_RAPIDA_BARCA.html` (HTML offline self-contained, ~822 KB)
**Stato:** completo e pubblicato. Ultimo commit `b619e7c`.
**Natura:** progetto personale pesca, **separato dall'ERP Unitec**.

> Onesta' brutale: questo documento confessa anche gli errori e i limiti. La guida e' uno strumento d'aiuto, **non una garanzia di pesca**: diversi parametri sono istantanee o stime, da verificare sul campo.

---

## 1. Obiettivo e contesto

Produrre un'unica guida HTML **leggibile offline** (al largo non c'e' segnale) da distribuire all'equipaggio via WhatsApp, con stile editoriale "standard", cartine a batimetria reale, rotte passo-passo con coordinate/orari/direzioni, base scientifica (fronte clorofilla, scarpata/shelfbreak, scienza colore-profondita' esche) e foto reali delle esche.

La gara: campo quadrilatero V1–V4 al largo di Ostia, partenza dal raduno 08:00, pesca fino al cessate 15:30, finestre solunari nel mattino. Tre specie target principali (tonno rosso ×2, alalunga/tunnidi/aguglia imperiale ×1, spada ×1 = bonus raro).

---

## 2. Cronologia sintetica della sessione (cosa e' stato fatto)

**Fase iniziale (pre-compattazione, riassunta):**
- Conversione HTML→MD dei file pesca Forio/Roma (script riusabile `_convert.py`).
- App **Clorofilla Live** (Leaflet + Copernicus WMTS + NASA PACE), deploy GitHub Pages; aggiunta layer SSHA/altimetria.
- **CampoGara3D** (Plotly 3D) trasformato in **PWA offline**, deploy Pages, fix controlli mobile.
- Costruzione della **GUIDA_RAPIDA_BARCA**: stile standard, font embeddati, sezioni I–IX, cartine batimetriche, rotte A/B/C passo-passo, tecnica, punteggio, foto esche reali (estratte dal PDF Briefing_tattico).

**Fase di questa continuazione (2026-06-24):**
1. **Foto polpetto** (octopus skirt) aggiunta alla galleria esche reali (Sez. VI tecnica), posizione C1/C7, con credito a maremossoforzasette.it. Chiarito che la guida e' privata; poi aggiornato anche il repo "pubblico ma a uso equipaggio".
2. **Nuova Sez. IV "La foce del Tevere e la clorofilla"**: meccanismo acqua dolce → fronte CHL → dove pescare, con schema SVG, base scientifica, nota di onesta'. Rinumerate sezioni V–IX e TOC.
3. **Stella "PESCA QUI"** spostata dentro il campo (era fuori dal poligono) → poi ridisegno completo della cartina Sez. IV in **proiezione reale** (poligono V1–V4 identico alle mappe rotte, foce Tevere/Ostia da coordinate, stella ancorata allo spot tonni reale 41.675/11.990).
4. **Confronto con lo spot di Silvio Riccardi**: identificate dai documenti la coordinata del check-point (41.6938/11.9998, 466 m) e la zona di cattura rossa (>700 m, ≈41.66/11.95). Overlay sulla Sez. IV (check-point giallo + fascia rossa + connettore "~3,7 km · +200 m") e su **tutte e 4 le cartine rotte** (solo fascia rossa, per non affollare la Rotta C).
5. **Rotta A**: lo step 09:03→09:47 ora cita il passaggio sulla **scarpata ~700 m a 41.656/11.963 (≈09:18)** = convergenza drop-off + fronte CHL + banda fredda, validato dai parametri (non dal segno di Silvio). Nessun waypoint numerato aggiunto (mappa invariata).
6. Aggiornati file di progetto (memoria), prodotti questo handover + il documento tecnico, aggiunti i link in Sez. IX.

---

## 3. Dove siamo arrivati (stato attuale)

- Guida completa, sezioni **I–IX**; cartina **Sez. IV in proiezione reale** con Tevere+CHL e confronto Silvio; **zona Silvio** su tutte le cartine rotte; **Rotta A** passa sul break ~700 m; galleria **foto esche reali** (incl. polpetto).
- **Pubblicata:** `https://marinovinc.github.io/GaraOstia2026/GUIDA_RAPIDA_BARCA.html` (commit `b619e7c`).
- **Copia WhatsApp** allineata: `C:\Users\marin\Downloads\Guida_Rapida_Ostia_2026.html`.
- App collegate live: Clorofilla Live, CampoGara3D (link in Sez. IX).

---

## 4. Errori confessati (onesti)

**Di merito (qualita'/correttezza):**
1. **Cartina Sez. IV prima versione: poligono campo INVENTATO** (rombo stilizzato) invece del poligono reale proiettato usato in tutto il resto della guida → stesso "campo gara" con due forme diverse. Individuato solo dopo che l'utente mi ha chiesto un'autorevisione. Corretto col ridisegno in proiezione reale. **Lezione: usare da subito la proiezione reale, mai schemi "non in scala" quando esiste il dato.**
2. **Stella "PESCA QUI" fuori dal campo** (515,215) nella prima Sez. IV → l'utente l'ha notato. Riposizionata dentro il poligono e poi ancorata allo spot reale 41.675/11.990.
3. (Pre-compattazione) **Spot tonni fuori campo** (41.673/12.097) e **minnow sullo shotgun 90 m** errati; corretti con gara_plan.js e ricerca distanze esche.
4. **Domande non necessarie**: ho chiesto conferma sul repo pubblico/privato quando l'utente voleva solo procedere ("perche' fai queste domande? non e' una pescatina tra amici"). Lezione: per un campionato, procedere con default sensati e dichiararli, non interrogare.

**Tecnici (processo/tooling):**
5. **Edit tool fallito** piu' volte su questo HTML enorme ("String to replace not found" per whitespace; "File modified since read"). Fallback: **script Python con replace esatto su byte**. Lezione: per file giganti a riga singola, usare Python, non Edit.
6. **Overlay Silvio prima versione**: check-point giallo sovrapposto ai waypoint nella Rotta C (angolo NE affollato). Ripristinato il backup e semplificato (solo fascia rossa sulle rotte).
7. Refuso didascalia (doppio punto) — intercettato prima dell'esecuzione.

**Tutti gli errori 1–6 sono stati corretti e verificati con render Playwright.**

---

## 5. Limiti dichiarati (cosa NON e' provato)

- **Segno di Silvio molto approssimativo** → in guida la zona e' ancorata alla **scarpata batimetrica** (dato fisso DEM), non al suo tratto; fronte/banda fredda vanno cercati *lungo il break* in giornata.
- **Fronte CHL e banda fredda** = istantanee delle sere prima (21/6, 22/6), oscillano di km da un giorno all'altro; **SST ~6 km** (grossolana per micro-anomalie). Da confermare col sensore di temperatura di bordo + Clorofilla Live il giorno stesso.
- **Fronte di clorofilla nello schema = concettuale** (orientamento plausibile, non misurato per il 26–27/6).
- **Linea di costa** nella Sez. IV = approssimata, non vettore costiero preciso.
- La guida **non e' stata testata su iPhone reale** (solo Playwright headless).

---

## 6. Come continuare

**Subito utile:**
- La sera del 25/6 (e 26/6) **rilanciare la routine "sera prima"** (`routine_sera_prima.py` nella cartella Roma) per CHL/SST/corrente aggiornate, e ritarare il punto fronte/PESCA QUI e l'orario del PRIME.
- Eventualmente **citare il break ~700 m anche nella Rotta B** (gia' lavora il profondo, ma il tratto 41.66/11.95 non e' esplicito).
- Valutare se reintrodurre il **check-point di Silvio sulle cartine rotte** in forma decluttered (oppure solo sulla mappa generale).
- **Test su iPhone reale** (apertura offline, leggibilita', tap sui link).

**Procedura operativa per ogni modifica alla guida:**
1. `Copy-Item GUIDA_RAPIDA_BARCA.html GUIDA_RAPIDA_BARCA.html.BACKUP_<timestamp>`
2. modifica (Python replace su byte per blocchi grandi)
3. render Playwright + screenshot, verifica visiva
4. copia su `C:\Users\marin\Downloads\Guida_Rapida_Ostia_2026.html`
5. `git add GUIDA_RAPIDA_BARCA.html` → commit → push (NON committare `ROTTA_A_LA_MIGLIORE.html`, sessione parallela)
6. se ok, cancella il backup

Dettagli tecnici completi (proiezioni, coordinate, metodi, fonti) nel documento tecnico affiancato.

---

## 7. Possibili sviluppi e miglioramenti futuri

**Guida / contenuti:**
- Rendere la guida una **PWA offline** (manifest + service worker, come CampoGara3D) per "Aggiungi a Home" e apertura affidabile al largo.
- **Versioni per-barca** (Barca 1 NE / Barca 2 centro / Barca 3 SW) con la rotta dedicata in evidenza.
- **Scheda "sera prima" auto-generata** incorporata: ultimo CHL/SST/corrente + finestra solunare del giorno.
- **Checklist pre-partenza** e **tabella nodi/weak-link** (gia' presenti immagini nella cartella Roma) come sezione.
- **QR code** nella guida verso Clorofilla Live / CampoGara3D per apertura rapida da telefono.

**Cartografia / dati:**
- Sostituire il **fronte concettuale** della Sez. IV con il **fronte CHL reale** dell'ultima passata satellitare (snapshot la sera prima), marcato come misurato.
- Disegnare le **isobate reali** (200/500/700/900 m) sulle cartine rotte come linee, non solo background.
- **Georeferenziare meglio lo spot di Silvio** chiedendogli la coordinata esatta (il segno attuale e' largo): se la fornisce, marcarla [MIS] puntuale.
- **Marker catture storiche** se disponibili waypoint reali (come fatto per GaraForio2026 da Waypoints.kmz).

**Integrazione app:**
- **Tracking GPS** della barca nella companion app (gia' implementato in GaraForio2026: `trkBtn`/watchPosition) — portarlo su una app Ostia.
- **Percorso animato** Rotta A/B/C nella Clorofilla Live (gia' presente il motore percorso+scia+ticker).
- **Export GPX** delle rotte A/B/C dalla guida per caricarle sul chartplotter (esiste `ROTTE_OSTIA_2026.gpx`).

**Scientifico:**
- Modello **catch-led** (storico catture peso 0.55 + ambiente 0.45) gia' validato su Forio: replicarlo per Ostia se si raccolgono catture storiche del campo.
- Backend Python (Fase 4 Clorofilla) per **medie d'area e serie storiche** CHL/SST (richiede account Copernicus).

---

## 8. Riferimenti incrociati

- Documento tecnico: `DOCUMENTAZIONE_TECNICA_GaraOstia2026_20260624.md` (stessa cartella/repo).
- Fonti dati e materiale gara: `D:\claude_handoff\outbox\Roma_pesca_campionato_2026\` (Note di Silvio Riccardi.txt, SCHEDA_RIFERIMENTO_21-06-2026, REPORT_sera_prima_*, BRIEFING_ROTTE_OSTIA_2026.md, DOCUMENTAZIONE_TECNICA_roma2026_20260602.md, Briefing_tattico_Roma_2026.pdf con foto esche, routine_sera_prima.py).
- App collegate: Clorofilla Live `https://marinovinc.github.io/ClorofillaLive/`, CampoGara3D `https://marinovinc.github.io/CampoGara3D/`, GaraForio2026 `https://marinovinc.github.io/GaraForio2026/`.
- Memoria progetto: `progetto-gara-ostia-2026` (vedi anche `progetto-clorofilla-app`, `forio-2026-conversione-md`).
