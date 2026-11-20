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

The following configuration is in place. End-to-end receipt remains subject to
the pending checks below.

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
  Keep token values, verification links and private configuration out of commits.
- Production Pages settings and the production branch retain their existing
  configuration.

When updating the preview Worker, verify the EVS account, the preview Worker
name and its preview bindings before using
`npx wrangler deploy --config worker/wrangler.toml --env preview`.
Manage BOOKING_FROM through the Worker secret interface. Preview service-binding
changes require a new Pages preview deployment. Push the reviewed redesign
commit only to codex/evs-redesign and verify that commit under Pages Deployments.

### Preview acceptance checks still pending

1. Verify the latest reviewed commit at the branch alias. GET /api/inquiry must
   return JSON, status 405 and Allow: POST.
2. Submit one controlled booking request and one contact inquiry from the alias.
   Confirm that each reports success and arrives at the verified studio inbox,
   with the correct service, package, preferred dates, location and Reply-To.
   A successful website receipt means Cloudflare accepted the notification.
3. Check invalid email, unknown service, invalid package/service combinations,
   invalid dates and the honeypot. Confirm useful errors and no accepted request.
   Verify foreign-origin rejection and rate-limit handling in the preview.
4. Confirm a failed or timed-out submission preserves entered details, restores
   the submit button and shows the studio email fallback. Use the local mock
   tests for delivery failures. Check that API responses contain JSON and
   Cache-Control: no-store.
5. Verify a deep missing page returns the branded 404 with working root links.
   Check static security headers, Pages preview noindex headers, navigation and
   gallery viewing on mobile and desktop.

Record the actual results before treating live delivery as verified. Customers
receive an on-site submission receipt; dates remain subject to studio approval
and the existing retainer policy. This flow sends the studio notification and
does not send an automatic customer email.

## Production readiness and release approval

The main website can be released independently with the Events email fallback
while GALLERY_URL remains unset. Review the release commit and existing Pages
production branch, repository, build root and output before requesting approval.
The buildless output must include the generated HTML, 404.html, _headers,
_routes.json and the project-root functions directory.

During a separately approved release, configure the EVS production Worker with
the production origins, rate limiter, verified fixed studio destination and
sender secret. Configure its Pages Production INQUIRY_WORKER service binding
separately from Preview, then verify controlled booking/contact inbox delivery.
Keep this deployment on the free verified-destination path.

Approval to merge into main is required because that merge triggers production
deployment. Verify enhancevisualstudio.com and the EVS project before release.
Gallery public access, subscription purchases and gallery DNS changes require
their own authorization and readiness checks.

- [Pages branch controls](https://developers.cloudflare.com/pages/configuration/branch-build-controls/)
- [Pages service bindings](https://developers.cloudflare.com/pages/functions/bindings/#service-bindings)
- [Worker rate limiting](https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/)

## SmugMug galleries

The gallery platform is the EVS SmugMug Luna site. Setup, the native block
layout, privacy presets, and Lightroom Classic workflow are in
[smugmug/README.md](smugmug/README.md). The customization files contain a staged
menu that points back to the redesign preview until the main site is released.
The main Events page keeps GALLERY_URL unset while the SmugMug trial is private.
Regenerating tools/build_site.py also updates the shared SmugMug snippets.
Their default main-site origin stays on the redesign preview. After an
approved main-site release, generate production links with
`python3 -B tools/build_site.py --smugmug-site-origin https://www.enhancevisualstudio.com`.
Apply the generated footer and update native SmugMug menu destinations there;
generating these files alone updates the repository artifacts.
The native gallery service is independent of the existing booking integration.
