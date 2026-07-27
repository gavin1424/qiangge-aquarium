# Design QA

## Comparison target

- Source visual truth:
  - `assets/images/source/reference-concept-01-home-desktop.jpg`
  - `assets/images/source/reference-concept-02-home-mobile.jpg`
  - `assets/images/source/reference-concept-03-fish-list.jpg`
  - `assets/images/source/reference-concept-04-gallery.jpg`
  - `assets/images/source/reference-concept-05-fish-detail.jpg`
- Browser-rendered implementation:
  - `qa/screenshots/home-desktop-1440x1000.png`
  - `qa/screenshots/home-mobile-390x844-v2.png`
  - `qa/screenshots/fish-desktop-1440x1000-v2.png`
  - `qa/screenshots/gallery-desktop-1440x1000-v4.png`
  - `qa/screenshots/detail-desktop-1440x1000.png`
- Side-by-side evidence:
  - `qa/screenshots/compare-home-desktop.jpg`
  - `qa/screenshots/compare-home-mobile-v2.jpg`
  - `qa/screenshots/compare-fish-desktop-v2.jpg`
  - `qa/screenshots/compare-gallery-desktop-v4.jpg`
  - `qa/screenshots/compare-detail-desktop.jpg`

## Viewport and normalization

- Desktop implementation viewport: 1440 × 1000 CSS px, device scale factor 1.
- Mobile implementation viewport: requested 390 × 844 CSS px; browser content width 375 px because of the visible scrollbar, device scale factor 1.
- Source concepts: 1024 × 1280 px each.
- Desktop comparisons preserve each artifact's aspect ratio inside equal 860 × 960 panels.
- Mobile source was cropped to the visible phone frame before being contained in the equal comparison panel.
- State: default home, unfiltered fish list, default gallery, light-stripe detail, closed mobile menu.
- The concepts are visual-direction references rather than exact production copy: they contain invented prices, contact details, scientific names, L numbers and commerce controls that the user explicitly prohibited unless confirmed.

## Required fidelity surfaces

### Fonts and typography

- Uses the requested system font stack and a system serif display stack, with no downloaded font dependency.
- Display headlines reproduce the high-contrast editorial character of the concepts.
- Navigation, filters, metadata and body copy maintain readable optical sizes on desktop and mobile.
- Mobile heading scale was reduced after the first pass so the real fish photo and the start of the brand statement share the first viewport.

### Spacing and layout rhythm

- Desktop uses the concepts' white navigation bar, dark ocean hero, photo-led cards, rounded content surfaces and generous section rhythm.
- Inner-page heroes were shortened after the first pass so fish cards and gallery imagery enter the desktop first viewport sooner.
- Mobile layout has no horizontal overflow at 390 × 844 and preserves the fixed four-item dock without covering the final page content.
- Radii, borders and shadows are consistent across filter panels, cards, notices and forms.

### Colors and visual tokens

- Uses the requested navy, deep ocean, teal, aqua, white surface and soft gray-green background tokens.
- Aqua is reserved for active states, labels and primary actions; no inexpensive neon glow treatment is used.
- Dark backgrounds retain readable white and muted text contrast.

### Image quality and asset fidelity

- All eight content images are user-provided real fish photos.
- No concept screenshot, AI fish image, network image or screenshot crop is used as page content.
- Each original remains unchanged in `assets/images/source/`.
- Each used photo has 400, 640 and 960 px WebP variants plus a 960 px progressive JPG fallback.
- Aspect ratios are preserved and fish bodies are not stretched.
- Homepage hero uses preload, eager loading and high fetch priority; remaining images use lazy loading.
- All image elements include Traditional Chinese alt text and intrinsic dimensions.

### Copy and content

- Brand name, positioning and supporting line match the brief.
- Scientific names, L numbers, prices, inventory, reviews, phone, address, hours and social accounts are not invented.
- Each fish entry clearly states that the visible category is an appearance description and the formal strain remains to be confirmed.
- The static contact form explicitly says it does not submit, upload or store personal data.

## Full-view comparison evidence

- Home desktop: matches the white header, deep ocean hero, serif display type, teal actions and right-side fish emphasis. The production version intentionally uses a more editorial, less commerce-heavy first viewport.
- Home mobile: after iteration, the real fish photo leads the page and is visible before the headline, matching the reference's photo-first mobile hierarchy.
- Fish list: retains the dark introduction, category chips, search and image-card grid. Price, stock and unsupported side filters were intentionally removed.
- Gallery: retains a dark editorial introduction followed by a dense photo grid. It uses only the eight verified fish photos.
- Detail: retains the large individual image plus a structured facts panel, while replacing unsupported scientific and commercial facts with cautious care guidance.

## Focused-region comparison evidence

- Header: consistent logo scale, white surface and teal active underline across all routes.
- Hero: serif headline weight, dark ocean balance, image crop and glass note checked at desktop and mobile.
- Fish filter: selected, search and empty-result paths tested; one-result state remains readable with no horizontal overflow.
- Contact form: labels, required fields, select state, summary state and copy state tested at mobile width.
- Focused checks were sufficient because the remaining lower-page content reuses the same verified tokens and component patterns.

## Comparison history

1. Initial mobile home finding — P2:
   - Evidence: the first 390 × 844 capture showed only the oversized headline and proof panel; the real fish photo remained below the fold.
   - Fix: reordered the mobile hero image before the copy, tightened spacing and reduced the mobile display size.
   - Post-fix evidence: `qa/screenshots/home-mobile-390x844-v2.png` and `qa/screenshots/compare-home-mobile-v2.jpg`.
   - Result: real fish photo fills the upper mobile viewport and the headline begins before the dock.

2. Initial inner-page density finding — P2:
   - Evidence: fish and gallery desktop captures devoted too much of the first viewport to the introduction, leaving insufficient visible image content.
   - Fix: reduced desktop page-hero height and top section padding; replaced the gallery's redundant second heading with a compact status/filter row.
   - Post-fix evidence: `qa/screenshots/fish-desktop-1440x1000-v2.png` and `qa/screenshots/gallery-desktop-1440x1000-v4.png`.
   - Result: fish cards and gallery photography enter the first viewport without crowding the introduction.

## Findings

- No actionable P0, P1 or P2 findings remain.
- P3: the concepts show more inventory density and commerce UI. This is an intentional product constraint because prices, stock, account, cart and checkout data are not confirmed and are outside this static site's authorized scope.
- P3: the original concepts use different fish imagery. The implementation intentionally prioritizes the user's real photos over visual imitation.

## Primary interactions tested

- Desktop and mobile navigation.
- Mobile menu open, close, Escape-ready state and body scroll lock.
- Fish JSON loading: eight initial cards.
- Category filter: star-point category returns two cards.
- Search within selected category: “藍點” returns one matching card.
- Dynamic detail query: correct title, image and care data for `gold-spotted` and `light-stripe`.
- Contact form: required fields, native select, date, summary generation and clipboard copy.
- Eleven routes inspected at 1280 × 900 with no horizontal overflow, broken images, missing image alt or browser console errors.

## Final result

final result: passed
