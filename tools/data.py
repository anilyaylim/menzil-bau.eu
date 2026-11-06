# -*- coding: utf-8 -*-
"""Single source of truth for site content (DE default, EN, TR).

Edit texts / numbers / addresses here, then run:  python3 tools/build.py
Items marked  # PLATZHALTER  are placeholders to be replaced with real data.
"""

SITE = {
    'domain': 'https://www.menzil-bau.eu',
    # public address of the site (used for absolute og:image URLs) – change to https://www.menzil-bau.eu/ after the domain switch
    'public_base': 'https://anilyaylim.github.io/menzil-bau.eu/',
    'phone': '+43 664 64 76 640',
    'phone_local': '0664 / 64 76 640',
    'phone_href': 'tel:+436646476640',
    'whatsapp': 'https://wa.me/436646476640',
    'email': 'office@menzil-bau.eu',
    'facebook': 'https://www.facebook.com/MenzilBau/',
    'calendar': 'https://calendar.app.google/hD41pCdMktn8eXWa8',
    # Same endpoint as the DKI landing page; change to office@menzil-bau.eu once activated on formsubmit.co
    'form_endpoint': 'https://formsubmit.co/ajax/anil@no7software.co.uk',
    'company': 'MENZIL S.R.O.',
    # Adresse 1 = Österreich (wie auf der bisherigen Website nur "AUSTRIA"), Adresse 2 = Firmensitz
    'addr1': ['Menzil-Bau', 'Niederösterreich · Österreich'],  # PLATZHALTER (genaue Adresse folgt)
    'addr2': ['MENZIL S.R.O. · Gorkeho 3', '81102 Bratislava · Slowakei'],
    'addr2_plain': 'Gorkeho 3, 81102 Bratislava',  # für Impressum / Google Maps
    'hours': 'Mo – Fr · 07:30 – 17:00',
    'founded': 2010,
}

# ── Photos (Dropbox "Mehr Bilder", 2019). src = number in "2019_Referenzen (n).jpeg"
#    cat: fassade | rohbau | innen      (project assignment follows later)
_P = [
    (13, 'fassade'), (1, 'fassade'), (15, 'fassade'), (10, 'fassade'), (8, 'fassade'), (2, 'fassade'),
    (18, 'fassade'), (4, 'fassade'), (6, 'fassade'), (65, 'fassade'), (21, 'fassade'),
    (17, 'fassade'), (11, 'fassade'), (56, 'fassade'),
    (14, 'rohbau'), (16, 'rohbau'), (24, 'rohbau'), (5, 'rohbau'), (3, 'rohbau'), (20, 'rohbau'), (23, 'rohbau'),
    (64, 'innen'), (52, 'innen'), (61, 'innen'), (60, 'innen'), (63, 'innen'), (41, 'innen'), (42, 'innen'),
    (48, 'innen'), (49, 'innen'), (62, 'innen'), (29, 'innen'), (34, 'innen'), (32, 'innen'), (35, 'innen'),
    (51, 'innen'), (37, 'innen'), (46, 'innen'), (44, 'innen'),
]
PHOTOS = [{'id': 'f%02d' % n, 'src': n, 'cat': c} for n, c in _P]

# ── Projects (Dropbox "Weitere abgeschlossene Projekte" – Einreichpläne)
#    cat: neubau | zubau | sanierung | wohnbau
def _t(de, en, tr):
    return {'de': de, 'en': en, 'tr': tr}

EFH = _t('Einfamilienhaus', 'Single-family house', 'Müstakil konut')
DH = _t('Doppelhaus', 'Semi-detached house', 'İkiz konut')
PROJECTS = [
    {'id': 'mattersburg', 'files': ['7210_Mattersburg_Doppelhaus.png'], 'cat': 'neubau', 'loc': '7210 Mattersburg', 'title': DH},
    {'id': 'traiskirchen', 'files': ['2514_Traiskirchen_Wohnungen.png'], 'cat': 'wohnbau', 'loc': '2514 Traiskirchen', 'title': _t('Wohnhausanlage', 'Residential complex', 'Konut projesi')},
    {'id': 'reihenhaus-102', 'files': ['102_Ansicht.png', '102_Erdgeschoss.png', '102_Obergeschoss.png'], 'cat': 'wohnbau', 'loc': 'Niederösterreich', 'title': _t('Reihenhausanlage', 'Terraced housing', 'Sıra evler')},
    {'id': 'ternitz-zubau', 'files': ['2630_Ternitz_Zubau.png'], 'cat': 'zubau', 'loc': '2630 Ternitz', 'title': _t('Zubau Wohnhaus', 'House extension', 'Konut ek binası')},
    {'id': 'ternitz-sanierung', 'files': ['2630_Ternitz_Sanierung.png'], 'cat': 'sanierung', 'loc': '2630 Ternitz', 'title': _t('Sanierung Wohnhaus', 'House renovation', 'Konut renovasyonu')},
    {'id': 'goetzendorf', 'files': ['2434_G#U00f6tzendorf_Neubau.png', '2434_G#U00f6tzendorf_Neubau_2.png'], 'cat': 'neubau', 'loc': '2434 Götzendorf', 'title': _t('Neubau Wohnhaus', 'New residential build', 'Yeni konut')},
    {'id': 'sollenau-dh', 'files': ['2601_Sollenau_Doppelhaus.png'], 'cat': 'neubau', 'loc': '2601 Sollenau', 'title': DH},
    {'id': 'sollenau-efh', 'files': ['EFH_Sollenau.png'], 'cat': 'neubau', 'loc': '2601 Sollenau', 'title': EFH},
    {'id': 'eggendorf-dh', 'files': ['2492_Eggendorf_Doppelhaus.png'], 'cat': 'neubau', 'loc': '2492 Eggendorf', 'title': DH},
    {'id': 'eggendorf-efh', 'files': ['2492_Eggendorf_Einfamilienhaus.png'], 'cat': 'neubau', 'loc': '2492 Eggendorf', 'title': EFH},
    {'id': 'eggendorf-dh-2', 'files': ['2493_Eggendorf_Doppelhaus.png'], 'cat': 'neubau', 'loc': 'Eggendorf', 'title': DH},
    {'id': 'lichtenwoerth', 'files': ['2493_LICHTENW#U00d6RTH_Einfamilienhaus.png'], 'cat': 'neubau', 'loc': '2493 Lichtenwörth', 'title': EFH},
    {'id': 'pernitz', 'files': ['2763_Pernitz_Einfamilienhaus.png'], 'cat': 'neubau', 'loc': '2763 Pernitz', 'title': EFH},
    {'id': 'tribuswinkel', 'files': ['4034_Tribuswinkel_Einfamielienhaus.png'], 'cat': 'neubau', 'loc': 'Tribuswinkel', 'title': EFH},
    {'id': 'deutsch-wagram', 'files': ['2232_DeutschWagram_EinfamilienhausZubau.png'], 'cat': 'zubau', 'loc': '2232 Deutsch-Wagram', 'title': _t('Zubau Einfamilienhaus', 'Single-family house extension', 'Müstakil konut ek binası')},
    {'id': 'neudoerfl', 'files': ['7201_Neud#U00f6rfl.png'], 'cat': 'neubau', 'loc': '7201 Neudörfl', 'title': _t('Wohnhaus', 'Residential house', 'Konut')},
    {'id': 'wienersdorf', 'files': ['EFH_Wienersdorf.png'], 'cat': 'neubau', 'loc': 'Wienersdorf', 'title': EFH},
    {'id': 'wiener-neustadt', 'files': ['Haus_WienerNeustadt.png'], 'cat': 'neubau', 'loc': '2700 Wiener Neustadt', 'title': _t('Wohnhaus', 'Residential house', 'Konut')},
    {'id': 'wiener-neustadt-ep', 'files': ['ERPL_WienerNeustadt.png'], 'cat': 'wohnbau', 'loc': '2700 Wiener Neustadt', 'title': _t('Wohnbau · Einreichplanung', 'Residential · permit planning', 'Konut · ruhsat projesi')},
    {'id': 'wien', 'files': ['EP_Wien.png'], 'cat': 'wohnbau', 'loc': 'Wien', 'title': _t('Wohnbau · Einreichplanung', 'Residential · permit planning', 'Konut · ruhsat projesi')},
    {'id': 'efh-pool', 'files': ['EFH_xxx.jpeg'], 'cat': 'neubau', 'loc': 'Niederösterreich', 'title': _t('Einfamilienhaus mit Pool', 'House with pool', 'Havuzlu müstakil konut')},
    {'id': 'efh-grundriss', 'files': ['xxxx_EGuOG.png'], 'cat': 'neubau', 'loc': 'Niederösterreich', 'title': EFH},
]

LANGS = ['de', 'en', 'tr']
LANG_NAMES = {'de': 'DE', 'en': 'EN', 'tr': 'TR'}
PAGES = ['index', 'projekte', 'referenzen', 'zertifikate', 'kontakt']

T = {}

# ══════════════════════════════ DEUTSCH ══════════════════════════════
T['de'] = {
    'html_lang': 'de', 'og_locale': 'de_AT',
    'motto': 'Ihr Partner im und rund um den Baubereich',
    'skip': 'Zum Inhalt springen',
    'menu': 'Menü',
    'meta': {
        'index': ('Menzil-Bau | Baumeisterbetrieb für Planung, Rohbau & Sanierung', 'Menzil-Bau – Planung, Rohbau, Fassade, Umbau, Sanierung und Abbruch aus einer Hand. Seit 2010 auf Baustellen in Niederösterreich, Burgenland und Wien.'),
        'projekte': ('Projekte | Menzil-Bau', 'Abgeschlossene Projekte und Einreichplanungen von Menzil-Bau: Einfamilienhäuser, Doppelhäuser, Wohnbau, Zubau und Sanierung.'),
        'referenzen': ('Referenzen | Menzil-Bau', 'Was unsere Kunden sagen – Kundenstimmen und Referenzliste von Menzil-Bau.'),
        'zertifikate': ('Zertifikate & Qualität | Menzil-Bau', 'Berechtigungen, Versicherungen und Qualitätsstandards von Menzil-Bau.'),
        'kontakt': ('Kontakt | Menzil-Bau', 'Kontaktieren Sie Menzil-Bau: Telefon, WhatsApp, E-Mail oder Beratungstermin buchen.'),
    },
    'nav': {'leistungen': 'Leistungen', 'warum': 'Warum Menzil', 'projekte': 'Projekte', 'referenzen': 'Referenzen', 'zertifikate': 'Zertifikate', 'kontakt': 'Kontakt', 'cta': 'Beratung buchen'},
    'hero': {
        'eyebrow': 'Baumeisterbetrieb · Niederösterreich & Wien',
        'title1': 'Bauen mit Verlass.', 'title2': 'Termingerecht.',
        'sub': 'Planung, Rohbau, Fassade, Umbau, Sanierung und Abbruch aus einer Hand. Ein Ansprechpartner, ein verbindlicher Zeitplan, ein transparentes Angebot.',
        'stats': [('30', '+', 'Jahre Erfahrung'), ('120', '+', 'Projekte'), ('6', '', 'Leistungsbereiche'), ('100', '%', 'aus einer Hand')],  # PLATZHALTER Zahlen
    },
    'form': {
        'title': 'Kostenlose Erstberatung anfragen',
        'first': 'Vorname', 'last': 'Nachname', 'phone': 'Mobiltelefon', 'email': 'E-Mail-Adresse',
        'type': 'Art des Bauvorhabens',
        'types': ['Neubau', 'Zubau / Umbau', 'Sanierung', 'Fassade', 'Abbruch', 'Planung / Einreichung', 'Sonstiges'],
        'location': 'Ort des Bauvorhabens (PLZ / Ort)',
        'message': 'Ihre Nachricht (Umfang, Zeitrahmen, WhatsApp …)',
        'submit': 'Anfrage senden', 'sending': 'Wird gesendet …',
        'success': 'Vielen Dank! Wir melden uns innerhalb von 24 Stunden bei Ihnen.',
        'again': 'Weitere Anfrage senden',
        'err': 'Etwas ist schiefgelaufen. Bitte versuchen Sie es erneut.',
        'net_err': 'Netzwerkfehler. Bitte versuchen Sie es erneut.',
        'email_err': 'Bitte geben Sie eine gültige E-Mail-Adresse mit @ ein.',
        'privacy': 'Ihre Daten werden ausschließlich zur Bearbeitung Ihrer Anfrage verwendet.',
        'subject': 'Neue Anfrage – Menzil-Bau Website',
    },
    'challenge': {
        'label': 'Die Herausforderung',
        'title': 'Bauprojekte scheitern selten am Können – sondern an der Organisation',
        'items': [
            'Die Bauzeit verzögert sich, Einzugs- und Finanzierungstermine geraten ins Wanken',
            'Nachträge und unklare Positionen sprengen das ursprüngliche Budget',
            'Zu viele Gewerke, aber niemand, der sie koordiniert',
            'Planung und Ausführung kommen von verschiedenen Firmen und passen nicht zusammen',
            'Ansprechpartner sind schwer erreichbar, wenn auf der Baustelle Entscheidungen fallen müssen',
        ],
    },
    'solution': {
        'label': 'Der Menzil-Weg',
        'title': 'Ein Team. Ein Zeitplan. Ein Ansprechpartner.',
        'items': [
            'Verbindlicher Bauzeitplan mit klaren Etappen – von der Einreichung bis zur Übergabe',
            'Transparentes Angebot mit nachvollziehbaren Positionen, ohne versteckte Kosten',
            'Wir koordinieren alle Gewerke – Sie müssen sich um nichts kümmern',
            'Planung und Ausführung aus einem Haus: Was gezeichnet wird, wird auch gebaut',
            'Persönlicher Ansprechpartner, Mo – Fr von 07:30 bis 17:00 erreichbar',
        ],
    },
    'metrics': {
        'highlight': 2,  # Index der hervorgehobenen Zahl (gold)
        'eyebrow': 'Menzil in Zahlen', 'title': 'Erfahrung, die man<br>auf der Baustelle sieht',
        'items': [('15', '+', 'Jahre als eigenständiges Bauunternehmen – Menzil-Bau wurde 2010 gegründet, die Bauerfahrung des Gründers reicht bis 1996 zurück'),
                  ('15', '+', 'Gemeinden in Niederösterreich, im Burgenland und in Wien, in denen wir bereits gebaut, geplant oder saniert haben'),
                  ('1', '', 'Ansprechpartner für Ihr gesamtes Projekt – von der ersten Skizze über den Rohbau bis zur schlüsselfertigen Übergabe')],
    },
    'services': {
        'eyebrow': 'Leistungen', 'title': 'Alles rund um<br>Ihr Bauvorhaben',
        'items': [
            ('Planung', 'Wir entwickeln Ihr Bauvorhaben gedanklich und gestalterisch und halten es in Architektur- und Einreichplänen fest – die Basis für Genehmigung, Angebot und Ausführung.', ['Einreichplanung', 'Entwurf', 'Baubewilligung']),
            ('Rohbau', 'Wir errichten die äußere Kontur Ihres Gebäudes einschließlich Dachkonstruktion. Fenstereinbau, Fassade und Innenausbau übernehmen wir auf Wunsch ebenfalls.', ['Massivbau', 'Mauerwerk', 'Dachkonstruktion']),
            ('Fassade', 'Die Fassade ist der repräsentative Teil Ihres Gebäudes. Wir gestalten sie nach Ihren Wünschen – optisch ansprechend und technisch sauber ausgeführt.', ['Vollwärmeschutz', 'Putz', 'Gestaltung']),
            ('Umbau & Zubau', 'Veränderungen ganz nach Ihren Wünschen – innen wie außen. Vom Zubau bis zur neuen Raumaufteilung, sauber geplant und ohne unnötigen Flurschaden.', ['Zubau', 'Innenausbau', 'Raumaufteilung']),
            ('Sanierung', 'Baulich-technische Wiederherstellung und Modernisierung Ihres Objekts – um Schäden zu beseitigen und den Wohnstandard nachhaltig zu erhöhen.', ['Altbau', 'Bad & Küche', 'Modernisierung']),
            ('Abbruch', 'Wenn ein Gebäude weichen muss oder ein Umbau es erfordert, übernehmen wir den fachgerechten Abbruch bzw. Abriss inklusive Entsorgung.', ['Abriss', 'Rückbau', 'Entsorgung']),
        ],
    },
    'why': {
        'eyebrow': 'Warum Menzil', 'title': 'Vom Maurer zum<br>Baumeisterbetrieb',
        'items': [
            ('Alles aus einer Hand', 'Planung, Rohbau, Fassade, Umbau, Sanierung und Abbruch – <strong>sechs Leistungsbereiche, ein Vertragspartner</strong>. Sie haben einen Ansprechpartner statt fünf Firmen.'),
            ('Erfahrung seit 1996', 'Der Gründer hat seine Fachausbildung als Maurer abgeschlossen und in Tirol die <strong>Polierschule absolviert</strong>. Diese Praxis von der Baustelle steckt in jedem Projekt.'),
            ('Planung im eigenen Haus', 'Einreichpläne, Grundrisse und Ansichten entstehen bei uns. <strong>Was geplant wird, wird auch so gebaut</strong> – ohne Reibungsverluste zwischen Planer und Baufirma.'),
            ('Qualität zu fairen Preisen', 'Klare Angebote, saubere Ausführung, kein Flurschaden. Unsere Kunden empfehlen uns weiter – <strong>wegen der Beratung, der Qualität und des Preises</strong>.'),
        ],
    },
    'featured': {
        'eyebrow': 'Projekte', 'title': 'Gebaut in<br>Niederösterreich & Wien',
        'intro': 'Vom Einfamilienhaus über Doppel- und Reihenhäuser bis zur Wohnhausanlage – ein Auszug aus unseren Baustellen.',
        'cards': [('f13', 'Wohnbau', 'Mehrfamilienhaus'), ('f14', 'Rohbau', 'Massivbau'), ('f15', 'Neubau', 'Reihenhausanlage'),
                  ('f01', 'Neubau', 'Wohnhaus mit Terrasse'), ('f64', 'Sanierung', 'Badezimmer'), ('f52', 'Innenausbau', 'Wohnküche')],
        'more': 'Alle Projekte ansehen',
        'places_title': 'Projektstandorte',
    },
    'reviews': {
        'eyebrow': 'Kundenstimmen', 'title': 'Was unsere<br>Kunden sagen',
        'items': [
            ('Umbau', 'Ich bin mehr als glücklich und zufrieden, MENZIL-BAU engagiert zu haben. Die qualifizierte Beratung vor Beginn der Baustelle war sensationell, durch die Fachkenntnisse konnte einiges vorab geklärt werden. Ich kann und werde sie weiterempfehlen.', 'Maria K.', '2603 Felixdorf'),
            ('Renovierung', 'Wir haben Menzil-Bau mit der Renovierung eines älteren Hauses beauftragt. Viele praktische Ideen zur Umgestaltung haben uns binnen kürzester Zeit und zu einem unschlagbaren Preis zu unserem Familientraumhaus verholfen.', 'Josef T.', '2700 Wiener Neustadt'),
            ('Zubau', 'Er war schnell, kompetent und genau – und wir mussten uns um nichts kümmern, alles wurde organisiert. Unser Zubau entstand ohne Flurschaden im Garten, sogar die hohe Hecke blieb unbeschädigt: Der Bagger wurde einfach drübergehoben!', 'Sylvia & Herbert', '2700 Wiener Neustadt'),
        ],
        'more': 'Alle Referenzen',
    },
    'cta': {
        'title': 'Ihr Bauvorhaben.<br>Unser Zeitplan.',
        'sub': 'Erzählen Sie uns von Ihrem Projekt – Neubau, Zubau oder Sanierung. Im kostenlosen Erstgespräch klären wir Umfang, Zeitrahmen und die nächsten Schritte.',
        'btn1': 'Beratungstermin buchen', 'btn2': 'Jetzt anrufen',
    },
    'footer': {'rights': 'Alle Rechte vorbehalten', 'addr1': 'Adresse 1 · Österreich', 'addr2': 'Adresse 2 · Firmensitz', 'impressum': 'Impressum'},
    'p_projekte': {
        'eyebrow': 'Projekte', 'title': 'Abgeschlossene<br>Projekte',
        'sub': 'Einreichplanungen und ausgeführte Bauvorhaben – Einfamilien- und Doppelhäuser, Wohnbau, Zubau und Sanierung.',
        'filters': {'all': 'Alle', 'neubau': 'Neubau', 'zubau': 'Zubau & Umbau', 'sanierung': 'Sanierung', 'wohnbau': 'Wohnbau'},
        'plan': 'Einreichplan', 'plans': 'Pläne',
        'gallery_eyebrow': 'Impressionen', 'gallery_title': 'Von der Baustelle<br>bis zur Übergabe',
        'gfilters': {'all': 'Alle', 'fassade': 'Neubau & Fassade', 'rohbau': 'Rohbau', 'innen': 'Innenausbau & Sanierung'},
    },
    'p_referenzen': {
        'eyebrow': 'Referenzen', 'title': 'Vertrauen, das<br>weiterempfohlen wird',
        'sub': 'Unsere besten Referenzen sind zufriedene Bauherren – und Häuser, die stehen.',
        'list_eyebrow': 'Referenzliste', 'list_title': 'Wo wir bereits<br>gebaut haben',
        'list_intro': 'Eine Auswahl an Standorten, an denen Menzil-Bau geplant, gebaut, zugebaut oder saniert hat.',
        'stats': [('22', '+', 'dokumentierte Projekte'), ('15', '+', 'Gemeinden'), ('3', '', 'Bundesländer')],  # PLATZHALTER
    },
    'p_zertifikate': {
        'eyebrow': 'Zertifikate & Qualität', 'title': 'Berechtigt.<br>Versichert. Geprüft.',
        'sub': 'Bauen ist Vertrauenssache. Diese Nachweise und Standards stehen hinter jedem Menzil-Projekt.',
        'badges': [  # PLATZHALTER – durch echte Nachweise ersetzen
            ('Gewerbeberechtigung', 'Baugewerbe', 'Ausübung des Baugewerbes gemäß Gewerbeordnung'),
            ('Wirtschaftskammer', 'Mitglied', 'Mitgliedsbetrieb der Wirtschaftskammer'),
            ('Betriebshaftpflicht', 'Versichert', 'Umfassende Haftpflichtversicherung für alle Bauleistungen'),
            ('ÖNORM', 'Konforme Ausführung', 'Ausführung nach den einschlägigen österreichischen Normen'),
            ('Arbeitssicherheit', 'Unterwiesen', 'Regelmäßige Sicherheitsunterweisung aller Mitarbeiter'),
            ('Polierschule', 'Absolviert', 'Fachausbildung zum Polier in Tirol'),
        ],
        'note': 'Kopien der Nachweise stellen wir Ihnen auf Anfrage gerne zur Verfügung.',
        'process_eyebrow': 'Unser Ablauf', 'process_title': 'In fünf Schritten<br>zum fertigen Bau',
        'steps': [
            ('Erstberatung', 'Kostenloses Gespräch vor Ort oder telefonisch: Wünsche, Grundstück, Budget und Zeitrahmen.'),
            ('Planung & Einreichung', 'Entwurf, Einreichpläne und Begleitung durch das Bewilligungsverfahren.'),
            ('Angebot', 'Transparentes Angebot mit klaren Positionen und verbindlichem Zeitplan.'),
            ('Ausführung', 'Koordination aller Gewerke, regelmäßige Abstimmung, saubere Baustelle.'),
            ('Übergabe', 'Gemeinsame Abnahme und Übergabe – und auch danach sind wir für Sie da.'),
        ],
    },
    'p_kontakt': {
        'eyebrow': 'Kontakt', 'title': 'Wir freuen uns auf<br>Ihre Nachricht',
        'sub': 'Nennen Sie uns gerne auch Ihre WhatsApp-Nummer oder andere Dienste, über die wir Sie erreichen sollen.',
        'phone': 'Telefon', 'whatsapp': 'WhatsApp', 'whatsapp_cta': 'Nachricht schreiben', 'email': 'E-Mail', 'hours': 'Bürozeiten',
        'book': 'Beratungstermin online buchen', 'route': 'Route planen',
        'impressum_title': 'Impressum',
        'impressum': 'Inhaltlich verantwortlich: MENZIL S.R.O., Gorkeho 3, 81102 Bratislava. Technische Umsetzung und Hosting begründen keine inhaltliche Haftung.',
    },
    'build': {'label': 'Baufortschritt', 'done': 'Schlüsselfertig'},
    'legal': {'title': 'Impressum', 'eyebrow': 'Rechtliches', 'company': 'Firma', 'address': 'Firmensitz', 'contact': 'Kontakt'},  # PLATZHALTER Text (Lorem ipsum)
    'regions': {'noe': 'Niederösterreich', 'bgld': 'Burgenland', 'wien': 'Wien'},
    'places_sub': '{n} Standorte in {r} Bundesländern',
    'tabs': {'photos': 'Fotos: Baustelle bis Übergabe', 'plans': 'Architekturpläne', 'plans_eyebrow': 'Einreichpläne', 'plans_title': 'Geplant und<br>eingereicht'},
    'cert': {'view': 'Nachweis ansehen', 'label': 'Zertifikat', 'pending_title': 'Dokument folgt', 'pending': 'Das Originaldokument wird in Kürze hier hinterlegt. Auf Anfrage senden wir Ihnen gerne eine Kopie.'},  # PLATZHALTER bis Originaldokumente vorliegen
    'lb': {'close': 'Schließen', 'prev': 'Zurück', 'next': 'Weiter'},
}

# ══════════════════════════════ ENGLISH ══════════════════════════════
T['en'] = {
    'html_lang': 'en', 'og_locale': 'en_GB',
    'motto': 'Your partner in and around construction',
    'skip': 'Skip to content',
    'menu': 'Menu',
    'meta': {
        'index': ('Menzil-Bau | Construction company for planning, shell construction & renovation', 'Menzil-Bau – planning, shell construction, facades, conversions, renovation and demolition from a single source. Building across Lower Austria, Burgenland and Vienna since 2010.'),
        'projekte': ('Projects | Menzil-Bau', 'Completed projects and permit plans by Menzil-Bau: single-family and semi-detached houses, residential buildings, extensions and renovations.'),
        'referenzen': ('References | Menzil-Bau', 'What our clients say – testimonials and reference list of Menzil-Bau.'),
        'zertifikate': ('Certificates & Quality | Menzil-Bau', 'Licences, insurance and quality standards of Menzil-Bau.'),
        'kontakt': ('Contact | Menzil-Bau', 'Contact Menzil-Bau by phone, WhatsApp or e-mail, or book a consultation.'),
    },
    'nav': {'leistungen': 'Services', 'warum': 'Why Menzil', 'projekte': 'Projects', 'referenzen': 'References', 'zertifikate': 'Certificates', 'kontakt': 'Contact', 'cta': 'Book a Consultation'},
    'hero': {
        'eyebrow': 'Construction company · Lower Austria & Vienna',
        'title1': 'Built to rely on.', 'title2': 'Delivered on time.',
        'sub': 'Planning, shell construction, facades, conversions, renovation and demolition from a single source. One contact person, one binding schedule, one transparent quote.',
        'stats': [('30', '+', 'Years of experience'), ('120', '+', 'Projects'), ('6', '', 'Service areas'), ('100', '%', 'Single source')],
    },
    'form': {
        'title': 'Request a Free Consultation',
        'first': 'First name', 'last': 'Last name', 'phone': 'Mobile phone', 'email': 'Email address',
        'type': 'Type of project',
        'types': ['New build', 'Extension / conversion', 'Renovation', 'Facade', 'Demolition', 'Planning / permit', 'Other'],
        'location': 'Project location (postcode / town)',
        'message': 'Your message (scope, timeline, WhatsApp …)',
        'submit': 'Send Request', 'sending': 'Sending …',
        'success': "Thank you! We'll be in touch within 24 hours.",
        'again': 'Send Another Request',
        'err': 'Something went wrong. Please try again.',
        'net_err': 'Network error. Please try again.',
        'email_err': 'Please include @ in the email address.',
        'privacy': 'Your data is used solely to process your enquiry.',
        'subject': 'New enquiry – Menzil-Bau website',
    },
    'challenge': {
        'label': 'The Challenge',
        'title': 'Building projects rarely fail on skill – they fail on organisation',
        'items': [
            'Construction drags on and move-in and financing dates start to slip',
            'Change orders and vague line items blow the original budget',
            'Too many trades, and nobody coordinating them',
            'Planning and execution come from different firms and do not fit together',
            'Contacts are hard to reach just when decisions have to be made on site',
        ],
    },
    'solution': {
        'label': 'The Menzil Way',
        'title': 'One team. One schedule. One contact.',
        'items': [
            'Binding construction schedule with clear milestones – from permit to handover',
            'Transparent quote with traceable line items and no hidden costs',
            'We coordinate every trade – you do not have to worry about a thing',
            'Planning and execution under one roof: what is drawn is what gets built',
            'Personal contact, available Mon – Fri from 07:30 to 17:00',
        ],
    },
    'metrics': {
        'highlight': 2,
        'eyebrow': 'Menzil in numbers', 'title': 'Experience you can<br>see on site',
        'items': [('15', '+', 'Years as an independent construction company – Menzil-Bau was founded in 2010, the founder\'s site experience goes back to 1996'),
                  ('15', '+', 'Municipalities across Lower Austria, Burgenland and Vienna where we have built, planned or renovated'),
                  ('1', '', 'Contact person for your entire project – from the first sketch through the shell to turnkey handover')],
    },
    'services': {
        'eyebrow': 'Services', 'title': 'Everything around<br>your building project',
        'items': [
            ('Planning', 'We develop and design your project and capture it in architectural and permit drawings – the basis for approval, quotation and construction.', ['Permit planning', 'Design', 'Building permit']),
            ('Shell Construction', 'We build the outer structure of your building including the roof. Windows, facade and interior fit-out can be added on request.', ['Masonry', 'Solid construction', 'Roof structure']),
            ('Facades', 'The facade is the most visible part of your building. We design it to your wishes – attractive and technically sound.', ['ETICS insulation', 'Render', 'Design']),
            ('Conversions & Extensions', 'Changes exactly as you want them – inside and out. From extensions to new room layouts, carefully planned and without unnecessary damage.', ['Extensions', 'Interior works', 'Layouts']),
            ('Renovation', 'Structural and technical restoration and modernisation of your property – to repair damage and lastingly raise the living standard.', ['Old buildings', 'Bath & kitchen', 'Modernisation']),
            ('Demolition', 'When a building has to go or a conversion requires it, we carry out professional demolition including disposal.', ['Demolition', 'Strip-out', 'Disposal']),
        ],
    },
    'why': {
        'eyebrow': 'Why Menzil', 'title': 'From bricklayer to<br>master builder',
        'items': [
            ('Single source', 'Planning, shell, facade, conversion, renovation and demolition – <strong>six service areas, one contractor</strong>. One contact person instead of five companies.'),
            ('Experience since 1996', 'The founder trained as a bricklayer and <strong>graduated from foreman school</strong> in Tyrol. That hands-on site experience goes into every project.'),
            ('In-house planning', 'Permit plans, floor plans and elevations are drawn in-house. <strong>What is planned is what gets built</strong> – no friction between designer and builder.'),
            ('Quality at fair prices', 'Clear quotes, clean execution, no collateral damage. Our clients recommend us – <strong>for the advice, the quality and the price</strong>.'),
        ],
    },
    'featured': {
        'eyebrow': 'Projects', 'title': 'Built in Lower Austria<br>& Vienna',
        'intro': 'From single-family homes to semi-detached and terraced houses and residential complexes – a selection from our sites.',
        'cards': [('f13', 'Residential', 'Apartment building'), ('f14', 'Shell construction', 'Solid masonry'), ('f15', 'New build', 'Terraced housing'),
                  ('f01', 'New build', 'House with terrace'), ('f64', 'Renovation', 'Bathroom'), ('f52', 'Interior', 'Open-plan kitchen')],
        'more': 'View all projects',
        'places_title': 'Project locations',
    },
    'reviews': {
        'eyebrow': 'Testimonials', 'title': 'What our<br>clients say',
        'items': [
            ('Conversion', 'I am more than happy to have hired MENZIL-BAU. The expert advice before the start of construction was outstanding, and thanks to their know-how a lot could be clarified in advance. I can and will recommend them.', 'Maria K.', '2603 Felixdorf'),
            ('Renovation', 'We hired Menzil-Bau to renovate an older house. Many practical redesign ideas turned it into our family dream home in no time and at an unbeatable price.', 'Josef T.', '2700 Wiener Neustadt'),
            ('Extension', 'Fast, competent and precise – and we did not have to worry about anything, everything was organised. Our extension was built without damaging the garden; even the tall hedge survived: the excavator was simply lifted over it!', 'Sylvia & Herbert', '2700 Wiener Neustadt'),
        ],
        'more': 'All references',
    },
    'cta': {
        'title': 'Your project.<br>Our schedule.',
        'sub': 'Tell us about your project – new build, extension or renovation. In a free initial consultation we clarify scope, timeline and next steps.',
        'btn1': 'Book a Consultation', 'btn2': 'Call now',
    },
    'footer': {'rights': 'All rights reserved', 'addr1': 'Address 1 · Austria', 'addr2': 'Address 2 · Registered office', 'impressum': 'Legal notice'},
    'p_projekte': {
        'eyebrow': 'Projects', 'title': 'Completed<br>projects',
        'sub': 'Permit plans and completed builds – single-family and semi-detached houses, residential buildings, extensions and renovations.',
        'filters': {'all': 'All', 'neubau': 'New build', 'zubau': 'Extension & conversion', 'sanierung': 'Renovation', 'wohnbau': 'Residential'},
        'plan': 'Permit plan', 'plans': 'plans',
        'gallery_eyebrow': 'Impressions', 'gallery_title': 'From site<br>to handover',
        'gfilters': {'all': 'All', 'fassade': 'New build & facade', 'rohbau': 'Shell construction', 'innen': 'Interior & renovation'},
    },
    'p_referenzen': {
        'eyebrow': 'References', 'title': 'Trust that gets<br>recommended',
        'sub': 'Our best references are satisfied clients – and houses that stand.',
        'list_eyebrow': 'Reference list', 'list_title': 'Where we have<br>already built',
        'list_intro': 'A selection of locations where Menzil-Bau has planned, built, extended or renovated.',
        'stats': [('22', '+', 'documented projects'), ('15', '+', 'municipalities'), ('3', '', 'federal states')],
    },
    'p_zertifikate': {
        'eyebrow': 'Certificates & Quality', 'title': 'Licensed.<br>Insured. Proven.',
        'sub': 'Building is a matter of trust. These credentials and standards stand behind every Menzil project.',
        'badges': [
            ('Trade licence', 'Construction', 'Licensed to carry out construction work under the Trade Act'),
            ('Chamber of Commerce', 'Member', 'Member company of the Austrian Economic Chamber'),
            ('Liability insurance', 'Insured', 'Comprehensive liability cover for all construction work'),
            ('ÖNORM', 'Compliant', 'Execution according to the relevant Austrian standards'),
            ('Occupational safety', 'Trained', 'Regular safety training for all employees'),
            ('Foreman school', 'Graduated', 'Professional foreman training in Tyrol'),
        ],
        'note': 'Copies of all credentials are available on request.',
        'process_eyebrow': 'How we work', 'process_title': 'Five steps to<br>your finished build',
        'steps': [
            ('Consultation', 'Free meeting on site or by phone: wishes, plot, budget and timeline.'),
            ('Planning & permit', 'Design, permit drawings and support throughout the approval process.'),
            ('Quote', 'Transparent quote with clear line items and a binding schedule.'),
            ('Construction', 'Coordination of every trade, regular updates, a tidy site.'),
            ('Handover', 'Joint inspection and handover – and we are still there for you afterwards.'),
        ],
    },
    'p_kontakt': {
        'eyebrow': 'Contact', 'title': 'We look forward to<br>hearing from you',
        'sub': 'Feel free to give us your WhatsApp number or any other service we should use to reach you.',
        'phone': 'Phone', 'whatsapp': 'WhatsApp', 'whatsapp_cta': 'Send a message', 'email': 'Email', 'hours': 'Office hours',
        'book': 'Book a consultation online', 'route': 'Get directions',
        'impressum_title': 'Legal notice',
        'impressum': 'Responsible for content: MENZIL S.R.O., Gorkeho 3, 81102 Bratislava. Technical implementation and hosting do not establish liability for content.',
    },
    'build': {'label': 'Construction progress', 'done': 'Turnkey ready'},
    'legal': {'title': 'Legal notice', 'eyebrow': 'Legal', 'company': 'Company', 'address': 'Registered office', 'contact': 'Contact'},  # PLATZHALTER Text (Lorem ipsum)
    'regions': {'noe': 'Lower Austria', 'bgld': 'Burgenland', 'wien': 'Vienna'},
    'places_sub': '{n} locations in {r} federal states',
    'tabs': {'photos': 'Photos: site to handover', 'plans': 'Architectural plans', 'plans_eyebrow': 'Permit plans', 'plans_title': 'Planned and<br>submitted'},
    'cert': {'view': 'View certificate', 'label': 'Certificate', 'pending_title': 'Document to follow', 'pending': 'The original document will be added here shortly. A copy is available on request.'},  # PLATZHALTER bis Originaldokumente vorliegen
    'lb': {'close': 'Close', 'prev': 'Previous', 'next': 'Next'},
}

# ══════════════════════════════ TÜRKÇE ══════════════════════════════
T['tr'] = {
    'html_lang': 'tr', 'og_locale': 'tr_TR',
    'motto': 'İnşaatta ve inşaat çevresinde ortağınız',
    'skip': 'İçeriğe geç',
    'menu': 'Menü',
    'meta': {
        'index': ('Menzil-Bau | Planlama, kaba inşaat ve renovasyon', 'Menzil-Bau – planlama, kaba inşaat, cephe, tadilat, renovasyon ve yıkım tek elden. 2010’dan beri Aşağı Avusturya, Burgenland ve Viyana’da.'),
        'projekte': ('Projeler | Menzil-Bau', 'Menzil-Bau’nun tamamlanan projeleri ve ruhsat çizimleri: müstakil ve ikiz konutlar, konut projeleri, ek bina ve renovasyon.'),
        'referenzen': ('Referanslar | Menzil-Bau', 'Müşterilerimiz ne diyor – Menzil-Bau müşteri yorumları ve referans listesi.'),
        'zertifikate': ('Sertifikalar ve Kalite | Menzil-Bau', 'Menzil-Bau’nun ruhsatları, sigortaları ve kalite standartları.'),
        'kontakt': ('İletişim | Menzil-Bau', 'Menzil-Bau ile telefon, WhatsApp veya e-posta ile iletişime geçin ya da danışmanlık randevusu alın.'),
    },
    'nav': {'leistungen': 'Hizmetler', 'warum': 'Neden Menzil', 'projekte': 'Projeler', 'referenzen': 'Referanslar', 'zertifikate': 'Sertifikalar', 'kontakt': 'İletişim', 'cta': 'Randevu Al'},
    'hero': {
        'eyebrow': 'Müteahhitlik · Aşağı Avusturya ve Viyana',
        'title1': 'Güvenle inşa.', 'title2': 'Zamanında teslim.',
        'sub': 'Planlama, kaba inşaat, cephe, tadilat, renovasyon ve yıkım tek elden. Tek muhatap, bağlayıcı bir iş takvimi, şeffaf bir teklif.',
        'stats': [('30', '+', 'Yıl tecrübe'), ('120', '+', 'Proje'), ('6', '', 'Hizmet alanı'), ('100', '%', 'Tek elden')],
    },
    'form': {
        'title': 'Ücretsiz Ön Görüşme Talep Edin',
        'first': 'Ad', 'last': 'Soyad', 'phone': 'Cep telefonu', 'email': 'E-posta adresi',
        'type': 'Proje türü',
        'types': ['Yeni yapı', 'Ek bina / tadilat', 'Renovasyon', 'Cephe', 'Yıkım', 'Planlama / ruhsat', 'Diğer'],
        'location': 'Proje yeri (posta kodu / şehir)',
        'message': 'Mesajınız (kapsam, zaman planı, WhatsApp …)',
        'submit': 'Talebi Gönder', 'sending': 'Gönderiliyor …',
        'success': 'Teşekkürler! 24 saat içinde sizinle iletişime geçeceğiz.',
        'again': 'Yeni Talep Gönder',
        'err': 'Bir şeyler ters gitti. Lütfen tekrar deneyin.',
        'net_err': 'Bağlantı hatası. Lütfen tekrar deneyin.',
        'email_err': 'Lütfen e-posta adresine @ ekleyin.',
        'privacy': 'Verileriniz yalnızca talebinizi işlemek için kullanılır.',
        'subject': 'Yeni talep – Menzil-Bau web sitesi',
    },
    'challenge': {
        'label': 'Sorun',
        'title': 'İnşaat projeleri ustalıktan değil, organizasyondan aksar',
        'items': [
            'İnşaat süresi uzar, taşınma ve finansman tarihleri kayar',
            'Ek işler ve belirsiz kalemler başlangıçtaki bütçeyi aşar',
            'Çok sayıda taşeron vardır ama onları koordine eden kimse yoktur',
            'Planlama ve uygulama farklı firmalardan gelir, birbirine uymaz',
            'Şantiyede karar gerektiğinde muhataba ulaşmak zordur',
        ],
    },
    'solution': {
        'label': 'Menzil Yaklaşımı',
        'title': 'Tek ekip. Tek takvim. Tek muhatap.',
        'items': [
            'Ruhsattan teslimata kadar net aşamalı, bağlayıcı bir iş takvimi',
            'Kalemleri anlaşılır, gizli maliyeti olmayan şeffaf teklif',
            'Tüm taşeronları biz koordine ederiz, siz hiçbir şeyle uğraşmazsınız',
            'Planlama ve uygulama aynı çatı altında: çizilen neyse o inşa edilir',
            'Kişisel muhatap, Pazartesi–Cuma 07:30–17:00 arası ulaşılabilir',
        ],
    },
    'metrics': {
        'highlight': 2,
        'eyebrow': 'Rakamlarla Menzil', 'title': 'Şantiyede görülen<br>tecrübe',
        'items': [('15', '+', 'Yıllık bağımsız inşaat firması. Menzil-Bau 2010’da kuruldu, kurucunun şantiye tecrübesi 1996’ya dayanıyor'),
                  ('15', '+', 'Aşağı Avusturya, Burgenland ve Viyana’da inşa ettiğimiz, planladığımız veya yenilediğimiz belediye'),
                  ('1', '', 'Projenizin tamamı için tek muhatap: ilk eskizden kaba inşaata, anahtar teslimine kadar')],
    },
    'services': {
        'eyebrow': 'Hizmetler', 'title': 'Projenizle ilgili<br>her şey',
        'items': [
            ('Planlama', 'Projenizi tasarlar, mimari ve ruhsat çizimlerine dökeriz. Onay, teklif ve uygulamanın temeli budur.', ['Ruhsat projesi', 'Tasarım', 'Yapı izni']),
            ('Kaba İnşaat', 'Binanızın çatı dahil dış iskeletini inşa ederiz. İsterseniz pencere, cephe ve iç tadilatı da üstleniriz.', ['Yığma yapı', 'Duvar', 'Çatı']),
            ('Cephe', 'Cephe binanızın en görünür yüzüdür. İsteğinize göre, estetik ve teknik açıdan kusursuz uygularız.', ['Mantolama', 'Sıva', 'Tasarım']),
            ('Tadilat ve Ek Bina', 'İç ve dış mekânda tam istediğiniz değişiklikler. Ek binadan yeni oda düzenine kadar, özenle planlanmış ve gereksiz hasar vermeden.', ['Ek bina', 'İç tadilat', 'Mekân düzeni']),
            ('Renovasyon', 'Hasarları gidermek ve yaşam standardını kalıcı olarak yükseltmek için yapı-teknik yenileme ve modernizasyon.', ['Eski yapı', 'Banyo ve mutfak', 'Modernizasyon']),
            ('Yıkım', 'Bir binanın kaldırılması gerektiğinde veya tadilat bunu zorunlu kıldığında, atık bertarafı dahil profesyonel yıkım yaparız.', ['Yıkım', 'Söküm', 'Bertaraf']),
        ],
    },
    'why': {
        'eyebrow': 'Neden Menzil', 'title': 'Duvar ustalığından<br>müteahhitliğe',
        'items': [
            ('Tek elden', 'Planlama, kaba inşaat, cephe, tadilat, renovasyon ve yıkım. <strong>Altı hizmet alanı, tek sözleşme</strong>. Beş firma yerine tek muhatap.'),
            ('1996’dan beri tecrübe', 'Kurucumuz duvarcı olarak meslek eğitimini tamamladı ve Tirol’de <strong>şantiye şefliği okulunu bitirdi</strong>. Bu saha tecrübesi her projeye yansır.'),
            ('Kendi bünyemizde planlama', 'Ruhsat projeleri, kat planları ve cephe çizimleri bizde hazırlanır. <strong>Ne planlanırsa o inşa edilir</strong>; mimar ile müteahhit arasında kayıp olmaz.'),
            ('Uygun fiyata kalite', 'Net teklif, temiz işçilik, çevreye hasar yok. Müşterilerimiz bizi <strong>danışmanlık, kalite ve fiyat için</strong> tavsiye ediyor.'),
        ],
    },
    'featured': {
        'eyebrow': 'Projeler', 'title': 'Aşağı Avusturya ve<br>Viyana’da inşa edildi',
        'intro': 'Müstakil evlerden ikiz ve sıra evlere, konut projelerine kadar şantiyelerimizden bir seçki.',
        'cards': [('f13', 'Konut', 'Apartman'), ('f14', 'Kaba inşaat', 'Yığma yapı'), ('f15', 'Yeni yapı', 'Sıra evler'),
                  ('f01', 'Yeni yapı', 'Teraslı konut'), ('f64', 'Renovasyon', 'Banyo'), ('f52', 'İç tadilat', 'Açık mutfak')],
        'more': 'Tüm projeleri gör',
        'places_title': 'Proje lokasyonları',
    },
    'reviews': {
        'eyebrow': 'Müşteri Yorumları', 'title': 'Müşterilerimiz<br>ne diyor',
        'items': [
            ('Tadilat', 'MENZIL-BAU ile çalıştığım için çok mutluyum. Şantiye başlamadan önceki uzman danışmanlık harikaydı; bilgi birikimleri sayesinde pek çok konu önceden netleşti. Onları kesinlikle tavsiye ederim.', 'Maria K.', '2603 Felixdorf'),
            ('Renovasyon', 'Eski bir evin renovasyonunu Menzil-Bau’ya verdik. Pratik fikirleriyle evi çok kısa sürede ve rakipsiz bir fiyata hayalimizdeki aile evine dönüştürdüler.', 'Josef T.', '2700 Wiener Neustadt'),
            ('Ek bina', 'Hızlı, yetkin ve titiz çalıştılar, biz hiçbir şeyle uğraşmadık, her şeyi onlar organize etti. Ek binamız bahçeye zarar vermeden yapıldı; yüksek çitimiz bile sağlam kaldı: ekskavatörü çitin üstünden kaldırdılar!', 'Sylvia & Herbert', '2700 Wiener Neustadt'),
        ],
        'more': 'Tüm referanslar',
    },
    'cta': {
        'title': 'Sizin projeniz.<br>Bizim takvimimiz.',
        'sub': 'Projenizi anlatın: yeni yapı, ek bina ya da renovasyon. Ücretsiz ön görüşmede kapsamı, süreyi ve sonraki adımları netleştirelim.',
        'btn1': 'Randevu Al', 'btn2': 'Hemen arayın',
    },
    'footer': {'rights': 'Tüm hakları saklıdır', 'addr1': 'Adres 1 · Avusturya', 'addr2': 'Adres 2 · Merkez', 'impressum': 'Künye'},
    'p_projekte': {
        'eyebrow': 'Projeler', 'title': 'Tamamlanan<br>projeler',
        'sub': 'Ruhsat projeleri ve uygulanan inşaatlar: müstakil ve ikiz konutlar, konut projeleri, ek bina ve renovasyon.',
        'filters': {'all': 'Tümü', 'neubau': 'Yeni yapı', 'zubau': 'Ek bina ve tadilat', 'sanierung': 'Renovasyon', 'wohnbau': 'Konut projesi'},
        'plan': 'Ruhsat projesi', 'plans': 'çizim',
        'gallery_eyebrow': 'İzlenimler', 'gallery_title': 'Şantiyeden<br>teslimata',
        'gfilters': {'all': 'Tümü', 'fassade': 'Yeni yapı ve cephe', 'rohbau': 'Kaba inşaat', 'innen': 'İç tadilat ve renovasyon'},
    },
    'p_referenzen': {
        'eyebrow': 'Referanslar', 'title': 'Tavsiye edilen<br>güven',
        'sub': 'En iyi referansımız memnun ev sahipleri ve ayakta duran binalar.',
        'list_eyebrow': 'Referans listesi', 'list_title': 'İnşaat yaptığımız<br>yerler',
        'list_intro': 'Menzil-Bau’nun planladığı, inşa ettiği, ek bina yaptığı veya yenilediği lokasyonlardan bir seçki.',
        'stats': [('22', '+', 'belgelenmiş proje'), ('15', '+', 'belediye'), ('3', '', 'eyalet')],
    },
    'p_zertifikate': {
        'eyebrow': 'Sertifikalar ve Kalite', 'title': 'Ruhsatlı.<br>Sigortalı. Denetimli.',
        'sub': 'İnşaat bir güven işidir. Her Menzil projesinin arkasında bu belgeler ve standartlar var.',
        'badges': [
            ('İnşaat ruhsatı', 'Yetkili', 'Esnaf ve Sanatkârlar Kanunu’na göre inşaat yetkisi'),
            ('Ticaret Odası', 'Üye', 'Avusturya Ekonomi Odası üyesi firma'),
            ('Mesleki sorumluluk', 'Sigortalı', 'Tüm inşaat işleri için kapsamlı sorumluluk sigortası'),
            ('ÖNORM', 'Uyumlu', 'İlgili Avusturya standartlarına uygun uygulama'),
            ('İş güvenliği', 'Eğitimli', 'Tüm çalışanlara düzenli iş güvenliği eğitimi'),
            ('Şantiye şefliği', 'Mezun', 'Tirol’de şantiye şefliği meslek eğitimi'),
        ],
        'note': 'Belgelerin kopyalarını talep üzerine memnuniyetle iletiyoruz.',
        'process_eyebrow': 'Çalışma şeklimiz', 'process_title': 'Beş adımda<br>tamamlanan yapı',
        'steps': [
            ('Ön görüşme', 'Yerinde veya telefonda ücretsiz görüşme: istekler, arsa, bütçe ve süre.'),
            ('Planlama ve ruhsat', 'Tasarım, ruhsat çizimleri ve onay sürecinde destek.'),
            ('Teklif', 'Net kalemli şeffaf teklif ve bağlayıcı iş takvimi.'),
            ('Uygulama', 'Tüm taşeronların koordinasyonu, düzenli bilgilendirme, temiz şantiye.'),
            ('Teslim', 'Birlikte kabul ve teslim. Sonrasında da yanınızdayız.'),
        ],
    },
    'p_kontakt': {
        'eyebrow': 'İletişim', 'title': 'Mesajınızı<br>bekliyoruz',
        'sub': 'Size ulaşmamız için WhatsApp numaranızı veya başka bir kanalı da paylaşabilirsiniz.',
        'phone': 'Telefon', 'whatsapp': 'WhatsApp', 'whatsapp_cta': 'Mesaj yazın', 'email': 'E-posta', 'hours': 'Çalışma saatleri',
        'book': 'Online randevu alın', 'route': 'Yol tarifi',
        'impressum_title': 'Künye',
        'impressum': 'İçerikten sorumlu: MENZIL S.R.O., Gorkeho 3, 81102 Bratislava. Teknik uygulama ve barındırma içerik sorumluluğu doğurmaz.',
    },
    'build': {'label': 'İnşaat ilerlemesi', 'done': 'Anahtar teslim'},
    'legal': {'title': 'Künye', 'eyebrow': 'Yasal bilgiler', 'company': 'Firma', 'address': 'Merkez', 'contact': 'İletişim'},  # PLATZHALTER Text (Lorem ipsum)
    'regions': {'noe': 'Aşağı Avusturya', 'bgld': 'Burgenland', 'wien': 'Viyana'},
    'places_sub': '{r} eyalette {n} lokasyon',
    'tabs': {'photos': 'Fotoğraflar: şantiyeden teslimata', 'plans': 'Mimari çizimler', 'plans_eyebrow': 'Ruhsat projeleri', 'plans_title': 'Planlandı ve<br>onaya sunuldu'},
    'cert': {'view': 'Belgeyi görüntüle', 'label': 'Sertifika', 'pending_title': 'Belge eklenecek', 'pending': 'Orijinal belge yakında buraya eklenecek. Talep üzerine bir kopyasını memnuniyetle iletiyoruz.'},  # PLATZHALTER bis Originaldokumente vorliegen
    'lb': {'close': 'Kapat', 'prev': 'Önceki', 'next': 'Sonraki'},
}

# Places for the reference list (from plan file names + testimonials)
def _places():
    seen = {}
    for loc in [p['loc'] for p in PROJECTS] + ['2603 Felixdorf']:
        if loc == 'Niederösterreich':
            continue
        town = loc.split(' ', 1)[-1] if loc.split(' ', 1)[0].isdigit() else loc
        if town not in seen or (loc[0].isdigit() and not seen[town][0].isdigit()):
            seen[town] = loc
    return sorted(seen.values(), key=lambda s: s.split(' ', 1)[-1] if s[0].isdigit() else s)
PLACES = _places()

# Bundesland per location (for the grouped "Projektstandorte" block); default = Niederösterreich
REGION_OF = {'7210 Mattersburg': 'bgld', '7201 Neudörfl': 'bgld', 'Wien': 'wien'}

LOREM = [
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante venenatis dapibus posuere velit aliquet. Donec ullamcorper nulla non metus auctor fringilla. Cras mattis consectetur purus sit amet fermentum.',
    'Maecenas faucibus mollis interdum. Vestibulum id ligula porta felis euismod semper. Nullam quis risus eget urna mollis ornare vel eu leo. Aenean lacinia bibendum nulla sed consectetur. Etiam porta sem malesuada magna mollis euismod.',
    'Curabitur blandit tempus porttitor. Donec sed odio dui. Morbi leo risus, porta ac consectetur ac, vestibulum at eros. Praesent commodo cursus magna, vel scelerisque nisl consectetur et. Sed posuere consectetur est at lobortis.',
]  # PLATZHALTER – echter Impressumstext folgt
