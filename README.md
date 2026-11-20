# Enhance Visual Studio website

Cloudflare Pages project `enhancevisualstudio-site` serves the GitHub repository
`EnhanceVisualStudio/enhancevisualstudio-site`. The production branch is `main`.
Booking and contact both POST to the same-origin `/api/inquiry` route. The Pages
Function forwards to a private EVS Worker through `INQUIRY_WORKER`. The Worker
owns validation, rate limiting and fixed-recipient notifications through the
Cloudflare send_email binding.

## Maintain and test locally

- Edit shared menus, page copy, services, packages, policies and the photography
  inventory in `tools/build_site.py`. Run `python3 tools/build_site.py` and
  commit the generated HTML, sitemap and browser booking catalog.
- Add portfolio JPEGs under `images/`, then add the dimensions, factual alt
  text and category to `PHOTOS` and its position to `portfolio()`. With Pillow
  9.1+ installed, run `python3 -B tools/build_images.py`, then regenerate the
  HTML. The gallery opens the originals.
- Run `python3 -m http.server 8000` for static preview. It serves the forms
  without a function runtime. Test the adapter and Worker with mock bindings
  or use Wrangler local simulation. Never use a real mail binding in local tests.
- Run `node tests/inquiry.mjs` for the 54 Worker and Pages adapter checks.
  With the local server running on port 8000, run `node tests/forms.cjs` for
  12 mocked booking/contact submissions, including invalid responses and
  timeouts. The form tests need Playwright installed or its absolute module
  path in `EVS_PLAYWRIGHT_MODULE`. Set `EVS_CHROME_EXECUTABLE` when using an
  existing Chrome installation. Both suites use mocked delivery.

## Current free preview configuration

The EVS preview uses the existing account's verified Email Routing destination.
Cloudflare supports free sending to verified account destinations, including
accounts configured only for Email Routing. The EMAIL binding restricts each
notification to hello@enhancevisualstudio.com. This setup stays within the
free plan and the existing DNS configuration. [Verified-destination pricing](https://developers.cloudflare.com/email-service/platform/pricing/)
[Fixed-recipient bindings](https://developers.cloudflare.com/email-service/configuration/send-bindings/)

The following preview configuration is in place. End-to-end receipt passed the
checks recorded below.

- Private Worker enhance-visual-studio-inquiries-preview is deployed with its
  preview rate-limit binding and exact preview origin allowlist.
- hello@enhancevisualstudio.com is verified as an Email Routing destination.
  BOOKING_FROM is configured as a Worker secret.
- The Pages Preview environment has INQUIRY_WORKER bound to that private Worker.
  Its branch alias is
  https://codex-evs-redesign.enhancevisualstudio-site.pages.dev.
- The temporary provisioning token has only Workers Scripts Edit, Pages Edit,
  and Email Routing Addresses Edit permissions in the authorized EVS account.
  It is stored outside the repository with mode 0600 and expires on
  November 26, 2026. Renew or replace it through the owner's account when needed.
  Its expiry affects administration, not the running Worker or notification binding.
  Keep token values, verification links and private configuration out of commits.
- Preview remains isolated from the production Worker and its rate-limit namespace.

When updating the preview Worker, verify the EVS account, the preview Worker
name and its preview bindings before using
`npx wrangler deploy --config worker/wrangler.toml --env preview`.
Manage BOOKING_FROM through the Worker secret interface. Preview service-binding
changes require a new Pages preview deployment. Push the reviewed redesign
commit only to codex/evs-redesign and verify that commit under Pages Deployments.

### Verified preview — November 19, 2026

Runtime changes at e755c28 passed the following checks on the branch alias:

- Nine pages and the branded deep-path 404 passed 40 responsive checks at
  320, 390, 768 and 1440 px. Gallery filters, keyboard lightbox navigation,
  all 15 photography services, approved package choices, mobile menus,
  centered branding/copyright and the floating call link work.
- GET /api/inquiry returns JSON 405 with Allow: POST. Valid booking/contact
  forms return JSON 200 only after the email service accepts the notification.
  Both notifications were received in the actual studio mailbox. Recipient,
  Reply-To, EVS-domain signing and TLS were verified in Gmail.
- Gmail initially classified contact tests as Spam. A studio-mailbox filter
  now matches only the configured EVS sender, hello@enhancevisualstudio.com,
  and the subject phrase "New Enhance Visual Studio", with Never send it to
  Spam as its only incoming action. The final contact test reached Inbox.
  The filter does not archive, forward, delete or auto-reply to messages.
- Foreign origin, incorrect content type, oversized body, invalid email,
  unknown service, incompatible package, invalid date, honeypot and malformed
  JSON were rejected. The live rate limiter returned 429 and Retry-After: 60.
  Its six-per-minute threshold is approximate per Cloudflare location, so a
  brief burst can exceed six while counters synchronize.
- Local suites passed 54 Worker/adapter checks and 12 mocked form cases.
  Delivery errors/timeouts retain entered details, restore the submit button
  and show the studio email fallback, without automatic retries.
- API responses use Cache-Control: no-store. Preview static pages have noindex
  and the configured security headers. Deep missing URLs return a styled 404
  with working root-relative links. No inaccessible gallery links are exposed.

A website success means Cloudflare accepted the studio notification. Dates
remain subject to studio approval and the existing retainer policy. This flow
sends no automatic customer email and does not reserve a date. Check Inbox and
Spam during routine operation; mailbox classification remains provider-controlled.

## Production release — launched November 19, 2026

The owner explicitly approved the completed production launch. Live verification
is recorded in [the release report](docs/production-launch-2026-11-19.md).
The production target is
https://www.enhancevisualstudio.com, with enhancevisualstudio.com retained as an
existing domain. GitHub main is the automatic Pages production branch.

The production booking Worker is enhance-visual-studio-inquiries, configured by
the default section of worker/wrangler.toml. Its exact origin allowlist contains
only the www and apex EVS HTTPS origins. It has its own rate-limit namespace,
the verified fixed studio email destination and BOOKING_FROM secret. The Pages
Production INQUIRY_WORKER binding targets that Worker. Preview keeps its
separate Worker, origin allowlist and namespace.

Before each release, verify the repository, branch, release commit, account,
Worker target and environment without printing secrets. Deploy the production
Worker with `npx wrangler deploy --config worker/wrangler.toml --env ""` and
manage BOOKING_FROM through the secure secret interface. Merge the reviewed
release into main to trigger the buildless Pages deployment. Verify the actual
production deployment commit and controlled inbox delivery after deployment.
The output must include the generated HTML, 404.html, _headers, _routes.json
and the project-root functions directory.

The prelaunch production checkpoint is d12d0571431389b8851abc7db84249f6ee759392,
Cloudflare deployment 391cf752-af34-44b2-93ea-a9a81c1cfd20. A verified source
bundle, local Git tag, homepage snapshot and rollback metadata are saved outside
the web root in ~/Documents/Enhance Visual Studio Backups/2026-11-19-production-launch/.
If a critical production check fails, restore that successful deployment first,
then resolve the issue. Restore Pages production bindings separately when needed;
keep preview intact and preserve the private Workers. Never apply a whole old
project snapshot over unrelated current settings.

The main website launches independently with GALLERY_URL unset and the Events
email fallback. SmugMug remains an owner-only trial. Purchases, public gallery
activation and custom gallery DNS remain deferred; no new paid service or DNS
change is required for this release.

- [Pages branch controls](https://developers.cloudflare.com/pages/configuration/branch-build-controls/)
- [Pages service bindings](https://developers.cloudflare.com/pages/functions/bindings/#service-bindings)
- [Worker rate limiting](https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/)

## SmugMug galleries

The gallery platform is the EVS SmugMug Luna site. Setup, the native block
layout, privacy presets, and Lightroom Classic workflow are in
[smugmug/README.md](smugmug/README.md). The customization files default to the production main-site origin. The
SmugMug trial remains private.
The main Events page keeps GALLERY_URL unset while the SmugMug trial is private.
Regenerating tools/build_site.py also updates the shared SmugMug snippets.
Generate production links with the default `python3 -B tools/build_site.py`.
For a deliberate preview-only pack, use
`python3 -B tools/build_site.py --smugmug-site-origin https://codex-evs-redesign.enhancevisualstudio-site.pages.dev`.
Apply the generated footer and update native SmugMug menu destinations there;
generating these files alone updates the repository artifacts.
The native gallery service is independent of the existing booking integration.
