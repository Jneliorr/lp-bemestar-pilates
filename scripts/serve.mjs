import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { resolve, extname, dirname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const port = Number(process.env.PORT || 4173);
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2', '.xml': 'application/xml', '.txt': 'text/plain; charset=utf-8' };
http.createServer(async (req, res) => {
  try {
    const pathname = decodeURIComponent(new URL(req.url, `http://localhost:${port}`).pathname);
    const file = resolve(root, `.${pathname === '/' ? '/index.html' : pathname}`);
    if (file !== root && !file.startsWith(root + sep)) { res.writeHead(403).end(); return; }
    const relative = file.slice(root.length + 1).replaceAll('\\', '/');
    const allowed = ['assets/', 'index.html', 'privacidade.html', 'styles.css', 'app.js', 'config.js', 'robots.txt', 'sitemap.xml'];
    if (relative.split('/').some(part => part.startsWith('.')) || !allowed.some(path => path.endsWith('/') ? relative.startsWith(path) : relative === path)) {
      res.writeHead(404).end('Não encontrado'); return;
    }
    if (!(await stat(file)).isFile()) { res.writeHead(404).end('Não encontrado'); return; }
    res.writeHead(200, { 'Content-Type': types[extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' });
    res.end(await readFile(file));
  } catch { res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' }).end('Página não encontrada'); }
}).listen(port, '127.0.0.1', () => console.log(`Local: http://localhost:${port}`));
