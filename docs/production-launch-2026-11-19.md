# Enhance Visual Studio production launch — November 19, 2026

The owner explicitly approved this release. The reviewed redesign was merged
into main and deployed to https://www.enhancevisualstudio.com from
EnhanceVisualStudio/enhancevisualstudio-site. Initial release commit:
8a8b7de295aafb8c2bc11b5f654e6bd7c82fd603. Initial production deployment:
da4bda6c-b1de-4546-a13f-2afb544317d4. Later verification-only documentation
commits preserve the same website and booking implementation.

## Production verification

- All nine pages return HTTP 200; deep missing URLs return the branded 404.
  HTTPS works on www and the existing apex domain redirects to www.
- Mobile/tablet/desktop checks cover 320, 390, 768 and 1440 px. The official
  logo remains centered above navigation, with the collapsible mobile menu.
  Pose. Click. Enhance is exact, and the centered bottom copyright is
  ©2026 Enhance Visual Studio - All Rights Reserved.
- Fourteen photographs, all gallery filters, full-size viewing, keyboard
  navigation, close controls and original proportions were checked. Fifteen
  photography services and the approved $200/$350/$550 package choices remain.
  The safe-area-aware Call Now button uses tel:+13233271806 and stays in its
  own reserved viewport row so it cannot cover forms or page controls.
- Descriptions, canonical/OG metadata, structured data, sitemap, robots,
  internal navigation, assets and indexability were checked on production.
  The nine content pages have no unintended noindex; the 404 is noindex.
- GET /api/inquiry returns JSON 405 with Allow: POST. Controlled live booking
  and contact forms returned 200 and their actual notifications were found
  in the authorized studio mailbox, without a spam warning. The booking
  email preserved the Essential $200 selection and preferred date. The
  contact email recipient, Reply-To, studio-domain signature and TLS were
  verified. These tests did not request a real session.
- Foreign-origin, invalid-email, honeypot and incompatible-package requests
  were rejected with accurate JSON errors and Cache-Control: no-store.
  Preview rate-limit testing and local 54-backend/12-form regression checks
  remain valid for the unchanged implementation.

The production private Worker is enhance-visual-studio-inquiries, through the
Pages Production INQUIRY_WORKER service binding. It uses only the two EVS
HTTPS origins, its own namespace 49127531, the verified fixed studio
notification destination and secure sender secret. Preview retains its own
Worker, namespace 49127532 and exact branch origin. There is no customer
auto-email or automatic date reservation.

## SmugMug remains private

The existing Luna design was updated only for production link destinations:
global logo, native menu, shared footer and homepage booking CTA. Homepage,
Public Events / 2026 and the private publishing-check gallery were verified
with one shared logo/menu, matching footer and intact native legal controls.
Signed-out SmugMug access still returns the private-trial 404. The main site
has GALLERY_URL unset and exposes no inaccessible gallery links. Subscription
purchase, public gallery activation and gallery DNS remain postponed.

## Rollback and restoration

The prelaunch checkpoint remains d12d0571431389b8851abc7db84249f6ee759392,
Cloudflare deployment 391cf752-af34-44b2-93ea-a9a81c1cfd20. Its source bundle,
local rollback tag, homepage snapshot and non-secret configuration metadata
are preserved in ~/Documents/Enhance Visual Studio Backups/2026-11-19-production-launch/.
The same folder contains current branding/customization, original photographs,
verification reports, restoration instructions and checksums. Credentials,
OAuth material and Lightroom catalogs are excluded.

Use the supported Pages rollback to restore that successful deployment if a
critical release check fails. Restore the prior production binding separately;
keep preview and the private Workers intact. The old deployment predates the
new booking adapter and branded 404, so verify it against its saved baseline.

No paid service or subscription was activated, no DNS record was changed,
and no Enhance My Ride resource or repository was modified.
