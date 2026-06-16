/* =============================================================================
 * FILE: gara_plan.js
 * App: IschiaFishing - rotte manche DATA-DRIVEN, waypoint TUTTI DENTRO il campo
 * Aggiornato: 2026-06-16
 * Correzioni: (1) tutti i waypoint validati DENTRO il quadrilatero (point-in-polygon);
 *   (2) si pesca FINO alle 15:30 - l'ultimo waypoint e' uno spot in pesca, niente
 *   rientro anticipato (il rientro a Ostia e' DOPO il cessate).
 * Basi: DEM (banco 717m, drop-off, NE produttivo in-campo) + CHL reale (campo blu;
 *   piu' produttivo NE - il 148m piu' ricco e' FUORI campo, non pescabile) +
 *   marea + solunare verificati. Spot prime nel solunare in riflusso.
 * ========================================================================== */
window.GARA_PLAN = {
  routes: {
    A: { nome: "A - Produttivo NE poi scarpata (tonni->alalunga)", wp: [
      { m:0,   lat:41.680, lon:11.985, nota:"Start NE in-campo (acqua piu' produttiva del campo): cala lo spread per tonni", spot:false },
      { m:60,  lat:41.665, lon:11.965, nota:"Bordo NE nel solunare (tonni). NB: il 148m piu' ricco e' FUORI campo", spot:true },
      { m:120, lat:41.675, lon:11.990, nota:"SOLUNARE angolo NE in-campo: prime tonni", spot:true },
      { m:180, lat:41.620, lon:11.910, nota:"Scendi SW verso le strutture profonde", spot:false },
      { m:240, lat:41.554, lon:11.861, nota:"Banco 717m: alalunga sull'orlo", spot:true },
      { m:300, lat:41.530, lon:11.873, nota:"Drop-off 76% / 924m: spada profondo, stop&go", spot:true },
      { m:360, lat:41.560, lon:11.885, nota:"Muri / orlo banco lato W", spot:true },
      { m:450, lat:41.585, lon:11.910, nota:"Ultima passata sulle strutture: IN PESCA fino allo scadere (15:30)", spot:true }
    ]},
    B: { nome: "B - Scarpata profonda (alalunga/spada, blu)", wp: [
      { m:0,   lat:41.600, lon:11.900, nota:"Arrivo settore SW (acqua blu), orlo del 500m", spot:false },
      { m:60,  lat:41.570, lon:11.870, nota:"Sul 1000m / fianco del banco", spot:false },
      { m:120, lat:41.554, lon:11.861, nota:"BANCO 717m nel solunare: alalunga sull'orlo", spot:true },
      { m:180, lat:41.530, lon:11.873, nota:"Drop-off 76% (parete 924m): spada profondo, stop&go", spot:true },
      { m:240, lat:41.510, lon:11.882, nota:"Muri profondi SW (974-987m)", spot:true },
      { m:300, lat:41.555, lon:11.855, nota:"Risali l'orlo del banco lato W", spot:false },
      { m:360, lat:41.580, lon:11.890, nota:"Passata sul banco", spot:true },
      { m:450, lat:41.540, lon:11.870, nota:"Ultima passata sui muri: IN PESCA fino allo scadere (15:30)", spot:true }
    ]},
    C: { nome: "C - Bordo NE produttivo in-campo (tonni)", wp: [
      { m:0,   lat:41.685, lon:11.990, nota:"Bordo NE in-campo (acqua produttiva): cala lo spread", spot:false },
      { m:60,  lat:41.670, lon:11.960, nota:"Lavora l'angolo NE verso il bordo", spot:false },
      { m:120, lat:41.680, lon:11.985, nota:"SOLUNARE NE in-campo: tonni", spot:true },
      { m:180, lat:41.660, lon:11.945, nota:"Scendi sulla 200-300m in-campo", spot:true },
      { m:240, lat:41.640, lon:11.920, nota:"Break in-campo: tunnidi / aguglia", spot:true },
      { m:300, lat:41.670, lon:11.970, nota:"Risali il bordo NE produttivo", spot:false },
      { m:360, lat:41.685, lon:11.995, nota:"Angolo NE: passata", spot:true },
      { m:450, lat:41.665, lon:11.955, nota:"Ultima passata NE: IN PESCA fino allo scadere (15:30)", spot:true }
    ]}
  },
  spots: [
    { lat:41.675,   lon:11.990,   nome:"NE produttivo in-campo (tonni; il 148m piu' ricco e' fuori)" },
    { lat:41.55417, lon:11.86146, nome:"Banco 717m (alalunga)" },
    { lat:41.53021, lon:11.87292, nome:"Drop-off 76% / 924m (spada)" }
  ],
  manche: [
    { id:1, giorno:"Venerdi 26 giugno", date:"2026-06-26", solunare:"09:22-11:22", alta:"07:54", bassa:"14:09" },
    { id:2, giorno:"Sabato 27 giugno",  date:"2026-06-27", solunare:"10:09-12:09", alta:"08:42", bassa:"14:49" }
  ]
};
