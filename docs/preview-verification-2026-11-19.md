# EVS free hybrid preview verification — November 19, 2026

Repository: EnhanceVisualStudio/enhancevisualstudio-site. Branch:
codex/evs-redesign. Runtime checkpoint tested: e755c28.
Preview: https://codex-evs-redesign.enhancevisualstudio-site.pages.dev/.

## Main website and bookings

All nine public pages plus the deep-path 404 passed 40 live responsive checks
at 320/390/768/1440 px. Another 45 local header/footer checks covered 1080 px.
All 14 portfolio photographs, five filters, keyboard lightbox controls, 15
photography service selections, package compatibility and approved $200/$350/$550
prices were checked. The official logo, exact Pose. Click. Enhance slogan,
centered copyright and Call Now link are preserved. Main-site navigation
exposes no private SmugMug trial links.

The private preview Worker and Pages preview service binding processed real
booking and contact forms. Studio receipt, recipient, Reply-To, domain signing
and TLS were verified in the authorized studio mailbox. The initial contact
tests were classified as Spam. An EVS-only incoming-mail filter now prevents
that classification for the configured studio sender, hello recipient and
notification subject phrase. A subsequent contact test arrived in Inbox.
No forwarding, archiving, deletion or automatic customer replies were added.

Live validation rejected foreign origin, bad content type, oversized data,
invalid email/service/package/date, honeypot and malformed JSON. Native
approximate rate limiting returned 429 with a 60-second retry instruction.
Local tests passed 54 backend/adapter checks and 12 mocked frontend cases,
including uncertain response and timeout handling. No customer date is booked
or confirmed automatically.

Preview static responses carry noindex and security headers; missing URLs
return the branded 404. Canonical metadata, descriptions, structured data,
assets and internal navigation were checked. The existing main domain has
valid HTTPS. The future gallery subdomain remains inactive.

Local unthrottled homepage measurements: mobile LCP 300 ms / CLS 0; desktop
LCP 272 ms / CLS 0.00125, with no observed long tasks. These are local lab
estimates, not production field Core Web Vitals or a Lighthouse score.

## SmugMug and Lightroom

The existing Luna design remains published within the private trial. Entire
Site branding and navigation are inherited by folders and galleries. The
native platform/legal footer remains intact below the shared content, with
the required centered copyright row at the bottom.

Fourteen approved portfolio originals remain in their three native galleries.
Public Events / 2026 and Client Delivery are organized separately. EVS Public
Event, EVS Private Client and EVS Portfolio presets and EVS Proof watermark
are saved. Private access/password/invitation settings remain per-gallery;
downloads and visitor sales are disabled. No sales pricing is activated.

Official SmugMug plug-in 3.5.19.1 is enabled and authorized in Lightroom Classic
16.0.1. JPEG quality 90, sRGB, full dimensions, no video, removal of person/location
information and native SmugMug watermarking are configured. Three existing
website-photo copies were bulk published, then republished in place to the
Private (Only Me) EVS Publishing Check gallery. The same three image identities
were preserved. Existing catalog photographs and original files were untouched.

An owner-only local backup outside every website root contains customization,
branding, 14 originals, native settings, the official plug-in archive, Git
checkpoints and checksums. It excludes credentials and Lightroom catalogs.

## Deferred by owner instruction

- SmugMug subscription purchase and public gallery activation.
- Gallery DNS/custom hostname activation and signed-out privacy/download tests.
- Production Worker/binding configuration and the main-site release, subject
  to explicit owner approval. Main remains at d12d057.

No subscription or paid service was activated. No DNS, production deployment,
Enhance My Ride repository or Enhance My Ride infrastructure was changed.
