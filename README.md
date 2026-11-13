# X Vertical Carousel Slicer

Transforms a single image into a ZIP containing **exactly 20 vertical slices** optimized for X (Twitter) carousel posts.

When the 20 images are posted in numerical order (`part_01.jpg` → `part_20.jpg`), users can swipe through the carousel and reconstruct the original continuous image.

## Example

**Source image**

![Source image](assets/example-source.jpg)

**Result — 20 slices side by side**

![Preview of 20 slices](assets/example-preview.jpg)

Download the complete example ZIP (all 20 slices + preview):  
[example-slices.zip](assets/example-slices.zip)

## Live Example on X

https://x.com/CaduBarbosaBR/status/2121245526859681832

## Features

- Resizes image to exactly **1200 px height** (aspect ratio preserved)
- Splits into **exactly 20 equal vertical slices** (left → right)
- Distributes remainder pixels so the full width is covered with no gaps
- Saves as high-quality JPEG (quality 95)
- Naming: `part_01.jpg` (leftmost) to `part_20.jpg` (rightmost)
- Generates an optional horizontal preview
- Packages everything into a single `x_carousel_slices.zip`
- No borders, spacing, or extra elements between slices

## Installation

### As a Grok skill

```bash
mkdir -p ~/.grok/skills
cp -r skills/x-vertical-carousel-slicer ~/.grok/skills/
```

### As a Grok Build plugin

Once listed in the [xAI Plugin Marketplace](https://github.com/xai-org/plugin-marketplace):

```bash
grok plugin install x-vertical-carousel-slicer --trust
```

## Usage

Ask Grok:

> Transform this image into 20 vertical slices for an X carousel

or

> Transforme a imagem anexada no formato de carrossel vertical de 20 fatias para o X

The skill will run the bundled script and deliver the ZIP.

## Standalone Script

```bash
python3 skills/x-vertical-carousel-slicer/scripts/slice_carousel.py input.png --preview --output-dir ./output
```

Requires Python 3 and Pillow (`pip install pillow`).

## License

MIT
