"""Generate the static pages and browser/Worker booking catalog from shared content."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.enhancevisualstudio.com"
EMAIL = "hello@enhancevisualstudio.com"
PHONE = "+13233271806"
PHONE_DISPLAY = "(323) 327-1806"
SOCIALS = [
    ("Instagram", "https://instagram.com/enhancevisualstudio"),
    ("TikTok", "https://tiktok.com/@enhancevisualstudio"),
    ("YouTube", "https://youtube.com/@enhancevisualstudio"),
    ("Facebook", "https://facebook.com/enhancevisualstudio"),
]
SERVICES = {
    "Photography": [
        ("portraits", "Portraits", "Individual portraits with guided posing, considered lighting and room for your personality."),
        ("studio", "Studio Photography", "Controlled lighting and backdrops for clean or expressive studio imagery."),
        ("headshots", "Professional Headshots", "Approachable, polished images for profiles, teams and professional use."),
        ("branding", "Personal Branding", "A coordinated set of portraits and lifestyle images for your website, launches and social channels."),
        ("weddings", "Weddings & Engagements", "Portraits and candid photography shaped around the people and moments that matter to you."),
        ("events", "Events & Celebrations", "Coverage of the setting, guests and key moments of your celebration."),
        ("family", "Family & Maternity", "Guided portraits with space for the spontaneous moments in between."),
        ("graduation", "Graduation Photography", "A portrait session to mark your graduation, with room for campus locations and regalia."),
        ("food", "Food & Restaurant Photography", "Menu, ingredient and dining-room imagery that reflects the character of your restaurant."),
        ("product", "Product & Commercial Photography", "Product details, styled scenes and campaign-ready photography shaped around your brief."),
        ("real-estate", "Real Estate & Architectural Photography", "Interior, exterior and detail photographs that communicate how a space looks and feels."),
    ],
    "Videography": [
        ("wedding-films", "Wedding Films", "A film built around the people, atmosphere and meaningful moments of your day."),
        ("event-video", "Event Videos", "Event coverage and edited highlights for sharing after the day."),
        ("promotional-video", "Promotional Videos", "A focused film for an offer, launch or upcoming event."),
        ("commercial-video", "Commercial Productions", "Video production shaped around the brief, audience and deliverables of your campaign."),
        ("social-video", "Social Media Content", "Short-form footage and edits framed for the channels where you plan to publish."),
        ("brand-film", "Brand Storytelling", "A film that brings your people, process and purpose into view."),
    ],
    "Graphic design": [
        ("logo", "Logo Design", "A visual mark developed around your name, audience and intended uses."),
        ("flyer", "Flyer Design", "A clear, visually cohesive layout for an event, promotion or announcement."),
        ("poster", "Poster Design", "A display-led composition that makes the message legible at a glance."),
        ("identity", "Brand Identity", "A coordinated visual system for how your business appears across touchpoints."),
        ("promo-graphics", "Promotional Graphics", "Campaign artwork shaped around your message and publishing formats."),
        ("social-design", "Social Media Creative Assets", "Graphics and templates sized for social channels and consistent with your brand."),
    ],
}
GROUPS = {
    "Photography": ("photography", "Portraits, people & places"),
    "Videography": ("videography", "Stories in motion"),
    "Graphic design": ("design", "Identity & campaigns"),
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
}
NAV = [
    ("services.html", "Services"), ("portfolio.html", "Portfolio"), ("about.html", "About"),
    ("packages.html", "Packages"), ("contact.html", "Contact"),
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


def page(path, title, description, content):
    canonical = f"{SITE}/{'' if path == 'index.html' else path}"
    current = ' aria-current="page"'
    links = "".join(
        f'<a href="{url}"{current if path == url else ""}>{label}</a>'
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
        "telephone": PHONE,
        "image": SITE + "/images/display/9-960.jpg",
        "slogan": "Pose. Capture. Enhance.",
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
  <meta name="description" content="{escape(description, quote=True)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Enhance Visual Studio">
  <meta property="og:title" content="{escape(title, quote=True)} | Enhance Visual Studio">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/images/display/9-960.jpg">
  <meta property="og:image:alt" content="{escape(PHOTOS[9][2], quote=True)}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="assets/evs-icon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&amp;family=Manrope:wght@400;500;600;700;800&amp;display=swap">
  <link rel="stylesheet" href="style.css">
  <script type="application/ld+json">{schema}</script>
  <script type="module" src="script.js"></script>
</head>
<body>
  <div class="site-scroll">
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap header-row">
      <a class="brand" href="index.html" aria-label="Enhance Visual Studio home">
        <span class="monogram" aria-hidden="true">EV</span>
        <span class="wordmark">Enhance<span>Visual Studio</span></span>
      </a>
      <button class="menu-button" type="button" aria-controls="site-nav" aria-expanded="false" hidden>Menu <span aria-hidden="true">☰</span></button>
      <nav class="site-nav" id="site-nav" aria-label="Primary">
        {links}
        <a class="button button-small" href="book.html"{booking_current}>Book a project <span aria-hidden="true">↗</span></a>
      </nav>
    </div>
  </header>
  <main id="main" tabindex="-1">
{content}
  </main>
  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div><p class="footer-name">Enhance Visual Studio</p><p>Pose. Capture. Enhance.</p><p>San Francisco Bay Area, California</p></div>
        <div>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
          <div><a href="tel:{PHONE}">{PHONE_DISPLAY}</a></div>
          <div class="footer-links">{socials}</div>
        </div>
        <div class="footer-links"><a href="book.html">Book a project</a><a href="policies.html">Booking policies</a></div>
      </div>
      <p class="copyright">© 2026 Enhance Visual Studio</p>
    </div>
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


def intro(label, title, description):
    return f'''
    <section class="page-heading"><div class="wrap">
      <p class="eyebrow">{label}</p>
      <h1>{title}</h1>
      <p class="lede">{description}</p>
    </div></section>'''


def cta(title, copy, url="book.html", label="Book a project"):
    return f'''
    <section class="section"><div class="wrap cta-panel">
      <div><h2>{title}</h2><p>{copy}</p></div>
      <a class="button" href="{url}">{label} <span aria-hidden="true">↗</span></a>
    </div></section>'''


def home():
    disciplines = "".join(
        f'<a href="services.html#{key}"><span><strong>{name}</strong><small>{subtitle}</small></span>'
        '<span class="arrow" aria-hidden="true">↗</span></a>'
        for name, (key, subtitle) in GROUPS.items()
    )
    return f'''
    <section class="hero" aria-labelledby="home-title">
      <div class="hero-media">{photo(9, '(max-width: 700px) 100vw, 65vw', eager=True, high=True)}</div>
      <div class="hero-shade"></div>
      <div class="wrap hero-inner">
        <p class="eyebrow"><span class="gold-rule"></span>San Francisco Bay Area</p>
        <h1 id="home-title">Pose. Capture. <span>Enhance.</span></h1>
        <p class="hero-description">Photography, videography and graphic design for the people, moments and brands worth remembering.</p>
        <div class="actions">
          <a class="button" href="portfolio.html">Explore the work <span aria-hidden="true">↗</span></a>
          <a class="button button-ghost" href="book.html">Book a project</a>
        </div>
      </div>
    </section>
    <div class="discipline-rail"><div class="wrap disciplines">{disciplines}</div></div>
    <section class="section work-section"><div class="wrap">
      <div class="section-heading">
        <div><p class="eyebrow">The portfolio</p><h2>Selected <em>photography.</em></h2></div>
        <a class="text-link" href="portfolio.html">View full portfolio <span aria-hidden="true">↗</span></a>
      </div>
      <div class="work-grid">
        <a class="work-tile" href="portfolio.html?category=studio">{photo(1, '(max-width: 700px) 45vw, 28vw')}<span>Studio Portraits <b aria-hidden="true">↗</b></span></a>
        <a class="work-tile" href="portfolio.html?category=editorial">{photo(3, '(max-width: 700px) 45vw, 28vw')}<span>Editorial <b aria-hidden="true">↗</b></span></a>
        <a class="work-tile wide" href="portfolio.html?category=engagements">{photo(10, '(max-width: 700px) 90vw, 45vw')}<span>Engagements <b aria-hidden="true">↗</b></span></a>
      </div>
    </div></section>
    <section class="section studio-note"><div class="wrap studio-grid">
      <div><p class="eyebrow">About the studio</p><h2>Creative direction.<br><em>Personal focus.</em></h2></div>
      <div><p>Enhance Visual Studio brings photography, film and design together. Whether you’re planning a portrait session, documenting a celebration or shaping a brand, the work starts with where the images will live and what you want them to say.</p>
      <a class="text-link" href="about.html">Meet the studio <span aria-hidden="true">↗</span></a></div>
    </div></section>
    {cta('What are you creating?', 'Tell us what you have in mind and when you’d like to get started.')}'''


def services():
    group_links = "".join(f'<a href="#{GROUPS[name][0]}">{name}</a>' for name in SERVICES)
    sections = []
    destination = {
        "photography": ("portfolio.html", "Explore photography"),
        "videography": ("videography.html", "Visit the film showcase"),
        "design": ("design.html", "Visit the design portfolio"),
    }
    for name, entries in SERVICES.items():
        key, tag = GROUPS[name]
        url, label = destination[key]
        cards = "".join(
            f'''<article class="service-card"><h3>{escape(service)}</h3><p>{escape(copy)}</p>
              <a class="text-link" href="book.html?service={slug}">Request {escape(service.lower())} <span aria-hidden="true">↗</span></a></article>'''
            for slug, service, copy in entries
        )
        sections.append(f'''
        <section class="section catalog-group" id="{key}"><div class="wrap">
          <div class="section-heading"><div><p class="eyebrow">{escape(tag)}</p><h2>{name}</h2></div>
          <a class="text-link" href="{url}">{label} <span aria-hidden="true">↗</span></a></div>
          <div class="card-grid">{cards}</div>
        </div></section>''')
    return (intro("What we do", "Studio services.", "Guided sessions, moving images and original design for personal and commercial projects.")
            + f'<nav class="wrap filter-bar" aria-label="Service categories">{group_links}</nav>'
            + "".join(sections))


def portfolio():
    categories = ["Studio", "Portraits", "Editorial", "Engagements"]
    filters = "".join(
        f'<button type="button" data-filter="{name.lower()}" aria-pressed="{str(name == "All").lower()}">{name}</button>'
        for name in ["All", *categories]
    )
    figures = []
    for number in [9, 3, 1, 10, 7, 4, 8, 2, 6, 5]:
        tags = PHOTOS[number][3:]
        tag_keys = " ".join(tag.lower() for tag in tags)
        img = photo(number, "(max-width: 560px) 100vw, (max-width: 900px) 50vw, 33vw", eager=number in [9, 3, 1])
        figures.append(f'''
        <figure data-categories="{tag_keys}">
          <a class="gallery-image" href="images/{number}.jpg">{img}</a>
          <figcaption>{" / ".join(tags)}</figcaption>
        </figure>''')
    return intro("Selected work", "Photography portfolio.", "Studio, portrait, editorial and engagement photography by Enhance Visual Studio.") + f'''
    <section class="wrap" aria-label="Photographs">
      <div class="filter-bar" id="gallery-filters" aria-label="Filter photographs" hidden>{filters}</div>
      <p id="gallery-count" class="sr-only" role="status"></p>
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


def showcase(group, label, headline, description, empty_copy):
    key = GROUPS[group][0]
    listing = "".join(
        f'<li><a href="book.html?service={slug}">{escape(name)} <span aria-hidden="true">↗</span></a></li>'
        for slug, name, _ in SERVICES[group]
    )
    return intro(label, headline, description) + f'''
    <section class="section"><div class="wrap feature-grid">
      <div class="empty-showcase"><h2>Portfolio availability</h2><p>{empty_copy}</p><a class="text-link" href="contact.html">Contact the studio <span aria-hidden="true">↗</span></a></div>
      <div><h2>Explore by project</h2><ul class="link-list">{listing}</ul><a class="text-link" href="services.html#{key}">See service details <span aria-hidden="true">↗</span></a></div>
    </div></section>'''


def packages():
    cards = []
    for slug, (name, price, label, inclusions) in PACKAGES.items():
        items = "".join(f"<li>{escape(item)}</li>" for item in inclusions)
        featured = ' class="package featured"' if slug == "signature" else ' class="package"'
        cards.append(f'''
        <article{featured}>
          <p class="eyebrow">{label}</p><h2>{name}</h2><p class="price">${price}</p><ul>{items}</ul>
          <a class="button{" button-ghost" if slug != "signature" else ""}" href="book.html?package={slug}">Request {name} <span aria-hidden="true">↗</span></a>
        </article>''')
    return intro("Photography pricing", "Packages.", "Compare session time, locations and retouched images to find the right fit.") + f'''
    <section class="section"><div class="wrap card-grid">{"".join(cards)}</div></section>
    <div class="wrap"><a class="text-link" href="policies.html">Read the booking policies <span aria-hidden="true">↗</span></a></div>
    {cta("Have a different brief?", "Request custom pricing for other photography, videography and design projects.", "book.html?package=custom", "Request a quote")}'''


def request_form(booking):
    kind = "booking" if booking else "contact"
    options = "".join(
        f'<optgroup label="{group}">' + "".join(
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
      <input id="location" name="location" maxlength="200" placeholder="City, venue, remote, or to be determined" required>
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
    title = "Book a project." if booking else "Contact the studio."
    description = ("Tell us what you’re planning and share your preferred dates. The studio will follow up about availability and next steps."
                   if booking else "Reach out about a project, collaboration or general question.")
    extra = f'''<p>Dates remain tentative until the studio confirms availability and receives the required retainer.</p>
      <p><a class="text-link" href="policies.html">Booking policies <span aria-hidden="true">↗</span></a></p>''' if booking else '''
      <p>Based in the San Francisco Bay Area, California.</p>
      <p><a class="text-link" href="book.html">Start a booking request <span aria-hidden="true">↗</span></a></p>'''
    return intro("Project requests" if booking else "Get in touch", title, description) + f'''
    <section class="section"><div class="wrap inquiry-grid">
      <aside class="contact-card"><h2>{"Before you request" if booking else "Studio inquiries"}</h2>{extra}
      <p><a href="mailto:{EMAIL}">{EMAIL}</a></p></aside>
      <div>{request_form(booking)}</div>
    </div></section>'''


def build():
    page("index.html", "Bay Area Photography, Videography & Graphic Design",
         "Enhance Visual Studio offers photography, videography and graphic design in the San Francisco Bay Area. Pose. Capture. Enhance.", home())
    page("services.html", "Creative Services", "Explore studio photography, videography and graphic design services from Enhance Visual Studio.", services())
    page("portfolio.html", "Photography Portfolio", "Browse studio portraits, editorial photography and engagement imagery by Enhance Visual Studio.", portfolio())
    page("videography.html", "Videography Showcase", "Explore wedding films, event videos, promotions and brand storytelling services.", showcase(
        "Videography", "Film & motion", "Videography showcase.", "Explore film services for weddings, events and brands.",
        "There are no films published here yet. Contact the studio to ask about examples relevant to your project."))
    page("design.html", "Creative Design Portfolio", "Explore logo, brand identity, poster, flyer and social media design services.", showcase(
        "Graphic design", "Visual identity", "Creative design portfolio.", "Explore graphic design for identities, campaigns and social channels.",
        "There are no design projects published here yet. Contact the studio to discuss the visual direction for your project."))
    page("about.html", "About the Studio", "Meet Enhance Visual Studio, a Bay Area photography, videography and graphic design studio.",
         intro("Pose. Capture. Enhance.", "About the studio.", "A Bay Area studio for photography, videography and graphic design.") + f'''
         <section class="section"><div class="wrap about-grid">
           <div>{photo(2, "(max-width: 760px) 100vw, 44vw")}</div>
           <div><h2>From idea to image.</h2><p>The studio works across portraits, celebrations, commercial imagery and visual identity. We begin with a conversation about the people, purpose and setting, then shape the direction around what the work needs to do.</p>
           <p>For photography, that can mean guidance on posing, lighting and the location. For film and design, it starts with the story, the audience and where the finished work will appear.</p>
           <a class="text-link" href="services.html">Explore studio services <span aria-hidden="true">↗</span></a></div>
         </div></section>{cta("Let’s talk about your project.", "Share your idea and tell us what you need.")}''')
    page("packages.html", "Photography Packages & Pricing", "Compare Essential, Signature and Creative Campaign photography packages from Enhance Visual Studio.", packages())
    page("book.html", "Book a Project", "Send a photography, videography or design booking request directly to Enhance Visual Studio.", inquiry(True))
    page("contact.html", "Contact", "Contact Enhance Visual Studio for creative projects and general inquiries in the San Francisco Bay Area.", inquiry(False))
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
    urls = ["", "services.html", "portfolio.html", "videography.html", "design.html", "about.html",
            "packages.html", "book.html", "contact.html", "policies.html"]
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{SITE}/{url}</loc></url>\n" for url in urls)
        + "</urlset>\n", encoding="utf-8"
    )


if __name__ == "__main__":
    build()
