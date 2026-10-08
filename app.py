import pickle
import pandas as pd
import streamlit as st

st.set_page_config(page_title="WasteWeave", page_icon="🧵", layout="wide")

# ================== CHOOSE YOUR COLOR THEME HERE ==================
# Options: "forest", "graphite", "signal", "midnight"
PALETTE = "forest"
# ===================================================================

PALETTES = {
    # Deep forest green + marigold on warm paper
    "forest": dict(PAGE="#F6F2E8", CARD="#FFFDF7", CARD_BORDER="1px solid #D9D2BE", CARD_TOP="4px solid #12372A",
                   CARD_SHADOW="none", RADIUS="8px", HERO_BG="#12372A", HERO_TITLE="#FBF7EC", HERO_SUB="#BFD3C7",
                   HERO_TAG="#F2B01E", HERO_EDGE="#F2B01E", HERO_BORDER="0 solid transparent", HERO_SHADOW="none",
                   BTN_BG="#F2B01E", BTN_TEXT="#12372A", BTN_HOVER="#D99A0E", BTN_BORDER="none", BTN_SHADOW="none",
                   TITLE="#12372A", BADGE_BG="#12372A", BADGE_TEXT="#F2B01E", INPUT_BG="#EFE9D8", SIDEBAR_BG="#E8E1CD",
                   TEXT="#1F2A24", LOGO_TILE="#FBF7EC", LOGO_H="#F2B01E", LOGO_V="#12372A"),
    # Charcoal + acid lime
    "graphite": dict(PAGE="#EDEDE8", CARD="#F9F9F6", CARD_BORDER="1px solid #CFCFC8", CARD_TOP="4px solid #1B1D21",
                     CARD_SHADOW="none", RADIUS="10px", HERO_BG="#1B1D21", HERO_TITLE="#FFFFFF", HERO_SUB="#B8BBC2",
                     HERO_TAG="#C6F432", HERO_EDGE="#C6F432", HERO_BORDER="0 solid transparent", HERO_SHADOW="none",
                     BTN_BG="#1B1D21", BTN_TEXT="#C6F432", BTN_HOVER="#000000", BTN_BORDER="none", BTN_SHADOW="none",
                     TITLE="#1B1D21", BADGE_BG="#C6F432", BADGE_TEXT="#1B1D21", INPUT_BG="#E7E7E1", SIDEBAR_BG="#E2E2DC",
                     TEXT="#1B1D21", LOGO_TILE="#FFFFFF", LOGO_H="#9BC400", LOGO_V="#1B1D21"),
    # Bold black outlines + signal orange (poster / editorial style)
    "signal": dict(PAGE="#F7F6F2", CARD="#FFFFFF", CARD_BORDER="2px solid #111111", CARD_TOP="2px solid #111111",
                   CARD_SHADOW="5px 5px 0 #111111", RADIUS="0px", HERO_BG="#FFFFFF", HERO_TITLE="#111111",
                   HERO_SUB="#444444", HERO_TAG="#E8420F", HERO_EDGE="#FF4B1F", HERO_BORDER="3px solid #111111",
                   HERO_SHADOW="6px 6px 0 #111111", BTN_BG="#FF4B1F", BTN_TEXT="#111111", BTN_HOVER="#FF6A45",
                   BTN_BORDER="2px solid #111111", BTN_SHADOW="4px 4px 0 #111111", TITLE="#111111",
                   BADGE_BG="#111111", BADGE_TEXT="#FFFFFF", INPUT_BG="#F1F0EA", SIDEBAR_BG="#EFEEE8",
                   TEXT="#111111", LOGO_TILE="#111111", LOGO_H="#FF4B1F", LOGO_V="#FFFFFF"),
    # Midnight navy + mint
    "midnight": dict(PAGE="#F1F5F4", CARD="#FFFFFF", CARD_BORDER="1px solid #D3DDDA", CARD_TOP="4px solid #0E1A2B",
                     CARD_SHADOW="none", RADIUS="10px", HERO_BG="#0E1A2B", HERO_TITLE="#FFFFFF", HERO_SUB="#A9B8CC",
                     HERO_TAG="#3DDC97", HERO_EDGE="#3DDC97", HERO_BORDER="0 solid transparent", HERO_SHADOW="none",
                     BTN_BG="#3DDC97", BTN_TEXT="#0E1A2B", BTN_HOVER="#2BC783", BTN_BORDER="none", BTN_SHADOW="none",
                     TITLE="#0E1A2B", BADGE_BG="#0E1A2B", BADGE_TEXT="#3DDC97", INPUT_BG="#E6EDEB", SIDEBAR_BG="#E1E9E7",
                     TEXT="#0E1A2B", LOGO_TILE="#FFFFFF", LOGO_H="#3DDC97", LOGO_V="#0E1A2B"),
}
P = PALETTES[PALETTE]

# ---------- Styling (CSS) ----------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Work+Sans:wght@400;500;600&display=swap');
#MainMenu, footer {visibility: hidden;}
.stApp {background: __PAGE__; color: __TEXT__;}
.block-container {padding-top: 1.6rem; max-width: 1100px;}
[data-testid="stSidebar"] {background: __SIDEBAR_BG__;}

.hero {background-color: __HERO_BG__;
       background-image: repeating-linear-gradient(0deg, rgba(255,255,255,0.04) 0 2px, transparent 2px 9px),
                         repeating-linear-gradient(90deg, rgba(255,255,255,0.04) 0 2px, transparent 2px 9px);
       border: __HERO_BORDER__; border-bottom: 8px solid __HERO_EDGE__; box-shadow: __HERO_SHADOW__;
       border-radius: __RADIUS__; padding: 30px 34px; display: flex; align-items: center; gap: 24px; margin-bottom: 28px;}
.hero svg {flex-shrink: 0;}
.hero h1 {font-family: 'Fraunces', serif; color: __HERO_TITLE__; margin: 0; font-size: 2.6rem; font-weight: 700;}
.hero p {font-family: 'Work Sans', sans-serif; color: __HERO_SUB__; margin: 6px 0 12px 0; font-size: 1.05rem;}
.tags {font-family: 'Work Sans', sans-serif; color: __HERO_TAG__; font-size: 0.78rem; font-weight: 600;
       letter-spacing: 1.6px; text-transform: uppercase;}
@media (max-width: 640px) {.hero {flex-direction: column; align-items: flex-start; padding: 22px;}
                           .hero h1 {font-size: 2rem;}}

[data-testid="stVerticalBlockBorderWrapper"], [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .card-title) {background: __CARD__; border: __CARD_BORDER__ !important;
        border-top: __CARD_TOP__ !important; border-radius: __RADIUS__ !important; box-shadow: __CARD_SHADOW__;}
.card-title {font-family: 'Fraunces', serif; font-weight: 700; font-size: 1.25rem; color: __TITLE__; margin-bottom: 12px;}
.card-title .num {display: inline-block; background: __BADGE_BG__; color: __BADGE_TEXT__; font-size: 0.85rem;
        padding: 3px 8px; margin-right: 10px; border-radius: 3px; font-family: 'Work Sans', sans-serif;}

div[data-baseweb="input"], div[data-baseweb="base-input"], div[data-baseweb="select"] > div {background-color: __INPUT_BG__ !important;}

[data-testid="stElementContainer"]:has([data-testid="stButton"]) {width: 100% !important;}
[data-testid="stButton"], div.stButton {width: 100% !important;}
[data-testid="stButton"] > button, div.stButton > button {width: 100% !important; background: __BTN_BG__; color: __BTN_TEXT__;
        border: __BTN_BORDER__; box-shadow: __BTN_SHADOW__; border-radius: __RADIUS__; padding: 0.85rem 1rem;
        font-family: 'Work Sans', sans-serif; font-size: 1rem; font-weight: 600; letter-spacing: 2px; text-transform: uppercase;}
div.stButton > button:hover {background: __BTN_HOVER__; color: __BTN_TEXT__;}
div.stButton > button:focus {color: __BTN_TEXT__;}

.result {border-radius: __RADIUS__; padding: 26px 30px; color: #FFFFFF; margin-top: 24px; text-align: center;
         border-top: 8px solid rgba(0,0,0,0.25); font-family: 'Work Sans', sans-serif;}
.result .title {font-size: 0.85rem; letter-spacing: 2px; text-transform: uppercase; font-weight: 600; opacity: 0.92;}
.result .level {font-family: 'Fraunces', serif; font-size: 1.8rem; font-weight: 700; margin-top: 2px;}
.result .msg {font-size: 1rem; opacity: 0.95; margin-top: 4px;}

.side-title {font-family: 'Fraunces', serif; color: __TITLE__; font-weight: 700; font-size: 1.2rem; margin-top: 6px;}
.footer {text-align: center; color: #6F6F6F; font-size: 0.85rem; margin-top: 34px; font-family: 'Work Sans', sans-serif;}
</style>
"""
for key, value in P.items():
    CSS = CSS.replace(f"__{key}__", value)
st.markdown(CSS, unsafe_allow_html=True)

# ---------- Logo (SVG weave pattern) ----------
LOGO = f"""<svg width="76" height="76" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
<rect width="64" height="64" rx="8" fill="{P['LOGO_TILE']}"/>
<rect x="10" y="12" width="44" height="10" rx="2" fill="{P['LOGO_H']}"/>
<rect x="10" y="27" width="44" height="10" rx="2" fill="{P['LOGO_H']}"/>
<rect x="10" y="42" width="44" height="10" rx="2" fill="{P['LOGO_H']}"/>
<rect x="12" y="8" width="10" height="48" rx="2" fill="{P['LOGO_V']}"/>
<rect x="27" y="8" width="10" height="48" rx="2" fill="{P['LOGO_V']}"/>
<rect x="42" y="8" width="10" height="48" rx="2" fill="{P['LOGO_V']}"/>
<rect x="12" y="12" width="10" height="10" fill="{P['LOGO_H']}"/>
<rect x="42" y="12" width="10" height="10" fill="{P['LOGO_H']}"/>
<rect x="27" y="27" width="10" height="10" fill="{P['LOGO_H']}"/>
<rect x="12" y="42" width="10" height="10" fill="{P['LOGO_H']}"/>
<rect x="42" y="42" width="10" height="10" fill="{P['LOGO_H']}"/>
</svg>"""

st.markdown(f"""
<div class="hero">
{LOGO}
<div>
<h1>WasteWeave</h1>
<p>Predict yield loss in weaving from your order specifications</p>
<div class="tags">Real factory data &nbsp;·&nbsp; Machine learning &nbsp;·&nbsp; Instant prediction</div>
</div>
</div>
""", unsafe_allow_html=True)

# ---------- Load model ----------
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("model.pkl was not found. Please place it in the same folder as app.py.")
    st.stop()

months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<div class="side-title">About WasteWeave</div>', unsafe_allow_html=True)
    st.write("WasteWeave uses a machine learning model trained on real weaving "
             "production data to estimate the yield loss (act_shrink %) of an order.")
    st.markdown('<div class="side-title">How it works</div>', unsafe_allow_html=True)
    st.write("1. Enter the order details\n\n2. Click **Predict**\n\n3. Read the expected yield loss")
    st.caption("This is an indicative estimate and should not be used as the only basis for production decisions.")

# ---------- Inputs ----------
left, right = st.columns(2, gap="large")

with left:
    with st.container(border=True):
        st.markdown('<div class="card-title"><span class="num">01</span>Order details</div>', unsafe_allow_html=True)
        month = st.selectbox("Month", months)
        req_fabric = st.number_input("Required finished fabric", value=10000)
        beam_len = st.number_input("Recommended beam length (yds)", value=3000.0)

with right:
    with st.container(border=True):
        st.markdown('<div class="card-title"><span class="num">02</span>Fabric specifications</div>', unsafe_allow_html=True)
        a1, a2 = st.columns(2)
        allowance = a1.number_input("Fabric allowance", value=7.0)
        shrink_allow = a2.number_input("Shrinkage allowance", value=12.5)
        warp = st.selectbox("Warp count", ["40", "50", "double"])
        c1, c2, c3 = st.columns(3)
        weft = c1.number_input("Weft count", value=40)
        epi = c2.number_input("EPI", value=110, help="Ends per inch")
        ppi = c3.number_input("PPI", value=80, help="Picks per inch")

st.write("")
predict = st.button("Predict yield loss")

# ---------- Prediction ----------
if predict:
    # same encoding as in training
    month_number = months.index(month)          # ordinal: January = 0 ... December = 11
    warp_40 = 1 if warp == "40" else 0          # one-hot: 3 columns
    warp_50 = 1 if warp == "50" else 0
    warp_double = 1 if warp == "double" else 0

    # column names and order must match training
    row = pd.DataFrame([[month_number, req_fabric, allowance, beam_len,
                         shrink_allow, weft, epi, ppi,
                         warp_40, warp_50, warp_double]],
                       columns=["Month", "Req_Finish_Fabrics", "Fabric_Allowance",
                                "Rec_Beam_length(yds)", "Shrink_allow", "weft_count",
                                "epi", "ppi", "warp_count_40", "warp_count_50",
                                "warp_count_double"])

    result = max(float(model.predict(row)[0]), 0.0)

    # level bands (illustrative, change as you like)
    if result < 10:
        bg, level, msg = "#2F7A56", "Low yield loss", "This order is expected to run efficiently."
    elif result < 20:
        bg, level, msg = "#B9801A", "Medium yield loss", "Moderate loss expected. Keep an eye on this order."
    else:
        bg, level, msg = "#B63A2B", "High yield loss", "High loss expected. Review the order specifications."

    arc = min(result / 50, 1) * 251.3           # gauge: 0% to 50%+
    gauge = f"""<svg width="270" viewBox="0 0 200 125" xmlns="http://www.w3.org/2000/svg">
<path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="14"/>
<path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#FFFFFF" stroke-width="14" stroke-dasharray="{arc} 251.3"/>
<text x="100" y="92" text-anchor="middle" font-size="30" font-weight="700" fill="#FFFFFF" font-family="Fraunces, serif">{result:.1f}%</text>
<text x="20" y="120" text-anchor="middle" font-size="10" fill="#FFFFFF">0%</text>
<text x="180" y="120" text-anchor="middle" font-size="10" fill="#FFFFFF">50%+</text>
</svg>"""

    st.markdown(f"""
<div class="result" style="background:{bg}">
<div class="title">Expected yield loss (act_shrink %)</div>
{gauge}
<div class="level">{level}</div>
<div class="msg">{msg}</div>
</div>
""", unsafe_allow_html=True)
    st.caption("Level bands (10% and 20%) are illustrative only. The model's estimate can differ noticeably from the actual value.")

st.markdown('<div class="footer">WasteWeave · Predictive analytics for textile weaving</div>', unsafe_allow_html=True)