# Enhance Visual Studio website

Cloudflare Pages project `enhancevisualstudio-site` serves the GitHub repository
`EnhanceVisualStudio/enhancevisualstudio-site`. The production branch is `main`.
Booking and contact both POST to the same-origin `/api/inquiry` route. The Pages
Function forwards to a private EVS Worker through `INQUIRY_WORKER`. The Worker
owns validation, rate limiting and Cloudflare Email Sending.

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

## Configure the Cloudflare preview

1. Sign in to the EVS Cloudflare account. Under **Workers & Pages**, select
   `enhancevisualstudio-site`. Under **Settings → Builds & deployments**,
   verify the repository and `main` as the production branch. Check the build
   root is the repository root, the build command is empty and the output
   directory is the repository root (`.`). The repository is buildless and
   contains both the pre-generated HTML and `_routes.json` at that output.
   If the existing project uses a staging output directory, confirm that its
   build copies the same static files and `_routes.json` to that output and
   locates `functions/` at the project root. Keep existing production settings
   intact until the verified release is approved.
2. Under **Preview branch controls**, verify that preview deployments are
   enabled and include `codex/evs-redesign`. If needed, enable only the EVS
   redesign branch. Verify the Pages project default hostname and use its
   branch alias `https://codex-evs-redesign.enhancevisualstudio-site.pages.dev`
   for the booking test. The preview Worker's origin allowlist is exact.
3. In **Email Service** in the EVS account, verify
   `hello@enhancevisualstudio.com` as a destination and confirm a sender on
   an EVS sending domain already onboarded to Cloudflare Email Sending. If
   onboarding requires DNS changes, obtain separate authorization for that
   setup. Enter any verification details in Cloudflare, never in the repo.
4. Authenticate Wrangler on the EVS account with `npx wrangler login` and
   verify the active account with `npx wrangler whoami`. Check the worker name
   `enhance-visual-studio-inquiries-preview` and rate-limit namespace are
   unique to this EVS preview. Resolve any collision before deploying. From
   the repo root, deploy only the private preview Worker:
   `npx wrangler deploy --config worker/wrangler.toml --env preview`.
   Set `BOOKING_FROM` to the exact verified EVS sender using
   `npx wrangler secret put BOOKING_FROM --config worker/wrangler.toml --env preview`
   or the preview Worker's dashboard. There is no public Worker URL or route.
5. In the Pages project's **Settings → Bindings**, select **Preview**, add a
   **Service binding** named `INQUIRY_WORKER`, and select
   `enhance-visual-studio-inquiries-preview`. Keep the production environment
   untouched. Redeploy the preview after a binding change. Authenticate
   GitHub with an account that has write access to the authorized repository,
   then push only `codex/evs-redesign` and confirm the resulting preview commit
   and URL under **Deployments**.
6. Open the branch alias. GET `/api/inquiry` must return JSON with status 405
   and `Allow: POST`. Then submit controlled booking and contact forms from
   that origin. Confirm both notifications arrive at the studio inbox with
   the expected Reply-To and details. Check invalid input and failure handling.
   An on-site success means the email service accepted the notification.
   The site does not automatically email the customer or reserve a date.

Before production, verify the approved release commit and production settings,
configure the production Worker and Pages service binding separately, and
obtain approval to merge into `main`. Merging triggers automatic production
deployment. No other Cloudflare project, Worker or brand is part of the release.

- [Pages branch controls](https://developers.cloudflare.com/pages/configuration/branch-build-controls/)
- [Pages service bindings](https://developers.cloudflare.com/pages/functions/bindings/#service-bindings)
- [Email binding and verified destinations](https://developers.cloudflare.com/email-service/configuration/send-bindings/)
- [Worker rate limiting](https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/)

## SmugMug galleries

The gallery platform is the EVS SmugMug Luna site. Setup, the native block
layout, privacy presets, and Lightroom Classic workflow are in
[smugmug/README.md](smugmug/README.md). The customization files contain a staged
menu that points back to the redesign preview until the main site is released.
The main Events page keeps GALLERY_URL unset while the SmugMug trial is private.
Regenerating tools/build_site.py also updates the shared SmugMug snippets.
The native gallery service is independent of the existing booking integration.
