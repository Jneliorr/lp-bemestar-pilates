import assert from 'node:assert/strict';
import { readFile, access } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { siteConfig, whatsappUrl } from '../config.js';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
for (const page of ['index.html', 'privacidade.html']) {
  const html = await readFile(resolve(root, page), 'utf8');
  assert.match(html, /<html lang="pt-BR">/, `${page}: idioma`);
  assert.equal((html.match(/<h1(?:\s[^>]*)?>/g) || []).length, 1, `${page}: apenas um H1`);
  const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
  assert.equal(new Set(ids).size, ids.length, `${page}: IDs únicos`);
  for (const match of html.matchAll(/(?:src|href)="([^"#?]+)(?:[?#][^"]*)?"/g)) {
    if (/^(?:https?:|tel:|data:)/.test(match[1])) continue;
    await access(resolve(root, match[1]));
  }
  for (const match of html.matchAll(/href="#([^"]+)"/g)) assert.ok(ids.includes(match[1]), `${page}: âncora ${match[1]}`);
  for (const match of html.matchAll(/<img\b[^>]*>/g)) {
    assert.match(match[0], /alt="[^"]+"/, `${page}: descrição de imagem`);
    assert.match(match[0], /width="\d+"/, `${page}: largura de imagem`);
    assert.match(match[0], /height="\d+"/, `${page}: altura de imagem`);
  }
  for (const match of html.matchAll(/<a\b[^>]*target="_blank"[^>]*>/g)) assert.match(match[0], /rel="noopener noreferrer"/, `${page}: link externo protegido`);
  assert.ok(!/href="(?:#|javascript:)["]/.test(html), `${page}: sem links vazios`);
  assert.ok(!/9773381|27 anos|há 6 anos|CREFITO/i.test(html), `${page}: sem informações não confirmadas`);
}
const html = await readFile(resolve(root, 'index.html'), 'utf8');
assert.equal((html.match(/<!-- \d+\./g) || []).length, 15, '15 blocos editoriais');
assert.equal((html.match(/<details>/g) || []).length, 5, '5 perguntas frequentes nativas');
for (const key of [...html.matchAll(/data-whatsapp="([^"]+)"/g)].map(match => match[1])) {
  assert.ok(siteConfig.messages[key], `Mensagem do WhatsApp: ${key}`);
  const url = new URL(whatsappUrl(key));
  assert.equal(url.hostname, 'wa.me');
  assert.equal(url.pathname, `/${siteConfig.phone}`);
  assert.equal(url.searchParams.get('text'), siteConfig.messages[key]);
}
assert.match(siteConfig.phone, /^55\d{11}$/);
assert.equal(siteConfig.posts.length, 2);
const css = await readFile(resolve(root, 'styles.css'), 'utf8');
for (const match of css.matchAll(/url\(['"]?([^)'"\s]+)['"]?\)/g)) await access(resolve(root, match[1]));
assert.match(css, /prefers-reduced-motion:reduce/);
assert.match(css, /:focus-visible/);
console.log('Verificação concluída: páginas, assets, âncoras, metadados básicos, WhatsApp, FAQ e conteúdo.');
