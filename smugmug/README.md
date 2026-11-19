# EVS SmugMug setup

This is a ready-to-apply customization pack for the existing Luna trial.
The public account currently displays “Private site” with HTTP 404.
The user confirmed a trial. Subscription eligibility, settings, real gallery
contents, upload behavior and client privacy still require owner-side checks.

The main website update is on codex/evs-redesign. Main and the booking system
remain independent. Native SmugMug handles gallery uploads, folders, privacy,
search, full-screen viewing, sharing, downloads and any later approved sales.

## Apply the branding in your signed-in Safari window

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
   the main website. Display at about 196px wide, retaining its proportions.
   Add a native Menu block with the seven entries below and Collapse for Mobile.
   The native Menu is preferred for its supported mobile behavior.
   navigation.html is an optional HTML block replacement if you prefer wrapping
   links. Use one menu, not both.
4. In Entire Site footer, add an HTML block containing footer.html. In Homepage,
   add an HTML block containing home-intro.html. HTML files contain only supported
   static markup. No JavaScript, album IDs, API keys or custom account access.
5. Use Save It For Later until you have checked the native blocks and privacy.
   Existing uploads need no GitHub deployment.

### Staging navigation

The supplied HTML links to the verified redesign preview while the main domain
still serves the original site. After the main website release, change the
preview origin to https://www.enhancevisualstudio.com in
build_smugmug_customization() in tools/build_site.py and regenerate the snippets.

| Label | Destination during staging |
| --- | --- |
| Home | https://codex-evs-redesign.enhancevisualstudio-site.pages.dev/ |
| Events | SmugMug Homepage, selected using the native page picker |
| Portfolio | https://codex-evs-redesign.enhancevisualstudio-site.pages.dev/portfolio |
| Packages | https://codex-evs-redesign.enhancevisualstudio-site.pages.dev/packages |
| About | https://codex-evs-redesign.enhancevisualstudio-site.pages.dev/about |
| Contact | https://codex-evs-redesign.enhancevisualstudio-site.pages.dev/contact |
| Book a Session | https://codex-evs-redesign.enhancevisualstudio-site.pages.dev/book |

Choose a horizontal header layout with logo left and menu right where Luna
allows it. Use native Entire Site Layout width and pinning options. Keep the
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
| Featured albums | Galleries → Galleries I Choose | 3–6 selected existing public galleries, curated order |
| Event archives | Folders, Galleries & Pages → Public Events folder | Year folder covers, names, newest year first |
| Book a Photographer | Native Button | Preview /book?service=events&package=custom |

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

Select the existing public albums directly in Featured albums, so photographs
need no duplicate upload. Publish new events under the current year.
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
