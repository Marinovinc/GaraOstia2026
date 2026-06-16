# -*- coding: utf-8 -*-
"""
=============================================================================
App: IschiaFishing - prepare_snapshot.py
Creato: 2026-06-14
Descrizione: prepara lo snapshot OFFLINE del giorno per il campo gara Roma-Ostia.
             Scarica i tile WMTS PUBBLICI Copernicus (clorofilla MED_L4 gapfree)
             per la zona del campo gara, cosi' l'app funziona in barca senza rete.
             NON richiede account (i tile teroWmts sono pubblici).
Uso:
    python prepare_snapshot.py [YYYY-MM-DD] [--zmin 7] [--zmax 11]
    (default data = ieri, perche' il dato di oggi spesso non e' ancora elaborato)
Output:
    snapshot/<DATE>/MED_L4/<z>/<x>/<y>.png  +  snapshot/<DATE>/manifest.json
=============================================================================
"""
import sys, os, json, math, argparse, datetime, time
import urllib.request

WMTS_BASE = "https://wmts.marine.copernicus.eu/teroWmts"
PRODUCT = "OCEANCOLOUR_MED_BGC_L4_NRT_009_142"
DATASET = "cmems_obs-oc_med_bgc-plankton_nrt_l4-gapfree-multi-1km_P1D_202207"
VARIABLE = "CHL"
STYLE = "cmap:jet"

# Bounding box campo gara (lon/lat) - da campo_gara.geojson
BBOX = {"lon_min": 11.7738, "lat_min": 41.4776, "lon_max": 12.0981, "lat_max": 41.7037}

HERE = os.path.dirname(os.path.abspath(__file__))


def deg2tile(lat, lon, z):
    n = 2 ** z
    x = int((lon + 180.0) / 360.0 * n)
    lat_r = math.radians(lat)
    y = int((1.0 - math.asinh(math.tan(lat_r)) / math.pi) / 2.0 * n)
    return x, y


def tile_url(z, x, y, date):
    return (WMTS_BASE + "?service=WMTS&version=1.0.0&request=GetTile"
            + "&layer=" + PRODUCT + "/" + DATASET + "/" + VARIABLE
            + "&style=" + STYLE + "&TileMatrixSet=EPSG:3857"
            + "&TileMatrix=%d&TileRow=%d&TileCol=%d" % (z, y, x)
            + "&format=image/png&TIME=" + date)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("date", nargs="?", default=None, help="YYYY-MM-DD (default: ieri)")
    ap.add_argument("--zmin", type=int, default=7)
    ap.add_argument("--zmax", type=int, default=11)
    args = ap.parse_args()

    if args.date:
        date = args.date
    else:
        date = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

    out_dir = os.path.join(HERE, "snapshot", date)
    os.makedirs(out_dir, exist_ok=True)

    total, ok, empty = 0, 0, 0
    tiles_meta = []
    for z in range(args.zmin, args.zmax + 1):
        x0, y0 = deg2tile(BBOX["lat_max"], BBOX["lon_min"], z)  # top-left
        x1, y1 = deg2tile(BBOX["lat_min"], BBOX["lon_max"], z)  # bottom-right
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                total += 1
                dest = os.path.join(out_dir, "MED_L4", str(z), str(x))
                os.makedirs(dest, exist_ok=True)
                fpath = os.path.join(dest, "%d.png" % y)
                url = tile_url(z, x, y, date)
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "IschiaFishing/1.0"})
                    with urllib.request.urlopen(req, timeout=30) as r:
                        data = r.read()
                    with open(fpath, "wb") as f:
                        f.write(data)
                    tiles_meta.append("MED_L4/%d/%d/%d.png" % (z, x, y))
                    if len(data) < 500:   # tile vuoto/trasparente
                        empty += 1
                    else:
                        ok += 1
                except Exception as e:
                    print("  ERR z%d x%d y%d: %s" % (z, x, y, e))
                time.sleep(0.05)
        print("z%d completato (x %d..%d, y %d..%d)" % (z, min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1)))

    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    manifest = {
        "date": date, "product": "MED_L4", "dataset": DATASET, "variable": VARIABLE,
        "bbox": BBOX, "zmin": args.zmin, "zmax": args.zmax,
        "tiles_total": total, "tiles_ok": ok, "tiles_empty": empty,
        "generated_utc": now_utc,
        "source": "Copernicus Marine teroWmts (public, no auth)"
    }
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    # elenco tile per pre-cache offline (usato dal pulsante "Prepara offline" dell'app)
    with open(os.path.join(out_dir, "tiles.json"), "w", encoding="utf-8") as f:
        json.dump(tiles_meta, f)

    # indice globale degli snapshot disponibili (l'app lo legge all'avvio)
    snap_root = os.path.join(HERE, "snapshot")
    dates = []
    for d in sorted(os.listdir(snap_root)):
        mf = os.path.join(snap_root, d, "manifest.json")
        if os.path.isdir(os.path.join(snap_root, d)) and os.path.exists(mf):
            try:
                with open(mf, encoding="utf-8") as fh:
                    m = json.load(fh)
                dates.append({"date": d, "product": m.get("product"),
                              "zmin": m.get("zmin"), "zmax": m.get("zmax"),
                              "tiles_total": m.get("tiles_total")})
            except Exception:
                pass
    with open(os.path.join(snap_root, "index.json"), "w", encoding="utf-8") as f:
        json.dump({"updated_utc": now_utc, "snapshots": dates}, f, indent=2)

    print("\nSnapshot %s pronto: %d tile (%d con dato, %d vuoti) -> %s"
          % (date, total, ok, empty, out_dir))
    print("Indice aggiornato: %d snapshot disponibili." % len(dates))


if __name__ == "__main__":
    main()
