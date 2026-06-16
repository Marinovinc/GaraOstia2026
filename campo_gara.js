/* =============================================================================
 * FILE: campo_gara.js
 * App: IschiaFishing - costanti geografiche gara Roma-Ostia 26-27/06/2026
 * Creato: 2026-06-14
 * Descrizione: espone window.CAMPO_GARA (stessa struttura di campo_gara.geojson)
 *              caricato da index.html via <script> per evitare fetch/CORS offline.
 * Mantenere in sync con campo_gara.geojson.
 * ========================================================================== */
window.CAMPO_GARA = {
  "type": "FeatureCollection",
  "features": [
    { "type": "Feature", "properties": { "id": "campo_gara", "tipo": "campo", "nome": "Campo gara 2026 (quadrilatero)" },
      "geometry": { "type": "Polygon", "coordinates": [[
        [12.00272,41.70370],[12.09808,41.53707],[11.88478,41.47762],[11.77377,41.63045],[12.00272,41.70370]
      ]] } },
    { "type": "Feature", "properties": { "id": "amp_tor_paterno", "tipo": "divieto", "nome": "AMP Secche di Tor Paterno (DIVIETO)", "buffer_m": 500, "nota": "fuori dal nuovo campo 2026 (riferimento)" },
      "geometry": { "type": "Polygon", "coordinates": [[
        [12.3417,41.6217],[12.3650,41.6000],[12.3250,41.5750],[12.3000,41.5967],[12.3417,41.6217]
      ]] } },
    { "type": "Feature", "properties": { "id": "alpha", "tipo": "hotspot", "nome": "alpha - drop-off nord", "prof_m": 390, "nota": "11nm da Ostia (VECCHIO CAMPO - da riverificare)" }, "geometry": { "type": "Point", "coordinates": [12.00,41.60] } },
    { "type": "Feature", "properties": { "id": "beta", "tipo": "hotspot", "nome": "beta - scarpata", "prof_m": 920, "nota": "22nm (VECCHIO CAMPO - da riverificare)" }, "geometry": { "type": "Point", "coordinates": [11.82,41.45] } },
    { "type": "Feature", "properties": { "id": "gamma", "tipo": "hotspot", "nome": "gamma - banco sud", "prof_m": 895, "nota": "VECCHIO CAMPO - da riverificare" }, "geometry": { "type": "Point", "coordinates": [11.88,41.40] } },
    { "type": "Feature", "properties": { "id": "foce_tevere", "tipo": "foce", "nome": "Foce Tevere (Fiumara Grande)" }, "geometry": { "type": "Point", "coordinates": [12.2333,41.7378] } },
    { "type": "Feature", "properties": { "id": "partenza_ostia", "tipo": "partenza", "nome": "Ostia (PARTENZA / START)", "nota": "confermato dal briefing tattico" }, "geometry": { "type": "Point", "coordinates": [12.243,41.745] } },
    { "type": "Feature", "properties": { "id": "fiumicino", "tipo": "porto", "nome": "Fiumicino (Canale, bocca ovest Tevere)" }, "geometry": { "type": "Point", "coordinates": [12.2150,41.7700] } },
    { "type": "Feature", "properties": { "id": "lido_ostia", "tipo": "riferimento", "nome": "Lido di Ostia" }, "geometry": { "type": "Point", "coordinates": [12.2800,41.7330] } },
    { "type": "Feature", "properties": { "id": "flotta_barca", "tipo": "flotta", "nome": "Barca flotta 13:25 (148m, 11.3C)", "nota": "posizione CONFERMATA da chartplotter" }, "geometry": { "type": "Point", "coordinates": [12.0970,41.6731] } },
    { "type": "Feature", "properties": { "id": "wp_tonni2", "tipo": "flotta", "nome": "Tonni2", "nota": "STIMA da foto - inviare coord esatte" }, "geometry": { "type": "Point", "coordinates": [12.074,41.689] } },
    { "type": "Feature", "properties": { "id": "wp_tonni3", "tipo": "flotta", "nome": "Tonni3", "nota": "STIMA da foto" }, "geometry": { "type": "Point", "coordinates": [12.071,41.687] } },
    { "type": "Feature", "properties": { "id": "wp_totan", "tipo": "flotta", "nome": "Totan (totano)", "nota": "STIMA da foto" }, "geometry": { "type": "Point", "coordinates": [12.087,41.684] } },
    { "type": "Feature", "properties": { "id": "wp_tonni4", "tipo": "flotta", "nome": "Tonni4 / WP13", "nota": "STIMA da foto" }, "geometry": { "type": "Point", "coordinates": [12.093,41.681] } },
    { "type": "Feature", "properties": { "id": "wp15", "tipo": "flotta", "nome": "Waypoint 15", "nota": "STIMA da foto" }, "geometry": { "type": "Point", "coordinates": [12.122,41.663] } },
    { "type": "Feature", "properties": { "id": "banco_campo", "tipo": "zona", "nome": "Banco ~717m (rilievo)", "raggio_m": 1500, "nota": "rilevato da DEM EMODnet F5 (prominenza 125m sui dintorni) - struttura da traina. Zona segnalata dalla flotta." }, "geometry": { "type": "Point", "coordinates": [11.86146,41.55417] } }
  ]
};
