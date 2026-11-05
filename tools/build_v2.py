# -*- coding: utf-8 -*-
"""Builds the motion version (v2/index.html, German) from tools/data.py.

    python3 tools/build_v2.py
"""
import os, sys, html
from datetime import date
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from data import SITE, T, PLACES
from build import logo_a, ARROW, CAL, TEL, PIN

E = html.escape
t = T['de']
A = '../assets/img/'
YEAR = date.today().year

def lines(*parts, cls=''):
    """Big headline split into masked lines for the reveal animation."""
    return ''.join(f'<span class="line"><span{(" class=%s" % c) if c else ""}>{x}</span></span>' for x, c in parts)

ICON_PLAN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M3 3h18v18H3z"/><path d="M3 12h8V3M11 12v9M15 12h6"/></svg>'
ICON_BUILD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M2 20h20"/><path d="M5 20V9l7-5 7 5v11"/><path d="M9 20v-6h6v6"/></svg>'
ICON_KEY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/></svg>'
ROT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 3v6h-6"/></svg>'
PLAY = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4l13 8-13 8z"/></svg>'
DRAG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M8 12h8M5 9l-3 3 3 3M19 9l3 3-3 3"/></svg>'
PREV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 5l-7 7 7 7"/></svg>'
NEXT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 5l7 7-7 7"/></svg>'

svc_imgs = [A + 'plans/mattersburg-1-t.jpg', A + 'photos/f14-t.jpg', A + 'photos/f10-t.jpg', A + 'photos/f04-t.jpg', A + 'photos/f64-t.jpg', A + 'photos/f05-t.jpg']
services = ''.join(f'''<article class="svc">
        <div class="svc-img"><img src="{svc_imgs[i]}" alt="{E(n)} – Menzil-Bau" loading="lazy" draggable="false"></div>
        <div class="svc-body"><div class="svc-no">0{i + 1}</div><h3>{E(n)}</h3><p>{E(d)}</p>
          <div class="svc-tags">{''.join(f'<span>{E(x)}</span>' for x in tags)}</div></div>
      </article>''' for i, (n, d, tags) in enumerate(t['services']['items']))

stack = ''.join(f'''<div class="scard"><div class="scard-no">0{i + 1}</div><div><h3>{E(a)}</h3><p>{b}</p></div></div>''' for i, (a, b) in enumerate(t['why']['items']))
reviews = ''.join(f'''<figure class="rev"><div class="stars">★★★★★</div><blockquote>{E(q)}</blockquote>
        <figcaption><b>{E(n)}</b>{E(tag)} · {E(l)}</figcaption></figure>''' for tag, q, n, l in t['reviews']['items'])
marquee_items = ''.join(f'<span>{PIN.replace("ref-pin", "")}{E(p)}</span>' for p in PLACES)

MODELS = [
    ('efh', 'Einfamilienhaus', 'Zweigeschossiges Wohnhaus mit Satteldach, Garage und Terrasse – so wie wir es in Niederösterreich am häufigsten planen und bauen.',
     [('Geschosse', '2'), ('Dach', 'Satteldach'), ('Bauweise', 'Massivbau'), ('Extras', 'Garage, Terrasse')]),
    ('dh', 'Doppelhaus', 'Zwei gespiegelte Haushälften mit gemeinsamer Trennwand – effizient im Grundstück, eigenständig im Wohnen.',
     [('Einheiten', '2'), ('Geschosse', '2 je Hälfte'), ('Dach', 'Satteldach'), ('Bauweise', 'Massivbau')]),
    ('mfh', 'Wohnhausanlage', 'Dreigeschossiger Wohnbau mit Balkonen und Walmdach – für Bauträger, Investoren und Gemeinden.',
     [('Geschosse', '3'), ('Dach', 'Walmdach'), ('Balkone', 'je Obergeschoss'), ('Bauweise', 'Massivbau')]),
]
model_tabs = ''.join(f'<button class="model-tab{" on" if i == 0 else ""}" type="button" data-model="{k}" aria-pressed="{"true" if i == 0 else "false"}">{E(n)}</button>' for i, (k, n, _, _) in enumerate(MODELS))
model_data = ''.join(f'''<template id="info-{k}"><span class="tag">Modellbeispiel</span><h3>{E(n)}</h3><p>{E(d)}</p>
      <dl>{''.join(f'<dt>{E(a)}</dt><dd>{E(b)}</dd>' for a, b in specs)}</dl></template>''' for k, n, d, specs in MODELS)

page = f'''<!DOCTYPE html>
<html lang="de" translate="no">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Menzil-Bau · Bauen mit Verlass</title>
<meta name="description" content="{E(t['meta']['index'][1])}">
<meta name="google" content="notranslate">
<meta name="theme-color" content="#121417">
<link rel="icon" href="../assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="v2.css">
</head>
<body>

<header class="nav" aria-label="Hauptnavigation">
  <a class="nav-logo" href="#top" aria-label="Menzil-Bau">{logo_a(w=150)}</a>
  <ul class="nav-links">
    <li><a href="#leistungen">Leistungen</a></li>
    <li><a href="#bauablauf">Bauablauf</a></li>
    <li><a href="#modelle">3D-Modelle</a></li>
    <li><a href="#projekte">Projekte</a></li>
    <li><a href="../kontakt.html">Kontakt</a></li>
  </ul>
  <div class="nav-right">
    <a class="pill pill-ghost pill-sm" href="../index.html">Klassisch</a>
    <a class="pill pill-red nav-cta" href="{SITE['calendar']}" target="_blank" rel="noopener">{E(t['nav']['cta'])}</a>
    <button class="nav-burger" type="button" aria-label="Menü"><span></span></button>
  </div>
</header>

<main id="top">
<!-- HERO -->
<section class="hero">
  <div class="hero-card">
    <div class="hero-media" aria-hidden="true">
      <img src="{A}photos/f01.jpg" alt=""><img src="{A}photos/f13.jpg" alt=""><img src="{A}photos/f15.jpg" alt=""><img src="{A}photos/f10.jpg" alt="">
    </div>
    <div class="hero-eyebrow">{E(t['hero']['eyebrow'])}</div>
    <h1 class="hero-title">{lines(('Bauen mit', ''), ('Verlass.', ''), ('Termingerecht.', 'red'))}</h1>
    <p class="hero-sub">{E(t['hero']['sub'])}</p>
    <div class="hero-ctas">
      <a class="pill pill-white" href="{SITE['calendar']}" target="_blank" rel="noopener">{CAL} {E(t['nav']['cta'])}</a>
      <a class="pill pill-ghost" href="#modelle">3D-Modelle ansehen {ARROW}</a>
    </div>
    <div class="hero-badge"><span class="hero-badge-ico"><svg viewBox="0 6 72 72"><path d="M14 62V32L25 21L36 32L47 21L58 32V62" fill="none" stroke="#fff" stroke-width="6"/><rect x="32" y="44" width="8" height="18" fill="#fff"/></svg></span>
      <span><b>Seit 2010</b>120+ Projekte in Niederösterreich, Burgenland &amp; Wien</span></div>
    <a class="hero-scroll" href="#start" aria-label="Weiter"></a>
  </div>
</section>

<!-- MARQUEE -->
<section class="marquee-sec" id="start">
  <div class="marquee-label">Gebaut, geplant und saniert in</div>
  <div class="marquee"><div class="marquee-track">{marquee_items}{marquee_items}</div></div>
</section>

<!-- STATEMENT + 3D OBJECT -->
<section class="statement">
  <div class="wrap">
    <div class="float3d" id="float3d" aria-hidden="true"></div>
    <h2 class="mega" data-split>{lines(('Bauprojekte', ''), ('scheitern nicht', ''), ('am Können.', 'muted'))}</h2>
    <p class="statement-sub">Sondern an Organisation, Zeitplänen und Nachträgen. Menzil-Bau nimmt Ihnen das ab – mit einem Team, einem Zeitplan und einem Ansprechpartner.</p>
    <div class="pillars" data-rise>
      <div class="pillar"><div class="pillar-ico">{ICON_PLAN}</div><h3>Planen</h3><p>Entwurf, Einreichpläne und Baubewilligung aus dem eigenen Haus – was gezeichnet wird, wird auch gebaut.</p></div>
      <div class="pillar"><div class="pillar-ico">{ICON_BUILD}</div><h3>Bauen</h3><p>Rohbau, Fassade, Umbau und Sanierung. Wir koordinieren alle Gewerke nach einem verbindlichen Zeitplan.</p></div>
      <div class="pillar"><div class="pillar-ico">{ICON_KEY}</div><h3>Übergeben</h3><p>Gemeinsame Abnahme, saubere Baustelle, schlüsselfertige Übergabe – und auch danach erreichbar.</p></div>
    </div>
  </div>
</section>

<!-- RED PANEL -->
<section class="panel panel-red">
  <div class="wrap">
    <div class="panel-head">
      <h2 class="mega" data-split>{lines(('Sie planen', ''), ('Ihr Leben.', ''), ('Wir bauen', ''), ('das Haus.', ''))}</h2>
      <p>Seit 1996 auf der Baustelle, seit 2010 mit eigenem Unternehmen. Planung, Ausführung und Übergabe aus einer Hand.</p>
    </div>
    <div class="stat-cards">
      <div class="stat-card"><div class="stat-top"><span class="stat-tag">Erfahrung</span></div><div class="stat-num"><span data-count="30">30</span><em>+</em></div><div class="stat-desc">Jahre Bauerfahrung – vom Maurer über die Polierschule zum eigenen Betrieb.</div></div>
      <div class="stat-card"><div class="stat-top"><span class="stat-tag">Projekte</span></div><div class="stat-num"><span data-count="120">120</span><em>+</em></div><div class="stat-desc">Einfamilien- und Doppelhäuser, Wohnbau, Zubau und Sanierung.</div></div>
      <div class="stat-card gold"><div class="stat-top"><span class="stat-tag">Ihr Kontakt</span></div><div class="stat-num"><span data-count="1">1</span></div><div class="stat-desc">Ansprechpartner für Ihr gesamtes Projekt – von der Skizze bis zum Schlüssel.</div></div>
    </div>
  </div>
</section>

<!-- STICKY 3D BUILD -->
<section class="build" id="bauablauf">
  <div class="build-sticky">
    <div class="build-text">
      <div class="build-eyebrow">Bauablauf</div>
      <h2 class="build-title">Vom Plan<br>zum Schlüssel</h2>
      <ol class="steps">
        <li class="step"><b><i>01</i>Planung &amp; Einreichung</b><p>Entwurf, Einreichpläne und Begleitung durch das Bewilligungsverfahren.</p></li>
        <li class="step"><b><i>02</i>Fundament &amp; Rohbau</b><p>Bodenplatte, Mauerwerk und Decken – massiv und termingerecht.</p></li>
        <li class="step"><b><i>03</i>Dach &amp; Fassade</b><p>Dachkonstruktion, Eindeckung und die Fassade nach Ihren Wünschen.</p></li>
        <li class="step"><b><i>04</i>Fenster &amp; Übergabe</b><p>Fenster, Türen, Ausbau – und die schlüsselfertige Übergabe.</p></li>
      </ol>
    </div>
    <div class="build-stage" id="buildStage">
      <div class="blueprint-grid"></div>
      <span class="build-done">✓ Schlüsselfertig</span>
      <div class="build-hud"><span>Baufortschritt</span><span class="build-bar"><i></i></span><span class="build-pct">0%</span></div>
    </div>
  </div>
</section>

<!-- 3D MODELS -->
<section class="models" id="modelle">
  <div class="wrap">
    <div class="models-head">
      <h2 class="mega" data-split>{lines(('3D-Modell', ''), ('beispiele', 'muted'))}</h2>
      <p>So planen wir: Jedes Bauvorhaben entsteht zuerst als Modell. Drehen Sie die Beispiele mit der Maus oder dem Finger – und sehen Sie zu, wie sie entstehen.</p>
    </div>
    <div class="model-tabs" role="group" aria-label="Modell wählen">{model_tabs}</div>
    <div class="model-view" id="modelView">
      <div class="model-info" id="modelInfo"></div>
      <div class="model-tools">
        <button type="button" id="mReplay" aria-label="Bauablauf abspielen" title="Bauablauf abspielen">{PLAY}</button>
        <button type="button" id="mSpin" class="on" aria-label="Automatisch drehen" title="Automatisch drehen">{ROT}</button>
      </div>
      <div class="model-hint">{DRAG} Ziehen zum Drehen</div>
    </div>
    {model_data}
  </div>
</section>

<!-- SERVICES CAROUSEL -->
<section class="services" id="leistungen">
  <div class="wrap services-head">
    <h2 class="mega" data-split>{lines(('Sechs', ''), ('Leistungen.', 'muted'))}</h2>
    <div class="car-btns"><button class="car-btn" type="button" data-car="prev" aria-label="Zurück">{PREV}</button><button class="car-btn" type="button" data-car="next" aria-label="Weiter">{NEXT}</button></div>
  </div>
  <div class="carousel">{services}</div>
</section>

<!-- SCATTER -->
<section class="scatter" id="projekte">
  <div class="scatter-sticky">
    <div class="sw" data-from="l" style="left:6%;top:12%">Ein</div>
    <div class="sw red" data-from="r" style="right:8%;top:30%">Partner.</div>
    <div class="sw" data-from="l" style="left:10%;top:56%">Alle</div>
    <div class="sw" data-from="r" style="right:6%;top:72%">Gewerke.</div>
    <a class="sp" href="../projekte.html" style="left:36%;top:6%;width:220px;height:280px"><img src="{A}photos/f13-t.jpg" alt="Mehrfamilienhaus – Menzil-Bau"></a>
    <a class="sp" href="../projekte.html" style="left:4%;top:34%;width:260px;height:190px"><img src="{A}photos/f52-t.jpg" alt="Wohnküche – Menzil-Bau"></a>
    <a class="sp" href="../projekte.html" style="right:30%;top:60%;width:280px;height:200px"><img src="{A}photos/f15-t.jpg" alt="Reihenhausanlage – Menzil-Bau"></a>
    <a class="sp" href="../projekte.html" style="right:5%;top:4%;width:200px;height:250px"><img src="{A}photos/f64-t.jpg" alt="Badezimmer – Menzil-Bau"></a>
    <div class="float3d" id="float3d2" aria-hidden="true"></div>
  </div>
</section>

<!-- STACKED CARDS -->
<section class="stack-sec">
  <div class="wrap stack-grid">
    <div class="stack-left">
      <h2 class="mega" data-split>{lines(('Warum', ''), ('Menzil.', 'muted'))}</h2>
      <p>Vom Maurer zum Baumeisterbetrieb: vier Gründe, warum Bauherren uns weiterempfehlen.</p>
      <p style="margin-top:22px"><a class="pill pill-dark" href="../referenzen.html">Alle Referenzen {ARROW}</a></p>
    </div>
    <div class="stack-list">{stack}</div>
  </div>
</section>

<!-- REVIEWS -->
<section class="reviews"><div class="wrap rev-grid" data-rise>{reviews}</div></section>

<!-- BIG CTA -->
<section class="cta" id="kontakt">
  <div class="wrap">
    <h2 class="mega" data-split>{lines(('Fangen wir', ''), ('an zu bauen.', 'red'))}</h2>
    <p>{E(t['cta']['sub'])}</p>
    <div class="cta-box">
      <a class="pill pill-red" href="{SITE['calendar']}" target="_blank" rel="noopener">{CAL} {E(t['cta']['btn1'])}</a>
      <a class="pill pill-dark" href="{SITE['phone_href']}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{TEL[TEL.index('<path'):TEL.index('</svg>')]}</svg> {SITE['phone_local']}</a>
      <a class="pill pill-white" href="../kontakt.html">Kontaktformular {ARROW}</a>
    </div>
  </div>
</section>
</main>

<footer class="foot">
  <div class="wrap">
    <div class="foot-word" aria-label="Menzil-Bau">{''.join(f'<span{" class=r" if ch in "MB" and i in (0, 7) else ""}>{ch}</span>' for i, ch in enumerate('MENZIL-BAU'))}</div>
    <div class="foot-cols">
      <div>{logo_a(w=200)}<p style="margin-top:14px;font-size:14px;color:rgba(255,255,255,.7);line-height:1.6;max-width:320px">{E(t['motto'])}.</p></div>
      <div><h4>Seiten</h4><ul><li><a href="../projekte.html">Projekte</a></li><li><a href="../referenzen.html">Referenzen</a></li><li><a href="../zertifikate.html">Zertifikate</a></li><li><a href="../kontakt.html">Kontakt</a></li></ul></div>
      <div><h4>Kontakt</h4><ul><li><a href="{SITE['phone_href']}">{SITE['phone_local']}</a></li><li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li><li><a href="{SITE['whatsapp']}" target="_blank" rel="noopener">WhatsApp</a></li><li>{E(SITE['hours'])}</li></ul></div>
      <div><h4>Adressen</h4><ul>{''.join(f'<li>{E(x)}</li>' for x in SITE['addr1'])}<li style="margin-top:10px">{'</li><li>'.join(E(x) for x in SITE['addr2'])}</li></ul></div>
    </div>
    <div class="foot-bottom"><span>&copy; {SITE['founded']}–{YEAR} Menzil-Bau · {E(t['footer']['rights'])}</span><span>Motion-Version · <a href="../index.html">Klassische Version ansehen</a> · <a href="../kontakt.html#impressum">Impressum</a></span></div>
  </div>
</footer>

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="v2.js" defer></script>
<script type="importmap">{{"imports": {{"three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js", "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}}}</script>
<script type="module">
  import {{ makeModel, createViewer }} from './houses.js';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // small rotating houses next to headlines
  for (const [id, type] of [['float3d', 'efh'], ['float3d2', 'dh']]) {{
    const el = document.getElementById(id); if (!el || getComputedStyle(el).display === 'none') continue;
    const v = createViewer(el, {{ autoRotate: reduce ? 0 : 1.2, camPos: [26, 20, 30], target: [0, 3, 0], fov: 30 }});
    const m = makeModel(type, {{ floating: true }}); m.setProgress(1); v.setModel(m);
  }}

  // sticky build: assembles with scroll
  const stage = document.getElementById('buildStage');
  const bv = createViewer(stage, {{ autoRotate: reduce ? 0 : 0.35, camPos: [24, 17, 28], target: [0, 3.2, 0], fov: 30 }});
  const bm = makeModel('efh'); bm.setProgress(reduce ? 1 : 0); bv.setModel(bm);
  window.__buildProgress = p => bm.setProgress(Math.min(1, p * 1.08));

  // interactive models
  const view = document.getElementById('modelView'), info = document.getElementById('modelInfo');
  const mv = createViewer(view, {{ interactive: true, autoRotate: reduce ? 0 : 1.1, camPos: [26, 16, 30], target: [0, 4, 0], fov: 30 }});
  let current = null, anim = 0;
  function play(model) {{
    cancelAnimationFrame(anim);
    if (reduce) {{ model.setProgress(1); return; }}
    const t0 = performance.now(), dur = 2600;
    const tick = now => {{ const p = Math.min(1, (now - t0) / dur); model.setProgress(p); if (p < 1) anim = requestAnimationFrame(tick); }};
    anim = requestAnimationFrame(tick);
  }}
  function load(type) {{
    current = makeModel(type); mv.setModel(current); play(current);
    info.innerHTML = document.getElementById('info-' + type).innerHTML;
    document.querySelectorAll('.model-tab').forEach(b => {{ const on = b.dataset.model === type; b.classList.toggle('on', on); b.setAttribute('aria-pressed', on); }});
  }}
  document.querySelectorAll('.model-tab').forEach(b => b.addEventListener('click', () => load(b.dataset.model)));
  document.getElementById('mReplay').addEventListener('click', () => play(current));
  const spin = document.getElementById('mSpin');
  spin.addEventListener('click', () => {{ spin.classList.toggle('on'); mv.controls.autoRotate = spin.classList.contains('on'); }});
  // build the first model when the section comes into view
  let started = false;
  new IntersectionObserver(([e]) => {{ if (e.isIntersecting && !started) {{ started = true; load('efh'); }} }}, {{ threshold: 0.3 }}).observe(view);
</script>
</body>
</html>
'''
with open(os.path.join(ROOT, 'v2', 'index.html'), 'w', encoding='utf-8') as f:
    f.write(page)
print('built v2/index.html')
