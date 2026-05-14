# Design Notes — MediStock Mockups

This document explains the intent and suggested usage for the included SVG mockups. Use these notes when iterating on UI or creating marketing/design assets.

## General

- All mockups are intentionally simplified SVGs intended for documentation and early-stage review, not production assets.
- Files are located under `static/images` and `static/images/mockups`.
- Use the SVGs as-is for documentation or export them to PNG at required sizes for presentations.

## Mockup catalog

- `static/images/product_design_1.svg`
  - Product card with a location stock summary and an "Add to Cart" CTA. Useful when testing per-location inventory displays on product cards.

- `static/images/product_design_2.svg`
  - Product detail + low-stock alert panel. Useful for error/alert states and reordering flows.

- `static/images/mockups/product_list_desktop.svg`
  - Desktop grid layout for browsing multiple products. Shows primary CTAs and low-stock states.

- `static/images/mockups/product_list_tablet.svg`
  - Two-column tablet layout; useful for responsive checks and spacing adjustments.

- `static/images/mockups/product_list_mobile.svg`
  - Vertical stacked mobile layout; focuses on compact CTAs and single-column flow.

- `static/images/mockups/product_detail_desktop.svg`
  - Full product detail with image area, details column, and per-location stock summary.

- `static/images/mockups/cart_mobile.svg`
  - Mobile cart summary, line items, and final checkout CTA.

- `static/images/mockups/inventory_dashboard_tablet.svg`
  - Inventory dashboard focusing on low-stock items and suggested actions.

## Suggested next steps

- Export the SVGs to PNG at 1x/2x/3x sizes for inclusion in docs or marketing.
- Replace placeholders with real product images and real data when preparing high-fidelity prototypes.
- Use the mockups as the basis for a simple style guide (colors, button sizes, spacing) if you plan UI updates.

## How to export

From most image editors or command-line tools (e.g., ImageMagick or Inkscape) you can export SVG → PNG. Example (Inkscape):

```bash
inkscape static/images/mockups/product_list_desktop.svg --export-type=png --export-filename=static/images/mockups/product_list_desktop@2x.png --export-width=2400
```

If you want, I can generate PNG exports at common sizes. Request which files and sizes you want.
