# EVS SmugMug setup

This pack is the recoverable source for the native EVS Luna trial customization.
The finalized text slogan is exactly **Pose. Click. Enhance**. The supplied gold
camera and metallic silver logo uses that slogan too. Its artwork is retained
as provided, with its original colors and proportions.
The public account currently displays “Private site” with HTTP 404.
The user confirmed a trial. Native owner-side checks verified uploads, the
shared header and footer, mobile collapse, gallery viewing and saved protection
settings. Public sharing and signed-out client-privacy checks remain blocked by
the trial; no subscription or DNS change was made.

The main website update is on codex/evs-redesign. Main and the booking system
remain independent. Native SmugMug handles gallery uploads, folders, privacy,
search, full-screen viewing, sharing, downloads and any later approved sales.

## Native setup published on November 19, 2026

- Existing theme: Enhance Visual Studio - Gold. Primary #000000, text #f7f4ed,
  accent #e0bb69; Barlow Condensed headings and Manrope body.
- Entire Site: one original official logo above the centered native Menu, compact
  pure-black header, seven main-site links and Collapse for Mobile enabled. The
  original logo uses a sharp 600px native rendition, displayed at 168–196px by CSS.
- Homepage, All Folders and All Galleries inherit that header and shared footer.
- Footer copyright: ©2026 Enhance Visual Studio - All Rights Reserved.
  The theme appends this centered row after the native platform/legal links.
  The HTML copyright is a fallback and is hidden while the native footer exists.
- Organizer: Public Events / 2026; Portfolio; Unlisted Client Delivery.
  Client Delivery has web and SmugMug search disabled. Existing Unlisted brand
  assets, watermark assets and the original empty default gallery are retained.
- Portfolio contains 14 unique photographs already approved on the main site:
  Portraits & Studio (5), Fashion & Editorial (4), Weddings & Engagements (5).
  No event dates, client assignments or new photography were invented.
- Featured photography uses the native Portfolio folder dynamically. Latest
  events uses Public Events / 2026, newest first. Search is gallery-first and
  restricted to Public Events. Event archives lists its native year folders.
  The existing gold Book a Photographer button links to the main-site booking page.
- Three native presets saved: EVS Public Event, EVS Private Client, EVS Portfolio.
  See gallery-presets.md for actual protections and the per-gallery Access step.
- Owner preview verified the native lightbox, image proportions and navigation.
  Trial sharing explicitly remains owner-only. Owner purchase/download controls
  can still appear even when Visitor Shopping Cart and downloads are disabled;
  saved gallery settings are the authoritative configuration.

The design was published through SmugMug’s native confirmation after owner-side
verification. Publication does not remove the trial’s private-site restriction.
The main-site production release is managed independently; the trial remains private.

The official Lightroom plug-in is installed and authorized. A three-photo batch
and an in-place republish passed in the owner-only Client Delivery / EVS
Publishing Check gallery. Native image identities remained unchanged. See
lightroom-workflow.md for saved export and privacy settings.

A local restoration backup is saved outside the web root at
~/Documents/Enhance Visual Studio Backups/2026-11-19-free-hybrid-setup/.
It contains the code pack, original branding, fourteen approved photographs,
native settings manifest, official plug-in archive, Git checkpoint and checksums.
Credentials, cookies and Lightroom catalogs are excluded.

The following instructions reproduce or adjust the saved customization. Do not
upload another logo or add duplicate shared blocks.

## Branding in the authorized signed-in Chrome session

1. Open My Site → Customize Design. Select Entire Site. Keep the chosen Luna
   design and its native gallery/lightbox controls. If the homepage has an
   independent design, check its header/footer inheritance and apply the shared
   blocks there too.
2. Theme → edit the theme. Set background #0a0a0a, panels #141413, text #f7f4ed,
   secondary text #bab5aa, and accent #e0bb69. Select Barlow Condensed for headings
   and Manrope for body if present in the picker. Otherwise use a condensed
   sans heading font and a plain sans body font. Set body to 16px or larger.
   In Advanced CSS, paste theme.css.
3. In Entire Site header, set the native Logo block to evs-logo.png, linked to
   the main website. Set Resize Width to 600px for a sharp rendition; theme.css
   displays it compactly at 168–196px, retaining its original proportions.
   Add a native Menu block with the seven entries below and Collapse for Mobile.
   The native Menu is preferred for its supported mobile behavior.
   navigation.html is an optional HTML block replacement if you prefer wrapping
   links. Use one menu, not both.
4. In Entire Site footer, add an HTML block containing footer.html. In Homepage,
   add an HTML block containing home-intro.html. HTML files contain only supported
   static markup. No JavaScript, album IDs, API keys or custom account access.
5. Use Save It For Later until you have checked the native blocks and privacy.
   Existing uploads need no GitHub deployment.

### Main-site navigation

The owner approved the main website production launch on November 19, 2026.
The supplied HTML now defaults to https://www.enhancevisualstudio.com.
Generate it with `python3 -B tools/build_site.py`. A deliberate preview-only
pack may use `--smugmug-site-origin https://codex-evs-redesign.enhancevisualstudio-site.pages.dev`.
The generator accepts only these EVS origins.
The existing native logo, Menu, footer and homepage booking CTA were updated
to these production destinations and saved in the existing Luna trial design.
Homepage, the 2026 folder and a private gallery were checked afterward; one
shared logo/menu and native legal footer remain. Signed-out access still
returns the private-trial 404. No public activation or DNS change occurred.

Apply the footer to its existing shared block and update the existing native
Menu, logo target and homepage booking button to the main production domain.
Keep Events linked to the native SmugMug homepage. These navigation changes
must not enable public trial access or activate the future custom subdomain.

| Label | Destination |
| --- | --- |
| Home | https://www.enhancevisualstudio.com/ |
| Events | Native SmugMug Homepage |
| Portfolio | https://www.enhancevisualstudio.com/portfolio |
| Packages | https://www.enhancevisualstudio.com/packages |
| About | https://www.enhancevisualstudio.com/about |
| Contact | https://www.enhancevisualstudio.com/contact |
| Book a Session | https://www.enhancevisualstudio.com/book |

Booking verification is recorded in the main README. Public gallery access
remains gated by the private trial and signed-out HTTPS/privacy checks. The
main site uses its Events email fallback independently.

Use a compact Entire Site header with the centered official Logo block above
the centered native Menu block. Retain the logo artwork and its aspect ratio;
remove block padding instead of adding spacers. The header background is pure
black (#000), with white navigation and subtle gold hover accents. Keep native
Collapse for Mobile enabled. Check Homepage, All Folders and All Galleries for
header overrides, using the shared header rather than duplicated blocks. Keep the
SmugMug mini footer and its required privacy/report/login links.

## Native event homepage

Use the following blocks on Homepage in this order. They are content blocks,
not custom code. Add only your own albums and photographs. Leave a section out
until it contains published public material.

| Section | Native block and source | Settings |
| --- | --- | --- |
| Introduction | HTML using home-intro.html | Official slogan, minimal text |
| Gallery search | Discovery → Search Box | Gallery results first; source Public Events folder; “Search event galleries” |
| Latest events | Galleries → Folder → Public Events / current year | Date added, descending; landscape collage or grid; visible titles |
| Featured photography | Galleries → Folder → Portfolio | Dynamic source; three genuine photography galleries; landscape collage; visible titles |
| Event archives | Folders, Galleries & Pages → Public Events folder | Year folder covers, names, newest year first |
| Book a Photographer | Native Button | Main-site /book?service=events&package=custom |

New galleries added to the current-year source appear without code changes.
Once each year, select the new year folder in that native block. Native Recent
Galleries is another automatic source if the live control supports restricting
it to Public Events. Otherwise Recent Galleries is site-wide and can include
public portfolio galleries. Do not assume that a Folder source recursively
collects galleries inside year folders.

Create this Organizer structure using native folders:

- Public Events / year / event gallery
- Portfolio / photography categories
- Client Delivery / unlisted client galleries

The configured Featured photography block lists the Portfolio folder without
duplicate uploads or manual album lists. Additional curated event features may
use Galleries I Choose later. Publish new events under the current year.
Create each year's folder once, then let the native folder block list the
years. Set a representative photograph as each event and year-folder cover.
The date timeline (/date) groups photographs by capture date. Year/event
archives come from your Organizer folders.

Use native gallery layout and Lightbox settings for responsive photos,
captions, previous/next, full-screen viewing, downloads and Share controls.
Enable Share only for public presets. Do not place private gallery URLs in
public descriptions, menus, featured blocks or manually selected gallery blocks.

## Privacy, sales, and publishing

Apply gallery-presets.md before uploading client material. Keep Visitor Shopping
Cart off in every preset and gallery. Prepare native folders and source image
quality for possible later sales, but leave pricing and selling disabled.

The trial site can be prepared while private. Public sharing and the branded
domain need an eligible active plan chosen by the owner. No purchase is made
by this implementation.

### Owner-side acceptance checks

- Check logo and native menu at 320, 390, 768 and 1440px.
- Open one public gallery as a signed-out visitor after public access is available.
  Check landscape and portrait proportions, cover/title, full-screen arrows,
  Share link, search results and archive placement.
- Create a test Unlisted client gallery with password access. In a signed-out
  browser, confirm it is absent from homepage, featured blocks, browse, search
  and year folders. Opening its direct link must require the password.
- Check a delivery gallery's download setting independently of its display size.
- Upload one EVS photo through Lightroom to a private test gallery, revise it
  and republish, and confirm that it updates rather than creates a duplicate.
- Confirm shopping and sales prices remain disabled.
- Main-site booking is still the existing independent system and email fallback.

## Future branded hostname — no DNS change made

Only after owner authorization, confirm Portfolio eligibility and a public,
working account site. Preserve every existing website and email record.

1. Add exactly one Cloudflare record: CNAME, Name gallery,
   Target domains.smugmug.com, Proxy DNS only. Check for an existing gallery
   record before adding or changing anything.
2. In SmugMug Site Settings → Site → General → Custom Domain, set
   gallery.enhancevisualstudio.com and save.
3. Wait for SmugMug HTTPS provisioning. Test the HTTPS homepage, /browse,
   /search, public gallery and password-protected link in a signed-out browser.
4. Only then set GALLERY_URL in tools/build_site.py to
   https://gallery.enhancevisualstudio.com and regenerate the static pages.
   A verified public SmugMug hostname may be used temporarily before the domain
   move, but the current trial URL is not linked from public site pages.

## Recoverable source checkpoint

The pre-hybrid redesign is preserved at Git commit ee86a26. The audit found no
Studio Manager backend, gallery database, or custom gallery storage to retire.

## Sources

- [Native content blocks](https://www.smugmughelp.com/hc/en-us/articles/18212941353364-Fine-tune-my-Site-Design-with-content-blocks)
- [Themes and CSS](https://www.smugmughelp.com/hc/en-us/articles/18212317845012-Use-themes-to-tweak-my-design)
- [Navigation and mobile menu](https://www.smugmughelp.com/hc/en-us/articles/18212261586580-Use-the-navigation-content-blocks)
- [Native gallery blocks](https://www.smugmughelp.com/hc/en-us/articles/18212965685780-Customize-the-galleries-content-block)
- [Folders and galleries](https://www.smugmughelp.com/hc/en-us/articles/18212912396436-Use-the-Folders-Galleries-Pages-content-block)
- [Gallery search](https://www.smugmughelp.com/hc/en-us/articles/18212968678804-Add-search-to-my-site)
- [Trial sharing limits](https://www.smugmughelp.com/hc/en-us/articles/18212817296660-Quickstart-guide)
- [Custom domain](https://www.smugmughelp.com/hc/en-us/articles/18212351739284-Use-a-custom-domain)
