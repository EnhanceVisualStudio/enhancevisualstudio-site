"""Generate the static pages and browser/Worker booking catalog from shared content."""
import argparse
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.enhancevisualstudio.com"
PREVIEW_ORIGIN = "https://codex-evs-redesign.enhancevisualstudio-site.pages.dev"
EMAIL = "hello@enhancevisualstudio.com"
PHONE = "+13233271806"
PHONE_DISPLAY = "(323) 327-1806"
SLOGAN = "Pose. Click. Enhance"
COPYRIGHT = "©2026 Enhance Visual Studio - All Rights Reserved."
# Enable only after signed-out HTTPS checks of the homepage, browse, and search.
GALLERY_URL = None
SOCIALS = [
    ("Instagram", "https://instagram.com/enhancevisualstudio"),
    ("TikTok", "https://tiktok.com/@enhancevisualstudio"),
    ("YouTube", "https://youtube.com/@enhancevisualstudio"),
    ("Facebook", "https://facebook.com/enhancevisualstudio"),
]
SERVICES = {
    "Portraits & studio": [
        ("portraits", "Portrait Photography", "Individual portraits with guided posing and lighting that suits the mood."),
        ("studio", "Studio Photography", "A studio session with backdrops and lighting tailored to the look you want."),
        ("maternity", "Maternity Photography", "Studio or outdoor portraits to mark this chapter of your family’s story."),
        ("family", "Family & Children", "Relaxed group portraits and candid moments, with space for kids to be themselves."),
        ("graduation", "Graduation Photography", "Celebrate your milestone with cap-and-gown portraits and a location that means something to you."),
        ("editorial", "Beauty & Editorial Photography", "Portraits built around styling, expressive poses, and considered light."),
        ("couples", "Couples Photography", "Guided portraits for two, from an easy outdoor session to a studio setting."),
    ],
    "Weddings & celebrations": [
        ("birthdays", "Birthday Photography", "Birthday portraits or candid coverage of the people and details that make the day yours."),
        ("weddings", "Weddings & Engagements", "Guided portraits and candid coverage of your engagement or wedding day."),
        ("events", "Event Photography", "Coverage of the setting, guests, and key moments of your event."),
    ],
    "Business & commercial": [
        ("headshots", "Professional Headshots", "Polished, approachable portraits for professional profiles, teams, and websites."),
        ("branding", "Personal Branding Photography", "A coordinated set of portraits and lifestyle images for your business and campaigns."),
        ("food", "Food & Restaurant Photography", "Photographs of dishes, ingredients, and spaces for menus and restaurant marketing."),
        ("real-estate", "Real Estate & Interior Photography", "Interior, exterior, and detail photographs that show how a property looks and feels."),
        ("product", "Commercial & Product Photography", "Product details and styled scenes for websites, catalogs, and campaigns."),
    ],
}
SERVICE_ANCHORS = {
    "Portraits & studio": "portraits",
    "Weddings & celebrations": "celebrations",
    "Business & commercial": "commercial",
}
PACKAGES = {
    "essential": ("Essential", 200, "Portrait / Studio", [
        "45 minutes", "1 person", "1 outfit, 1 location",
        "5 professionally retouched images", "Studio or on-location",
    ]),
    "signature": ("Signature", 350, "Portrait / Studio", [
        "Up to 90 minutes", "1 person", "Up to 2 outfits, 2 locations",
        "12 professionally retouched images", "Studio or on-location",
    ]),
    "creative-campaign": ("Creative Campaign", 550, "Branding / Editorial", [
        "2–3 hour session", "Up to 3 people", "1–5 outfit changes, up to 3 locations",
        "20 professionally retouched images", "Studio or on-location",
    ]),
}
PACKAGE_SERVICES = {
    "portraits": ["essential", "signature", "creative-campaign"],
    "studio": ["essential", "signature", "creative-campaign"],
    "headshots": ["essential", "signature"],
    "branding": ["creative-campaign"],
    "editorial": ["creative-campaign"],
}
POLICIES = [
    ("Retainers", "A non-refundable retainer is required to secure all bookings."),
    ("Late Arrivals", "Clients arriving more than 15 minutes late may receive a shortened session. Arrivals exceeding 30 minutes will be cancelled and your retainer will be forfeited."),
    ("Rescheduling", "Sessions may be rescheduled once with at least 48 hours notice."),
    ("Image Delivery", "Final edited images are delivered through a private online gallery."),
    ("Turnaround Time", "Final edited galleries are typically delivered within 7–14 business days depending on session type. Express delivery options are also available for a fee."),
    ("RAW Files", "RAW/unedited files are not included or delivered."),
    ("Creative Direction", "Enhance Visual Studio maintains all ownership rights and creative discretion regarding posing, editing style, lighting, and final image selection to preserve brand quality and artistic consistency."),
]
DISPLAY_WIDTHS = (480, 960, 1440, 1920)
PHOTOS = {
    1: (1080, 1364, "Studio portrait of a woman with silver hair in a black sequined gown", "Studio", "Portraits"),
    2: (1080, 1364, "Full-length studio portrait in a black gown and silver heels", "Studio", "Portraits"),
    3: (1080, 1920, "Close-up in white cat-eye sunglasses and a vivid pink jacket", "Editorial"),
    4: (677, 1016, "Portrait with a rainbow lollipop held over one eye", "Editorial"),
    5: (1080, 1363, "Kneeling studio portrait in a black outfit against a white backdrop", "Studio"),
    6: (803, 1427, "Portrait in a bright pink top against a green backdrop", "Portraits"),
    7: (1080, 1363, "Studio portrait in a black leather jacket and heeled boots", "Studio", "Editorial"),
    8: (8145, 5433, "Reclining studio portrait in a black leopard-print outfit and platform heels", "Editorial"),
    9: (2732, 4096, "Smiling woman in a red ruffled dress against a charcoal backdrop", "Studio", "Portraits"),
    10: (1997, 1123, "Couple posing beneath a white parasol at an outdoor celebration", "Engagements"),
    11: (1365, 2048, "Couple holding hands beneath a canopy at their outdoor engagement picnic", "Engagements"),
    12: (2048, 1365, "Engaged couple posing with guests on the lawn at their celebration", "Engagements"),
    13: (1365, 2048, "The engaged couple posing with a guest beneath garden trees", "Engagements"),
    14: (2048, 1365, "Guests gathered around a low picnic table at an outdoor engagement celebration", "Engagements"),
}
NAV = [
    ("index.html", "Home"), ("events.html", "Events"), ("portfolio.html", "Portfolio"), ("packages.html", "Packages"),
    ("about.html", "About"), ("contact.html", "Contact"),
]


def photo(number, sizes, *, eager=False, high=False):
    width, height, alt, *_ = PHOTOS[number]
    variants = [candidate for candidate in DISPLAY_WIDTHS if candidate < width]
    srcset = ", ".join(f"images/display/{number}-{variant}.jpg {variant}w" for variant in variants)
    if not srcset:
        srcset = f"images/{number}.jpg {width}w"
    src = f"images/display/{number}-{variants[0]}.jpg" if variants else f"images/{number}.jpg"
    priority = ' fetchpriority="high"' if high else ""
    return (
        f'<img src="{src}" srcset="{srcset}" sizes="{sizes}" width="{width}" height="{height}" '
        f'alt="{escape(alt)}" loading="{"eager" if eager else "lazy"}" decoding="async"'
        f'{priority}>'
    )


def page(path, title, description, content, *, noindex=False):
    link_prefix = "/" if path == "404.html" else ""
    robots = '\n  <meta name="robots" content="noindex, follow">' if noindex else ""
    canonical = SITE + ("/" if path == "index.html" else "/" + Path(path).stem)
    current = ' aria-current="page"'
    links = "".join(
        f'<a href="{link_prefix}{url}"{current if path == url else ""}>{label}</a>'
        for url, label in NAV
    )
    booking_current = ' aria-current="page"' if path == "book.html" else ""
    socials = "".join(f'<a href="{url}">{name}</a>' for name, url in SOCIALS)
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": SITE + "/#studio",
        "name": "Enhance Visual Studio",
        "url": SITE + "/",
        "email": EMAIL,
        "logo": SITE + "/assets/enhance-visual-studio-logo.webp",
        "telephone": PHONE,
        "image": SITE + "/images/display/9-960.jpg",
        "slogan": SLOGAN,
        "description": "Bay Area photography studio for portraits, celebrations, and commercial work.",
        "areaServed": {"@type": "Place", "name": "San Francisco Bay Area, California"},
        "sameAs": [url for _, url in SOCIALS],
    })
    document = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0a0a0a">
  <title>{escape(title)} | Enhance Visual Studio</title>
  <meta name="description" content="{escape(description, quote=True)}">{robots}
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Enhance Visual Studio">
  <meta property="og:title" content="{escape(title, quote=True)} | Enhance Visual Studio">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/images/display/9-960.jpg">
  <meta property="og:image:alt" content="{escape(PHOTOS[9][2], quote=True)}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{link_prefix}assets/evs-icon.png" type="image/png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&amp;family=Manrope:wght@400;500;600;700;800&amp;display=swap">
  <link rel="stylesheet" href="{link_prefix}style.css">
  <script type="application/ld+json">{schema}</script>
  <script type="module" src="{link_prefix}script.js"></script>
</head>
<body>
  <div class="site-scroll">
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap header-row">
      <a class="brand" href="{link_prefix}index.html" aria-label="Enhance Visual Studio home">
        <img src="{link_prefix}assets/enhance-visual-studio-logo.webp" width="560" height="315" alt="">
      </a>
      <button class="menu-button" type="button" aria-controls="site-nav" aria-expanded="false" hidden>Menu <span aria-hidden="true">☰</span></button>
      <nav class="site-nav" id="site-nav" aria-label="Primary">
        {links}
        <a class="button button-small" href="{link_prefix}book.html"{booking_current}>Book a session <span aria-hidden="true">↗</span></a>
      </nav>
    </div>
  </header>
  <main id="main" tabindex="-1">
{content}
  </main>
  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div><p class="footer-name">Enhance Visual Studio</p><p>{SLOGAN}</p><p>San Francisco Bay Area, California</p></div>
        <div>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
          <div><a href="tel:{PHONE}">{PHONE_DISPLAY}</a></div>
          <div class="footer-links">{socials}</div>
        </div>
        <div class="footer-links"><a href="{link_prefix}events.html">Event galleries</a><a href="{link_prefix}book.html">Book a session</a><a href="{link_prefix}policies.html">Booking policies</a></div>
      </div>
    </div>
    <p class="copyright">{COPYRIGHT}</p>
  </footer>
  </div>
  <div class="call-dock">
    <a class="floating-call" href="tel:{PHONE}" aria-label="Call now: Enhance Visual Studio at {PHONE_DISPLAY}">
      <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <path d="M6.6 10.8a15.2 15.2 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.2c1.1.4 2.3.6 3.6.6a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.3.2 2.5.6 3.6a1 1 0 0 1-.2 1z"/>
      </svg>
      <span>Call Now</span>
    </a>
  </div>
</body>
</html>
'''
    (ROOT / path).write_text("\n".join(line.rstrip() for line in document.splitlines()) + "\n", encoding="utf-8")


def intro(label, title, description, *, compact=False):
    modifier = " page-heading-compact" if compact else ""
    label_class = "eyebrow slogan" if label == SLOGAN else "eyebrow"
    return f'''
    <section class="page-heading{modifier}"><div class="wrap">
      <p class="{label_class}">{label}</p>
      <h1>{title}</h1>
      <p class="lede">{description}</p>
    </div></section>'''


def cta(title, copy, url="book.html", label="Book a session"):
    return f'''
    <section class="section"><div class="wrap cta-panel">
      <div><h2>{title}</h2><p>{copy}</p></div>
      <a class="button" href="{url}">{label} <span aria-hidden="true">↗</span></a>
    </div></section>'''


def home():
    white_text, gold_text = SLOGAN.rsplit(" ", 1)
    return f'''
    <section class="hero" aria-labelledby="home-title">
      <div class="hero-media">{photo(9, '(max-width: 700px) 100vw, 65vw', eager=True, high=True)}</div>
      <div class="hero-shade"></div>
      <div class="wrap hero-inner">
        <p class="eyebrow"><span class="gold-rule"></span>San Francisco Bay Area</p>
        <h1 id="home-title">{white_text} <span>{gold_text}</span></h1>
        <p class="hero-description">Portraits, celebrations, and commercial photography.</p>
        <div class="actions">
          <a class="button" href="book.html">Book a session <span aria-hidden="true">↗</span></a>
          <a class="button button-ghost" href="portfolio.html">View portfolio</a>
        </div>
      </div>
    </section>
    <section class="section work-section"><div class="wrap">
      <div class="section-heading">
        <div><h2>Selected <em>photography.</em></h2></div>
        <a class="text-link" href="portfolio.html">View full portfolio <span aria-hidden="true">↗</span></a>
      </div>
      <div class="work-grid">
        <a class="work-tile" href="portfolio.html?category=studio">{photo(1, '(max-width: 700px) 45vw, 28vw')}<span>Studio Portraits <b aria-hidden="true">↗</b></span></a>
        <a class="work-tile" href="portfolio.html?category=editorial">{photo(3, '(max-width: 700px) 45vw, 28vw')}<span>Editorial <b aria-hidden="true">↗</b></span></a>
        <a class="work-tile wide" href="portfolio.html?category=engagements">{photo(14, '(max-width: 700px) 90vw, 45vw')}<span>Engagements <b aria-hidden="true">↗</b></span></a>
      </div>
    </div></section>
    <section class="section event-feature"><div class="wrap event-split">
      <div>{photo(14, "(max-width: 760px) 90vw, 48vw")}</div>
      <div class="event-copy">
        <p class="eyebrow">Events &amp; celebrations</p>
        <h2>Find your <em>photographs.</em></h2>
        <p>Looking for photographs from an event? Visit the event gallery page or ask the studio for your private gallery link.</p>
        <div class="actions">
          <a class="button" href="events.html">Event galleries</a>
          <a class="text-link" href="book.html?service=events&amp;package=custom">Book a photographer</a>
        </div>
      </div>
    </div></section>
    <section class="section session-section"><div class="wrap cta-panel">
      <div><h2>Find your session.</h2><p>Compare portrait packages or explore photography for an event, business, or special occasion.</p></div>
      <div class="actions">
        <a class="button" href="packages.html">View packages <span aria-hidden="true">↗</span></a>
        <a class="button button-ghost" href="services.html">Photography services</a>
      </div>
    </div></section>'''


def events():
    if GALLERY_URL:
        if GALLERY_URL not in (
            "https://enhancevisualstudio.smugmug.com",
            "https://gallery.enhancevisualstudio.com",
        ):
            raise ValueError("Use a verified EVS gallery host without a trailing slash.")
        gallery_actions = f"""
          <p>Explore public event galleries, browse the archive, or search for your event.</p>
          <div class="actions">
            <a class="button" href="{GALLERY_URL}/">Latest galleries</a>
            <a class="button button-ghost" href="{GALLERY_URL}/browse">Event archives</a>
            <a class="text-link" href="{GALLERY_URL}/search">Search galleries</a>
          </div>"""
    else:
        gallery_actions = f"""
          <p>Event galleries are being prepared. For an existing album or a private client link, contact the studio.</p>
          <a class="button" href="mailto:{EMAIL}?subject=Event%20gallery%20request">Request your gallery link</a>"""
    return f"""
    <section class="section"><div class="wrap event-split event-intro">
      <div class="event-copy">
        <p class="eyebrow">Event photography / Bay Area</p>
        <h1>Your moments.<br><em>Your photographs.</em></h1>
        {gallery_actions}
        <p class="event-contact"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <figure>{photo(10, "(max-width: 760px) 90vw, 48vw", eager=True, high=True)}
        <figcaption>Engagement photography by Enhance Visual Studio</figcaption>
      </figure>
    </div></section>
    {cta("Bring your next event into focus.", "Photography for celebrations, gatherings, and the moments in between.", "book.html?service=events&amp;package=custom", "Book a photographer")}"""


def services():
    group_links = "".join(
        f'<a href="#{SERVICE_ANCHORS[name]}">{escape(name)}</a>' for name in SERVICES
    )
    sections = []
    for name, entries in SERVICES.items():
        cards = []
        for slug, service, copy in entries:
            fixed_price = slug in PACKAGE_SERVICES
            query = "" if fixed_price else "&amp;package=custom"
            label = "Book a session" if fixed_price else "Request a Custom Quote"
            cards.append(f"""
            <article class="service-card">
              <h3>{escape(service)}</h3><p>{escape(copy)}</p>
              <a class="text-link" href="book.html?service={slug}{query}">{label} <span aria-hidden="true">↗</span></a>
            </article>""")
        sections.append(f"""
        <section class="section catalog-group" id="{SERVICE_ANCHORS[name]}"><div class="wrap">
          <div class="section-heading"><h2>{escape(name)}</h2></div>
          <div class="card-grid">{"".join(cards)}</div>
        </div></section>""")
    return (intro("San Francisco Bay Area", "Photography services.", "Choose a session or request a quote for specialty coverage.")
            + f'<nav class="wrap filter-bar" id="photography" aria-label="Photography categories">{group_links}</nav>'
            + "".join(sections))


def portfolio():
    labels = {
        "Portraits": "Portraits",
        "Studio": "Studio Photography",
        "Engagements": "Weddings & Engagements",
        "Editorial": "Fashion & Editorial",
    }
    available = {tag for photo_data in PHOTOS.values() for tag in photo_data[3:]}
    categories = ["All", *(name for name in labels if name in available)]
    filters = "".join(
        f'<button type="button" data-filter="{name.lower()}" aria-pressed="{str(name == "All").lower()}">{escape(labels.get(name, name))}</button>'
        for name in categories
    )
    figures = []
    for number in [9, 3, 1, 10, 11, 7, 14, 4, 8, 12, 2, 6, 13, 5]:
        tags = PHOTOS[number][3:]
        tag_keys = " ".join(tag.lower() for tag in tags)
        img = photo(number, "(max-width: 560px) 100vw, (max-width: 900px) 50vw, 33vw", eager=number in [9, 3, 1])
        figures.append(f'''
        <figure data-categories="{tag_keys}">
          <a class="gallery-image" href="images/{number}.jpg">{img}</a>
          <figcaption>{escape(" / ".join(labels.get(tag, tag) for tag in tags))}</figcaption>
        </figure>''')
    return intro("Selected work", "Photography portfolio.", "Studio, portrait, editorial and engagement photography by Enhance Visual Studio.") + f'''
    <section class="wrap" aria-label="Photographs">
      <div class="portfolio-gateway"><p>Looking for a complete event gallery?</p><a class="text-link" href="events.html">Find your event</a></div>
      <div class="filter-bar" id="gallery-filters" role="group" aria-label="Filter photographs" hidden>{filters}</div>
      <p id="gallery-count" class="gallery-count" role="status" hidden></p>
      <div class="gallery" id="gallery">{"".join(figures)}</div>
    </section>
    <dialog class="lightbox" aria-label="Full-size photograph">
      <div class="lightbox-tools">
        <p class="lightbox-count" role="status"></p>
        <button type="button" class="lightbox-close" autofocus>Close <span aria-hidden="true">×</span></button>
      </div>
      <div class="lightbox-image"><img alt=""></div>
      <div class="lightbox-controls">
        <button type="button" data-advance="-1" aria-label="Previous photograph">←</button>
        <button type="button" data-advance="1" aria-label="Next photograph">→</button>
      </div>
    </dialog>
    {cta("Plan your own session.", "Explore photography packages or tell us about a custom project.", "packages.html", "View packages")}'''


def packages():
    cards = []
    package_images = {"essential": 1, "signature": 7, "creative-campaign": 3}
    for slug, (name, price, label, inclusions) in PACKAGES.items():
        items = "".join(f"<li>{escape(item)}</li>" for item in inclusions)
        featured = ' class="package featured"' if slug == "signature" else ' class="package"'
        cards.append(f'''
        <article{featured}>
          <div class="package-photo">{photo(package_images[slug], "(max-width: 560px) 90vw, (max-width: 900px) 45vw, 30vw")}</div>
          <div class="package-body">
          <p class="eyebrow">{label}</p><h2>{name}</h2><p class="price">${price}</p><ul>{items}</ul>
          <a class="button{" button-ghost" if slug != "signature" else ""}" href="book.html?package={slug}">Request {name} <span aria-hidden="true">↗</span></a>
          </div>
        </article>''')
    return intro("Photography pricing", "Packages.", "Compare session time, locations and retouched images to find the right fit.", compact=True) + f'''
    <section class="section package-section"><div class="wrap card-grid">{"".join(cards)}</div></section>
    <div class="wrap package-links">
      <a class="text-link" href="policies.html">Booking policies <span aria-hidden="true">↗</span></a>
      <a class="text-link" href="services.html">All photography services <span aria-hidden="true">↗</span></a>
    </div>
    {cta("Specialty photography.", "Request a tailored quote for events, weddings, commercial photography, and other specialty sessions.", "book.html?package=custom", "Request a Custom Quote")}'''


def request_form(booking):
    kind = "booking" if booking else "contact"
    options = "".join(
        f'<optgroup label="{escape(group, quote=True)}">' + "".join(
            f'<option value="{slug}">{escape(name)}</option>' for slug, name, _ in entries
        ) + "</optgroup>"
        for group, entries in SERVICES.items()
    )
    pack_options = "".join(f'<option value="{slug}">{name} · ${price}</option>'
                           for slug, (name, price, _, _) in PACKAGES.items())
    booking_fields = f'''
      <label for="package">Package or quote</label>
      <select name="package" id="package" aria-describedby="package-note" required><option value="custom">Custom quote</option>{pack_options}</select>
      <p class="field-note" id="package-note">Photography package availability depends on the service. <a href="packages.html">Compare packages</a>.</p>
      <div class="form-grid">
        <div><label for="preferredDate">Preferred date <small>(optional)</small></label><input type="date" id="preferredDate" name="preferredDate"></div>
        <div><label for="alternateDate">Alternate date <small>(optional)</small></label><input type="date" id="alternateDate" name="alternateDate"></div>
      </div>
      <label for="location">Project location</label>
      <input id="location" name="location" maxlength="200" placeholder="City, venue, or to be determined" required>
''' if booking else ""
    return f'''
    <form class="request-form" data-kind="{kind}" hidden>
      <h2>{"Project details" if booking else "Send an inquiry"}</h2>
      <div class="form-grid">
        <div><label for="name">Full name</label><input id="name" name="name" autocomplete="name" maxlength="120" required></div>
        <div><label for="email">Email address</label><input type="email" id="email" name="email" autocomplete="email" maxlength="254" required></div>
      </div>
      <label for="service">Service</label>
      <select name="service" id="service" {"required" if booking else ""}><option value="">{"Choose a service" if booking else "General inquiry"}</option>{options}</select>
      {booking_fields}
      <label for="message">{"Tell us about your project" if booking else "Your message"}</label>
      <textarea id="message" name="message" rows="5" minlength="10" maxlength="3000" required></textarea>
      <div class="request-trap" aria-hidden="true"><label for="website">Leave this field empty</label><input id="website" name="website" tabindex="-1" autocomplete="off"></div>
      <button type="submit" class="button">{"Send booking request" if booking else "Send inquiry"} <span aria-hidden="true">↗</span></button>
      <p class="form-status" role="status" aria-live="polite"></p>
    </form>
    <noscript><p>To send a request with JavaScript disabled, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></noscript>'''


def inquiry(booking):
    title = "Book a session." if booking else "Contact the studio."
    description = ("Choose a photography service, share your preferred dates, and ask about availability."
                   if booking else "Ask about photography sessions, coverage, or availability.")
    extra = f'''<p>Dates remain tentative until the studio confirms availability and receives the required retainer.</p>
      <p><a class="text-link" href="policies.html">Booking policies <span aria-hidden="true">↗</span></a></p>''' if booking else '''
      <p>Based in the San Francisco Bay Area, California.</p>
      <p><a class="text-link" href="book.html">Start a booking request <span aria-hidden="true">↗</span></a></p>'''
    return intro("Project requests" if booking else "Get in touch", title, description) + f'''
    <section class="section"><div class="wrap inquiry-grid">
      <aside class="contact-card"><h2>{"Before you request" if booking else "Studio inquiries"}</h2>{extra}
      <p>{"If online submission is unavailable, email us your session type, dates, and location." if booking else "If online submission is unavailable, you can email the studio directly."}</p>
      <p><a class="text-link" href="mailto:{EMAIL}">{"Email a booking request" if booking else "Email the studio"}</a></p>
      <p><a href="mailto:{EMAIL}">{EMAIL}</a></p></aside>
      <div>{request_form(booking)}</div>
    </div></section>'''


def build_smugmug_customization(site_origin=SITE):
    if site_origin not in (PREVIEW_ORIGIN, SITE):
        raise ValueError("Use the EVS preview or production origin for SmugMug links.")
    folder = ROOT / "smugmug"
    folder.mkdir(exist_ok=True)
    nav = []
    for url, label in NAV:
        target = "/" if url == "events.html" else site_origin + ("/" if url == "index.html" else "/" + Path(url).stem)
        nav.append(f'<a href="{target}">{label}</a>')
    nav.append(f'<a class="evs-button" href="{site_origin}/book">Book a Session</a>')
    navigation = '<nav class="evs-gallery-nav" aria-label="Primary">' + "".join(nav) + "</nav>\n"
    footer = f"""<footer class="evs-gallery-footer">
  <div><p class="evs-footer-name">Enhance Visual Studio</p><p>{SLOGAN}</p><p>San Francisco Bay Area, California</p></div>
  <div><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="tel:{PHONE}" aria-label="Call Enhance Visual Studio at {PHONE_DISPLAY}">{PHONE_DISPLAY}</a></div>
  <nav aria-label="Social media">{"".join(f'<a href="{url}">{name}</a>' for name, url in SOCIALS)}</nav>
  <p><a href="{site_origin}/">Main website</a> · <a href="{site_origin}/book">Book a Photographer</a> · <a href="{site_origin}/policies">Booking policies</a></p>
  <p class="evs-copyright">{COPYRIGHT}</p>
</footer>\n"""
    intro = f"""<section class="evs-gallery-intro">
  <p class="evs-eyebrow">Enhance Visual Studio · Bay Area photography</p>
  <h1>Event <span>galleries.</span></h1>
  <p>{SLOGAN}</p>
</section>\n"""
    for name, content in (("navigation.html", navigation), ("home-intro.html", intro), ("footer.html", footer)):
        (folder / name).write_text(content, encoding="utf-8")


def build(smugmug_site_origin=SITE):
    build_smugmug_customization(smugmug_site_origin)
    page("404.html", "Page Not Found", "Find your way back to Enhance Visual Studio photography.",
         intro("404", "Page not found.", "The page you’re looking for is unavailable. Explore our photography or contact the studio.") +
         cta("Find your next session.", "Browse our work or tell us what you’d like photographed.", "/index.html", "Return home"),
         noindex=True)
    page("index.html", "Bay Area Photography Studio",
         f"Bay Area portraits, studio sessions, weddings, events, headshots, and commercial photography by Enhance Visual Studio. {SLOGAN}", home())
    page("events.html", "Event Photography & Galleries", "Find your Enhance Visual Studio event gallery or request a private photography gallery link.", events())
    page("services.html", "Photography Services", "Explore Bay Area portrait, wedding, event, headshot, branding, and commercial photography.", services())
    page("portfolio.html", "Photography Portfolio", "Browse studio portraits, editorial photography and engagement imagery by Enhance Visual Studio.", portfolio())
    page("about.html", "About the Studio", "Meet Enhance Visual Studio, a Bay Area photography studio for portraits, celebrations, and commercial work.",
         intro(SLOGAN, "About the studio.", "Enhance Visual Studio is based in the San Francisco Bay Area.") + f'''
         <section class="section"><div class="wrap about-grid">
           <div>{photo(2, "(max-width: 760px) 100vw, 44vw")}</div>
           <div><h2>Photography with direction.</h2><p>We photograph portraits, milestones, and commercial work in the studio and on location. Sessions start with a conversation about the people, the setting, and how you’ll use your images.</p>
           <p>We guide posing and lighting and leave room for the candid moments that make a session yours.</p>
           <a class="text-link" href="services.html">Explore photography services <span aria-hidden="true">↗</span></a></div>
         </div></section>{cta("Plan a photography session.", "Tell us what you’d like photographed.")}''')
    page("packages.html", "Photography Packages & Pricing", "Compare Essential, Signature and Creative Campaign photography packages from Enhance Visual Studio.", packages())
    page("book.html", "Book a Photography Session", "Request a Bay Area photography session or a custom quote from Enhance Visual Studio.", inquiry(True))
    page("contact.html", "Contact", "Contact Enhance Visual Studio for photography and session inquiries in the San Francisco Bay Area.", inquiry(False))
    policy_cards = "".join(f'<article class="service-card"><h2>{name}</h2><p>{copy}</p></article>' for name, copy in POLICIES)
    page("policies.html", "Booking Policies", "Read Enhance Visual Studio’s photography booking and delivery policies.",
         intro("Photography sessions", "Booking policies.", "Review retainers, scheduling, delivery and creative direction before reserving your session.") +
         f'<section class="section"><div class="wrap card-grid policy-grid">{policy_cards}</div></section>' +
         cta("Planning a photography session?", "Compare packages and select a session that fits your project.", "packages.html", "View packages"))

    catalog = {
        "services": {slug: name for entries in SERVICES.values() for slug, name, _ in entries},
        "packages": {"custom": "Custom quote", **{slug: f"{name} · ${price}" for slug, (name, price, _, _) in PACKAGES.items()}},
        "packageServices": PACKAGE_SERVICES,
    }
    (ROOT / "assets" / "booking-catalog.mjs").write_text(
        "// Generated by tools/build_site.py.\nexport const catalog = " + json.dumps(catalog, indent=2, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    urls = ["", "events.html", "services.html", "portfolio.html", "about.html",
            "packages.html", "book.html", "contact.html", "policies.html"]
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{SITE}/{Path(url).stem}</loc></url>\n" for url in urls)
        + "</urlset>\n", encoding="utf-8"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--smugmug-site-origin",
        choices=(PREVIEW_ORIGIN, SITE),
        default=SITE,
        help="Main website origin used in SmugMug snippets. Defaults to the production website.",
    )
    args = parser.parse_args()
    build(smugmug_site_origin=args.smugmug_site_origin)
