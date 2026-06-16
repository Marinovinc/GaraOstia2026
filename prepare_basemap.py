# -*- coding: utf-8 -*-
"""
=============================================================================
App: IschiaFishing - prepare_basemap.py
Creato: 2026-06-14
Descrizione: scarica UNA VOLTA i tile della mappa base (ESRI World Imagery,
             satellite) per la sola area del campo gara, per l'uso OFFLINE in
             barca. La costa non cambia: non serve rigenerarlo ogni giorno.
Uso:
    python prepare_basemap.py [--zmin 7] [--zmax 12]
Output:
    basemap/esri/<z>/<x>/<y>.png  +  basemap/index.json
NOTA ToS: ESRI World Imagery e' soggetto a termini d'uso. Caching per area
          piccola, uso personale/non commerciale (ASD): generalmente tollerato.
          Non ridistribuire i tile.
=============================================================================
"""
import os, json, math, argparse, datetime, time
import urllib.request

ESRI = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/%d/%d/%d"
BBOX = {"lon_min": 11.7738, "lat_min": 41.4776, "lon_max": 12.0981, "lat_max": 41.7037}
HERE = os.path.dirname(os.path.abspath(__file__))


def deg2tile(lat, lon, z):
    n = 2 ** z
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n)
    return x, y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zmin", type=int, default=7)
    ap.add_argument("--zmax", type=int, default=12)
    args = ap.parse_args()

    out = os.path.join(HERE, "basemap", "esri")
    total, ok = 0, 0
    rel_paths = []
    for z in range(args.zmin, args.zmax + 1):
        x0, y0 = deg2tile(BBOX["lat_max"], BBOX["lon_min"], z)
        x1, y1 = deg2tile(BBOX["lat_min"], BBOX["lon_max"], z)
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                total += 1
                dest = os.path.join(out, str(z), str(x))
                os.makedirs(dest, exist_ok=True)
                fpath = os.path.join(dest, "%d.png" % y)
                rel_paths.append("esri/%d/%d/%d.png" % (z, x, y))
                if os.path.exists(fpath) and os.path.getsize(fpath) > 0:
                    ok += 1
                    continue
                url = ESRI % (z, y, x)   # ESRI usa /z/y/x
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "IschiaFishing/1.0"})
                    with urllib.request.urlopen(req, timeout=30) as r:
                        data = r.read()
                    with open(fpath, "wb") as f:
                        f.write(data)
                    ok += 1
                except Exception as e:
                    print("  ERR z%d x%d y%d: %s" % (z, x, y, e))
                time.sleep(0.04)
        print("z%d completato (x %d..%d, y %d..%d)" % (z, min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1)))

    index = {
        "provider": "esri", "name": "ESRI World Imagery (satellite)",
        "bbox": BBOX, "zmin": args.zmin, "zmax": args.zmax,
        "tiles_total": total, "tiles_ok": ok,
        "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    with open(os.path.join(HERE, "basemap", "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    with open(os.path.join(HERE, "basemap", "tiles.json"), "w", encoding="utf-8") as f:
        json.dump(rel_paths, f)
    print("\nBasemap offline pronta: %d/%d tile -> %s" % (ok, total, out))


if __name__ == "__main__":
    main()
