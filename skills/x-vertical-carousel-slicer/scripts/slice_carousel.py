#!/usr/bin/env python3
"""
X Vertical Carousel Slicer
Transforms an image into 20 equal vertical slices for X (Twitter) carousel posts.
"""

import argparse
import sys
from pathlib import Path
from PIL import Image
import zipfile

def resize_to_height(image: Image.Image, target_height: int = 1200) -> Image.Image:
    """Resize image to target height while maintaining aspect ratio."""
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGB")
    width, height = image.size
    if height == target_height:
        return image
    ratio = target_height / height
    new_width = int(width * ratio)
    return image.resize((new_width, target_height), Image.Resampling.LANCZOS)

def create_slices(image: Image.Image, num_slices: int = 20, quality: int = 95) -> list[Path]:
    """Divide image into num_slices equal vertical slices from left to right."""
    width, height = image.size
    base_slice_width = width // num_slices
    remainder = width % num_slices

    output_paths = []
    x_offset = 0

    for i in range(num_slices):
        # Distribute remainder pixels to the first 'remainder' slices
        slice_width = base_slice_width + (1 if i < remainder else 0)
        box = (x_offset, 0, x_offset + slice_width, height)
        slice_img = image.crop(box)

        filename = f"part_{i+1:02d}.jpg"
        output_path = Path(filename)
        slice_img.save(output_path, "JPEG", quality=quality, optimize=True)
        output_paths.append(output_path)
        x_offset += slice_width

    return output_paths

def create_preview(slices: list[Path], preview_height: int = 200) -> Path:
    """Create a horizontal preview of all slices side by side."""
    if not slices:
        return None
    first = Image.open(slices[0])
    slice_width = first.width
    total_width = sum(Image.open(s).width for s in slices)
    preview = Image.new("RGB", (total_width, first.height))
    x = 0
    for s in slices:
        img = Image.open(s)
        preview.paste(img, (x, 0))
        x += img.width
    # Scale down for preview
    ratio = preview_height / preview.height
    new_w = int(preview.width * ratio)
    preview = preview.resize((new_w, preview_height), Image.Resampling.LANCZOS)
    preview_path = Path("preview_carousel.jpg")
    preview.save(preview_path, "JPEG", quality=90)
    return preview_path

def create_zip(files: list[Path], zip_name: str = "x_carousel_slices.zip") -> Path:
    """Package all slice files into a single ZIP."""
    zip_path = Path(zip_name)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, f.name)
    return zip_path

def main():
    parser = argparse.ArgumentParser(description="Slice image into vertical parts for X carousel")
    parser.add_argument("input_image", type=Path, help="Path to the input image")
    parser.add_argument("--slices", type=int, default=20, choices=range(4, 21),
                        help="Number of slices (4 to 20, default: 20)")
    parser.add_argument("--output-dir", type=Path, default=Path("."), help="Output directory")
    parser.add_argument("--preview", action="store_true", help="Also generate a horizontal preview")
    parser.add_argument("--zip-name", default="x_carousel_slices.zip", help="Name of the output ZIP")
    args = parser.parse_args()

    if not args.input_image.exists():
        print(f"Error: Input image not found: {args.input_image}", file=sys.stderr)
        sys.exit(1)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    original_cwd = Path.cwd()
    try:
        import os
        os.chdir(args.output_dir)

        print(f"Loading image: {args.input_image}")
        img = Image.open(args.input_image)
        print(f"Original size: {img.size}")

        resized = resize_to_height(img, 1200)
        print(f"Resized to: {resized.size}")

        print(f"Creating {args.slices} vertical slices...")
        slice_paths = create_slices(resized, num_slices=args.slices, quality=95)
        print(f"Created slices: {[p.name for p in slice_paths]}")

        files_to_zip = list(slice_paths)
        if args.preview:
            print("Generating preview...")
            preview = create_preview(slice_paths)
            if preview:
                files_to_zip.append(preview)
                print(f"Preview: {preview}")

        zip_path = create_zip(files_to_zip, args.zip_name)
        print(f"ZIP created: {zip_path.resolve()}")
        print(f"Total files in ZIP: {len(files_to_zip)}")

    finally:
        os.chdir(original_cwd)

if __name__ == "__main__":
    main()
