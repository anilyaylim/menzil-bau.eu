# -*- coding: utf-8 -*-
"""Builds the motion version from tools/data.py in three languages:

    v2/index.html (DE, default) · v2/en/index.html · v2/tr/index.html

    python3 tools/build_v2.py
"""
import os, sys, html
from datetime import date
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from data import SITE, T, PLACES, LANGS, LANG_NAMES
from build import logo_a, ARROW, CAL, TEL, PIN

E = html.escape
YEAR = date.today().year

ICON_PLAN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M3 3h18v18H3z"/><path d="M3 12h8V3M11 12v9M15 12h6"/></svg>'
ICON_BUILD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M2 20h20"/><path d="M5 20V9l7-5 7 5v11"/><path d="M9 20v-6h6v6"/></svg>'
ICON_KEY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/></svg>'
ROT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 3v6h-6"/></svg>'
PLAY = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4l13 8-13 8z"/></svg>'
DRAG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M8 12h8M5 9l-3 3 3 3M19 9l3 3-3 3"/></svg>'
PREV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 5l-7 7 7 7"/></svg>'
NEXT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 5l7 7-7 7"/></svg>'

# ── v2-only texts (everything else comes from T in data.py) ──
V = {
 'de': {
  'title': 'Menzil-Bau · Bauen mit Verlass',
  'nav': ['Leistungen', 'Bauablauf', '3D-Modelle', 'Projekte', 'Kontakt'], 'classic': 'Klassisch', 'menu': 'Menü', 'langs': 'Sprache',
  'hero': ['Bauen mit', 'Verlass.', 'Termingerecht.'], 'cta2': '3D-Modelle ansehen', 'next': 'Weiter',
  'badge': ('Seit 2010', '120+ Projekte in Niederösterreich, Burgenland &amp; Wien'),
  'marquee': 'Gebaut, geplant und saniert in',
  'statement': ['Bauprojekte', 'scheitern nicht', 'am Können.'],
  'statement_p': 'Sondern an Organisation, Zeitplänen und Nachträgen. Menzil-Bau nimmt Ihnen das ab – mit einem Team, einem Zeitplan und einem Ansprechpartner.',
  'pillars': [('Planen', 'Entwurf, Einreichpläne und Baubewilligung aus dem eigenen Haus – was gezeichnet wird, wird auch gebaut.'),
              ('Bauen', 'Rohbau, Fassade, Umbau und Sanierung. Wir koordinieren alle Gewerke nach einem verbindlichen Zeitplan.'),
              ('Übergeben', 'Gemeinsame Abnahme, saubere Baustelle, schlüsselfertige Übergabe – und auch danach erreichbar.')],
  'panel': ['Sie planen', 'Ihr Leben.', 'Wir bauen', 'das Haus.'],
  'panel_p': 'Seit 1996 auf der Baustelle, seit 2010 mit eigenem Unternehmen. Planung, Ausführung und Übergabe aus einer Hand.',
  'stats': [('Erfahrung', 'Jahre Bauerfahrung – vom Maurer über die Polierschule zum eigenen Betrieb.'),
            ('Projekte', 'Einfamilien- und Doppelhäuser, Wohnbau, Zubau und Sanierung.'),
            ('Ihr Kontakt', 'Ansprechpartner für Ihr gesamtes Projekt – von der Skizze bis zum Schlüssel.')],
  'build': ('Bauablauf', 'Vom Plan<br>zum Schlüssel', 'Baufortschritt', 'Schlüsselfertig'),
  'steps': [('Planung &amp; Einreichung', 'Entwurf, Einreichpläne und Begleitung durch das Bewilligungsverfahren.'),
            ('Fundament &amp; Rohbau', 'Bodenplatte, Mauerwerk und Decken – massiv und termingerecht.'),
            ('Dach &amp; Fassade', 'Dachkonstruktion, Eindeckung und die Fassade nach Ihren Wünschen.'),
            ('Fenster &amp; Übergabe', 'Fenster, Türen, Ausbau – und die schlüsselfertige Übergabe.')],
  'models': (['3D-Modell', 'beispiele'], 'So planen wir: Jedes Bauvorhaben entsteht zuerst als Modell. Drehen Sie die Beispiele mit der Maus oder dem Finger – und sehen Sie zu, wie sie entstehen.',
             'Modellbeispiel', 'Ziehen zum Drehen', 'Bauablauf abspielen', 'Automatisch drehen', 'Modell wählen'),
  'model_list': [
    ('efh', 'Einfamilienhaus', 'Zweigeschossiges Wohnhaus mit Satteldach, Garage und Terrasse – so wie wir es in Niederösterreich am häufigsten planen und bauen.',
     [('Geschosse', '2'), ('Dach', 'Satteldach'), ('Bauweise', 'Massivbau'), ('Extras', 'Garage, Terrasse')]),
    ('dh', 'Doppelhaus', 'Zwei gespiegelte Haushälften mit gemeinsamer Trennwand – effizient im Grundstück, eigenständig im Wohnen.',
     [('Einheiten', '2'), ('Geschosse', '2 je Hälfte'), ('Dach', 'Satteldach'), ('Bauweise', 'Massivbau')]),
    ('mfh', 'Wohnhausanlage', 'Dreigeschossiger Wohnbau mit Balkonen und Walmdach – für Bauträger, Investoren und Gemeinden.',
     [('Geschosse', '3'), ('Dach', 'Walmdach'), ('Balkone', 'je Obergeschoss'), ('Bauweise', 'Massivbau')])],
  'services': ['Sechs', 'Leistungen.'], 'prev': 'Zurück',
  'scatter': ['Ein', 'Partner.', 'Alle', 'Gewerke.'],
  'why': (['Warum', 'Menzil.'], 'Vom Maurer zum Baumeisterbetrieb: vier Gründe, warum Bauherren uns weiterempfehlen.'),
  'cta': ['Fangen wir', 'an zu bauen.'], 'form': 'Kontaktformular',
  'foot': ('Seiten', 'Kontakt', 'Adressen', 'Motion-Version', 'Klassische Version ansehen'),
 },
 'en': {
  'title': 'Menzil-Bau · Built to rely on',
  'nav': ['Services', 'How we build', '3D models', 'Projects', 'Contact'], 'classic': 'Classic', 'menu': 'Menu', 'langs': 'Language',
  'hero': ['Built to', 'rely on.', 'On time.'], 'cta2': 'View 3D models', 'next': 'Next',
  'badge': ('Since 2010', '120+ projects in Lower Austria, Burgenland &amp; Vienna'),
  'marquee': 'Built, planned and renovated in',
  'statement': ['Projects', 'don’t fail', 'on skill.'],
  'statement_p': 'They fail on organisation, schedules and change orders. Menzil-Bau takes that off your hands – with one team, one schedule and one contact person.',
  'pillars': [('Plan', 'Design, permit drawings and building permit in-house – what is drawn is what gets built.'),
              ('Build', 'Shell, facade, conversion and renovation. We coordinate every trade on a binding schedule.'),
              ('Hand over', 'Joint inspection, a clean site, turnkey handover – and still there for you afterwards.')],
  'panel': ['You plan', 'your life.', 'We build', 'the house.'],
  'panel_p': 'On site since 1996, with our own company since 2010. Planning, construction and handover from a single source.',
  'stats': [('Experience', 'Years of building experience – from bricklayer through foreman school to our own company.'),
            ('Projects', 'Single-family and semi-detached houses, residential buildings, extensions and renovations.'),
            ('Your contact', 'Contact person for your whole project – from the first sketch to the keys.')],
  'build': ('How we build', 'From plan<br>to keys', 'Construction progress', 'Turnkey'),
  'steps': [('Planning &amp; permit', 'Design, permit drawings and support through the approval process.'),
            ('Foundation &amp; shell', 'Base slab, masonry and floor slabs – solid and on schedule.'),
            ('Roof &amp; facade', 'Roof structure, covering and a facade to your wishes.'),
            ('Windows &amp; handover', 'Windows, doors, fit-out – and the turnkey handover.')],
  'models': (['3D model', 'examples'], 'This is how we plan: every project starts as a model. Rotate the examples with your mouse or finger – and watch them being built.',
             'Model example', 'Drag to rotate', 'Play build sequence', 'Auto-rotate', 'Choose a model'),
  'model_list': [
    ('efh', 'Single-family house', 'Two-storey home with gable roof, garage and terrace – the type we plan and build most often in Lower Austria.',
     [('Storeys', '2'), ('Roof', 'Gable roof'), ('Construction', 'Solid masonry'), ('Extras', 'Garage, terrace')]),
    ('dh', 'Semi-detached house', 'Two mirrored halves sharing one party wall – efficient on the plot, independent to live in.',
     [('Units', '2'), ('Storeys', '2 per half'), ('Roof', 'Gable roof'), ('Construction', 'Solid masonry')]),
    ('mfh', 'Residential complex', 'Three-storey residential building with balconies and a hipped roof – for developers, investors and municipalities.',
     [('Storeys', '3'), ('Roof', 'Hipped roof'), ('Balconies', 'every upper floor'), ('Construction', 'Solid masonry')])],
  'services': ['Six', 'services.'], 'prev': 'Previous',
  'scatter': ['One', 'partner.', 'Every', 'trade.'],
  'why': (['Why', 'Menzil.'], 'From bricklayer to master builder: four reasons why clients recommend us.'),
  'cta': ['Let’s start', 'building.'], 'form': 'Contact form',
  'foot': ('Pages', 'Contact', 'Addresses', 'Motion version', 'View classic version'),
 },
 'tr': {
  'title': 'Menzil-Bau · Güvenle inşa',
  'nav': ['Hizmetler', 'İnşa süreci', '3D modeller', 'Projeler', 'İletişim'], 'classic': 'Klasik', 'menu': 'Menü', 'langs': 'Dil',
  'hero': ['Güvenle', 'inşa.', 'Zamanında.'], 'cta2': '3D modelleri gör', 'next': 'Devam',
  'badge': ('2010’dan beri', 'Aşağı Avusturya, Burgenland ve Viyana’da 120+ proje'),
  'marquee': 'İnşa ettiğimiz, planladığımız ve yenilediğimiz yerler',
  'statement': ['Projeler', 'ustalıktan', 'aksamaz.'],
  'statement_p': 'Organizasyondan, takvimden ve ek işlerden aksar. Menzil-Bau bunu sizin yerinize üstlenir: tek ekip, tek takvim, tek muhatap.',
  'pillars': [('Planla', 'Tasarım, ruhsat çizimleri ve yapı izni kendi bünyemizde: çizilen neyse o inşa edilir.'),
              ('İnşa et', 'Kaba inşaat, cephe, tadilat ve renovasyon. Tüm taşeronları bağlayıcı bir takvimle koordine ederiz.'),
              ('Teslim et', 'Birlikte kabul, temiz şantiye, anahtar teslim. Sonrasında da yanınızdayız.')],
  'panel': ['Siz hayatınızı', 'planlayın.', 'Evi biz', 'inşa edelim.'],
  'panel_p': '1996’dan beri şantiyede, 2010’dan beri kendi firmamızla. Planlama, uygulama ve teslim tek elden.',
  'stats': [('Tecrübe', 'Yıllık inşaat tecrübesi: duvarcılıktan şantiye şefliği okuluna, oradan kendi firmamıza.'),
            ('Projeler', 'Müstakil ve ikiz konutlar, konut projeleri, ek bina ve renovasyon.'),
            ('Muhatabınız', 'Projenizin tamamı için tek muhatap: ilk eskizden anahtara kadar.')],
  'build': ('İnşa süreci', 'Plandan<br>anahtara', 'İnşaat ilerlemesi', 'Anahtar teslim'),
  'steps': [('Planlama ve ruhsat', 'Tasarım, ruhsat çizimleri ve onay sürecinde destek.'),
            ('Temel ve kaba inşaat', 'Radye temel, duvarlar ve döşemeler: sağlam ve zamanında.'),
            ('Çatı ve cephe', 'Çatı konstrüksiyonu, kaplama ve isteğinize göre cephe.'),
            ('Pencere ve teslim', 'Pencereler, kapılar, iç işler ve anahtar teslim.')],
  'models': (['3D model', 'örnekleri'], 'Böyle planlıyoruz: her proje önce bir model olarak doğar. Örnekleri fare ya da parmağınızla çevirin ve nasıl inşa edildiklerini izleyin.',
             'Model örneği', 'Çevirmek için sürükleyin', 'İnşa sürecini oynat', 'Otomatik döndür', 'Model seçin'),
  'model_list': [
    ('efh', 'Müstakil konut', 'Beşik çatılı, garajlı ve teraslı iki katlı konut; Aşağı Avusturya’da en sık planlayıp inşa ettiğimiz tip.',
     [('Kat', '2'), ('Çatı', 'Beşik çatı'), ('Yapı', 'Yığma'), ('Ekstra', 'Garaj, teras')]),
    ('dh', 'İkiz konut', 'Ortak bir duvarı paylaşan iki simetrik konut: arsada verimli, yaşamda bağımsız.',
     [('Birim', '2'), ('Kat', 'Her biri 2'), ('Çatı', 'Beşik çatı'), ('Yapı', 'Yığma')]),
    ('mfh', 'Konut projesi', 'Balkonlu ve kırma çatılı üç katlı konut binası; yatırımcılar, geliştiriciler ve belediyeler için.',
     [('Kat', '3'), ('Çatı', 'Kırma çatı'), ('Balkon', 'Her üst katta'), ('Yapı', 'Yığma')])],
  'services': ['Altı', 'hizmet.'], 'prev': 'Önceki',
  'scatter': ['Tek', 'muhatap.', 'Tüm', 'işler.'],
  'why': (['Neden', 'Menzil.'], 'Duvar ustalığından müteahhitliğe: müşterilerimizin bizi tavsiye etmesinin dört nedeni.'),
  'cta': ['Hadi', 'başlayalım.'], 'form': 'İletişim formu',
  'foot': ('Sayfalar', 'İletişim', 'Adresler', 'Hareketli sürüm', 'Klasik sürümü gör'),
 },
}


def lines(parts, last_cls=''):
    """Big headline split into masked lines for the reveal animation; last line can be accented."""
    out = []
    for i, x in enumerate(parts):
        c = last_cls if (last_cls and i == len(parts) - 1) else ''
        out.append(f'<span class="line"><span{(" class=%s" % c) if c else ""}>{x}</span></span>')
    return ''.join(out)


def build(lang):
    t, v = T[lang], V[lang]
    sub = lang != 'de'
    R = '../../' if sub else '../'            # → repo root
    VD = '../' if sub else ''                 # → v2 dir
    A = R + 'assets/img/'
    CL = R + ('' if lang == 'de' else lang + '/')   # classic pages in the same language
    def v2_href(target):
        if lang == 'de': return 'index.html' if target == 'de' else f'{target}/index.html'
        return '../index.html' if target == 'de' else ('index.html' if target == lang else f'../{target}/index.html')
    langs = ''.join(f'<a href="{v2_href(l)}" hreflang="{l}" lang="{l}"{" class=on aria-current=true" if l == lang else ""}>{LANG_NAMES[l]}</a>' for l in LANGS)

    svc_imgs = [A + 'plans/mattersburg-1-t.jpg', A + 'photos/f14-t.jpg', A + 'photos/f10-t.jpg', A + 'photos/f04-t.jpg', A + 'photos/f64-t.jpg', A + 'photos/f05-t.jpg']
    services = ''.join(f'''<article class="svc">
        <div class="svc-img"><img src="{svc_imgs[i]}" alt="{E(n)} – Menzil-Bau" loading="lazy" draggable="false"></div>
        <div class="svc-body"><div class="svc-no">0{i + 1}</div><h3>{E(n)}</h3><p>{E(d)}</p>
          <div class="svc-tags">{''.join(f'<span>{E(x)}</span>' for x in tags)}</div></div>
      </article>''' for i, (n, d, tags) in enumerate(t['services']['items']))
    stack = ''.join(f'<div class="scard"><div class="scard-no">0{i + 1}</div><div><h3>{E(a)}</h3><p>{b}</p></div></div>' for i, (a, b) in enumerate(t['why']['items']))
    reviews = ''.join(f'''<figure class="rev"><div class="stars">★★★★★</div><blockquote>{E(q)}</blockquote>
        <figcaption><b>{E(n)}</b>{E(tag)} · {E(l)}</figcaption></figure>''' for tag, q, n, l in t['reviews']['items'])
    marquee_items = ''.join(f'<span>{PIN.replace("ref-pin", "")}{E(p)}</span>' for p in PLACES)
    feat = {pid: nm for pid, _, nm in t['featured']['cards']}

    mt, mp, mtag, mhint, mplay, mspin, mgroup = v['models']
    model_tabs = ''.join(f'<button class="model-tab{" on" if i == 0 else ""}" type="button" data-model="{k}" aria-pressed="{"true" if i == 0 else "false"}">{E(n)}</button>' for i, (k, n, _, _) in enumerate(v['model_list']))
    model_data = ''.join(f'''<template id="info-{k}"><span class="tag">{E(mtag)}</span><h3>{E(n)}</h3><p>{E(d)}</p>
      <dl>{''.join(f'<dt>{E(a)}</dt><dd>{E(b)}</dd>' for a, b in specs)}</dl></template>''' for k, n, d, specs in v['model_list'])
    stats = ''.join(f'''<div class="stat-card{" gold" if i == 2 else ""}"><div class="stat-top"><span class="stat-tag">{E(tag)}</span></div>
        <div class="stat-num"><span data-count="{n}">{n}</span>{f"<em>{u}</em>" if u else ""}</div><div class="stat-desc">{E(d)}</div></div>'''
        for i, ((tag, d), (n, u)) in enumerate(zip(v['stats'], [('30', '+'), ('120', '+'), ('1', '')])))
    steps = ''.join(f'<li class="step"><b><i>0{i + 1}</i>{a}</b><p>{E(b)}</p></li>' for i, (a, b) in enumerate(v['steps']))
    pillars = ''.join(f'<div class="pillar"><div class="pillar-ico">{ic}</div><h3>{E(a)}</h3><p>{E(b)}</p></div>' for ic, (a, b) in zip([ICON_PLAN, ICON_BUILD, ICON_KEY], v['pillars']))
    n = v['nav']; f = v['foot']; bt = v['build']

    return f'''<!DOCTYPE html>
<html lang="{lang}" translate="no">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(v['title'])}</title>
<meta name="description" content="{E(t['meta']['index'][1])}">
<meta name="google" content="notranslate">
<meta name="theme-color" content="#121417">
{''.join(f'<link rel="alternate" hreflang="{l}" href="{v2_href(l)}">' for l in LANGS)}
<link rel="icon" href="{R}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{VD}v2.css">
</head>
<body>

<div class="nav-wrap">
<header class="nav" aria-label="Navigation">
  <a class="nav-logo" href="#top" aria-label="Menzil-Bau">{logo_a(w=150)}</a>
  <ul class="nav-links">
    <li><a href="#leistungen">{E(n[0])}</a></li>
    <li><a href="#bauablauf">{E(n[1])}</a></li>
    <li><a href="#modelle">{E(n[2])}</a></li>
    <li><a href="#projekte">{E(n[3])}</a></li>
    <li><a href="{CL}kontakt.html">{E(n[4])}</a></li>
    <li class="nav-lang-m" aria-label="{E(v['langs'])}">{langs}</li>
    <li class="nav-cta-m"><a class="pill pill-red" href="{SITE['calendar']}" target="_blank" rel="noopener">{CAL} {E(t['nav']['cta'])}</a></li>
  </ul>
  <div class="nav-right">
    <div class="nav-lang" role="group" aria-label="{E(v['langs'])}">{langs}</div>
    <a class="pill pill-ghost pill-sm nav-classic" href="{CL}index.html">{E(v['classic'])}</a>
    <a class="pill pill-red nav-cta" href="{SITE['calendar']}" target="_blank" rel="noopener">{E(t['nav']['cta'])}</a>
    <button class="nav-burger" type="button" aria-label="{E(v['menu'])}" aria-expanded="false"><span></span></button>
  </div>
</header>
</div>

<main id="top">
<section class="hero">
  <div class="hero-card">
    <div class="hero-media" aria-hidden="true">
      <img src="{A}photos/f01.jpg" alt=""><img src="{A}photos/f13.jpg" alt=""><img src="{A}photos/f15.jpg" alt=""><img src="{A}photos/f10.jpg" alt="">
    </div>
    <div class="hero-eyebrow">{E(t['hero']['eyebrow'])}</div>
    <h1 class="hero-title">{lines(v['hero'], 'red')}</h1>
    <p class="hero-sub">{E(t['hero']['sub'])}</p>
    <div class="hero-ctas">
      <a class="pill pill-white" href="{SITE['calendar']}" target="_blank" rel="noopener">{CAL} {E(t['nav']['cta'])}</a>
      <a class="pill pill-ghost" href="#modelle">{E(v['cta2'])} {ARROW}</a>
    </div>
    <div class="hero-badge"><span class="hero-badge-ico"><svg viewBox="0 6 72 72"><path d="M14 62V32L25 21L36 32L47 21L58 32V62" fill="none" stroke="#fff" stroke-width="6"/><rect x="32" y="44" width="8" height="18" fill="#fff"/></svg></span>
      <span><b>{v['badge'][0]}</b>{v['badge'][1]}</span></div>
    <a class="hero-scroll" href="#start" aria-label="{E(v['next'])}"></a>
  </div>
</section>

<section class="marquee-sec" id="start">
  <div class="marquee-label">{E(v['marquee'])}</div>
  <div class="marquee"><div class="marquee-track">{marquee_items}{marquee_items}</div></div>
</section>

<section class="statement">
  <div class="wrap">
    <div class="float3d" id="float3d" aria-hidden="true"></div>
    <h2 class="mega" data-split>{lines(v['statement'], 'muted')}</h2>
    <p class="statement-sub">{E(v['statement_p'])}</p>
    <div class="pillars" data-rise>{pillars}</div>
  </div>
</section>

<section class="panel panel-red">
  <div class="wrap">
    <div class="panel-head">
      <h2 class="mega" data-split>{lines(v['panel'])}</h2>
      <p>{E(v['panel_p'])}</p>
    </div>
    <div class="stat-cards">{stats}</div>
  </div>
</section>

<section class="build" id="bauablauf">
  <div class="build-sticky">
    <div class="build-text">
      <div class="build-eyebrow">{E(bt[0])}</div>
      <h2 class="build-title">{bt[1]}</h2>
      <ol class="steps">{steps}</ol>
    </div>
    <div class="build-stage" id="buildStage">
      <div class="blueprint-grid"></div>
      <span class="build-done">✓ {E(bt[3])}</span>
      <div class="build-hud"><span>{E(bt[2])}</span><span class="build-bar"><i></i></span><span class="build-pct">0%</span></div>
    </div>
  </div>
</section>

<section class="models" id="modelle">
  <div class="wrap">
    <div class="models-head">
      <h2 class="mega" data-split>{lines(mt, 'muted')}</h2>
      <p>{E(mp)}</p>
    </div>
    <div class="model-tabs" role="group" aria-label="{E(mgroup)}">{model_tabs}</div>
    <div class="model-view" id="modelView">
      <div class="model-info" id="modelInfo"></div>
      <div class="model-tools">
        <button type="button" id="mReplay" aria-label="{E(mplay)}" title="{E(mplay)}">{PLAY}</button>
        <button type="button" id="mSpin" class="on" aria-label="{E(mspin)}" title="{E(mspin)}">{ROT}</button>
      </div>
      <div class="model-hint">{DRAG} {E(mhint)}</div>
    </div>
    {model_data}
  </div>
</section>

<section class="services" id="leistungen">
  <div class="wrap services-head">
    <h2 class="mega" data-split>{lines(v['services'], 'muted')}</h2>
    <div class="car-btns"><button class="car-btn" type="button" data-car="prev" aria-label="{E(v['prev'])}">{PREV}</button><button class="car-btn" type="button" data-car="next" aria-label="{E(v['next'])}">{NEXT}</button></div>
  </div>
  <div class="carousel">{services}</div>
</section>

<section class="scatter" id="projekte">
  <div class="scatter-sticky">
    <div class="sw" data-from="l" style="left:6%;top:12%">{E(v['scatter'][0])}</div>
    <div class="sw red" data-from="r" style="right:8%;top:30%">{E(v['scatter'][1])}</div>
    <div class="sw" data-from="l" style="left:10%;top:56%">{E(v['scatter'][2])}</div>
    <div class="sw" data-from="r" style="right:6%;top:72%">{E(v['scatter'][3])}</div>
    <a class="sp" href="{CL}projekte.html" style="left:36%;top:6%;width:220px;height:280px"><img src="{A}photos/f13-t.jpg" alt="{E(feat.get('f13', ''))} – Menzil-Bau"></a>
    <a class="sp" href="{CL}projekte.html" style="left:4%;top:34%;width:260px;height:190px"><img src="{A}photos/f52-t.jpg" alt="{E(feat.get('f52', ''))} – Menzil-Bau"></a>
    <a class="sp" href="{CL}projekte.html" style="right:30%;top:60%;width:280px;height:200px"><img src="{A}photos/f15-t.jpg" alt="{E(feat.get('f15', ''))} – Menzil-Bau"></a>
    <a class="sp" href="{CL}projekte.html" style="right:5%;top:4%;width:200px;height:250px"><img src="{A}photos/f64-t.jpg" alt="{E(feat.get('f64', ''))} – Menzil-Bau"></a>
    <div class="float3d" id="float3d2" aria-hidden="true"></div>
  </div>
</section>

<section class="stack-sec">
  <div class="wrap stack-grid">
    <div class="stack-left">
      <h2 class="mega" data-split>{lines(v['why'][0], 'muted')}</h2>
      <p>{E(v['why'][1])}</p>
      <p style="margin-top:22px"><a class="pill pill-dark" href="{CL}referenzen.html">{E(t['reviews']['more'])} {ARROW}</a></p>
    </div>
    <div class="stack-list">{stack}</div>
  </div>
</section>

<section class="reviews"><div class="wrap rev-grid" data-rise>{reviews}</div></section>

<section class="cta" id="kontakt">
  <div class="wrap">
    <h2 class="mega" data-split>{lines(v['cta'], 'red')}</h2>
    <p>{E(t['cta']['sub'])}</p>
    <div class="cta-box">
      <a class="pill pill-red" href="{SITE['calendar']}" target="_blank" rel="noopener">{CAL} {E(t['cta']['btn1'])}</a>
      <a class="pill pill-dark" href="{SITE['phone_href']}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{TEL[TEL.index('<path'):TEL.index('</svg>')]}</svg> {SITE['phone_local']}</a>
      <a class="pill pill-white" href="{CL}kontakt.html">{E(v['form'])} {ARROW}</a>
    </div>
  </div>
</section>
</main>

<footer class="foot">
  <div class="wrap">
    <div class="foot-word" aria-label="Menzil-Bau">{''.join(f'<span{" class=r" if i in (0, 7) else ""}>{ch}</span>' for i, ch in enumerate('MENZIL-BAU'))}</div>
    <div class="foot-cols">
      <div>{logo_a(w=200)}<p style="margin-top:14px;font-size:14px;color:rgba(255,255,255,.7);line-height:1.6;max-width:320px">{E(t['motto'])}.</p></div>
      <div><h4>{E(f[0])}</h4><ul><li><a href="{CL}projekte.html">{E(t['nav']['projekte'])}</a></li><li><a href="{CL}referenzen.html">{E(t['nav']['referenzen'])}</a></li><li><a href="{CL}zertifikate.html">{E(t['nav']['zertifikate'])}</a></li><li><a href="{CL}kontakt.html">{E(t['nav']['kontakt'])}</a></li></ul></div>
      <div><h4>{E(f[1])}</h4><ul><li><a href="{SITE['phone_href']}">{SITE['phone_local']}</a></li><li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li><li><a href="{SITE['whatsapp']}" target="_blank" rel="noopener">WhatsApp</a></li><li>{E(SITE['hours'])}</li></ul></div>
      <div><h4>{E(f[2])}</h4><ul>{''.join(f'<li>{E(x)}</li>' for x in SITE['addr1'])}<li style="margin-top:10px">{'</li><li>'.join(E(x) for x in SITE['addr2'])}</li></ul></div>
    </div>
    <div class="foot-bottom"><span>&copy; {SITE['founded']}–{YEAR} Menzil-Bau · {E(t['footer']['rights'])}</span><span>{E(f[3])} · <a href="{CL}index.html">{E(f[4])}</a> · <a href="{CL}kontakt.html#impressum">{E(t['footer']['impressum'])}</a></span></div>
  </div>
</footer>

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="{VD}v2.js" defer></script>
<script type="importmap">{{"imports": {{"three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js", "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}}}</script>
<script type="module">
  import {{ makeModel, createViewer }} from '{VD or "./"}houses.js';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  for (const [id, type] of [['float3d', 'efh'], ['float3d2', 'dh']]) {{
    const el = document.getElementById(id); if (!el || getComputedStyle(el).display === 'none') continue;
    const v = createViewer(el, {{ autoRotate: reduce ? 0 : 1.2, camPos: [26, 20, 30], target: [0, 3, 0], fov: 30 }});
    const m = makeModel(type, {{ floating: true }}); m.setProgress(1); v.setModel(m);
  }}
  const stage = document.getElementById('buildStage');
  const bv = createViewer(stage, {{ autoRotate: reduce ? 0 : 0.35, camPos: [24, 17, 28], target: [0, 3.2, 0], fov: 30 }});
  const bm = makeModel('efh'); bm.setProgress(reduce ? 1 : 0); bv.setModel(bm);
  window.__buildProgress = p => bm.setProgress(Math.min(1, p * 1.08));
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
  let started = false;
  new IntersectionObserver(([e]) => {{ if (e.isIntersecting && !started) {{ started = true; load('efh'); }} }}, {{ threshold: 0.3 }}).observe(view);
</script>
</body>
</html>
'''


def main():
    for lang in LANGS:
        out = os.path.join(ROOT, 'v2') if lang == 'de' else os.path.join(ROOT, 'v2', lang)
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, 'index.html'), 'w', encoding='utf-8') as fh:
            fh.write(build(lang))
    print('built v2: ' + ', '.join(LANGS))


if __name__ == '__main__':
    main()
