// Copies the finished site (index.html, models, textures, fonts, icons) into www/ for Capacitor.
import fs from 'node:fs'; import path from 'node:path';
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..'), out = path.join(root, 'www');
fs.rmSync(out, {recursive:true, force:true}); fs.mkdirSync(out);
const keep = f => /^[0-9a-f]{32}\.(bin|webp)$/.test(f) || ['index.html', 'manifest.webmanifest', 'apple-touch-icon.png', 'icon-192.png', 'icon-512.png', 'privacy.html', 'impressum.html', 'credits.html'].includes(f);
let n = 0, bytes = 0;
for (const f of fs.readdirSync(root)) if (keep(f)){ fs.copyFileSync(path.join(root, f), path.join(out, f)); n++; bytes += fs.statSync(path.join(out, f)).size; }
fs.cpSync(path.join(root, 'fonts'), path.join(out, 'fonts'), {recursive:true});
console.log(`www/: ${n} files, ${(bytes / 1048576).toFixed(1)} MB`);
