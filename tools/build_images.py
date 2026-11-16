"""Create responsive display JPEGs with Pillow 9.1+; original files remain untouched."""
from PIL import Image, ImageOps

from build_site import DISPLAY_WIDTHS, PHOTOS, ROOT


def main():
    output = ROOT / "images" / "display"
    output.mkdir(exist_ok=True)
    for number, (expected_width, expected_height, *_) in PHOTOS.items():
        with Image.open(ROOT / "images" / f"{number}.jpg") as source:
            image = ImageOps.exif_transpose(source)
            if image.size != (expected_width, expected_height):
                raise ValueError(f"Update PHOTOS dimensions for images/{number}.jpg: {image.size}")
            profile = source.info.get("icc_profile")
            for width in DISPLAY_WIDTHS:
                if width >= image.width:
                    continue
                height = round(image.height * width / image.width)
                target = image.resize((width, height), Image.Resampling.LANCZOS)
                target.save(output / f"{number}-{width}.jpg", quality=86, optimize=True, progressive=True,
                            icc_profile=profile)


if __name__ == "__main__":
    main()
