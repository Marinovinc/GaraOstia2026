# -*- coding: utf-8 -*-
"""
Estrae la finestra del campo gara dal DEM EMODnet F5_2024.asc (~115m),
localizza il BANCO (punto piu' basso = piu' alto del fondo) dentro il campo,
e genera isobate accurate -> isobate_hr.js (window.ISOBATE, [lon,lat]).
"""
import os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path as MplPath

ASC = r"C:\Users\marin\Downloads\f5_bathy\F5_2024.asc"
HERE = os.path.dirname(os.path.abspath(__file__))
FIELD = [(12.00272,41.70370),(12.09808,41.53707),(11.88478,41.47762),(11.77377,41.63045)]
LEVELS = [100,200,300,500,700,1000]
# finestra (lon/lat) con margine
LON0,LON1,LAT0,LAT1 = 11.74,12.13,41.45,41.72


def main():
    import itertools
    with open(ASC) as f:
        hdr = {}
        for _ in range(6):
            k,v = f.readline().split()
            hdr[k.lower()] = float(v)
        ncols=int(hdr["ncols"]); nrows=int(hdr["nrows"])
        xll=hdr["xllcorner"]; yll=hdr["yllcorner"]; cs=hdr["cellsize"]; nod=hdr["nodata_value"]

        c0=max(0,int((LON0-xll)/cs)); c1=min(ncols-1,int((LON1-xll)/cs))
        r0=max(0,int(nrows-1-(LAT1-yll)/cs)); r1=min(nrows-1,int(nrows-1-(LAT0-yll)/cs))
        # valori a 10 per riga, stream row-major: indice flat = R*ncols + c
        PER=10
        fmin=r0*ncols+c0; fmax=r1*ncols+c1
        L0=fmin//PER; L1=fmax//PER
        buf=[]
        for line in itertools.islice(f, L0, L1+1):
            buf.extend(line.split())
        base=L0*PER
        rows=[]; lats=[]
        for ridx in range(r0,r1+1):
            off=ridx*ncols
            rows.append([float(buf[off+c-base]) for c in range(c0,c1+1)])
            lats.append(yll+(nrows-1-ridx)*cs)

    arr=np.array(rows)                       # [N->S, W->E]
    lons=np.array([xll+c*cs for c in range(c0,c1+1)])
    lats=np.array(lats)
    valid=(arr!=nod)
    sea=valid & (arr<0)
    depth=np.where(sea, -arr, np.nan)        # profondita' positiva, NaN su terra/nodata
    print("finestra %dx%d  prof min/max sea: %.0f / %.0f m" % (arr.shape[0],arr.shape[1],
          np.nanmin(depth), np.nanmax(depth)))

    # BANCO isolato (chart 673/726m): rilevazione per PROMINENZA - punto piu' alto del fondo
    # rispetto ai dintorni (~3km), nella fascia 400-950m dentro il campo (esclude shelf NE).
    from scipy.ndimage import uniform_filter
    poly=MplPath(FIELD)
    df=np.where(np.isnan(depth), 9999.0, depth)
    ring=uniform_filter(df, size=27, mode="nearest")   # 27 celle ~3 km
    prom=ring-depth                                     # >0 = piu' basso dei dintorni (rilievo)
    mask=np.zeros(depth.shape, bool)
    for iy in range(depth.shape[0]):
        for ix in range(depth.shape[1]):
            d=depth[iy,ix]
            if np.isnan(d) or d<400 or d>950: continue
            if poly.contains_point((lons[ix],lats[iy])): mask[iy,ix]=True
    pm=np.where(mask, prom, -9999.0)
    iy,ix=np.unravel_index(int(np.argmax(pm)), pm.shape)
    best=(depth[iy,ix], lats[iy], lons[ix])
    print("BANCO (prominenza %.0f m): prof %.0f m  @ %.5f N, %.5f E" % (pm[iy,ix], best[0], best[1], best[2]))

    # DROP-OFF: pendenza del fondo (slope %), spot piu' ripidi (pareti) nel campo
    import math
    mlat=111320.0*cs
    mlon=111320.0*math.cos(math.radians(float(lats.mean())))*cs
    gy,gx=np.gradient(depth)
    slope=np.sqrt((gx/mlon)**2+(gy/mlat)**2)*100.0     # percento (dislivello/distanza)
    cands=[]
    for jy in range(depth.shape[0]):
        for jx in range(depth.shape[1]):
            d=depth[jy,jx]; s=slope[jy,jx]
            if np.isnan(d) or np.isnan(s) or d<150 or d>1000: continue
            if poly.contains_point((lons[jx],lats[jy])): cands.append((s,d,lats[jy],lons[jx]))
    cands.sort(reverse=True)
    def dkm(a,b): return math.hypot((a[2]-b[2])*111.0,(a[3]-b[3])*111.0*math.cos(math.radians(a[2])))
    sel=[]
    for c in cands:
        if all(dkm(c,s)>=2.0 for s in sel): sel.append(c)
        if len(sel)>=8: break
    drops=[{"lat":round(c[2],5),"lon":round(c[3],5),"slope_pct":round(c[0]),"prof_m":round(c[1])} for c in sel]
    print("DROP-OFF spot (slope%/prof):", [(d["slope_pct"],d["prof_m"]) for d in drops])
    with open(os.path.join(HERE,"dropoff.js"),"w",encoding="utf-8") as fo:
        fo.write("/* dropoff.js - spot drop-off (pareti ripide) da DEM EMODnet F5. */\n")
        fo.write("window.DROPOFF = "+json.dumps(drops)+";\n")

    # ISOBATE accurate via contour
    LON,LAT=np.meshgrid(lons,lats)
    cset=plt.contour(LON,LAT,depth,levels=LEVELS)
    out=[]
    try: allsegs=cset.allsegs
    except Exception: allsegs=None
    if allsegs is not None:
        for i,lev in enumerate(cset.levels):
            for seg in allsegs[i]:
                c=[[round(float(p[0]),4),round(float(p[1]),4)] for p in seg[::2]]
                if len(c)>=2: out.append({"el":int(lev),"c":c})
    print("linee isobate generate:", len(out))
    with open(os.path.join(HERE,"isobate.js"),"w",encoding="utf-8") as fo:
        fo.write("/* isobate.js - isobate da DEM EMODnet F5_2024 (~115m), campo Ostia. [lon,lat]. */\n")
        fo.write("window.ISOBATE = "+json.dumps(out)+";\n")
    # salva anche la coord banco per l'app
    with open(os.path.join(HERE,"banco.json"),"w",encoding="utf-8") as fo:
        json.dump({"prof_m":round(best[0]), "lat":round(best[1],5), "lon":round(best[2],5)}, fo)
    print("isobate.js + banco.json scritti")


if __name__=="__main__":
    main()
