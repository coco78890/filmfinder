# Integrating FilmFinder Design System into your Streamlit app

This folder is a **drop-in theme layer** for the existing `coco78890/filmfinder` Streamlit app. It is the maximum amount of the design system Streamlit can render without re-architecting the UI.

## What you get
- **Colors**: paper background, signal-red primary, ink text, warm neutrals.
- **Fonts**: Source Serif 4 (headings, captions) + Work Sans (UI) via Google Fonts.
- **Overrides** for: buttons, inputs, tabs, dataframes, alerts, expanders, forms, form-submit buttons, spinners.
- **A serif editorial hero** component to swap in above the search input.

## What you don't get (Streamlit limits)
- Channel-logo chip rail, per-program cards, the "Jetzt live" red bar, the custom subscribe dialog, and the hand-tuned program rows are all **not representable** with Streamlit's widget set. Those require the full React prototype under `ui_kits/filmfinder/`.

If you want the full design, you'd need to migrate off Streamlit. This folder stops at the 20% that Streamlit can render.

---

## Integration steps (≈10 minutes)

### 1. Copy two files into your repo

From this project into your `coco78890/filmfinder` checkout:

```bash
# from your filmfinder repo root:
cp path/to/streamlit_integration/.streamlit/config.toml  .streamlit/config.toml
cp path/to/streamlit_integration/theme.py                src/ui/theme.py
```

The `config.toml` overwrites your existing one — it uses the design-system palette for Streamlit's built-in theming hooks (`primaryColor`, `backgroundColor`, `secondaryBackgroundColor`, `textColor`, `font`).

### 2. Wire up `theme.py` in `app.py`

Edit `app.py`. Find the existing `st.set_page_config(...)` call and add **two** imports + one call right after it:

```python
import streamlit as st
from src.ui.theme import inject_theme   # ← add

st.set_page_config(
    page_title="FilmFinder",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_theme()   # ← add this line
```

Everything after that point renders with the FilmFinder palette + typeface.

### 3. (Optional) Use the editorial hero on the search page

Edit `src/ui/pages/search.py`. At the top of `render_search_page()`, **replace**:

```python
st.header("Suche")
```

with:

```python
from src.ui.theme import hero
hero()
```

You'll lose the "Suche" tab heading but gain a real editorial hero block above the search input.

### 4. Commit + push

```bash
git add .streamlit/config.toml src/ui/theme.py app.py src/ui/pages/search.py
git commit -m "Apply FilmFinder design system theme"
git push
```

---

## Publishing to Streamlit Community Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub.
2. Click **New app** → pick `coco78890/filmfinder`, branch `main`, main file `app.py`.
3. Expand **Advanced settings** → paste any SMTP/Supabase secrets from `config/settings.py`:
   ```
   FILMFINDER_SMTP_HOST="smtp.gmail.com"
   FILMFINDER_SMTP_USER="you@gmail.com"
   FILMFINDER_SMTP_PASSWORD="app-password-here"
   FILMFINDER_SMTP_FROM="you@gmail.com"
   ```
4. Click **Deploy**. First build takes ~2 minutes (pip install).
5. You'll get a URL like `https://filmfinder-<hash>.streamlit.app`.

Streamlit Cloud auto-redeploys on every push to `main`.

### Notes
- Streamlit Cloud runs one Python process per app — the in-process `_run_daily_notification_check()` in `app.py` will fire on cold start but won't run reliably "daily". For real daily notifications, keep `check_notifications.py` running on a **separate** cron (GitHub Actions works — see the `.github/` folder in your repo).
- Free tier sleeps after inactivity. First visitor after that waits ~30s for wake.
- Google-font imports work fine in Streamlit Cloud — no extra config.

---

## Troubleshooting

**"My buttons don't turn red."**
Streamlit versions before 1.30 use different `data-testid` attributes. Your `requirements.txt` pins `streamlit>=1.30.0` so this should be fine — if not, upgrade: `pip install -U streamlit`.

**"Fonts look the same as before."**
Check the browser's Network tab for the Google Fonts request. Streamlit Cloud's Content-Security-Policy sometimes blocks external fonts on very old builds — in that case, fall back to the system serif by editing the `--ff-font-serif` var in `theme.py`.

**"I want to disable the theme temporarily."**
Comment out the `inject_theme()` call in `app.py`. The `config.toml` changes are easier to roll back by restoring the old `primaryColor = "#1E88E5"`.
