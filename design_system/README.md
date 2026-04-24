# FilmFinder Design System

> A German-language web app to search free-to-air TV listings and get email notifications when films or shows air.

## What FilmFinder is

FilmFinder is a search tool for German linear television. A user types a film or show name (e.g. *Tatort*, *James Bond*, *Krimi*), optionally filters by channel, and gets a list of upcoming broadcasts across **free-to-air German TV** — public broadcasters (ARD, ZDF, arte, 3sat, the regional "Dritte" like WDR/NDR/BR…) and private channels (RTL, SAT.1, ProSieben, VOX, kabel eins, …). If a title isn't airing soon, the user can subscribe by email and be notified when it appears in a future schedule.

Data comes from two sources:
- **MagentaTV EPG API** — live electronic program guide, 48-hour window
- **MediathekViewWeb API** — public broadcaster mediatheken (catch-up)

Search uses fuzzy matching (RapidFuzz), weighting partial-ratio and token-set ratios so users don't have to type exact titles. A background job (`check_notifications.py`) runs daily, re-runs each active subscription, and sends SMTP email alerts for new matches.

### Source material

Everything here is derived from the **`coco78890/filmfinder`** GitHub repo (main branch). Key files read:

- `app.py` — Streamlit entry, two tabs: *Suche* / *Benachrichtigungen*
- `src/ui/pages/search.py` — the main search interface (input, filters, results table, coverage table, inline notification signup)
- `src/ui/pages/notifications.py` — subscription form
- `src/ui/pages/favorites.py` — session-based favorites list
- `config/channels.py` — canonical list of German broadcasters
- `config/settings.py` — API URLs, fuzzy-search weights, SMTP config
- `.streamlit/config.toml` — the only existing theme file (primaryColor `#1E88E5`, sans-serif)
- `src/notifications/notify.py` — SMTP email sender with plain + HTML bodies
- `src/scrapers/magentatv.py`, `src/scrapers/mediathekview.py` — EPG/Mediathek fetchers
- `src/search/engine.py` — fuzzy search

> **Note:** the existing UI is pure Streamlit with default widgets — there is no custom design system in the repo. This project therefore creates an **aspirational redesign** grounded in the product's domain (German free TV, editorial/newsprint adjacency, broadcaster branding) rather than copying Streamlit's look.

---

## Product & context

- **Users**: German-speaking viewers, skewing a bit older (the free-TV / "kostenloses Fernsehen" audience is not Netflix-native). They are used to the visual language of the TV-Zeitschrift (TV-Spielfilm, Hörzu, TV Digital) — dense grids, channel logos, bold titles, time columns.
- **Core jobs**:
  1. *"Wann läuft X?"* — when does my show air?
  2. *"Erinnere mich"* — notify me by email when it returns.
  3. *"Was läuft auf Sender Y?"* — browse a single channel.
- **Tone**: helpful, formal-ish German (Sie-form), direct, no marketing fluff.
- **Not in scope** for the existing app: streaming paywalls, accounts, recommendations, mobile push. This redesign keeps that scope.

---

## CONTENT FUNDAMENTALS

Observed from the Streamlit source strings and the SMTP email templates.

### Language & form of address
- **German, Sie-form throughout**. Examples from the codebase:
  - "Bitte geben Sie eine gueltige E-Mail-Adresse ein."
  - "Lassen Sie sich per E-Mail benachrichtigen, wenn ein gewünschter Film oder eine Sendung im Programm erscheint."
  - "Nutzen Sie zuerst die Suche."
- Never "du". Never first-person ("ich"). The product refers to itself as *"Ihr FilmFinder"* ("Yours, FilmFinder") in email sign-offs — warm but formal.

### Microcopy patterns
- **Buttons are imperative verbs**: *Suchen*, *Hinzufügen*, *Entfernen*, *Benachrichtigung erstellen*.
- **Labels are nouns**: *Suchbegriff*, *Sender*, *E-Mail-Adresse*, *Datum*, *Uhrzeit*, *Titel*, *Beschreibung*.
- **Placeholders teach by example**: `"z.B. Tatort, James Bond, Krimi..."` — "e.g." prefix + real German titles + ellipsis. Always real shows, never lorem-ipsum.
- **Success messages name the thing**: *"'Tatort' wurde zu den Favoriten hinzugefügt."* — quote the user's input back in single-quotes.
- **Result counts are parenthetical**: `Ergebnisse für "Tatort" (14 Treffer)` — query in double-quotes, count + noun in parens.
- **Relative-time phrasing** for EPG coverage: *"2,3 Std."*, *"1,8 Tage"*, *"Keine zukünftigen Daten"* — German decimal comma, abbreviated units.

### Casing
- **Section headers: Title Case in German** (i.e. noun-case — *Neue Benachrichtigung einrichten*, *Abdeckung pro Sender*). Nouns capitalized per German orthography.
- **Buttons: Sentence case** — *Suchen*, *Benachrichtigung einrichten*. Never ALL CAPS.
- **Table columns: single word when possible** — *Sender*, *Datum*, *Uhrzeit*, *Titel*.

### Tone & vibe
- Utilitarian, helpful, a little warm at the edges (the email sign-off). Think **Öffentlich-rechtlich** (public-service) voice: reliable, plainspoken, no hype.
- **No emoji** in UI copy. The app icon is `🎬` in `st.set_page_config` but that's the browser favicon only — nothing in-product uses emoji.
- **No exclamation points** except one success confirmation (*"… wurde eingerichtet!"*). Restraint is the default.
- **Technical errors are translated** into user language: "Bitte geben Sie eine gültige E-Mail-Adresse ein" instead of a validation regex complaint.

### Example copy inventory (verbatim from source)
- Page headers: *Suche*, *Benachrichtigungen*, *Favoriten*
- Tab labels: *Suche*, *Benachrichtigungen*
- Section headers: *Neue Benachrichtigung einrichten*, *Abdeckung pro Sender*, *Programmabdeckung pro Sender*, *Neuen Favoriten hinzufügen*
- Filters: *Sender*, *Alle Sender*, *Vergangene Sendungen anzeigen*
- Empty states: *"Keine Treffer gefunden. Versuchen Sie einen anderen Suchbegriff."*, *"Noch keine Favoriten gespeichert. Fügen Sie welche über die Suche hinzu."*
- Email body: opens with *"Hallo,"*, closes with *"Viele Grüße, Ihr FilmFinder"*.

---

## VISUAL FOUNDATIONS

The existing Streamlit app has **no visual identity** beyond its single `primaryColor = "#1E88E5"` (Material blue). This section defines the aspirational system we're introducing — calibrated to the product domain (German free TV, print-heritage TV guides, broadcaster logos).

### Palette philosophy
A **warm paper-neutral background** (off-white with a whisper of cream, like a TV-Zeitschrift page) against **ink-near-black text** and a single **vivid broadcast red** as the accent (echoing the ARD/Tagesschau red that's visually synonymous with German public TV). Channel logos carry their own colors; the UI chrome stays neutral so they pop.

- **Neutrals**: paper `#FBF8F3`, ink `#141414`, warm grays (`#E8E3D9`, `#8F887B`).
- **Accent**: signal red `#D8352A` for primary CTAs, "live now" badges, and focus rings.
- **Semantic**: green `#1F7A4D` (notified/saved), amber `#C98A00` (upcoming soon), info blue `#2C6FB8` (links).
- **No gradients for backgrounds** — paper is paper. A single subtle vertical gradient is allowed on the hero search bar to suggest depth.

### Typography
- **Display / headings**: **Fraunces** substituted with a neutral serif feel — actually we use **GT Sectra**-alike via **Source Serif 4** (Google Fonts fallback). Serif heads evoke newsprint + TV-guide editorial heritage, and distance us from generic SaaS sans.
- **Body + UI**: **Inter** substituted — actually **Work Sans** — humanist sans, German-diacritic-friendly, good at small sizes.
- **Tabular / times**: **JetBrains Mono** — for broadcast times (`20:15`) where columnar alignment matters.
- **Scale** (rem, base 16): `0.75 / 0.875 / 1 / 1.125 / 1.25 / 1.5 / 2 / 2.5 / 3.25`.
- **Weights**: Serif 400/500/600. Sans 400/500/600. Never 700+; keep it editorial.

> **Font substitution flagged**: the repo ships no font files. If you prefer a different pairing (e.g. actual licensed GT Sectra + Söhne, or a broadcaster-specific face like **ARD Sans**), please attach the files and we'll swap them in.

### Spacing
- **4-based scale**: 4, 8, 12, 16, 20, 24, 32, 40, 56, 72, 96.
- **Content width**: 1200px max for dense schedule tables; 680px for form/reading blocks.
- **Generous vertical rhythm** — 32–56px between sections. German compound words are long; cramped rows kill legibility.

### Backgrounds & surfaces
- **Base background**: solid paper `#FBF8F3`.
- **Cards**: white `#FFFFFF` with a 1px warm gray border (`#E8E3D9`) and no shadow (or a whisper-soft `0 1px 0 rgba(20,20,20,0.04)`). Never chunky `box-shadow: 0 10px 40px`.
- **Imagery**: broadcaster logos (SVG, color), program stills if available (full-bleed 16:9 cards, slight warm overlay at 6% to unify). No stock photography, no AI-generated film posters.
- **No repeating textures or patterns** in v1.

### Borders & corners
- **Corner radius**: `4px` on inputs/buttons, `8px` on cards, `999px` on pill badges (channel chips, "Live" indicator). Nothing "squishy" — restraint.
- **Borders**: always `1px`, warm gray. Hairline dividers between table rows.

### Shadows & elevation
- **Level 0**: no shadow (default).
- **Level 1**: `0 1px 0 rgba(20,20,20,0.04)` — cards.
- **Level 2**: `0 8px 24px -12px rgba(20,20,20,0.18)` — dropdowns, menus, modal.
- No inner shadows. No colored shadows.

### States
- **Hover**: darken background by ~4% (e.g. paper card → `#F6F1E8`); never glow, never scale up. Cursor `pointer`.
- **Press**: background darkens another ~4%; no scale animation — TV-guide users don't expect bouncy UI.
- **Focus**: 2px signal-red outline offset 2px. Keyboard-first.
- **Disabled**: 50% opacity, `cursor: not-allowed`, no hover response.

### Animation
- **Philosophy**: minimal, fast, purposeful. We're a tool, not a toy.
- **Durations**: 120ms (hover/focus), 200ms (panel open), 320ms (page transition).
- **Easing**: `cubic-bezier(0.2, 0, 0, 1)` (smooth-out) for enters; linear for simple color swaps.
- **No bounces**, no springs, no parallax.
- **Loaders**: pulsing skeleton rows for the result table, not spinners.

### Transparency & blur
- **Blur is rare**. Reserved for one thing: a sticky search bar that gets `backdrop-filter: blur(12px)` + `rgba(251,248,243,0.85)` when the page scrolls underneath.
- Everything else is opaque. Better contrast, better accessibility.

### Layout rules
- **Sticky elements**: top nav, search bar on scroll (becomes compact).
- **Grid**: 12-col, 24px gutter on desktop; single column stacked on mobile.
- **Channel logos render at 24×24 (inline), 32×32 (filter chips), 48×48 (cards)**. Always padded — never bleed to the edge.
- **Time columns** (`20:15`, `22:00`) are **right-aligned, tabular-nums**.

### "Live now" treatment
A 6px-tall signal-red bar + tiny pulsing dot next to programs currently on air. This is a free-to-air app — *right now* is more important than *this weekend*.

---

## ICONOGRAPHY

The codebase ships **no icons** — Streamlit's defaults do the work. For the redesign we use:

- **[Lucide](https://lucide.dev/)** (CDN) — clean, 1.5px-stroke SVG icons. Free, consistent, and German-diacritic-friendly in a metaphorical sense (minimal, not too Americana). This is a **substitution**, since the original repo had no icon system. If you have a brand icon kit, please attach it.
- **Channel logos** — SVGs should be placed in `assets/channels/` (one per broadcaster: `ard.svg`, `zdf.svg`, `arte.svg`, `rtl.svg`, `sat1.svg`, `prosieben.svg`, etc.). This project stubs them as colored monograms (e.g. "ARD" on #003d7a rounded tile) until real logos are supplied. **Flag**: we intentionally do NOT copy broadcaster logos from the web — those are trademarked. Users or rightsholders must provide them.
- **Emoji**: **never in product UI**. (The `🎬` in `app.py` is favicon-only; kept for now but would become a proper favicon SVG in production.)
- **Unicode characters as icons**: avoided except `•` as a dot separator in metadata rows and `→` in "see all" links.

### Usage rules
- Always 1.5px stroke weight. Never fill + stroke mixed.
- Size: 16/20/24. Never smaller than 16.
- Icon color inherits from text `currentColor`. Accent-red icons only for destructive actions (delete favorite).
- Pair with a text label in 90% of cases; icon-only is acceptable for universally-understood affordances (close, search, bell for notifications).

---

## Index (what's in this folder)

| File / folder | What it is |
| --- | --- |
| `README.md` | This file — brand context, content rules, visual foundations. |
| `SKILL.md` | Agent-Skills compatible entry point. |
| `colors_and_type.css` | All CSS custom properties + base typographic styles. |
| `fonts/` | Web fonts (Google Fonts via CSS import — no local files yet). |
| `assets/` | Logos, channel marks, imagery. |
| `assets/channels/` | Stub channel logos (SVG monograms until real logos attached). |
| `preview/` | Small HTML cards that populate the Design System review tab. |
| `ui_kits/filmfinder/` | React/JSX UI kit — high-fidelity redesign of the website. |

### UI Kits
- **`ui_kits/filmfinder/`** — the website redesign. `index.html` is a clickable prototype showing the search flow, a results view with channel logos and "Live now" indicators, the notification subscribe dialog, and a single-channel listings view.

### Caveats / known substitutions
- **Fonts**: Source Serif 4 + Work Sans via Google Fonts, standing in for a licensed serif/sans pair. Swap if you have a preferred pairing.
- **Channel logos**: stubbed as monogram tiles. Real broadcaster SVGs (ARD, ZDF, RTL, etc.) are trademarked — please drop them into `assets/channels/`.
- **Icons**: Lucide CDN substitution (the repo had none).
- **Visual identity**: the existing app has none; this is a **net-new aspirational system** derived from the product's domain (German free TV, editorial heritage) rather than copied from the source.
