/* Service worker IschiaFishing - cache app shell per uso offline (modalita barca).
   Strategia: cache-first per gli asset locali; rete per i tile satellitari live. */
const CACHE = 'ischiafishing-v22';
const SHELL = [
  'index.html', 'campo_gara.js', 'front_drift.js', 'gara_plan.js', 'isobate.js', 'dropoff.js', 'manifest.webmanifest',
  'lib/leaflet.js', 'lib/leaflet.css', 'icon-192.png', 'icon-512.png'
];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) {
    // tile/servizi esterni: rete, fallback cache
    e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
    return;
  }
  // App shell (html/js/webmanifest): NETWORK-FIRST -> sempre aggiornato online, cache solo offline.
  if (url.pathname.endsWith('/') || /\.(html|js|webmanifest)$/.test(url.pathname)) {
    e.respondWith(
      fetch(e.request).then(resp => { const c = resp.clone(); caches.open(CACHE).then(ca => ca.put(e.request, c)); return resp; })
        .catch(() => caches.match(e.request))
    );
    return;
  }
  // Resto same-origin (tile snapshot, batimetria locale, lib, icone): cache-first.
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(resp => {
    const copy = resp.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return resp;
  }).catch(() => r)));
});
