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
from build import logo_a, ARROW, CAL, TEL, PIN, MAIL, WA, CLOCK, seal, COUNTRIES
from data import LOREM
import json
from blog_data import POSTS, BLOG_UI, BLOG_DATE, CHAT_UI, INTENTS, CHAT_LINKS, CHIP_INTENTS

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
  'nav': ['Leistungen', 'Bauablauf', '3D-Modelle', 'Projekte', 'Zertifikate', 'Blog', 'Kontakt'], 'classic': 'Klassisch', 'cta_short': 'Termin', 'menu': 'Menü', 'langs': 'Sprache',
  'hero': ['Bauen mit', 'Verlass.', ('Termingerecht.', 'red')], 'cta2': '3D-Modelle ansehen', 'next': 'Weiter',
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
  'services': ['Sechs Kern-', 'leistungen.'], 'prev': 'Zurück',
  'scatter': ['Ein', 'Partner.', 'Alle', 'Gewerke.'],
  'why': (['Warum', 'Menzil.'], 'Vom Maurer zum Baumeisterbetrieb: vier Gründe, warum Bauherren uns weiterempfehlen.'),
  'cta': ['Fangen wir', 'an zu bauen.'], 'form': 'Kontaktformular',
  'places': ('Standorte', 'Bundesländer', 'Von Wien bis ins Burgenland: Hier haben wir bereits geplant, gebaut, zugebaut oder saniert.'),
  'cookie': ('Cookies &amp; Datenschutz', 'Diese Website verwendet nur technisch notwendige Speicherung (z.&nbsp;B. diese Auswahl) und lädt Schriften und 3D-Bibliotheken von externen Servern. Tracking-Cookies werden nicht gesetzt.', 'Akzeptieren', 'Ablehnen'),
  'top': 'Nach oben',
  'process_p': 'Klare Schritte, feste Ansprechpartner, keine Überraschungen: So läuft Ihr Bauvorhaben mit Menzil-Bau ab – vom ersten Gespräch bis zur Schlüsselübergabe.',
  'contact': (['Lassen Sie', ('uns reden.', 'red')], 'Wir melden uns innerhalb von 24 Stunden.'),
  'certs': (['Berechtigt.', 'Versichert.', ('Geprüft.', 'red')], 'Nachweis ansehen'),
  'foot': ('Seiten', 'Kontakt', 'Adressen', 'Motion-Version', 'Klassische Version ansehen'),
 },
 'en': {
  'title': 'Menzil-Bau · Built to rely on',
  'nav': ['Services', 'How we build', '3D models', 'Projects', 'Certificates', 'Blog', 'Contact'], 'classic': 'Classic', 'cta_short': 'Book', 'menu': 'Menu', 'langs': 'Language',
  'hero': ['Built to', 'rely on.', ('On time.', 'red')], 'cta2': 'View 3D models', 'next': 'Next',
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
  'services': ['Six main', 'services.'], 'prev': 'Previous',
  'scatter': ['One', 'partner.', 'Every', 'trade.'],
  'why': (['Why', 'Menzil.'], 'From bricklayer to master builder: four reasons why clients recommend us.'),
  'cta': ['Let’s start', 'building.'], 'form': 'Contact form',
  'places': ('locations', 'federal states', 'From Vienna to Burgenland: where we have already planned, built, extended or renovated.'),
  'cookie': ('Cookies &amp; privacy', 'This website only uses technically necessary storage (e.g. this choice) and loads fonts and 3D libraries from external servers. No tracking cookies are set.', 'Accept', 'Decline'),
  'top': 'Back to top',
  'process_p': 'Clear steps, one contact person, no surprises: this is how your project runs with Menzil-Bau – from the first conversation to the handover of the keys.',
  'contact': (['Let’s', ('talk.', 'red')], 'We reply within 24 hours.'),
  'certs': (['Licensed.', 'Insured.', ('Proven.', 'red')], 'View certificate'),
  'foot': ('Pages', 'Contact', 'Addresses', 'Motion version', 'View classic version'),
 },
 'tr': {
  'title': 'Menzil-Bau · Güvenle inşa',
  'nav': ['Hizmetler', 'İnşa süreci', '3D modeller', 'Projeler', 'Sertifikalar', 'Blog', 'İletişim'], 'classic': 'Klasik', 'cta_short': 'Randevu Al', 'menu': 'Menü', 'langs': 'Dil',
  'hero': ['Güvenle inşa.', ('Zamanında', 'red'), ('teslim.', 'red')], 'cta2': '3D modelleri gör', 'next': 'Devam',
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
  'services': ['Altı temel', 'hizmet.'], 'prev': 'Önceki',
  'scatter': ['Tek', 'muhatap.', 'Tüm', 'işler.'],
  'why': (['Neden', 'Menzil.'], 'Duvar ustalığından müteahhitliğe: müşterilerimizin bizi tavsiye etmesinin dört nedeni.'),
  'cta': ['Hadi', 'başlayalım.'], 'form': 'İletişim formu',
  'places': ('lokasyon', 'eyalet', 'Viyana’dan Burgenland’a: planladığımız, inşa ettiğimiz, ek bina yaptığımız ya da yenilediğimiz yerler.'),
  'cookie': ('Çerezler ve gizlilik', 'Bu site yalnızca teknik olarak gerekli depolamayı (ör. bu tercih) kullanır; yazı tipleri ve 3D kütüphaneleri harici sunuculardan yüklenir. İzleme çerezi kullanılmaz.', 'Kabul et', 'Reddet'),
  'top': 'Yukarı çık',
  'process_p': 'Net adımlar, sabit muhatap, sürpriz yok: Menzil-Bau ile projeniz ilk görüşmeden anahtar teslimine kadar böyle ilerler.',
  'contact': (['Hadi', ('konuşalım.', 'red')], '24 saat içinde dönüş yapıyoruz.'),
  'certs': (['Ruhsatlı.', 'Sigortalı.', ('Denetimli.', 'red')], 'Belgeyi görüntüle'),
  'foot': ('Sayfalar', 'İletişim', 'Adresler', 'Hareketli sürüm', 'Klasik sürümü gör'),
 },
}


def lines(parts, last_cls=''):
    """Big headline split into masked lines. An item may be 'text' or ('text', 'class')."""
    out = []
    for i, x in enumerate(parts):
        txt, c = (x if isinstance(x, tuple) else (x, ''))
        if not c and last_cls and i == len(parts) - 1: c = last_cls
        out.append(f'<span class="line"><span{(" class=%s" % c) if c else ""}>{txt}</span></span>')
    return ''.join(out)

CLOSE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 6l12 12M18 6L6 18"/></svg>'
UP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 19V5M5 12l7-7 7 7"/></svg>'
DOC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 11h6M9 14h6M9 17h4"/></svg>'
CHK = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2" width="12" height="12"><path d="M3 8.5l3 3 7-7"/></svg>'
PIN_S = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s7-7 7-12a7 7 0 0 0-14 0c0 5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>'
PAGE_FILES = {'index': 'index.html', 'kontakt': 'kontakt.html', 'zertifikate': 'zertifikate.html', 'blog': 'blog.html'}
PAGE_FILES.update({f"blog-{p['slug']}": f"blog-{p['slug']}.html" for p in POSTS})


class Ctx:
    def __init__(self, lang, page):
        self.lang, self.page, self.t, self.v = lang, page, T[lang], V[lang]
        sub = lang != 'de'
        self.R = '../../' if sub else '../'           # → repo root
        self.VD = '../' if sub else ''                # → v2 dir
        self.A = self.R + 'assets/img/'
        self.CL = self.R + ('' if lang == 'de' else lang + '/')   # classic pages, same language
    def href(self, target_lang, page=None):
        f = PAGE_FILES[page or self.page]
        if self.lang == 'de': return f if target_lang == 'de' else f'{target_lang}/{f}'
        if target_lang == 'de': return f'../{f}'
        return f if target_lang == self.lang else f'../{target_lang}/{f}'
    def anchor(self, a):
        return f'#{a}' if self.page == 'index' else f'index.html#{a}'


def head(c, title, desc):
    return f'''<!DOCTYPE html>
<html lang="{c.lang}" translate="no">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="google" content="notranslate">
<meta name="theme-color" content="#121417">
{''.join(f'<link rel="alternate" hreflang="{l}" href="{c.href(l)}">' for l in LANGS)}
<link rel="icon" href="{c.R}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{c.VD}v2.css">
</head>
<body>
'''


def nav(c):
    v, t, n = c.v, c.t, c.v['nav']
    langs = ''.join(f'<a href="{c.href(l)}" hreflang="{l}" lang="{l}"{" class=on aria-current=true" if l == c.lang else ""}>{LANG_NAMES[l]}</a>' for l in LANGS)
    items = [(c.anchor('leistungen'), n[0]), (c.anchor('bauablauf'), n[1]), (c.anchor('modelle'), n[2]), (c.anchor('projekte'), n[3]),
             ('zertifikate.html', n[4]), ('blog.html', n[5]), ('kontakt.html', n[6])]
    cur = {'zertifikate': 4, 'blog': 5, 'kontakt': 6}.get(c.page, 5 if c.page.startswith('blog-') else -1)
    li = ''.join(f'<li><a href="{h}"{" aria-current=page class=cur" if i == cur else ""}>{E(x)}</a></li>' for i, (h, x) in enumerate(items))
    return f'''<div class="nav-wrap">
<header class="nav" aria-label="Navigation">
  <a class="nav-logo" href="{"#top" if c.page == "index" else "index.html"}" aria-label="Menzil-Bau">{logo_a(w=150)}</a>
  <ul class="nav-links">{li}
    <li class="nav-cta-m"><a class="pill pill-red" href="{SITE['calendar']}" target="_blank" rel="noopener">{CAL} {E(t['nav']['cta'])}</a></li>
  </ul>
  <div class="nav-right">
    <div class="nav-lang" role="group" aria-label="{E(v['langs'])}">{langs}</div>
    <a class="pill pill-red nav-cta" href="{SITE['calendar']}" target="_blank" rel="noopener" aria-label="{E(t['nav']['cta'])}">{CAL}<span class="cta-long">{E(t['nav']['cta'])}</span><span class="cta-short">{E(v['cta_short'])}</span></a>
    <button class="nav-burger" type="button" aria-label="{E(v['menu'])}" aria-expanded="false"><span></span></button>
  </div>
</header>
</div>
'''


def legal_modal(c):
    L = c.t['legal']
    return f'''<div class="v-modal" id="legalModal" role="dialog" aria-modal="true" aria-labelledby="legalTitle" hidden>
  <div class="v-modal-box">
    <button class="v-modal-close" type="button" aria-label="{E(c.t['lb']['close'])}">{CLOSE}</button>
    <div class="eyebrow">{E(L['eyebrow'])}</div>
    <h2 id="legalTitle">{E(L['title'])}</h2>
    <dl class="v-facts">
      <div><dt>{E(L['company'])}</dt><dd>{E(SITE['company'])}</dd></div>
      <div><dt>{E(L['address'])}</dt><dd>{E(SITE['addr2_plain'])}</dd></div>
      <div><dt>{E(L['contact'])}</dt><dd><a href="mailto:{SITE['email']}">{SITE['email']}</a> · {SITE['phone']}</dd></div>
    </dl>
    <div class="v-modal-body"><p>{E(c.t['p_kontakt']['impressum'])}</p>{''.join(f'<p>{E(x)}</p>' for x in LOREM)}</div>
  </div>
</div>'''


def footer(c):
    t, v, f = c.t, c.v, c.v['foot']
    ck = v['cookie']
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-word" aria-label="Menzil-Bau">{''.join(f'<span{" class=r" if i in (0, 7) else ""}>{ch}</span>' for i, ch in enumerate('MENZIL-BAU'))}</div>
    <div class="foot-cols">
      <div>{logo_a(w=200)}<p style="margin-top:14px;font-size:14px;color:rgba(255,255,255,.7);line-height:1.6;max-width:320px">{E(t['motto'])}.</p></div>
      <div><h4>{E(f[0])}</h4><ul><li><a href="{c.anchor('leistungen')}">{E(v['nav'][0])}</a></li><li><a href="{c.anchor('modelle')}">{E(v['nav'][2])}</a></li><li><a href="{c.CL}projekte.html">{E(t['nav']['projekte'])}</a></li><li><a href="{c.CL}referenzen.html">{E(t['nav']['referenzen'])}</a></li><li><a href="zertifikate.html">{E(v['nav'][4])}</a></li><li><a href="blog.html">{E(v['nav'][5])}</a></li><li><a href="kontakt.html">{E(v['nav'][6])}</a></li></ul></div>
      <div><h4>{E(f[1])}</h4><ul><li><a href="{SITE['phone_href']}">{SITE['phone_local']}</a></li><li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li><li><a href="{SITE['whatsapp']}" target="_blank" rel="noopener">WhatsApp</a></li><li>{E(SITE['hours'])}</li></ul></div>
      <div><h4>{E(f[2])}</h4><ul>{''.join(f'<li>{E(x)}</li>' for x in SITE['addr1'])}<li style="margin-top:10px">{'</li><li>'.join(E(x) for x in SITE['addr2'])}</li></ul></div>
    </div>
    <div class="foot-bottom"><span>&copy; {SITE['founded']}–{YEAR} Menzil-Bau · {E(t['footer']['rights'])}</span><span><button type="button" data-modal="legalModal">{E(t['footer']['impressum'])}</button> · <a href="{SITE['facebook']}" target="_blank" rel="noopener">Facebook</a></span></div>
  </div>
</footer>
<button class="to-top" type="button" aria-label="{E(v['top'])}">{UP}</button>
<div class="cookie" role="dialog" aria-label="{ck[0]}">
  <b>{ck[0]}</b>
  <p>{ck[1]} <a data-modal="legalModal">{E(t['footer']['impressum'])}</a></p>
  <div class="cookie-btns"><button class="pill pill-dark pill-sm" type="button" data-cookie="accepted">{E(ck[2])}</button><button class="pill pill-sm" type="button" data-cookie="declined" style="background:var(--paper-2)">{E(ck[3])}</button></div>
</div>
{legal_modal(c)}
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="{c.VD}v2.js" defer></script>
{chat_widget(c)}
'''


def chat_href(c, key):
    if key == 'calendar': return SITE['calendar']
    if key == 'phone': return SITE['phone_href']
    if key == 'whatsapp': return SITE['whatsapp']
    if key.startswith('home#'): return c.anchor(key[5:])
    if key in ('projekte', 'referenzen'): return f'{c.CL}{key}.html'
    return f'{key}.html'


def chat_widget(c):
    ui = CHAT_UI[c.lang]; L = c.lang
    data = {'ui': ui, 'chipIntents': CHIP_INTENTS,
            'intents': [{'id': i, 'kw': kw, 'a': ans[L], 'links': [{'l': CHAT_LINKS[k][L], 'h': chat_href(c, h)} for k, h in lk]} for i, kw, ans, lk in INTENTS],
            'fallbackLinks': [{'l': CHAT_LINKS[k][L], 'h': chat_href(c, h)} for k, h in [('call', 'phone'), ('whatsapp', 'whatsapp'), ('contact', 'kontakt')]]}
    js = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    BOT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 5h16v11H9l-5 4z"/><path d="M8 10h.01M12 10h.01M16 10h.01" stroke-width="2.6" stroke-linecap="round"/></svg>'
    return f'''<div class="chat">
  <div class="chat-panel" role="dialog" aria-label="{E(ui['name'])}">
    <div class="chat-head"><span class="chat-ava"><svg viewBox="0 6 72 72"><path d="M14 62V32L25 21L36 32L47 21L58 32V62" fill="none" stroke="#fff" stroke-width="6"/><rect x="32" y="44" width="8" height="18" fill="#fff"/></svg></span>
      <div><b>{E(ui['name'])}</b><small>{E(ui['sub'])}</small></div>
      <button class="chat-x" type="button" aria-label="{E(ui['close'])}">{CLOSE}</button></div>
    <div class="chat-log" aria-live="polite"></div>
    <form class="chat-form"><input class="chat-in" type="text" maxlength="200" placeholder="{E(ui['placeholder'])}" aria-label="{E(ui['placeholder'])}" autocomplete="off"><button type="submit" aria-label="{E(ui['send'])}">{ARROW}</button></form>
    <div class="chat-note">{E(ui['note'])}</div>
  </div>
  <button class="chat-fab" type="button" aria-label="{E(ui['open'])}" aria-expanded="false">{BOT}<span class="chat-fab-x">{CLOSE}</span></button>
</div>
<script>window.MENZIL_CHAT = {js};</script>
<script src="{c.VD}chat.js" defer></script>'''


def sub_hero(c, img, title_lines, sub, crumb):
    return f'''<section class="sub-hero">
  <div class="sub-hero-card">
    <img src="{c.A}photos/{img}.jpg" alt="">
    <div class="crumbs"><a href="index.html">Menzil-Bau</a> &nbsp;/&nbsp; {E(crumb)}</div>
    <h1>{lines(title_lines)}</h1>
    <p class="sub-hero-p">{E(sub)}</p>
  </div>
</section>
'''


def process_section(c, sid=''):
    z = c.t['p_zertifikate']
    steps = ''.join(f'<div class="pstep"><i>0{i + 1}</i><div><b>{E(a)}</b><p>{E(b)}</p></div></div>' for i, (a, b) in enumerate(z['steps']))
    return f'''<section class="process"{f' id="{sid}"' if sid else ''}>
  <div class="wrap">
    <div class="process-head">
      <h2 class="mega" data-split>{lines(z['process_title'].split('<br>'), 'muted')}</h2>
      <p>{E(c.v['process_p'])}</p>
    </div>
    <div class="process-grid" data-rise>{steps}</div>
  </div>
</section>'''


# ───────────────────────── pages ─────────────────────────
def page_index(c):
    t, v, A, CL = c.t, c.v, c.A, c.CL
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
    # grouped locations
    from data import REGION_OF
    groups = {'noe': [], 'bgld': [], 'wien': []}
    for p in PLACES: groups[REGION_OF.get(p, 'noe')].append(p)
    regions = ''.join(f'''<div class="region-col"><h4>{E(t['regions'][k])}<span>{len(g)}</span></h4><ul>{''.join(f'<li>{PIN_S}{E(x)}</li>' for x in g)}</ul></div>''' for k, g in groups.items() if g)
    nreg = sum(1 for g in groups.values() if g)
    pl = v['places']

    mt, mp, mtag, mhint, mplay, mspin, mgroup = v['models']
    model_tabs = ''.join(f'<button class="model-tab{" on" if i == 0 else ""}" type="button" data-model="{k}" aria-pressed="{"true" if i == 0 else "false"}">{E(n)}</button>' for i, (k, n, _, _) in enumerate(v['model_list']))
    model_data = ''.join(f'''<template id="info-{k}"><span class="tag">{E(mtag)}</span><h3>{E(n)}</h3><p>{E(d)}</p>
      <dl>{''.join(f'<dt>{E(a)}</dt><dd>{E(b)}</dd>' for a, b in specs)}</dl></template>''' for k, n, d, specs in v['model_list'])
    stats = ''.join(f'''<div class="stat-card{" gold" if i == 2 else ""}"><div class="stat-top"><span class="stat-tag">{E(tag)}</span></div>
        <div class="stat-num"><span data-count="{n}">{n}</span>{f"<em>{u}</em>" if u else ""}</div><div class="stat-desc">{E(d)}</div></div>'''
        for i, ((tag, d), (n, u)) in enumerate(zip(v['stats'], [('30', '+'), ('120', '+'), ('1', '')])))
    steps = ''.join(f'<li class="step"><b><i>0{i + 1}</i>{a}</b><p>{E(b)}</p></li>' for i, (a, b) in enumerate(v['steps']))
    pillars = ''.join(f'<div class="pillar"><div class="pillar-ico">{ic}</div><h3>{E(a)}</h3><p>{E(b)}</p></div>' for ic, (a, b) in zip([ICON_PLAN, ICON_BUILD, ICON_KEY], v['pillars']))
    bt = v['build']
    sw = v['scatter']

    return head(c, v['title'], t['meta']['index'][1]) + nav(c) + f'''
<main id="top">
<section class="hero">
  <div class="hero-card">
    <div class="hero-media" aria-hidden="true">
      <img src="{A}photos/f01.jpg" alt=""><img src="{A}photos/f13.jpg" alt=""><img src="{A}photos/f15.jpg" alt=""><img src="{A}photos/f10.jpg" alt="">
    </div>
    <div class="hero-eyebrow">{E(t['hero']['eyebrow'])}</div>
    <h1 class="hero-title">{lines(v['hero'])}</h1>
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

<section class="places">
  <div class="wrap">
    <div class="places-card">
      <div class="places-hero">
        <div class="places-eyebrow">{E(t['featured']['places_title'])}</div>
        <div class="places-nums">
          <div><span data-count="{len(PLACES)}">{len(PLACES)}</span><small>{E(pl[0])}</small></div>
          <div><span data-count="{nreg}">{nreg}</span><small>{E(pl[1])}</small></div>
        </div>
        <p>{E(pl[2])}</p>
      </div>
      <div class="regions">{regions}</div>
    </div>
  </div>
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
      <div class="model-stage" id="modelStage">
      <div class="model-tools">
        <button type="button" id="mReplay" aria-label="{E(mplay)}" title="{E(mplay)}">{PLAY}</button>
        <button type="button" id="mSpin" class="on" aria-label="{E(mspin)}" title="{E(mspin)}">{ROT}</button>
      </div>
      <div class="model-hint">{DRAG} {E(mhint)}</div>
      </div>
      <div class="model-info" id="modelInfo"></div>
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
  <div class="scatter-sticky"><div class="scatter-inner">
    <div class="sw" style="left:0;top:10%">{E(sw[0])}</div>
    <div class="sw red" style="left:0;top:30%">{E(sw[1])}</div>
    <div class="sw" style="left:0;top:53%">{E(sw[2])}</div>
    <div class="sw red" style="left:0;top:73%">{E(sw[3])}</div>
    <a class="sp" href="{CL}projekte.html" style="right:0;top:8%;width:240px;height:300px"><img src="{A}photos/f13-t.jpg" alt="{E(feat.get('f13', ''))} – Menzil-Bau"></a>
    <a class="sp" href="{CL}projekte.html" style="right:270px;top:22%;width:250px;height:180px"><img src="{A}photos/f52-t.jpg" alt="{E(feat.get('f52', ''))} – Menzil-Bau"></a>
    <a class="sp" href="{CL}projekte.html" style="right:0;top:56%;width:280px;height:200px"><img src="{A}photos/f15-t.jpg" alt="{E(feat.get('f15', ''))} – Menzil-Bau"></a>
    <a class="sp" href="{CL}projekte.html" style="right:310px;top:52%;width:210px;height:260px"><img src="{A}photos/f64-t.jpg" alt="{E(feat.get('f64', ''))} – Menzil-Bau"></a>
  </div></div>
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

{process_section(c, 'ablauf')}

<section class="reviews"><div class="wrap rev-grid" data-rise>{reviews}</div></section>

<section class="cta" id="kontakt">
  <div class="wrap">
    <h2 class="mega" data-split>{lines(v['cta'], 'red')}</h2>
    <p>{E(t['cta']['sub'])}</p>
    <div class="cta-box">
      <a class="pill pill-red" href="{SITE['calendar']}" target="_blank" rel="noopener">{CAL} {E(t['cta']['btn1'])}</a>
      <a class="pill pill-dark" href="{SITE['phone_href']}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{TEL[TEL.index('<path'):TEL.index('</svg>')]}</svg> {SITE['phone_local']}</a>
      <a class="pill pill-white" href="kontakt.html">{E(v['form'])} {ARROW}</a>
    </div>
  </div>
</section>
</main>
''' + footer(c) + f'''<script type="importmap">{{"imports": {{"three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js", "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}}}</script>
<script type="module">
  import {{ makeModel, createViewer }} from '{c.VD or "./"}houses.js';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fl = document.getElementById('float3d');
  if (fl && getComputedStyle(fl).display !== 'none') {{
    const v = createViewer(fl, {{ autoRotate: reduce ? 0 : 1.2, camPos: [26, 20, 30], target: [0, 3, 0], fov: 30 }});
    const m = makeModel('efh', {{ floating: true }}); m.setProgress(1); v.setModel(m);
  }}
  const bv = createViewer(document.getElementById('buildStage'), {{ autoRotate: reduce ? 0 : 0.35, camPos: [24, 17, 28], target: [0, 3.2, 0], fov: 30 }});
  const bm = makeModel('efh'); bm.setProgress(reduce ? 1 : 0); bv.setModel(bm);
  window.__buildProgress = p => bm.setProgress(Math.min(1, p * 1.08));
  const view = document.getElementById('modelStage'), info = document.getElementById('modelInfo');
  const small = matchMedia('(max-width: 760px)').matches;
  const mv = createViewer(view, {{ interactive: true, autoRotate: reduce ? 0 : 1.1, camPos: small ? [34, 22, 40] : [26, 16, 30], target: [0, 4, 0], fov: 30 }});
  let current = null, anim = 0;
  function play(model) {{
    cancelAnimationFrame(anim);
    if (reduce) {{ model.setProgress(1); return; }}
    const t0 = performance.now(), dur = 2600;
    const tick = now => {{ const p = Math.min(1, (now - t0) / dur); model.setProgress(p); if (p < 1) anim = requestAnimationFrame(tick); }};
    anim = requestAnimationFrame(tick);
  }}
  function load(type) {{
    current = pre[type] || makeModel(type); pre[type] = null; mv.setModel(current); play(current);
    info.innerHTML = document.getElementById('info-' + type).innerHTML;
    document.querySelectorAll('.model-tab').forEach(b => {{ const on = b.dataset.model === type; b.classList.toggle('on', on); b.setAttribute('aria-pressed', on); }});
  }}
  document.querySelectorAll('.model-tab').forEach(b => b.addEventListener('click', () => load(b.dataset.model)));
  document.getElementById('mReplay').addEventListener('click', () => play(current));
  const spin = document.getElementById('mSpin');
  spin.addEventListener('click', () => {{ spin.classList.toggle('on'); mv.controls.autoRotate = spin.classList.contains('on'); }});
  // prepare everything while the browser is idle, so scrolling past the 3D sections never stalls
  const idle = window.requestIdleCallback || (f => setTimeout(f, 300));
  const pre = {{}};
  idle(() => {{
    bv.warm();
    for (const k of ['efh', 'dh', 'mfh']) {{ pre[k] = makeModel(k); }}
    mv.setModel(pre.efh); pre.efh.setProgress(1); mv.warm();
    pre.efh.setProgress(0); current = pre.efh;
  }});
  let started = false;
  new IntersectionObserver(([e]) => {{ if (e.isIntersecting && !started) {{ started = true; load('efh'); }} }}, {{ threshold: 0.3 }}).observe(view);
</script>
</body>
</html>
'''


def page_kontakt(c):
    t, v = c.t, c.v
    k, f, ft = t['p_kontakt'], t['form'], t['footer']
    opts = ''.join(f'<option value="{code}"{" selected" if code == "+43" else ""}>{fl} {code}</option>' for code, fl in COUNTRIES)
    types = ''.join(f'<option>{E(x)}</option>' for x in f['types'])
    maps = 'https://www.google.com/maps/search/?api=1&query=' + '+'.join(SITE['addr2_plain'].replace(',', '').split())
    a1 = '<br>'.join(E(x) for x in SITE['addr1']); a2 = '<br>'.join(E(x) for x in SITE['addr2'])
    title, reply = v['contact']
    return head(c, f"{t['meta']['kontakt'][0]}", t['meta']['kontakt'][1]) + nav(c) + sub_hero(c, 'f02', title, k['sub'], v['nav'][5]) + f'''
<main>
<section class="contact">
  <div class="wrap contact-grid2" data-rise>
    <div class="c-info">
      <a class="c-card" href="{SITE['phone_href']}"><span class="c-ico">{TEL}</span><span class="c-label">{E(k['phone'])}</span><span class="c-val">{SITE['phone_local']}<small>{SITE['phone']}</small></span></a>
      <a class="c-card" href="{SITE['whatsapp']}" target="_blank" rel="noopener"><span class="c-ico">{WA}</span><span class="c-label">{E(k['whatsapp'])}</span><span class="c-val">{E(k['whatsapp_cta'])}<small>{SITE['phone']}</small></span></a>
      <a class="c-card" href="mailto:{SITE['email']}"><span class="c-ico">{MAIL}</span><span class="c-label">{E(k['email'])}</span><span class="c-val" style="font-size:20px;text-transform:none">{SITE['email']}</span></a>
      <div class="c-card"><span class="c-ico">{CLOCK}</span><span class="c-label">{E(k['hours'])}</span><span class="c-val">{E(SITE['hours'])}</span></div>
      <div class="c-card wide"><div class="c-addr"><div><b>{E(ft['addr1'])}</b>{a1}</div><div><b>{E(ft['addr2'])}</b>{a2}<br><a href="{maps}" target="_blank" rel="noopener">{E(k['route'])} →</a></div></div></div>
      <a class="c-card wide dark" href="{SITE['calendar']}" target="_blank" rel="noopener"><span class="c-ico">{CAL}</span><span><span class="c-label">{E(t['nav']['cta'])}</span><span class="c-val">{E(k['book'])} {ARROW}</span></span></a>
    </div>
    <div class="form-card">
      <h2>{E(f['title'])}</h2>
      <p>{E(reply)}</p>
      <form class="v-form" novalidate data-endpoint="{SITE['form_endpoint']}" data-subject="{E(f['subject'])}" data-sending="{E(f['sending'])}" data-err="{E(f['err'])}" data-net-err="{E(f['net_err'])}">
        <input class="v-in" name="first_name" placeholder="{E(f['first'])}" aria-label="{E(f['first'])}" autocomplete="given-name" data-letters required>
        <input class="v-in" name="last_name" placeholder="{E(f['last'])}" aria-label="{E(f['last'])}" autocomplete="family-name" data-letters required>
        <div class="v-phone full"><select class="v-in" name="country" aria-label="+43">{opts}</select><input class="v-in" name="phone" type="tel" inputmode="numeric" placeholder="{E(f['phone'])}" aria-label="{E(f['phone'])}" autocomplete="tel-national" required></div>
        <input class="v-in full" name="email" type="email" placeholder="{E(f['email'])}" aria-label="{E(f['email'])}" autocomplete="email" required>
        <span class="v-form-err full" hidden>{E(f['email_err'])}</span>
        <select class="v-in" name="project_type" aria-label="{E(f['type'])}"><option value="" selected disabled>{E(f['type'])}</option>{types}</select>
        <input class="v-in" name="location" placeholder="{E(f['location'])}" aria-label="{E(f['location'])}">
        <textarea class="v-in full" name="message" placeholder="{E(f['message'])}" aria-label="{E(f['message'])}"></textarea>
        <button class="pill pill-red full" type="submit">{E(f['submit'])} {ARROW}</button>
        <p class="v-note full">{E(f['privacy'])}</p>
      </form>
      <div class="v-form-ok" hidden><svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2.4"><path d="M20 6L9 17l-5-5"/></svg><b>✓</b><p>{E(f['success'])}</p><button class="pill pill-ghost" type="button">{E(f['again'])}</button></div>
    </div>
  </div>
</section>
</main>
''' + footer(c) + '</body>\n</html>\n'


def page_zertifikate(c):
    t, v = c.t, c.v
    z = t['p_zertifikate']; cv = t['cert']
    title, view = v['certs']
    cards = ''.join(f'''<button class="vcert" type="button" data-modal="cert{i}">
        <span class="vcert-no">0{i + 1}</span>{seal(a, i, 'c')}
        <h3>{E(a)}</h3><p>{E(d)}</p>
        <span class="chip">{CHK} {E(b)}</span>
        <span class="vcert-foot">{E(view)} {ARROW}</span>
      </button>''' for i, (a, b, d) in enumerate(z['badges']))
    modals = ''.join(f'''<div class="v-modal" id="cert{i}" role="dialog" aria-modal="true" aria-labelledby="certT{i}" hidden>
  <div class="v-modal-box">
    <button class="v-modal-close" type="button" aria-label="{E(t['lb']['close'])}">{CLOSE}</button>
    <div class="v-cert-head">{seal(a, i, 'm')}<div><div class="eyebrow">{E(cv['label'])} 0{i + 1}</div><h2 id="certT{i}">{E(a)}</h2><span class="chip">{CHK} {E(b)}</span></div></div>
    <p style="color:var(--mid);line-height:1.65">{E(d)}</p>
    <div class="v-doc">{DOC.replace('<svg ', '<svg width="34" height="34" ')}<strong>{E(cv['pending_title'])}</strong><span>{E(cv['pending'])}</span></div>
  </div>
</div>''' for i, (a, b, d) in enumerate(z['badges']))
    return head(c, t['meta']['zertifikate'][0], t['meta']['zertifikate'][1]) + nav(c) + sub_hero(c, 'f14', title, z['sub'], v['nav'][4]) + f'''
<main>
<section class="certs">
  <div class="wrap">
    <!-- PLATZHALTER: Nachweise werden nach Erhalt der Originaldokumente ersetzt -->
    <div class="cert-grid2" data-rise>{cards}</div>
    <p style="margin-top:20px;color:var(--mid);font-size:14px">{E(z['note'])}</p>
  </div>
</section>
{process_section(c)}
{modals}
</main>
''' + footer(c) + '</body>\n</html>\n'


def post_card(c, p, big=False):
    L = c.lang; P = p[L]; ui = BLOG_UI[L]
    return f'''<a class="post-card{' big' if big else ''}" href="blog-{p['slug']}.html">
      <div class="post-img"><img src="{c.A}{p['img']}{'' if big else '-t'}.jpg" alt="{E(p['alt'][L])}" loading="lazy" width="{1128 if big else 720}" height="{768 if big else 402}"></div>
      <div class="post-body"><div class="post-meta"><span class="chip">{E(p['cat'][L])}</span><span>{p['read']} {E(ui['read'])}</span></div>
        <h3>{E(P['title'])}</h3><p>{E(P['lead'])}</p><span class="post-more">{E(ui['more'])} {ARROW}</span></div>
    </a>'''


def page_blog(c):
    ui = BLOG_UI[c.lang]
    cards = post_card(c, POSTS[0], True) + ''.join(post_card(c, p) for p in POSTS[1:])
    return head(c, ui['meta'], ui['meta_d']) + nav(c) + sub_hero(c, 'f10', ui['title'], ui['sub'], 'Blog') + f'''
<main>
<section class="blog"><div class="wrap"><div class="post-grid" data-rise>{cards}</div></div></section>
</main>
''' + footer(c) + '</body>\n</html>\n'


def make_post_page(post):
    def page(c):
        L = c.lang; P = post[L]; ui = BLOG_UI[L]
        body = ''.join(f'<h2>{E(h)}</h2><p>{E(t)}</p>' for h, t in P['body'])
        others = ''.join(post_card(c, p) for p in POSTS if p is not post)
        return head(c, f"{P['title']} | Menzil-Bau", P['lead']).replace('<meta name="theme-color"', f'<meta property="og:image" content="{SITE['public_base']}assets/img/{post["img"]}.jpg">\n<meta property="og:title" content="{E(P["title"])}">\n<meta name="theme-color"', 1) + nav(c) + f'''
<main>
<article class="post">
  <header class="post-hero">
    <div class="wrap post-hero-in">
      <div class="crumbs dark"><a href="index.html">Menzil-Bau</a> &nbsp;/&nbsp; <a href="blog.html">Blog</a></div>
      <div class="post-meta"><span class="chip">{E(post['cat'][L])}</span><span>{post['read']} {E(ui['read'])}</span><time datetime="{BLOG_DATE}">{BLOG_DATE[8:10]}.{BLOG_DATE[5:7]}.{BLOG_DATE[:4]}</time></div>
      <h1>{E(P['title'])}</h1>
      <p class="post-lead">{E(P['lead'])}</p>
    </div>
    <div class="wrap"><figure class="post-cover"><img src="{c.A}{post['img']}.jpg" alt="{E(post['alt'][L])}"></figure></div>
  </header>
  <div class="wrap post-content">{body}
    <div class="post-cta"><div><b>{E(ui['cta_title'])}</b><p>{E(ui['cta_p'])}</p></div>
      <a class="pill pill-red" href="{SITE['calendar']}" target="_blank" rel="noopener">{CAL} {E(c.t['nav']['cta'])}</a></div>
    <p><a class="post-back" href="blog.html">← {E(ui['back'])}</a></p>
  </div>
</article>
<section class="blog related"><div class="wrap"><h2 class="mega" style="font-size:clamp(36px,4.5vw,64px);text-align:left;margin-bottom:26px">{E(ui['related'])}</h2><div class="post-grid two">{others}</div></div></section>
</main>
''' + footer(c) + '</body>\n</html>\n'
    return page


PAGES_V2 = {'index': page_index, 'kontakt': page_kontakt, 'zertifikate': page_zertifikate, 'blog': page_blog}
PAGES_V2.update({f"blog-{p['slug']}": make_post_page(p) for p in POSTS})


def main():
    for lang in LANGS:
        out = os.path.join(ROOT, 'v2') if lang == 'de' else os.path.join(ROOT, 'v2', lang)
        os.makedirs(out, exist_ok=True)
        for page, fn in PAGES_V2.items():
            with open(os.path.join(out, PAGE_FILES[page]), 'w', encoding='utf-8') as fh:
                fh.write(fn(Ctx(lang, page)))
    print('built v2: ' + ', '.join(LANGS) + ' × ' + ', '.join(PAGES_V2))


if __name__ == '__main__':
    main()
