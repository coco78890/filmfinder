# FilmFinder UI Kit

A hi-fi redesign of the FilmFinder website. The original repo (`coco78890/filmfinder`) is a Streamlit app with default widgets; this kit is the **aspirational visual rebuild** using the tokens defined in `../../colors_and_type.css`.

## Files
- `index.html` — clickable prototype: search → results → subscribe dialog → single-channel view.
- `TopNav.jsx` — sticky top navigation with logo + tabs.
- `SearchHero.jsx` — editorial hero with large serif headline + search input.
- `Filters.jsx` — channel + past-episodes filters (chip rail + toggle).
- `ProgramList.jsx` — a list of `ProgramRow`s with live-now treatment.
- `ProgramRow.jsx` — single broadcast: channel logo, time, title, metadata.
- `CoverageTable.jsx` — EPG coverage per broadcaster.
- `SubscribeDialog.jsx` — email notification signup.
- `NotificationsPage.jsx` — manage active subscriptions.
- `EmptyState.jsx`, `Skeleton.jsx` — supporting states.

## Screens represented
1. **Home / Suche** — hero + suggestions.
2. **Results** — table of hits with live badges + subscribe CTA.
3. **Subscribe dialog** — email capture inline.
4. **Benachrichtigungen** — list of active alerts.

All copy is in German, formal Sie-form, matching the original app's strings.
