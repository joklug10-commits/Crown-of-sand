#!/usr/bin/env python3
"""Builds index.html (GitHub Pages + iOS app) from src/crownofsand.html.

src/crownofsand.html is the artifact version: models as /_blob/<id> (base64 text),
fonts from Google Fonts. The site version loads binary models (./<id>.bin) and
textures (./<id>.webp) from this folder and uses the local fonts in fonts/.

    python3 tools/build_site.py            # writes index.html
    python3 tools/build_site.py --assets DIR   # also converts DIR/<id>.txt (base64) to ./<id>.bin
"""
import base64, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src', 'crownofsand.html')
HEAD = '''<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Crown of Sand">
<meta name="theme-color" content="#120d08">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
'''

def convert(assets):
    n = 0
    for f in os.listdir(assets):
        if f.endswith('.txt') and re.fullmatch(r'[0-9a-f]{32}\.txt', f):
            data = base64.b64decode(open(os.path.join(assets, f)).read().strip())
            open(os.path.join(ROOT, f[:-4] + '.bin'), 'wb').write(data); n += 1
        elif f.endswith('.webp'):
            dst = os.path.join(ROOT, f)
            if not os.path.exists(dst):
                open(dst, 'wb').write(open(os.path.join(assets, f), 'rb').read()); n += 1
    print('converted', n, 'assets')

def build():
    s = open(SRC, encoding='utf-8').read()
    def blob(m):
        i = m.group(1)
        if os.path.exists(os.path.join(ROOT, i + '.bin')): return './' + i + '.bin'
        if os.path.exists(os.path.join(ROOT, i + '.webp')): return './' + i + '.webp'
        raise SystemExit('missing asset ' + i)
    s = re.sub(r'/_blob/([0-9a-f]{32})', blob, s)
    s = re.sub(r'<link rel="preconnect" href="https://fonts\.g[^>]*>\n?', '', s)
    s = re.sub(r'<link href="https://fonts\.googleapis\.com/[^>]*>', '<link rel="stylesheet" href="fonts/fonts.css">', s)
    vp = '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    assert vp in s
    s = s.replace(vp, vp + HEAD, 1)
    assert 'fonts.googleapis' not in s and '/_blob/' not in s
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(s)
    print('index.html', len(s) // 1024, 'KB')

if __name__ == '__main__':
    if '--assets' in sys.argv: convert(sys.argv[sys.argv.index('--assets') + 1])
    build()
