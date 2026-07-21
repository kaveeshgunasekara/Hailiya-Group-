/**
 * Hailiya Group — Replit dev server (REPLIT PREVIEW ONLY — NOT USED IN PRODUCTION)
 *
 * This file exists solely to work around a CORS limitation in the Replit
 * preview pane (origin: 127.0.0.1:5000), which is not on Sanity's CORS
 * allowlist. It is not deployed to cPanel, Vercel, Netlify, or anywhere else.
 *
 * The live site (cPanel / hailiya.com.au) serves netlify_deploy/ as plain
 * static files. index.html fetches Sanity data directly from apicdn.sanity.io
 * in the browser — no proxy, no server-side code required.
 */
const http  = require('http');
const https = require('https');
const fs    = require('fs');
const path  = require('path');
const url   = require('url');

const PORT       = 5000;
const STATIC_DIR = path.join(__dirname, 'netlify_deploy');

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css':  'text/css',
  '.js':   'application/javascript',
  '.json': 'application/json',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg':  'image/svg+xml',
  '.ico':  'image/x-icon',
  '.mp4':  'video/mp4',
  '.webp': 'image/webp',
  '.woff': 'font/woff',
  '.woff2':'font/woff2',
  '.ttf':  'font/ttf',
  '.txt':  'text/plain',
  '.xml':  'application/xml',
};

// ── Sanity reverse-proxy ──────────────────────────────────────────────────
// The browser calls  GET /sanity-proxy?query=...
// We forward it to  https://15fxxqgw.apicdn.sanity.io/... server-side.
const SANITY_HOST    = '15fxxqgw.apicdn.sanity.io';
const SANITY_BASE    = '/v2021-10-21/data/query/production';

function proxySanity(req, res) {
  const parsed   = url.parse(req.url, true);
  const query    = parsed.query.query || '';
  const sanityUrl = 'https://' + SANITY_HOST + SANITY_BASE +
                    '?query=' + encodeURIComponent(query);

  https.get(sanityUrl, { headers: { 'Accept': 'application/json' } }, (upstream) => {
    let body = '';
    upstream.on('data', chunk => { body += chunk; });
    upstream.on('end', () => {
      res.writeHead(200, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'no-store',
      });
      res.end(body);
    });
  }).on('error', (err) => {
    console.error('Sanity proxy error:', err.message);
    res.writeHead(502);
    res.end(JSON.stringify({ error: 'Sanity proxy failed', detail: err.message }));
  });
}

// ── Static file server ────────────────────────────────────────────────────
function serveStatic(req, res) {
  let reqPath = url.parse(req.url).pathname;

  // Strip trailing slash (except root)
  if (reqPath !== '/' && reqPath.endsWith('/')) reqPath = reqPath.slice(0, -1);

  // Default to index.html
  if (reqPath === '/') reqPath = '/index.html';

  const filePath = path.join(STATIC_DIR, reqPath);

  // Security: prevent path traversal
  if (!filePath.startsWith(STATIC_DIR)) {
    res.writeHead(403); res.end('Forbidden'); return;
  }

  fs.stat(filePath, (err, stat) => {
    if (err || !stat.isFile()) {
      // Try appending .html
      const htmlPath = filePath + '.html';
      fs.stat(htmlPath, (err2, stat2) => {
        if (!err2 && stat2.isFile()) {
          sendFile(htmlPath, res);
        } else {
          res.writeHead(404); res.end('Not found');
        }
      });
      return;
    }
    sendFile(filePath, res);
  });
}

function sendFile(filePath, res) {
  const ext  = path.extname(filePath).toLowerCase();
  const mime = MIME[ext] || 'application/octet-stream';
  const stream = fs.createReadStream(filePath);
  res.writeHead(200, { 'Content-Type': mime });
  stream.pipe(res);
  stream.on('error', () => { res.end(); });
}

// ── Main request router ───────────────────────────────────────────────────
const server = http.createServer((req, res) => {
  const pathname = url.parse(req.url).pathname;
  if (pathname === '/sanity-proxy') {
    proxySanity(req, res);
  } else {
    serveStatic(req, res);
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log('Hailiya dev server running on http://0.0.0.0:' + PORT);
  console.log('Sanity proxy: GET /sanity-proxy?query=<GROQ>');
});
