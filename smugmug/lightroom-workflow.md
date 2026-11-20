# Publish from Lightroom Classic

The daily workflow is photograph → edit in Lightroom Classic → publish to a
SmugMug gallery → share the branded link. Routine gallery publishing happens in
Lightroom and SmugMug. It requires no Codex, GitHub, or Cloudflare deployment.

## Verified free-trial setup — November 19, 2026

The official SmugMug plug-in 3.5.19.1 is installed and enabled in Lightroom
Classic 16.0.1. Its existing publishing service is authorized as Enhance Visual
Studio. The saved settings use JPEG quality 90, sRGB, full dimensions, no file
size cap, no video files, and removal of person and location information.
Lightroom does not burn in a watermark; the native SmugMug preset applies EVS
Proof to display copies.

A three-photo batch from the existing website library was imported using Add
from Pictures/Enhance Visual Studio/Publishing Check and published successfully
to Client Delivery / EVS Publishing Check. That test gallery is Private (Only Me),
with search and downloads off, X3 display size and the EVS Proof watermark.
It is a labeled verification gallery, not a client delivery or public event.
An in-place republish also completed successfully. The same gallery retained
three photographs and the same native image identities; no duplicate gallery
was created. The original fourteen portfolio uploads remain in their existing galleries.
Do not duplicate these galleries when synchronizing the publishing service.

The trial permits owner-side publishing tests. Public sharing, signed-out
client access and download testing remain deferred until an eligible active
plan. Subscription purchase and gallery DNS activation remain postponed.

## One-time setup in Lightroom Classic

1. Download the latest official [SmugMug Lightroom plugin](https://www.smugmug.com/software-updates/lightroom-plugin/latest).
   Unzip it and keep SmugMug.lrplugin in a stable local folder.
2. Lightroom Classic → File → Plug-in Manager → Add. Select SmugMug.lrplugin
   and confirm Installed and running. Use the official plugin's own update flow
   when available.
3. In Library → Publish Services, choose SmugMug → Set Up. Authorize in the
   browser as the owner of enhancevisualstudio.smugmug.com. Check the account
   name before returning to Lightroom and saving the publishing service.
4. Choose JPEG with an embedded sRGB profile for consistent web color. Keep full
   resolution and high quality (90–100), retain copyright metadata, and omit
   GPS/location metadata where the subject requires privacy. Use SmugMug native
   watermarks on display copies instead of burning a mark into exported images.
5. Synchronize existing folders and galleries. Verify the three native presets
   exist before creating a real event or delivery gallery. See gallery-presets.md.

## Each event

1. Edit and select the final photographs in Library.
2. Under the EVS SmugMug Publish Service, select the Public Events folder for
   the correct year and create a gallery. Choose the Public Event preset,
   provide an accurate title, cover photo, and useful description.
3. Drag the edited photos into that publish collection and click Publish.
   Wait until the upload completes.
4. In SmugMug, confirm the cover and gallery settings and test the link as a
   signed-out visitor. On an active plan, the public event gallery should appear
   in the Latest events block when uploaded to its configured current-year
   folder. The year archive lists native folders. A manually curated Featured
   albums block requires selecting the gallery once; it does not update itself.
   At each new year, create its folder and update the Latest events source.
5. Share its SmugMug link. After the future custom domain is configured and HTTPS
   is verified, use its gallery.enhancevisualstudio.com equivalent.

For private client delivery, use the Client Delivery folder and Private Client
preset, then set the actual per-gallery password or invite permissions. Test
the direct link before sharing. A trial remains private to the owner, so
visitor upload/delivery checks require an active eligible account.

## Updates and synchronization

- Edit an already published image, mark it for republishing if needed, and click
  Publish to update the remote copy. Test a single image first.
- Use the plugin's synchronization controls when folders or galleries change
  in SmugMug.
- Removing photos from a published collection can delete those remote photos
  on the next Publish. Inspect pending removals first and preserve the catalog
  and source files.
- Archive by native year folders. Do not duplicate a gallery merely to feature
  it on the homepage. Use a native selected-gallery block or shortcut.

[Official Lightroom Classic publishing guide](https://www.smugmughelp.com/hc/en-us/articles/18212816221332-Upload-from-Lightroom)
