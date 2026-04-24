---
name: filmfinder-design
description: Use this skill to generate well-branded interfaces and assets for FilmFinder, either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.
If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.
If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## What's here
- `README.md` — brand context, content fundamentals, visual foundations, iconography.
- `colors_and_type.css` — ready-to-import CSS custom properties + type roles.
- `assets/logo.svg`, `assets/favicon.svg`, `assets/channels/*.svg` — logos and 30 German broadcaster monograms.
- `preview/` — small showcase cards for the tokens and components.
- `ui_kits/filmfinder/` — full hi-fi web redesign (React via Babel) — useful as a component reference.

## Hard rules
- German, Sie-form. Never "du", never first person.
- No emoji in UI copy.
- Use Source Serif 4 for editorial heads; Work Sans for UI; JetBrains Mono for times.
- Accent is signal red `#D8352A`. Paper background `#FBF8F3`. Never bluish-purple gradients.
- Broadcaster logos must come from `assets/channels/` — do not invent or redraw.
