# Crown of Sand

Build. Defend. Conquer. Ein Burgen-Strategiespiel für Browser, iPhone und iPad.

- **Spielen (Web-App):** https://joklug10-commits.github.io/Crown-of-sand/ – in Safari öffnen, Teilen › „Zum Home-Bildschirm“.
- **Datenschutz:** [privacy.html](privacy.html) · **Impressum:** [impressum.html](impressum.html) · **Lizenzen:** [credits.html](credits.html)

## Aufbau

| Ordner / Datei | Inhalt |
| --- | --- |
| `src/crownofsand.html` | Quelle des Spiels (Artifact-Fassung, Modelle als `/_blob/<id>`) |
| `index.html` | gebaute Website: lädt Modelle binär (`<id>.bin`), Texturen (`<id>.webp`) und lokale Schriften (`fonts/`) |
| `tools/build_site.py` | baut `index.html` aus `src/` |
| `tools/build_www.mjs` | kopiert die Website nach `www/` für die iOS-App |
| `ios/` | Capacitor-Projekt der iOS-App (Bundle-ID `de.joklug.crownofsand`) |
| `assets/` | Quelle für App-Icon und Startbildschirm |
| `.github/workflows/ios-testflight.yml` | baut die App auf einem Mac von GitHub und lädt sie zu TestFlight |
| `codemagic.yaml` | Alternative mit Codemagic |
| `docs/store/` | App-Store-Texte (de/en) und Screenshots |

## Website aktualisieren

```
python3 tools/build_site.py
git commit -am "…" && git push
```

## iOS-App ohne eigenen Mac bauen

1. Apple Developer Program beitreten (99 € pro Jahr).
2. In App Store Connect die App mit der Bundle-ID `de.joklug.crownofsand` anlegen.
3. Unter Benutzer und Zugriff › Integrationen einen App-Store-Connect-API-Schlüssel (Rolle „App Manager“) erstellen und die `.p8`-Datei herunterladen.
4. Im GitHub-Repo unter Settings › Secrets and variables › Actions anlegen: `APPLE_TEAM_ID`, `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_KEY_P8`.
5. Actions › „iOS TestFlight“ › Run workflow. Nach ca. 20 Minuten erscheint der Build in TestFlight.

Lokal (mit Mac): `npm ci && npm run ios:sync && npx cap open ios`.
