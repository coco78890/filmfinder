"""FilmFinder — inject design-system CSS into Streamlit.

Usage in app.py (add AFTER st.set_page_config and BEFORE any other widgets):

    from src.ui.theme import inject_theme
    inject_theme()

This reads the FilmFinder design tokens and applies them to Streamlit's
built-in widgets via a single <style> block with !important overrides.
It is the maximum amount of the design system Streamlit can support without
re-architecting away from it.
"""

import streamlit as st


_CSS = """
<style>
/* ===== FilmFinder Design System — Streamlit override layer ===== */

@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&family=Work+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --ff-paper-0: #FFFFFF;
  --ff-paper-50: #FBF8F3;
  --ff-paper-100: #F6F1E8;
  --ff-paper-200: #E8E3D9;
  --ff-ink-900: #141414;
  --ff-ink-500: #5C5A54;
  --ff-ink-400: #8F887B;
  --ff-red-600: #D8352A;
  --ff-red-700: #B22820;
  --ff-red-100: #FBE8E6;
  --ff-green-600: #1F7A4D;
  --ff-font-serif: "Source Serif 4", Georgia, serif;
  --ff-font-sans:  "Work Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  --ff-font-mono:  "JetBrains Mono", ui-monospace, Menlo, Consolas, monospace;
}

/* ---------- Base ---------- */
html, body, [data-testid="stAppViewContainer"] {
  background: var(--ff-paper-50) !important;
  font-family: var(--ff-font-sans) !important;
  color: var(--ff-ink-900) !important;
}

/* Page padding + max width */
.main .block-container {
  max-width: 1200px !important;
  padding-top: 2rem !important;
  padding-bottom: 4rem !important;
}

/* ---------- Typography ---------- */
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
  font-family: var(--ff-font-serif) !important;
  font-weight: 500 !important;
  letter-spacing: -0.02em !important;
  color: var(--ff-ink-900) !important;
}
h1, .stMarkdown h1 { font-size: 2.5rem !important; line-height: 1.15 !important; }
h2, .stMarkdown h2 { font-size: 1.75rem !important; line-height: 1.25 !important; }
h3, .stMarkdown h3 { font-size: 1.25rem !important; font-family: var(--ff-font-sans) !important; font-weight: 600 !important; }

/* Headers (st.header) */
[data-testid="stHeader"] { background: transparent !important; }

.stCaption, .stMarkdown small {
  color: var(--ff-ink-500) !important;
  font-family: var(--ff-font-serif) !important;
  font-style: italic !important;
  font-size: 1rem !important;
}

/* ---------- Tabs ---------- */
[data-baseweb="tab-list"] {
  border-bottom: 1px solid var(--ff-paper-200) !important;
  gap: 4px !important;
}
[data-baseweb="tab"] {
  font-family: var(--ff-font-sans) !important;
  font-weight: 500 !important;
  color: var(--ff-ink-500) !important;
  padding: 10px 16px !important;
  border-radius: 4px 4px 0 0 !important;
}
[data-baseweb="tab"][aria-selected="true"] {
  color: var(--ff-red-600) !important;
  border-bottom: 2px solid var(--ff-red-600) !important;
}

/* ---------- Buttons ---------- */
.stButton > button {
  font-family: var(--ff-font-sans) !important;
  font-weight: 500 !important;
  font-size: 14px !important;
  border-radius: 4px !important;
  padding: 10px 16px !important;
  border: 1px solid var(--ff-paper-200) !important;
  background: var(--ff-paper-0) !important;
  color: var(--ff-ink-900) !important;
  transition: background 120ms ease !important;
}
.stButton > button:hover {
  background: var(--ff-paper-100) !important;
  border-color: var(--ff-paper-200) !important;
}
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {
  background: var(--ff-red-600) !important;
  color: #fff !important;
  border-color: var(--ff-red-600) !important;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover {
  background: var(--ff-red-700) !important;
  border-color: var(--ff-red-700) !important;
}

/* Form submit button */
[data-testid="stFormSubmitButton"] > button {
  background: var(--ff-red-600) !important;
  color: #fff !important;
  border-color: var(--ff-red-600) !important;
}

/* ---------- Inputs ---------- */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea textarea {
  font-family: var(--ff-font-sans) !important;
  font-size: 15px !important;
  background: var(--ff-paper-0) !important;
  border-radius: 4px !important;
  border-color: var(--ff-paper-200) !important;
  color: var(--ff-ink-900) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
  border-color: var(--ff-red-600) !important;
  box-shadow: 0 0 0 2px var(--ff-red-100) !important;
}
.stTextInput label, .stSelectbox label, .stTextArea label, .stCheckbox label {
  font-family: var(--ff-font-sans) !important;
  font-weight: 500 !important;
  color: var(--ff-ink-900) !important;
  font-size: 13px !important;
}

/* ---------- Dataframe / tables ---------- */
[data-testid="stDataFrame"] {
  border: 1px solid var(--ff-paper-200) !important;
  border-radius: 8px !important;
  overflow: hidden !important;
  background: var(--ff-paper-0) !important;
  box-shadow: 0 1px 0 rgba(20,20,20,0.04) !important;
}
[data-testid="stDataFrame"] table {
  font-family: var(--ff-font-sans) !important;
  font-size: 14px !important;
}
[data-testid="stDataFrame"] th {
  background: var(--ff-paper-100) !important;
  color: var(--ff-ink-500) !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  font-size: 11px !important;
  letter-spacing: 0.04em !important;
}

/* Mono-ish columns (time/date) — Streamlit can't easily target per-column,
   so we at least get tabular numerics across the board */
[data-testid="stDataFrame"] td {
  font-variant-numeric: tabular-nums !important;
  color: var(--ff-ink-900) !important;
}

/* ---------- Expander ---------- */
[data-testid="stExpander"] {
  border: 1px solid var(--ff-paper-200) !important;
  border-radius: 8px !important;
  background: var(--ff-paper-0) !important;
  box-shadow: 0 1px 0 rgba(20,20,20,0.04) !important;
}
[data-testid="stExpander"] summary {
  font-family: var(--ff-font-sans) !important;
  font-weight: 500 !important;
  color: var(--ff-ink-900) !important;
}

/* ---------- Alerts (success/info/warning/error) ---------- */
[data-testid="stAlert"] {
  border-radius: 8px !important;
  border: 1px solid transparent !important;
  font-family: var(--ff-font-sans) !important;
  font-size: 14px !important;
}
[data-testid="stAlert"][data-baseweb="notification"] { padding: 12px 16px !important; }

/* Success → green tint */
div[data-baseweb="notification"][kind="success"],
[data-testid="stAlert"] div[data-baseweb="notification"][role="alert"][data-testid="stAlertContentSuccess"] {
  background: #E3F1E9 !important;
  color: #155A38 !important;
}
/* Info → paper */
[data-testid="stAlertContentInfo"] {
  background: #E1ECF7 !important;
  color: #1F5592 !important;
}
/* Warning */
[data-testid="stAlertContentWarning"] {
  background: #FAEFD0 !important;
  color: #9A6900 !important;
}
/* Error → accent tint */
[data-testid="stAlertContentError"] {
  background: var(--ff-red-100) !important;
  color: var(--ff-red-700) !important;
}

/* ---------- Form container ---------- */
[data-testid="stForm"] {
  background: var(--ff-paper-0) !important;
  border: 1px solid var(--ff-paper-200) !important;
  border-radius: 8px !important;
  padding: 20px !important;
  box-shadow: 0 1px 0 rgba(20,20,20,0.04) !important;
}

/* ---------- Spinner ---------- */
.stSpinner > div > div { border-top-color: var(--ff-red-600) !important; }
</style>
"""


def inject_theme() -> None:
    """Inject the FilmFinder CSS overrides. Call once, right after st.set_page_config."""
    st.markdown(_CSS, unsafe_allow_html=True)


def hero() -> None:
    """Render a serif editorial hero block above the search input."""
    st.markdown(
        """
        <div style="margin: 8px 0 32px;">
          <div style="font-size:11px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:#8F887B;margin-bottom:12px;display:flex;align-items:center;gap:8px;">
            <span style="width:6px;height:6px;border-radius:99px;background:#D8352A;display:inline-block"></span>
            Freies Fernsehen · durchsuchbar
          </div>
          <h1 style="font-family:'Source Serif 4',Georgia,serif;font-size:3rem;font-weight:500;line-height:1.1;letter-spacing:-0.02em;margin:0 0 12px;color:#141414;">
            Wann läuft <span style="color:#D8352A;">Ihr Film</span> <em style="color:#8F887B;font-weight:400;">im Fernsehen?</em>
          </h1>
          <p style="font-family:'Source Serif 4',Georgia,serif;font-style:italic;font-size:18px;color:#5C5A54;max-width:640px;margin:0;">
            Durchsuchen Sie das Programm von über 30 deutschen Sendern — und lassen Sie sich benachrichtigen, sobald Ihre Sendung wieder erscheint.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
