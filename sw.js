// Polaris offline helper.
// The app: network first, so a new version shows up right away; the saved copy when there's no connection,
// or when the connection is so slow that waiting would leave you staring at a blank screen.
// Fonts: the saved copy, refreshed in the background. Everything else (GitHub, Google, CDNs) is never cached here.
const CACHE = 'polaris-v2';
const SHELL = ['./index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png', './icon-maskable-512.png'];
const PAGE_WAIT = 4000;   // ms to wait for the network before showing the saved copy of the app
const FILE_WAIT = 8000;

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => Promise.all(SHELL.map((u) => c.add(u).catch(() => null)))).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)));
    // start fetching the page while this worker wakes up, instead of after
    if (self.registration.navigationPreload) { try { await self.registration.navigationPreload.enable(); } catch (err) {} }
    await self.clients.claim();
  })());
});

// a promise that settles with p, or fails after ms
function within(p, ms) {
  return new Promise((ok, no) => {
    const t = setTimeout(() => no(new Error('slow')), ms);
    p.then((v) => { clearTimeout(t); ok(v); }, (err) => { clearTimeout(t); no(err); });
  });
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  if (url.origin === self.location.origin) {
    const isPage = req.mode === 'navigate';
    // one saved copy per file: the page is always index.html, and query strings never pile up new entries
    const key = isPage ? new URL('./index.html', self.registration.scope).href : url.origin + url.pathname;
    let settle;
    e.waitUntil(new Promise((r) => { settle = r; }));   // keeps the worker alive until the saved copy is written
    const first = isPage && e.preloadResponse ? e.preloadResponse.then((r) => r || fetch(req)) : fetch(req);
    const net = first.then((res) => {
      if (res && res.ok && res.status === 200 && res.type === 'basic') {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put(key, copy)).catch(() => null).then(settle);
      } else settle();
      return res;
    }, (err) => { settle(); throw err; });
    net.catch(() => null);   // a late failure after the saved copy was shown is fine
    e.respondWith(
      within(net, isPage ? PAGE_WAIT : FILE_WAIT).catch(() =>
        caches.match(key, { ignoreSearch: true })
          .then((hit) => hit || (isPage ? caches.match('./') : null))
          .then((hit) => hit || net)   // nothing saved yet: keep waiting for the network
      ).catch(() => Response.error())
    );
    return;
  }

  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    let settle;
    e.waitUntil(new Promise((r) => { settle = r; }));
    const net = fetch(req).then((res) => {
      if (res && (res.ok || res.type === 'opaque')) {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => null).then(settle);
      } else settle();
      return res;
    }, (err) => { settle(); throw err; });
    net.catch(() => null);
    e.respondWith(caches.match(req).then((hit) => hit || net).catch(() => Response.error()));
  }
  // everything else (GitHub, Google, CDNs) goes straight to the network and is never cached
});
