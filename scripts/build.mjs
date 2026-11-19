import { cp, mkdir, rm } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve, dirname, join } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const out = join(root, 'dist');
if (dirname(out) !== root) throw new Error('Invalid build directory');
await rm(out, { recursive: true, force: true });
await mkdir(out, { recursive: true });
for (const file of ['index.html', 'privacidade.html', 'styles.css', 'app.js', 'config.js', 'robots.txt', 'sitemap.xml']) {
  await cp(join(root, file), join(out, file));
}
await cp(join(root, 'assets'), join(out, 'assets'), { recursive: true });
console.log('Build completo: dist/');
