# Enhance Visual Studio website

The existing GitHub-backed static pages remain at their original paths. The
booking and contact forms both submit to the same-origin Cloudflare endpoint
/api/inquiry. The Worker is separate from the static site and does not serve
pages or images.

## Maintain the site

- Edit shared menus, page copy, services, packages, policies and the photography
  inventory in tools/build_site.py. Run **python3 tools/build_site.py** and
  commit the generated HTML, sitemap.xml and assets/booking-catalog.mjs.
- For a portfolio addition, put the original JPEG in images/, add its dimensions,
  factual alt text and category to PHOTOS and its position to portfolio() in the
  generator. With Pillow 9.1+ installed, run **python3 -B tools/build_images.py**
  to generate display sizes, then regenerate the HTML. The gallery opens the
  original. Keep verified film and design examples on their own showcase pages.
- Preview the static pages with **python3 -m http.server 8000** from the root.
  This server does not run the Worker. Requests show a failure status and the
  studio email remains available. To exercise the Worker without sending email,
  use an injected EMAIL.send stub or Wrangler's local simulated email binding.
  Never use the real binding for local submissions.

## Cloudflare setup before production

1. Verify the active Git checkout, approved release branch and commit, existing
   static hosting, and the EVS Cloudflare account, zone and project. This repo
   currently has no verified Cloudflare account or zone ID. Preserve the static
   host, DNS, other brands' infrastructure and the existing deploy workflow.
2. In the EVS account, verify that Cloudflare Email Sending is available and that
   an EVS sending domain has already been onboarded. Verify
   hello@enhancevisualstudio.com as the fixed recipient. If sender onboarding
   would require DNS or shared account changes, obtain the required separate
   authorization before doing that setup.
3. Configure BOOKING_FROM as a Worker secret with the exact verified EVS sender
   address. The EMAIL binding restricts delivery to the studio inbox. Confirm
   INQUIRY_LIMITER uses an EVS-only namespace ID; if the template ID already
   exists in the account, use a different EVS-only positive integer. Confirm
   ALLOWED_ORIGINS lists only the actual EVS origins that serve the form.
4. After release approval, deploy the Worker in the verified EVS account. Bind
   it only to **www.enhancevisualstudio.com/api/inquiry** on the existing proxied
   host. If the apex also directly serves the site, bind
   **enhancevisualstudio.com/api/inquiry** there too. If it redirects to www, use
   the www route alone. The repository intentionally defines no route or account
   ID. Leave the existing static-site route and unrelated paths alone.
5. Verify with controlled booking and contact submissions on an approved EVS
   environment, confirm the inbox receives both and Reply-To points to the test
   sender, and verify invalid requests fail. A successful website receipt means
   the mail provider accepted the studio notification. Dates are still subject
   to studio approval and the existing retainer policy. No customer email is sent
   automatically and there is no separate booking database.

Use the existing production static host and deploy only after separate approval.
No production configuration or email delivery is verified by this repository.

- [Cloudflare Worker routes](https://developers.cloudflare.com/workers/configuration/routing/routes/)
- [Email binding and fixed recipients](https://developers.cloudflare.com/email-service/configuration/send-bindings/)
- [Local email simulation](https://developers.cloudflare.com/email-service/observability/local-development/sending/)
- [Rate limiting](https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/)
