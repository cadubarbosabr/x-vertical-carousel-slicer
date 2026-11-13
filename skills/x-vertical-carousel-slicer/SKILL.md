---
name: x-vertical-carousel-slicer
description: "Transforms an attached image into 4 to 20 equal vertical slices (left-to-right) for an X (Twitter) carousel post. Default is 20. Resizes to 1200px height, saves high-quality JPEGs named part_01.jpg onwards, and packages them into a single ZIP. Use when the user requests X/Twitter vertical carousel, image slices, or continuous swipe reconstruction."
type: workflow
lifecycle: active
---

# X Vertical Carousel Slicer — 20-Slice Image for X Posts

Transforms a single image into a ZIP containing 20 sequential vertical slices optimized for X (Twitter) carousel posts. When posted in numerical order, users can swipe left-to-right and reconstruct the original continuous image.

## Core Workflow

1. **Locate the input image**  
   The user will attach or provide a path to the source image. If no image is present, ask for it.

2. **Ask for number of slices (optional)**  
   If the user does not specify, use **20** (default).  
   Accepted range: **4 to 20**.

3. **Run the slicer script**  
   Execute the bundled script. Always use `--preview` unless the user explicitly disables it.

   ```bash
   python3 skills/x-vertical-carousel-slicer/scripts/slice_carousel.py INPUT_IMAGE.png --slices 12 --preview --output-dir /tmp/carousel_output
   ```

   - Replace `INPUT_IMAGE.png` with the actual file path.
   - Replace `12` with the desired number (or omit `--slices` to use the default 20).
   - The script automatically:
     - Resizes to exactly **1200 px height** (aspect ratio preserved)
     - Divides into the requested number of vertical slices from left to right
     - Distributes any remainder pixels across the first slices so total width is fully covered
     - Saves as `part_01.jpg` … `part_NN.jpg` at JPEG quality 95
     - Generates `preview_carousel.jpg` (horizontal reduced preview)
     - Creates `x_carousel_slices.zip` containing all slices (+ preview)

3. **Deliver the ZIP to the user**  
   After the script finishes, render the ZIP file so the user can download it:

   ```xml
   <grok type="render_file" file_path="/tmp/carousel_output/x_carousel_slices.zip" />
   ```

4. **Optional: Show the preview**  
   If useful, also render the preview image.

## Critical Rules (Must Follow)

| Rule | Requirement |
|------|-------------|
| Slice order | Strictly left → right. `part_01.jpg` = leftmost, `part_20.jpg` = rightmost |
| No gaps | Do **not** add borders, spacing, shadows, or separators between slices |
| Dimensions | Final height = 1200 px. Width of each slice ≈ total_width / 20 (rounding adjusted) |
| Format | JPEG, quality 95, no extra compression artifacts |
| Delivery | Single ZIP only. Never deliver loose files unless requested |
| Reconstruction | Goal is continuous image when swiping the X carousel in numerical order |

## Script Location

- Main script: `scripts/slice_carousel.py`
- The script is deterministic and handles all edge cases (odd widths, different aspect ratios, RGBA conversion).

## Common Issues

| Problem | Solution |
|---------|----------|
| Image too small | Script still resizes to 1200 px height; quality may degrade if original is tiny |
| Non-RGB image | Automatically converted to RGB before slicing |
| Script not found | Use absolute path from the skill directory |
| User wants different slice count | Ask or use the number they specified (must be between 4 and 20). Pass it with `--slices N` |

## Example Usage

User: "Transforme esta imagem em carrossel vertical de 20 fatias para o X"

→ Run the script on the attached image → deliver the ZIP.
