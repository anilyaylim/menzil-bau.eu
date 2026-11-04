# menzil-bau.eu

Website for **Menzil-Bau**, a construction company in Lower Austria and Vienna.
Static HTML, ready for GitHub Pages, no build pipeline needed on the server.

- **Languages:** German (default, `/`), English (`/en/`), Turkish (`/tr/`)
- **Pages:** `index` (landing), `projekte`, `referenzen`, `zertifikate`, `kontakt`
- **Structure based on:** DKI-Makine-Landing (nav with machine parade and conveyor belt, scroll logo swap, mobile menu, problem/solution, card grids, CTA, footer)

## Updating content

All texts, numbers, addresses, projects and photo assignments live in **`tools/data.py`**.
After editing, rebuild all 15 pages:

```bash
python3 tools/build.py
```

Placeholders are marked `# PLATZHALTER` in `data.py`:

| What | Where |
|---|---|
| Hero and reference numbers (30+, 120+, …) | `T[lang]['hero']['stats']`, `p_referenzen.stats` |
| Address 1 (Austria) | `SITE['addr1']` |
| Certificates (placeholder seals) | `T[lang]['p_zertifikate']['badges']` |
| Project ↔ photo assignment | `PHOTOS` (`cat`), `featured.cards` |
| Form recipient | `SITE['form_endpoint']` (formsubmit.co) |

## Images

Source files (Dropbox exports) are optimised into `assets/img/photos` and `assets/img/plans`:

```bash
python3 tools/images.py <photos_dir> <plans_dir>
```

Requires Pillow. Photos are 1600 px plus 720 px thumbnails; plans are 2200 px plus 800 px thumbnails.

## Publishing (GitHub Pages)

Settings → Pages → *Deploy from a branch* → `main` / `(root)`.
