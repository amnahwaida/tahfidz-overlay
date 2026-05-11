const CACHE_NAME = 'tahfidz-cache-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/icon.png',
  '/manifest.json',
  '/data/surah_list.json'
];

// Install Service Worker
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    })
  );
});

// Fetch Assets
self.addEventListener('fetch', (event) => {
  // Hanya cache file statis, jangan cache /sync karena itu real-time
  if (event.request.url.includes('/sync')) {
    return fetch(event.request);
  }

  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
