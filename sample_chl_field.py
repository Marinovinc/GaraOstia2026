# -*- coding: utf-8 -*-
"""
Campiona la clorofilla REALE (Copernicus MED L4 gap-free) su una griglia sul campo
gara, via WMTS GetFeatureInfo (pubblico, no account). Analizza: min/max, fronte
(gradiente/mediana), zona produttiva vs blu. Output: chl_field.json + stampa analisi.
Uso: python sample_chl_field.py [YYYY-MM-DD]   (default: ieri)
"""
import sys, math, json, datetime, time
import urllib.request

WMTS = "https://wmts.marine.copernicus.eu/teroWmts"
PRODUCT = "OCEANCOLOUR_MED_BGC_L4_NRT_009_142"
DATASET = "cmems_obs-oc_med_bgc-plankton_nrt_l4-gapfree-multi-1km_P1D_202207"
VAR = "CHL"
# bbox campo (un filo interno)
LON0, LON1, LAT0, LAT1 = 11.78, 12.095, 41.485, 41.700
N = 16   # griglia NxN
Z = 12


def tilexy(lat, lon, z):
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n
    y = (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n
    col = int(x); row = int(y)
    i = int((x - col) * 256); j = int((y - row) * 256)
    return col, row, i, j


def sample(lat, lon, date):
    col, row, i, j = tilexy(lat, lon, Z)
    url = (WMTS + "?service=WMTS&version=1.0.0&request=GetFeatureInfo"
           "&layer=" + PRODUCT + "/" + DATASET + "/" + VAR +
           "&style=cmap:jet&TileMatrixSet=EPSG:3857"
           "&TileMatrix=%d&TileRow=%d&TileCol=%d&I=%d&J=%d&infoformat=text/xml&TIME=%s"
           % (Z, row, col, i, j, date))
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "IschiaFishing/1.0"})
        t = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "ignore")
        import re
        m = re.search(r'uom="([^"]*)"\s*>([\-0-9.eE]+)<', t)
        return float(m.group(2)) if m else None
    except Exception:
        return None


def main():
    date = sys.argv[1] if len(sys.argv) > 1 else (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    lats = [LAT1 - (LAT1 - LAT0) * r / (N - 1) for r in range(N)]   # N->S
    lons = [LON0 + (LON1 - LON0) * c / (N - 1) for c in range(N)]
    grid = []
    vals = []
    for r, la in enumerate(lats):
        rowv = []
        for c, lo in enumerate(lons):
            v = sample(la, lo, date)
            rowv.append(v)
            if v is not None and v == v:
                vals.append((v, la, lo))
            time.sleep(0.04)
        grid.append(rowv)
        print("riga %2d/%d lat %.3f fatta" % (r + 1, N, la))

    json.dump({"date": date, "lats": lats, "lons": lons, "grid": grid},
              open("chl_field.json", "w"), indent=0)

    if not vals:
        print("NESSUN valore (data senza dato?)"); return
    vs = sorted(v for v, _, _ in vals)
    lo_v, hi_v, med = vs[0], vs[-1], vs[len(vs)//2]
    print("\n=== ANALISI CHL %s (%d punti) ===" % (date, len(vals)))
    print("min %.3f  mediana %.3f  max %.3f mg/m3" % (lo_v, med, hi_v))
    hi = max(vals); lo = min(vals)
    print("MAX (piu' produttivo) %.3f @ %.4fN %.4fE" % (hi[0], hi[1], hi[2]))
    print("MIN (piu' blu)        %.3f @ %.4fN %.4fE" % (lo[0], lo[1], lo[2]))
    # baricentro produttivo (sopra mediana) e blu (sotto)
    prod = [(la, lo2) for v, la, lo2 in vals if v >= med]
    blue = [(la, lo2) for v, la, lo2 in vals if v < med]
    def cen(pts): return (sum(p[0] for p in pts)/len(pts), sum(p[1] for p in pts)/len(pts))
    if prod: print("baricentro PRODUTTIVO (>=mediana): %.4fN %.4fE" % cen(prod))
    if blue: print("baricentro BLU (<mediana):         %.4fN %.4fE" % cen(blue))


if __name__ == "__main__":
    main()
