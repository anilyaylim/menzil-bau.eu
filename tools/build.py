# -*- coding: utf-8 -*-
"""Static site generator for menzil-bau.eu  (no dependencies except Pillow for image sizes).

    python3 tools/build.py

Generates  index.html, projekte.html, referenzen.html, zertifikate.html, kontakt.html
for DE (root), /en/ and /tr/ from tools/data.py.
"""
import os, sys, html
from datetime import date
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from data import SITE, PHOTOS, PROJECTS, LANGS, LANG_NAMES, PAGES, T, PLACES, REGION_OF, LOREM
try:
    from PIL import Image
except ImportError:  # sizes only used for gallery layout
    Image = None

E = html.escape
YEAR = date.today().year
R, RH, W = '#B3000A', '#D7141C', '#E9E6E1'

# ═══════════════════════ SVG library ═══════════════════════
FONT = "font-family=\"'Barlow Condensed','Arial Narrow',sans-serif\""

def wordmark(x, y, size, ls, fill='#fff', accent=RH, weight=800):
    """MENZIL-BAU with M and B accented – as in the original Menzil-Bau logo."""
    return (f'<text x="{x}" y="{y}" {FONT} font-weight="{weight}" font-size="{size}" letter-spacing="{ls}" fill="{fill}">'
            f'<tspan fill="{accent}">M</tspan>ENZIL-<tspan fill="{accent}">B</tspan>AU</text>')

LOGO_A_W = 316
def logo_a(fill='#fff', sub='#E9E6E1', bar='#B08D57', accent=RH, w=230, label='Menzil-Bau'):
    h = round(w * 84 / LOGO_A_W)
    return (f'<svg viewBox="0 0 {LOGO_A_W} 84" width="{w}" height="{h}" role="img" aria-label="{label}">'
            f'<rect x="0" y="6" width="72" height="72" fill="{R}"/>'
            f'<path d="M14 62V32L25 21L36 32L47 21L58 32V62" fill="none" stroke="#fff" stroke-width="5.5"/>'
            f'<rect x="32" y="44" width="8" height="18" fill="#fff"/>'
            + wordmark(88, 50, 46, 1.5, fill, accent) +
            f'<rect x="88" y="60" width="22" height="2" fill="{bar}"/>'
            f'<text x="118" y="68" {FONT} font-weight="500" font-size="15" letter-spacing="7" fill="{sub}">SEIT 2010</text></svg>')

def logo_b(w=330, h=120, label='Menzil-Bau'):
    """Crane logo – trolley travels, hook sways (SMIL, works inside <use> as well)."""
    return (f'<svg viewBox="0 0 330 122" width="{w}" height="{h}" role="img" aria-label="{label}">'
            f'<g stroke="{W}" stroke-width="2" fill="none">'
            '<path d="M22 70V8M34 70V8M22 8H34M22 20L34 32M34 20L22 32M22 32L34 44M34 32L22 44M22 44L34 56M34 44L22 56"/>'
            '<path d="M4 8H300" stroke-width="3"/><path d="M28 0V8M28 0L4 8M28 0L300 8" stroke-width="1.4" opacity=".7"/>'
            f'<rect x="4" y="10" width="14" height="10" fill="{W}" stroke="none"/></g>'
            '<g><animateTransform attributeName="transform" type="translate" values="0 0;-120 0;0 0" dur="9s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/>'
            f'<rect x="236" y="8" width="12" height="5" fill="{R}"/>'
            '<g><animateTransform attributeName="transform" type="rotate" values="-6 242 13;6 242 13;-6 242 13" dur="3.2s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/>'
            f'<path d="M242 13V40" stroke="{W}" stroke-width="1.4"/><path d="M238 40h8v3a4 4 0 1 1-8 0" fill="none" stroke="{RH}" stroke-width="2.4"/></g></g>'
            + wordmark(44, 102, 52, 1) +
            '<rect x="46" y="112" width="22" height="2" fill="#B08D57"/>'
            f'<text x="76" y="117" {FONT} font-weight="500" font-size="11" letter-spacing="3.4" fill="#8C9198">PLANUNG · ROHBAU · SANIERUNG</text></svg>')

def crane(w=300, h=122):
    return (f'<svg viewBox="0 0 300 122" width="{w}" height="{h}" fill="none" stroke="{W}" stroke-width="2" aria-hidden="true">'
            '<path d="M60 120V14M74 120V14M60 14H74"/>'
            '<path d="M60 26L74 40M74 26L60 40M60 40L74 54M74 40L60 54M60 54L74 68M74 54L60 68M60 68L74 82M74 68L60 82M60 82L74 96M74 82L60 96M60 96L74 110M74 96L60 110"/>'
            '<path d="M10 14H290" stroke-width="3"/><path d="M67 2V14M67 2L10 14M67 2L290 14" stroke-width="1.3" opacity=".7"/>'
            f'<rect x="12" y="16" width="26" height="14" fill="{W}" stroke="none"/><rect x="76" y="18" width="16" height="12"/>'
            '<g><animateTransform attributeName="transform" type="translate" values="0 0;80 0;0 0" dur="8s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/>'
            f'<rect x="150" y="14" width="14" height="6" fill="{R}" stroke="none"/>'
            '<g><animateTransform attributeName="transform" type="rotate" values="-5 157 20;5 157 20;-5 157 20" dur="3.4s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/>'
            f'<path d="M157 20V64" stroke-width="1.3"/><path d="M152 64h10v4a5 5 0 1 1-10 0" stroke="{RH}" stroke-width="2.6"/>'
            '<rect x="144" y="76" width="26" height="16" stroke-width="1.6"/><path d="M144 84H170" stroke-width="1" opacity=".5"/></g></g>'
            '<path d="M40 120H96" stroke-width="3"/></svg>')

def excavator(w=260, h=122):
    return (f'<svg viewBox="0 0 260 122" width="{w}" height="{h}" fill="none" stroke="{W}" stroke-width="2.4" aria-hidden="true">'
            '<rect x="14" y="96" width="132" height="22" rx="11"/><circle cx="28" cy="107" r="6"/><circle cx="132" cy="107" r="6"/>'
            '<circle cx="80" cy="107" r="4" opacity=".6"><animateTransform attributeName="transform" type="rotate" from="0 80 107" to="360 80 107" dur="2s" repeatCount="indefinite"/></circle>'
            '<path d="M58 99V115M102 99V115" stroke-width="1.4" opacity=".45"/>'
            '<path d="M20 96V66H76V40H112L120 66H140V96Z"/><path d="M82 46H108L114 64H82Z" opacity=".6"/><path d="M20 78H70" opacity=".5"/>'
            f'<circle cx="34" cy="56" r="3" fill="{RH}" stroke="none"><animate attributeName="opacity" values="1;.15;1" dur="1.4s" repeatCount="indefinite"/></circle><path d="M34 59V66" stroke-width="2"/>'
            '<g><animateTransform attributeName="transform" type="rotate" values="0 136 70;-10 136 70;0 136 70" dur="4s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/>'
            '<path d="M136 70L186 22L232 56" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M232 56L246 86L222 92L214 72Z" stroke="{RH}" stroke-width="2.6"/><path d="M160 58L186 30" stroke-width="1.4" opacity=".6"/></g></svg>')

def mixer(w=290, h=122):
    return (f'<svg viewBox="0 0 290 122" width="{w}" height="{h}" fill="none" stroke="{W}" stroke-width="2.4" aria-hidden="true">'
            '<path d="M12 96H272"/><path d="M206 96V54H240L268 78V96"/><path d="M214 60H238L256 78H214Z" opacity=".6"/>'
            '<g transform="rotate(-10 110 64)"><ellipse cx="110" cy="64" rx="74" ry="30"/>'
            f'<ellipse cx="110" cy="64" rx="74" ry="30" stroke="{RH}" stroke-width="3" stroke-dasharray="14 34"><animate attributeName="stroke-dashoffset" values="0;-48" dur="1.4s" repeatCount="indefinite"/></ellipse>'
            '<path d="M184 60L200 54"/><path d="M40 70L30 86" opacity=".6"/></g>'
            '<path d="M40 96V84M180 96V84"/>'
            + ''.join(f'<circle cx="{x}" cy="104" r="12"/><g><animateTransform attributeName="transform" type="rotate" from="0 {x} 104" to="360 {x} 104" dur="1.6s" repeatCount="indefinite"/><path d="M{x-7} 104H{x+7}M{x} 97V111" stroke-width="1.6"/></g>' for x in (48, 84, 236)) +
            '</svg>')

def house():
    """Detached house for the build scene. Each layer is animated by CSS (see .bs-house in style.css)."""
    G = '#D9B26A'
    star = lambda x, y, r, d: (f'<path class="h-star" style="animation-delay:{d}s" transform="translate({x} {y})" '
                               f'd="M0 -{r}L{r*.28} -{r*.28}L{r} 0L{r*.28} {r*.28}L0 {r}L-{r*.28} {r*.28}L-{r} 0L-{r*.28} -{r*.28}Z" fill="{G}"/>')
    bricks = ''.join(f'<path d="M42 {y}H218" />' for y in range(66, 118, 8))
    return (f'<svg viewBox="0 0 260 122" width="260" height="122" fill="none" aria-hidden="true">'
            '<defs><clipPath id="houseClip"><path d="M40 118V60L28 60L130 14L232 60H220V118Z"/></clipPath>'
            '<linearGradient id="sweepGrad" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
            f'<path d="M0 118.5H260" stroke="{W}" stroke-width="2.4"/>'
            # blueprint outline
            f'<g class="h-blueprint" stroke="{G}" stroke-width="1.6">'
            '<path pathLength="1" d="M40 118V60H220V118"/><path pathLength="1" d="M28 60L130 14L232 60"/>'
            '<path pathLength="1" d="M116 118V86H144V118M62 74H92V98H62ZM168 74H198V98H168Z"/></g>'
            # walls
            f'<g class="h-walls"><rect x="40" y="60" width="180" height="58" fill="#2A2F36" stroke="{W}" stroke-width="2.4"/>'
            f'<g stroke="{W}" stroke-width="1" opacity=".14">{bricks}</g>'
            f'<rect class="h-win" x="62" y="74" width="30" height="24" fill="#3A4049" stroke="{W}" stroke-width="2"/><path d="M77 74V98M62 86H92" stroke="{W}" stroke-width="1.2"/>'
            f'<rect class="h-win" x="168" y="74" width="30" height="24" fill="#3A4049" stroke="{W}" stroke-width="2"/><path d="M183 74V98M168 86H198" stroke="{W}" stroke-width="1.2"/>'
            f'<path d="M116 118V86H144V118" fill="#121417" stroke="{W}" stroke-width="2"/><circle cx="138" cy="103" r="1.6" fill="{G}"/></g>'
            # scaffolding
            '<g class="h-scaffold" stroke="#8C9198" stroke-width="1.4"><path d="M32 118V52M228 118V52M32 98H228M32 78H228M32 58H228M32 98L52 78M208 98L228 78"/></g>'
            # roof + chimney
            f'<g class="h-roof"><rect x="172" y="22" width="14" height="26" fill="#2A2F36" stroke="{W}" stroke-width="2"/>'
            f'<path d="M22 62L130 12L238 62Z" fill="{R}" stroke="{W}" stroke-width="2.4" stroke-linejoin="round"/>'
            '<path d="M60 45L130 23L200 45" stroke="#fff" stroke-width="1" opacity=".25"/><circle cx="130" cy="40" r="6" fill="#121417" stroke="#fff" stroke-width="1.6"/></g>'
            # light sweep
            '<g clip-path="url(#houseClip)"><rect class="h-sweep" x="-60" y="0" width="60" height="122" fill="url(#sweepGrad)" transform="skewX(-18)"/></g>'
            # sparkles
            '<g class="h-stars">' + star(14, 30, 7, 0) + star(246, 38, 6, .5) + star(130, 4, 5, .9) + star(60, 18, 4, 1.3) + star(206, 10, 5, .3) + star(250, 92, 4, 1.1) + star(8, 84, 4, .7) + '</g>'
            '</svg>')

def build_scene(c):
    """Desktop hero band: machines arrive → construction (progress) → finished house with shine. Loops (14 s)."""
    b = c['t']['build']
    return f'''<div class="build-band" aria-hidden="true">
    <div class="build-stage">
      <div class="bs-item bs-mixer">{mixer()}</div>
      <div class="bs-item bs-exc">{excavator()}</div>
      <div class="bs-item bs-crane">{crane()}</div>
      <div class="bs-house">{house()}</div>
      <div class="bs-progress">
        <div class="bs-label"><span class="bs-l1">{E(b['label'])}</span><span class="bs-l2">&#10003; {E(b['done'])}</span><span class="bs-pct"></span></div>
        <div class="bs-bar"><i></i></div>
      </div>
    </div>
  </div>'''

def parade(scale=1.0, sets=4):
    one = crane(int(300 * scale), int(122 * scale)) + excavator(int(260 * scale), int(122 * scale)) + mixer(int(290 * scale), int(122 * scale))
    return one * sets

ICON = {
    'check': '<svg class="ps-icon" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 9l5 5 7-8"/></svg>',
    'x': '<svg class="ps-icon" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 4l10 10M14 4L4 14"/></svg>',
    'clock': '<svg class="ps-icon" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="9" cy="9" r="7"/><path d="M9 5v4l3 2"/></svg>',
    'euro': '<svg class="ps-icon" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M13 4.5A5.5 5.5 0 1 0 13 13.5M3 7.5h7M3 10.5h7"/></svg>',
    'users': '<svg class="ps-icon" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="6.5" cy="6" r="2.5"/><circle cx="12.5" cy="7" r="2"/><path d="M2 15c0-2.5 2-4 4.5-4s4.5 1.5 4.5 4M11 11.2c2.6-.4 5 1 5 3.8"/></svg>',
    'layers': '<svg class="ps-icon" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 2l7 4-7 4-7-4z"/><path d="M2 10l7 4 7-4" opacity=".6"/></svg>',
    'phone': '<svg class="ps-icon" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 2h3l1.5 4-2 1.2a8 8 0 0 0 4.3 4.3L12 9.5l4 1.5v3a2 2 0 0 1-2 2A13 13 0 0 1 2 4a2 2 0 0 1 2-2z"/></svg>',
}
PROB_ICONS = ['clock', 'euro', 'users', 'layers', 'phone']
SVC_ICONS = [
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 21h18M5 21V9l7-5 7 5v12"/><path d="M9 21v-6h6v6"/><path d="M2 3l4 0M2 3v4" opacity=".5"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="15" width="9" height="5"/><rect x="13" y="15" width="9" height="5"/><rect x="7" y="9" width="10" height="5"/><rect x="4" y="3" width="7" height="5" opacity=".6"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="4" y="3" width="16" height="18"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2"/><path d="M10 21v-3h4v3"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 21V10l6-5 6 5v11z"/><path d="M15 21h6v-7l-3-3-3 3" /><path d="M7 14h4" opacity=".6"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 2v6l9 0"/><path d="M13 8v3"/><circle cx="13" cy="14" r="3"/><path d="M3 22h18"/><path d="M15 22v-4h4v4M17 18v-3" opacity=".6"/></svg>',
]
PIN = '<svg class="ref-pin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 22s7-7 7-12a7 7 0 0 0-14 0c0 5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>'
CAL = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="2" width="14" height="13" rx="1.5"/><path d="M1 6h14M5 1v3M11 1v3"/></svg>'
TEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>'
MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="14"/><path d="M3 6l9 7 9-7"/></svg>'
WA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 20l1.3-4A8 8 0 1 1 8.2 19z"/><path d="M9 9.5c.5 2.5 2.5 4.5 5 5l1.2-1.3-1.8-1-1 .8a4 4 0 0 1-2-2l.8-1-1-1.8z" stroke-width="1.3"/></svg>'
CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 8h11M9 4l4 4-4 4"/></svg>'
SEND = '<svg width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 4l6 5 6-5M2 4h12v9H2V4z"/></svg>'

# Distinct line icons per credential (24×24 grid, drawn white on the red medallion)
CERT_ICONS = [
    # trade licence: document with seal
    '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4"/><path d="M9 10h6M9 13h4"/><circle cx="13.5" cy="17.5" r="2.2"/><path d="M12.3 19.4l-.8 2.6 2-1 2 1-.8-2.6"/>',
    # chamber of commerce: classical building
    '<path d="M3 9l9-5 9 5"/><path d="M4 9h16"/><path d="M6 9v9M10 9v9M14 9v9M18 9v9"/><path d="M3 18h18M2 21h20"/>',
    # liability insurance: shield with check
    '<path d="M12 3l8 3v6c0 4.6-3.4 8.2-8 9-4.6-.8-8-4.4-8-9V6z"/><path d="M8.5 12.2l2.5 2.5 4.8-5"/>',
    # ÖNORM: set square + ruler
    '<path d="M4 20V5l15 15z"/><path d="M8 16v-3l3 3z"/><path d="M4 9h2M4 12h3M4 15h2"/>',
    # occupational safety: hard hat
    '<path d="M4 17a8 8 0 0 1 16 0"/><path d="M2.5 17h19v2.5h-19z"/><path d="M10 9.5V6.5h4v3"/><path d="M12 9v8"/>',
    # foreman school: graduation cap
    '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c0 1.6 2.7 3 6 3s6-1.4 6-3v-5"/><path d="M22 9v6"/>',
]

def seal(top, i):
    """Placeholder credential medallion (no third-party logos) – ring text, gold ticks, own icon per credential."""
    pid = f'sealpath{i}'
    ticks = ''.join(f'<path d="M50 4.5v3" transform="rotate({a} 50 50)"/>' for a in range(0, 360, 15))
    icon = CERT_ICONS[i % len(CERT_ICONS)]
    return (f'<svg class="cert-seal" viewBox="0 0 100 100" aria-hidden="true">'
            f'<defs><path id="{pid}" d="M50 50m-36 0a36 36 0 1 1 72 0a36 36 0 1 1-72 0"/>'
            f'<radialGradient id="sealg{i}" cx="40%" cy="35%"><stop offset="0" stop-color="{RH}"/><stop offset="1" stop-color="#7E0007"/></radialGradient></defs>'
            f'<circle cx="50" cy="50" r="48" fill="#fff" stroke="#B08D57" stroke-width="1.5"/>'
            f'<g class="seal-ticks" stroke="#B08D57" stroke-width="1.2">{ticks}</g>'
            f'<circle cx="50" cy="50" r="41.5" fill="none" stroke="#121417" stroke-width=".8" opacity=".35"/>'
            f'<text font-family="\'Barlow Condensed\',sans-serif" font-size="7.6" font-weight="600" letter-spacing="1.6" fill="#121417"><textPath href="#{pid}" textLength="222" lengthAdjust="spacing">MENZIL-BAU · QUALITÄT · SEIT 2010 · GEPRÜFT ·</textPath></text>'
            f'<circle cx="50" cy="50" r="27" fill="url(#sealg{i})"/><circle cx="50" cy="50" r="23.5" fill="none" stroke="#fff" stroke-width=".7" opacity=".45"/>'
            f'<g transform="translate(36 36) scale(1.17)" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{icon}</g></svg>')

COUNTRIES = [('+43', '🇦🇹'), ('+49', '🇩🇪'), ('+41', '🇨🇭'), ('+421', '🇸🇰'), ('+420', '🇨🇿'), ('+36', '🇭🇺'), ('+386', '🇸🇮'),
             ('+385', '🇭🇷'), ('+381', '🇷🇸'), ('+387', '🇧🇦'), ('+382', '🇲🇪'), ('+383', '🇽🇰'), ('+389', '🇲🇰'), ('+355', '🇦🇱'),
             ('+359', '🇧🇬'), ('+40', '🇷🇴'), ('+48', '🇵🇱'), ('+90', '🇹🇷'), ('+39', '🇮🇹'), ('+33', '🇫🇷'), ('+31', '🇳🇱'),
             ('+32', '🇧🇪'), ('+352', '🇱🇺'), ('+45', '🇩🇰'), ('+46', '🇸🇪'), ('+47', '🇳🇴'), ('+44', '🇬🇧'), ('+353', '🇮🇪'),
             ('+34', '🇪🇸'), ('+351', '🇵🇹'), ('+30', '🇬🇷'), ('+380', '🇺🇦'), ('+1', '🇺🇸')]

# ═══════════════════════ helpers ═══════════════════════
def ctx(lang, page):
    sub = lang != 'de'
    return {'lang': lang, 'page': page, 't': T[lang], 'a': '../' if sub else '', }

def page_href(c, page):
    return f'{page}.html'

def lang_href(c, target, page):
    if c['lang'] == 'de':
        return f'{target}/{page}.html' if target != 'de' else f'{page}.html'
    if target == 'de':
        return f'../{page}.html'
    return f'../{target}/{page}.html' if target != c['lang'] else f'{page}.html'

def anchor(c, a):
    return f'#{a}' if c['page'] == 'index' else f'index.html#{a}'

def photo(c, pid, t=True):
    return f"{c['a']}assets/img/photos/{pid}{'-t' if t else ''}.jpg"

def plan(c, prid, n, t=True):
    return f"{c['a']}assets/img/plans/{prid}-{n}{'-t' if t else ''}.jpg"

_sizes = {}
def is_portrait(pid):
    if pid not in _sizes:
        p = os.path.join(ROOT, f'assets/img/photos/{pid}-t.jpg')
        if Image and os.path.exists(p):
            with Image.open(p) as im: _sizes[pid] = im.size
        else:
            _sizes[pid] = (4, 3)
    w, h = _sizes[pid]
    return h > w

# ═══════════════════════ shared chunks ═══════════════════════
def head(c):
    t = c['t']; title, desc = t['meta'][c['page']]
    return f'''<!DOCTYPE html>
<html lang="{t['html_lang']}" translate="no">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#121417">
<meta name="google" content="notranslate">
<meta http-equiv="content-language" content="{t['html_lang']}">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:locale" content="{t['og_locale']}">
<meta property="og:image" content="{c['a']}assets/img/photos/f13.jpg">
{''.join(f'<link rel="alternate" hreflang="{l}" href="{lang_href(c, l, c["page"])}">' for l in LANGS)}
<link rel="icon" href="{c['a']}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@300;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{c['a']}assets/css/style.css">
</head>
'''

def nav(c):
    t = c['t']; n = t['nav']; p = c['page']
    def cur(x): return ' aria-current="page"' if p == x else ''
    langs = ''.join(f'<a href="{lang_href(c, l, p)}" hreflang="{l}" lang="{l}"{" class=\"active\"" if l == c["lang"] else ""}>{LANG_NAMES[l]}</a>' for l in LANGS)
    return f'''<a class="skip-link" href="#main">{E(t['skip'])}</a>
<nav class="site-nav" aria-label="Hauptnavigation">
  <div class="nav-inner">
    <a class="nav-logo" href="index.html" aria-label="Menzil-Bau – Start">
      <span class="nlm">{logo_b(185, 68)}</span>
      <span class="nlb">{logo_a(w=200)}</span>
      <span class="nav-motto"><span class="nav-motto-bar"></span>{E(t['motto'])}</span>
    </a>
    <button class="nav-hamburger" id="navToggle" aria-label="{E(t['menu'])}" aria-expanded="false" aria-controls="navLinks"><span></span></button>
    <ul class="nav-links" id="navLinks">
      <li><a href="{anchor(c, 'leistungen')}">{E(n['leistungen'])}</a></li>
      <li><a href="{anchor(c, 'warum')}">{E(n['warum'])}</a></li>
      <li><a href="projekte.html"{cur('projekte')}>{E(n['projekte'])}</a></li>
      <li><a href="referenzen.html"{cur('referenzen')}>{E(n['referenzen'])}</a></li>
      <li><a href="zertifikate.html"{cur('zertifikate')}>{E(n['zertifikate'])}</a></li>
      <li><a href="kontakt.html"{cur('kontakt')}>{E(n['kontakt'])}</a></li>
      <li class="nav-lang">{langs}</li>
      <li><a href="{SITE['calendar']}" target="_blank" rel="noopener" class="nav-cta">{E(n['cta'])}</a></li>
    </ul>
  </div>
</nav>
'''

def form(c):
    f = c['t']['form']
    opts = ''.join(f'<option value="{k}"{" selected" if k == "+43" else ""}>{fl} {k}</option>' for k, fl in COUNTRIES)
    types = ''.join(f'<option>{E(x)}</option>' for x in f['types'])
    return f'''<div class="hero-form-wrap">
      <div class="hero-form-label">{E(f['title'])}</div>
      <form class="hero-form" novalidate data-endpoint="{SITE['form_endpoint']}" data-subject="{E(f['subject'])}" data-sending="{E(f['sending'])}" data-err="{E(f['err'])}" data-net-err="{E(f['net_err'])}">
        <div class="hf-row">
          <input class="hf-input" name="first_name" type="text" placeholder="{E(f['first'])}" aria-label="{E(f['first'])}" autocomplete="given-name" data-letters required>
          <input class="hf-input" name="last_name" type="text" placeholder="{E(f['last'])}" aria-label="{E(f['last'])}" autocomplete="family-name" data-letters required>
        </div>
        <div class="hf-phone-row">
          <select class="hf-country" name="country" aria-label="Ländervorwahl">{opts}</select>
          <input class="hf-phone-num" name="phone" type="tel" placeholder="{E(f['phone'])}" aria-label="{E(f['phone'])}" inputmode="numeric" autocomplete="tel-national" required>
        </div>
        <input class="hf-input" name="email" type="email" placeholder="{E(f['email'])}" aria-label="{E(f['email'])}" autocomplete="email" required>
        <span class="hf-error" role="alert">{E(f['email_err'])}</span>
        <div class="hf-row">
          <select class="hf-select" name="project_type" aria-label="{E(f['type'])}"><option value="" selected disabled>{E(f['type'])}</option>{types}</select>
          <input class="hf-input" name="location" type="text" placeholder="{E(f['location'])}" aria-label="{E(f['location'])}">
        </div>
        <textarea class="hf-input hf-textarea" name="message" placeholder="{E(f['message'])}" aria-label="{E(f['message'])}" rows="3"></textarea>
        <button class="hf-submit" type="submit">{SEND} {E(f['submit'])}</button>
        <p class="hf-privacy">{E(f['privacy'])}</p>
      </form>
      <div class="hf-success" role="status">
        {logo_b(260, 95)}
        <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2.5"><path d="M20 6L9 17l-5-5"/></svg>
        <p>{E(f['success'])}</p>
        <button class="hf-close" type="button">{E(f['again'])}</button>
      </div>
    </div>'''

def cta(c):
    t = c['t']['cta']
    return f'''<section class="cta-section" id="beratung">
  <div class="cta-inner">
    <div class="reveal">
      <h2 class="cta-title">{t['title']}</h2>
      <p class="cta-sub">{E(t['sub'])}</p>
    </div>
    <div class="cta-buttons reveal reveal-d1">
      <a href="{SITE['calendar']}" target="_blank" rel="noopener" class="btn btn-white">{CAL} {E(t['btn1'])}</a>
      <a href="{SITE['phone_href']}" class="btn btn-ghost"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{TEL[TEL.index('<path'):TEL.index('</svg>')]}</svg> {E(t['btn2'])} · {SITE['phone_local']}</a>
    </div>
  </div>
</section>
'''

def footer(c):
    t = c['t']['footer']; a1 = '<br>'.join(E(x) for x in SITE['addr1']); a2 = '<br>'.join(E(x) for x in SITE['addr2'])
    return f'''<footer>
  <div class="footer-brand-row">
    <div class="footer-brand">
      {logo_a(w=230)}
      <div class="footer-copy">&copy; {SITE['founded']}–{YEAR} Menzil-Bau · {E(t['rights'])}</div>
      <div class="footer-links"><a href="kontakt.html#impressum" data-modal="legalModal">{E(t['impressum'])}</a><a href="{SITE['facebook']}" target="_blank" rel="noopener">Facebook</a></div>
    </div>
    <div class="footer-machine-mobile" aria-hidden="true">{crane(130, 53)}</div>
  </div>
  <div class="footer-machine" aria-hidden="true">{crane(300, 122)}</div>
  <div class="footer-info">
    <div><b>{E(t['addr1'])}</b>{a1}<br><a href="{SITE['phone_href']}">{SITE['phone_local']}</a></div>
    <div><b>{E(t['addr2'])}</b>{a2}<br><a href="mailto:{SITE['email']}">{SITE['email']}</a></div>
  </div>
</footer>
<button id="scroll-top" aria-label="Nach oben">&#8593;</button>
{legal_modal(c)}
<div class="lb" id="lightbox" role="dialog" aria-modal="true" aria-label="Galerie">
  <span class="lb-count"></span>
  <button class="lb-btn lb-close" aria-label="{E(c['t']['lb']['close'])}">&#10005;</button>
  <button class="lb-btn lb-prev" aria-label="{E(c['t']['lb']['prev'])}">&#8592;</button>
  <img class="lb-img" alt="">
  <div class="lb-cap"></div>
  <button class="lb-btn lb-next" aria-label="{E(c['t']['lb']['next'])}">&#8594;</button>
</div>
<script src="{c['a']}assets/js/main.js" defer></script>
</body>
</html>
'''

def legal_modal(c):
    L = c['t']['legal']
    paras = ''.join(f'<p>{E(x)}</p>' for x in LOREM)
    return f'''<div class="modal" id="legalModal" role="dialog" aria-modal="true" aria-labelledby="legalTitle" hidden>
  <div class="modal-box">
    <button class="modal-close" type="button" aria-label="{E(c['t']['lb']['close'])}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    <div class="section-eyebrow">{E(L['eyebrow'])}</div>
    <h2 class="modal-title" id="legalTitle">{E(L['title'])}</h2>
    <dl class="modal-facts">
      <div><dt>{E(L['company'])}</dt><dd>{E(SITE['company'])}</dd></div>
      <div><dt>{E(L['address'])}</dt><dd>{E(SITE['addr2_plain'])}</dd></div>
      <div><dt>{E(L['contact'])}</dt><dd><a href="mailto:{SITE['email']}">{SITE['email']}</a> · {SITE['phone']}</dd></div>
    </dl>
    <div class="modal-body">{paras}</div>
  </div>
</div>'''

MAP_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2-6-2z"/><path d="M9 4v14M15 6v14"/></svg>'
PIN_S = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s7-7 7-12a7 7 0 0 0-14 0c0 5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>'

def places_block(c):
    t = c['t']; groups = {'noe': [], 'bgld': [], 'wien': []}
    for p in PLACES:
        groups[REGION_OF.get(p, 'noe')].append(p)
    cols = ''.join(f'''<div class="region"><div class="region-name">{E(t['regions'][k])}<span>{len(v)}</span></div>
          <ul>{''.join(f'<li>{PIN_S}<span>{E(x)}</span></li>' for x in v)}</ul></div>''' for k, v in groups.items() if v)
    sub = t['places_sub'].format(n=len(PLACES), r=sum(1 for v in groups.values() if v))
    return f'''<div class="places-card reveal">
      <div class="places-head"><span class="places-icon">{MAP_ICON}</span>
        <div><div class="places-eyebrow">{E(t['featured']['places_title'])}</div><div class="places-title">{E(sub)}</div></div></div>
      <div class="places-regions">{cols}</div>
    </div>'''

def page_hero(c, pk, img):
    t = c['t'][pk]
    return f'''<section class="page-hero">
  <div class="hero-photo" style="background-image:url('{photo(c, img, False)}')"></div>
  <div class="hero-grid"></div>
  <div class="page-hero-inner">
    <div class="crumbs"><a href="index.html">Menzil-Bau</a> &nbsp;/&nbsp; {E(t['eyebrow'])}</div>
    <h1 class="page-title">{t['title']}</h1>
    <p class="page-sub">{E(t['sub'])}</p>
  </div>
  <div class="conveyor"></div>
</section>
'''

def proj_card_plan(c, pr, group='plans'):
    t = c['t']['p_projekte']; title = pr['title'][c['lang']]
    srcs = '|'.join(plan(c, pr['id'], i + 1, False) for i in range(len(pr['files'])))
    cnt = f'<span class="proj-count">{len(pr["files"])} {E(t["plans"])}</span>' if len(pr['files']) > 1 else ''
    cap = f'<b>{E(title)}</b>{E(pr["loc"])}'
    return f'''<button class="proj-card reveal" type="button" data-cat="{pr['cat']}" data-lb="{srcs}" data-lb-group="{group}" data-lb-cap="{E(cap)}" data-lb-alt="{E(title)} – {E(pr['loc'])}">
        <div class="proj-img plan"><img src="{plan(c, pr['id'], 1)}" alt="{E(t['plan'])}: {E(title)}, {E(pr['loc'])}" loading="lazy" width="800" height="560"></div>{cnt}
        <div class="proj-body"><div class="proj-tag">{E(t['filters'][pr['cat']])} · {E(t['plan'])}</div><div class="proj-name">{E(title)}</div><div class="proj-loc">{E(pr['loc'])}</div></div>
      </button>'''

def reviews_grid(c):
    out = []
    for i, (tag, q, name, loc) in enumerate(c['t']['reviews']['items']):
        ini = ''.join(w[0] for w in name.replace('&', ' ').split()[:2]).upper()
        out.append(f'''<figure class="review reveal reveal-d{i}">
        <div class="review-stars" aria-label="5/5">★★★★★</div>
        <div class="review-tag">{E(tag)}</div>
        <blockquote>{E(q)}</blockquote>
        <figcaption class="review-who"><span class="review-avatar">{E(ini)}</span><span><span class="review-name">{E(name)}</span><br><span class="review-loc">{E(loc)}</span></span></figcaption>
      </figure>''')
    return '<div class="review-grid">' + ''.join(out) + '</div>'

# ═══════════════════════ pages ═══════════════════════
def p_index(c):
    t = c['t']; h = t['hero']
    stats = ''.join(f'<div class="stat-item"><div class="stat-number">{n}<span>{u}</span></div><div class="stat-label">{E(l)}</div></div>' for n, u, l in h['stats'])
    prob = ''.join(f'<li>{ICON[PROB_ICONS[i]]}{E(x)}</li>' for i, x in enumerate(t['challenge']['items']))
    sol = ''.join(f'<li>{ICON["check"]}{E(x)}</li>' for x in t['solution']['items'])
    hl = t['metrics'].get('highlight')
    metrics = ''.join(f'<div class="metric-card{" gold" if i == hl else ""}"><div class="metric-num">{n}<span class="unit">{u}</span></div><div class="metric-desc">{E(d)}</div></div>' for i, (n, u, d) in enumerate(t['metrics']['items']))
    svcs = ''.join(f'''<div class="product-card reveal reveal-d{i % 3}">
        <span class="product-num">0{i + 1}</span>
        <div class="product-icon">{SVC_ICONS[i]}</div>
        <h3 class="product-name">{E(nm)}</h3>
        <p class="product-desc">{E(ds)}</p>
        <div class="product-tags">{''.join(f'<span class="tag">{E(x)}</span>' for x in tags)}</div>
      </div>''' for i, (nm, ds, tags) in enumerate(t['services']['items']))
    why = ''.join(f'<div class="diff-card reveal reveal-d{i % 2}"><div class="diff-num">0{i + 1}</div><h3 class="diff-title">{E(a)}</h3><p class="diff-body">{b}</p></div>' for i, (a, b) in enumerate(t['why']['items']))
    fe = t['featured']
    cards = ''.join(f'''<button class="proj-card reveal reveal-d{i % 3}" type="button" data-lb="{photo(c, pid, False)}" data-lb-group="featured" data-lb-cap="{E(f'<b>{E(nm)}</b>{E(tag)}')}" data-lb-alt="{E(nm)}">
        <div class="proj-img"><img src="{photo(c, pid)}" alt="{E(nm)} – Menzil-Bau" loading="lazy" width="720" height="540"></div>
        <div class="proj-body"><div class="proj-tag">{E(tag)}</div><div class="proj-name">{E(nm)}</div></div>
      </button>''' for i, (pid, tag, nm) in enumerate(fe['cards']))
    return head(c) + '<body class="has-parade">\n' + nav(c) + f'''<main id="main">
<section class="hero" id="hero">
  {build_scene(c)}
  <div class="conveyor"></div>
  <div class="hero-left">
    <div class="hero-photo" style="background-image:url('{photo(c, 'f01', False)}')"></div>
    <div class="hero-grid"></div>
    <div class="hero-logo-mark">{logo_b(380, 140)}</div>
    <div class="hero-eyebrow">{E(h['eyebrow'])}</div>
    <h1 class="hero-title">{E(h['title1'])}<span class="accent">{E(h['title2'])}</span></h1>
    <p class="hero-sub">{E(h['sub'])}</p>
    <div class="hero-stats">{stats}</div>
  </div>
  <div class="hero-right" id="anfrage">
    {form(c)}
  </div>
</section>

<section class="problem-solution" id="herausforderung">
  <div class="ps-grid">
    <div class="ps-panel problem reveal">
      <div class="ps-label">{E(t['challenge']['label'])}</div>
      <h2 class="ps-title">{E(t['challenge']['title'])}</h2>
      <ul class="ps-list">{prob}</ul>
    </div>
    <div class="ps-panel solution reveal reveal-d1">
      <div class="ps-label">{E(t['solution']['label'])}</div>
      <h2 class="ps-title">{E(t['solution']['title'])}</h2>
      <ul class="ps-list">{sol}</ul>
    </div>
  </div>
</section>

<section class="section concrete" id="zahlen">
  <div class="section-inner">
    <div class="section-eyebrow">{E(t['metrics']['eyebrow'])}</div>
    <h2 class="section-title">{t['metrics']['title']}</h2>
    <div class="metrics-grid">{metrics}</div>
  </div>
</section>

<section class="section" id="leistungen">
  <div class="section-inner">
    <div class="section-eyebrow">{E(t['services']['eyebrow'])}</div>
    <h2 class="section-title">{t['services']['title']}</h2>
    <div class="products-grid">{svcs}</div>
  </div>
</section>

<section class="section dark" id="warum">
  <div class="section-inner">
    <div class="section-eyebrow">{E(t['why']['eyebrow'])}</div>
    <h2 class="section-title">{t['why']['title']}</h2>
    <div class="diff-grid">{why}</div>
  </div>
</section>

<section class="section concrete" id="projekte">
  <div class="section-inner">
    <div class="section-head">
      <div><div class="section-eyebrow">{E(fe['eyebrow'])}</div><h2 class="section-title">{fe['title']}</h2></div>
      <p class="section-intro">{E(fe['intro'])}</p>
    </div>
    <div class="proj-grid">{cards}</div>
    {places_block(c)}
    <div class="btn-row"><a href="projekte.html" class="btn btn-dark">{E(fe['more'])} {ARROW}</a></div>
  </div>
</section>

<section class="section" id="kundenstimmen">
  <div class="section-inner">
    <div class="section-eyebrow">{E(t['reviews']['eyebrow'])}</div>
    <h2 class="section-title">{t['reviews']['title']}</h2>
    {reviews_grid(c)}
    <div class="btn-row"><a href="referenzen.html" class="btn btn-outline">{E(t['reviews']['more'])} {ARROW}</a></div>
  </div>
</section>
</main>
''' + cta(c) + footer(c)

def p_projekte(c):
    t = c['t']['p_projekte']
    counts = {k: sum(1 for p in PROJECTS if p['cat'] == k) for k in t['filters'] if k != 'all'}
    counts['all'] = len(PROJECTS)
    fbar = ''.join(f'<button class="filter{" active" if k == "all" else ""}" type="button" data-cat="{k}" aria-pressed="{"true" if k == "all" else "false"}">{E(v)}<span class="n">{counts[k]}</span></button>' for k, v in t['filters'].items())
    cards = ''.join(proj_card_plan(c, p) for p in PROJECTS)
    gcounts = {k: sum(1 for p in PHOTOS if p['cat'] == k) for k in t['gfilters'] if k != 'all'}; gcounts['all'] = len(PHOTOS)
    gbar = ''.join(f'<button class="filter{" active" if k == "all" else ""}" type="button" data-cat="{k}" aria-pressed="{"true" if k == "all" else "false"}">{E(v)}<span class="n">{gcounts[k]}</span></button>' for k, v in t['gfilters'].items())
    gal = []; land = 0
    for p in PHOTOS:
        cls = 'tall' if is_portrait(p['id']) else ''
        if not cls:
            land += 1
            if land % 5 == 1: cls = 'wide'
        lab = t['gfilters'][p['cat']]
        gal.append(f'<button class="g-item {cls}" type="button" data-cat="{p["cat"]}" data-lb="{photo(c, p["id"], False)}" data-lb-group="gallery" data-lb-cap="{E(f"<b>Menzil-Bau</b>{E(lab)}")}" data-lb-alt="{E(lab)}"><img src="{photo(c, p["id"])}" alt="{E(lab)} – Menzil-Bau" loading="lazy"></button>')
    tb = c['t']['tabs']
    CAM = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M4 7h3l2-3h6l2 3h3v13H4z"/><circle cx="12" cy="13" r="4"/></svg>'
    PLN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M3 3h18v18H3z"/><path d="M3 12h8V3M11 12v9M15 12h6M15 12v4"/></svg>'
    return head(c) + '<body>\n' + nav(c) + '<main id="main">\n' + page_hero(c, 'p_projekte', 'f15') + f'''
<section class="section tabs-section" id="projekte-tabs">
  <div class="section-inner">
    <div class="tabs" role="tablist" aria-label="{E(t['eyebrow'])}">
      <button class="tab active" role="tab" id="tab-impressionen" aria-controls="impressionen" aria-selected="true" type="button">{CAM}<span>{E(tb['photos'])}</span><span class="n">{len(PHOTOS)}</span></button>
      <button class="tab" role="tab" id="tab-plaene" aria-controls="plaene" aria-selected="false" tabindex="-1" type="button">{PLN}<span>{E(tb['plans'])}</span><span class="n">{len(PROJECTS)}</span></button>
    </div>
    <div class="tab-panel" role="tabpanel" id="impressionen" aria-labelledby="tab-impressionen">
      <div class="section-eyebrow">{E(t['gallery_eyebrow'])}</div>
      <h2 class="section-title">{t['gallery_title']}</h2>
      <div class="filters" data-filter-group="gallery" role="group">{gbar}</div>
      <div class="gallery" id="gallery">{''.join(gal)}</div>
    </div>
    <div class="tab-panel" role="tabpanel" id="plaene" aria-labelledby="tab-plaene" hidden>
      <div class="section-eyebrow">{E(tb['plans_eyebrow'])}</div>
      <h2 class="section-title">{tb['plans_title']}</h2>
      <div class="filters" data-filter-group="projGrid" role="group">{fbar}</div>
      <div class="proj-grid" id="projGrid">{cards}</div>
    </div>
  </div>
</section>
</main>
''' + cta(c) + footer(c)

def p_referenzen(c):
    t = c['t']['p_referenzen']
    stats = ''.join(f'<div class="metric-card"><div class="metric-num">{n}<span class="unit">{u}</span></div><div class="metric-desc">{E(d)}</div></div>' for n, u, d in t['stats'])
    items = []
    for p in PLACES:
        parts = p.split(' ', 1)
        plz, town = (parts[0], parts[1]) if parts[0].isdigit() else ('', p)
        items.append(f'<div class="ref-item">{PIN}<div><div class="ref-plz">{E(plz) or "&nbsp;"}</div><div class="ref-town">{E(town)}</div></div></div>')
    return head(c) + '<body>\n' + nav(c) + '<main id="main">\n' + page_hero(c, 'p_referenzen', 'f13') + f'''
<section class="section concrete">
  <div class="section-inner">
    <div class="section-eyebrow">{E(c['t']['reviews']['eyebrow'])}</div>
    <h2 class="section-title">{c['t']['reviews']['title']}</h2>
    {reviews_grid(c)}
  </div>
</section>
<section class="section">
  <div class="section-inner">
    <div class="section-head">
      <div><div class="section-eyebrow">{E(t['list_eyebrow'])}</div><h2 class="section-title">{t['list_title']}</h2></div>
      <p class="section-intro">{E(t['list_intro'])}</p>
    </div>
    <div class="ref-stats">{stats}</div>
    <div class="ref-list">{''.join(items)}</div>
    <div class="btn-row"><a href="projekte.html" class="btn btn-dark">{E(c['t']['featured']['more'])} {ARROW}</a></div>
  </div>
</section>
</main>
''' + cta(c) + footer(c)

def p_zertifikate(c):
    t = c['t']['p_zertifikate']
    # PLATZHALTER: generic placeholder seals – replace with real credentials
    CHK = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 8.5l3 3 7-7"/></svg>'
    badges = ''.join(f'''<div class="cert reveal reveal-d{i % 3}">
        <span class="cert-no">0{i + 1}</span>
        {seal(a, i)}
        <div class="cert-body"><div class="cert-name">{E(a)}</div><div class="cert-desc">{E(d)}</div>
          <span class="cert-chip">{CHK}{E(b)}</span></div>
      </div>''' for i, (a, b, d) in enumerate(t['badges']))
    steps = ''.join(f'<div class="step reveal reveal-d{i % 3}"><div class="step-title">{E(a)}</div><div class="step-body">{E(b)}</div></div>' for i, (a, b) in enumerate(t['steps']))
    return head(c) + '<body>\n' + nav(c) + '<main id="main">\n' + page_hero(c, 'p_zertifikate', 'f14') + f'''
<section class="section concrete">
  <div class="section-inner">
    <!-- PLATZHALTER: Nachweise werden nach Erhalt der Originaldokumente ersetzt -->
    <div class="cert-grid">{badges}</div>
    <p class="cert-note">{E(t['note'])}</p>
  </div>
</section>
<section class="section dark">
  <div class="section-inner">
    <div class="section-eyebrow">{E(t['process_eyebrow'])}</div>
    <h2 class="section-title">{t['process_title']}</h2>
    <div class="steps">{steps}</div>
  </div>
</section>
</main>
''' + cta(c) + footer(c)

def p_kontakt(c):
    t = c['t']['p_kontakt']; ft = c['t']['footer']
    a1 = '<br>'.join(E(x) for x in SITE['addr1']); a2 = '<br>'.join(E(x) for x in SITE['addr2'])
    maps = 'https://www.google.com/maps/search/?api=1&query=' + '+'.join(SITE['addr2_plain'].replace(',', '').split())
    return head(c) + '<body>\n' + nav(c) + '<main id="main">\n' + page_hero(c, 'p_kontakt', 'f02') + f'''
<section class="contact-grid" id="formular">
  <div class="contact-info">
    <a class="ci" href="{SITE['phone_href']}"><span class="ci-icon">{TEL}</span><span><div class="ci-label">{E(t['phone'])}</div><div class="ci-value">{SITE['phone_local']}<small>{SITE['phone']}</small></div></span></a>
    <a class="ci" href="{SITE['whatsapp']}" target="_blank" rel="noopener"><span class="ci-icon">{WA}</span><span><div class="ci-label">{E(t['whatsapp'])}</div><div class="ci-value">{E(t['whatsapp_cta'])}<small>{SITE['phone']}</small></div></span></a>
    <a class="ci" href="mailto:{SITE['email']}"><span class="ci-icon">{MAIL}</span><span><div class="ci-label">{E(t['email'])}</div><div class="ci-value">{SITE['email']}</div></span></a>
    <div class="ci"><span class="ci-icon">{CLOCK}</span><span><div class="ci-label">{E(t['hours'])}</div><div class="ci-value">{SITE['hours']}</div></span></div>
    <div class="addr-grid">
      <div class="addr"><div class="addr-label">{E(ft['addr1'])}</div>{a1}</div>
      <div class="addr"><div class="addr-label">{E(ft['addr2'])}</div>{a2}<br><a href="{maps}" target="_blank" rel="noopener">{E(t['route'])} →</a></div>
    </div>
    <a href="{SITE['calendar']}" target="_blank" rel="noopener" class="btn btn-red">{CAL} {E(t['book'])}</a>
  </div>
  <div class="contact-form-side">
    {form(c)}
  </div>
</section>
<section class="section concrete" id="impressum">
  <div class="section-inner">
    <div class="section-eyebrow">{E(t['impressum_title'])}</div>
    <p class="impressum">{E(t['impressum'])}<br>{E(SITE['company'])} · {E(SITE['addr2_plain'])} · <a href="mailto:{SITE['email']}">{SITE['email']}</a> · {SITE['phone']}</p>
  </div>
</section>
</main>
''' + footer(c)

RENDER = {'index': p_index, 'projekte': p_projekte, 'referenzen': p_referenzen, 'zertifikate': p_zertifikate, 'kontakt': p_kontakt}

def favicon():
    os.makedirs(os.path.join(ROOT, 'assets/img'), exist_ok=True)
    with open(os.path.join(ROOT, 'assets/img/favicon.svg'), 'w', encoding='utf-8') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72"><rect width="72" height="72" fill="{R}"/>'
                '<path d="M14 56V26L25 15L36 26L47 15L58 26V56" fill="none" stroke="#fff" stroke-width="6.5"/><rect x="32" y="38" width="8" height="18" fill="#fff"/></svg>')

def main():
    favicon()
    n = 0
    for lang in LANGS:
        out_dir = ROOT if lang == 'de' else os.path.join(ROOT, lang)
        os.makedirs(out_dir, exist_ok=True)
        for page in PAGES:
            c = ctx(lang, page)
            with open(os.path.join(out_dir, f'{page}.html'), 'w', encoding='utf-8') as f:
                f.write(RENDER[page](c))
            n += 1
    print(f'built {n} pages')

if __name__ == '__main__':
    main()
