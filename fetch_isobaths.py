# -*- coding: utf-8 -*-
"""
Scarica le isobate (EMODnet emodnet:contours) sul bbox del nuovo campo gara Ostia,
filtra alle profondita' utili, semplifica, scrive isobate.js (window.ISOBATE, [lon,lat]).
Uso: python fetch_isobaths.py
"""
import urllib.request, json, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
BBOX = "41.45,11.74,41.72,12.12"           # lat,lon - nuovo campo + margine
TARGET = {50, 100, 200, 500, 1000, 1500}   # profondita' (m) di interesse


def decimate(coords, step):
    if len(coords) <= step + 1:
        return coords
    out = coords[::step]
    if out[-1] != coords[-1]:
        out.append(coords[-1])
    return out


def main():
    url = ("https://ows.emodnet-bathymetry.eu/wfs?service=WFS&version=2.0.0&request=GetFeature"
           "&typeName=emodnet:contours&bbox=" + BBOX + ",urn:ogc:def:crs:EPSG::4326"
           "&outputFormat=application/json&count=12000")
    req = urllib.request.Request(url, headers={"User-Agent": "IschiaFishing/1.0"})
    j = json.loads(urllib.request.urlopen(req, timeout=120).read())
    feats = j.get("features", [])
    print("feature totali:", len(feats))
    elevs = Counter(abs(f["properties"].get("elevation", 0)) for f in feats)
    print("elevazioni disponibili:", dict(sorted(elevs.items())))

    out = []
    for f in feats:
        el = abs(f["properties"].get("elevation", 0))
        if el not in TARGET:
            continue
        g = f["geometry"]
        lines = g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]
        for ln in lines:
            c = [[round(p[0], 4), round(p[1], 4)] for p in decimate(ln, 3)]
            if len(c) >= 2:
                out.append({"el": el, "c": c})

    print("linee isobate filtrate:", len(out))
    with open(os.path.join(HERE, "isobate.js"), "w", encoding="utf-8") as fo:
        fo.write("/* isobate.js - isobate EMODnet (emodnet:contours) bbox nuovo campo Ostia. [lon,lat]. */\n")
        fo.write("window.ISOBATE = " + json.dumps(out) + ";\n")
    sz = os.path.getsize(os.path.join(HERE, "isobate.js"))
    print("isobate.js scritto (%d KB)" % (sz // 1024))


if __name__ == "__main__":
    main()
