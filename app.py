"""Minimal scrap gold melt-value calculator for Streamlit Community Cloud."""

import streamlit as st

GRAMS_PER_TROY_OZ = 31.1035

PURITY_RATIOS = {
    "24K": 24 / 24,
    "22K": 22 / 24,
    "21K": 21 / 24,
    "18K": 18 / 24,
    "14K": 14 / 24,
    "10K": 10 / 24,
    "9K": 9 / 24,
}

BUYER_RATES = {
    "Pawn shop (~50%)": 0.50,
    "Online buyer (~70%)": 0.70,
    "Jewelry store (~80%)": 0.80,
    "Refinery (~90%)": 0.90,
}


def melt_value(weight_g: float, purity: str, price_24k_per_g: float) -> float:
    ratio = PURITY_RATIOS.get(purity, 14 / 24)
    return weight_g * price_24k_per_g * ratio


st.set_page_config(
    page_title="Scrap Gold Calculator — melt value by karat",
    page_icon="🥇",
    layout="centered",
)

st.title("Scrap gold melt value calculator")
st.caption(
    "Estimate melt value from weight, karat, and spot gold. "
    "For selling jewelry or scrap gold — not a formal appraisal."
)

st.markdown(
    """
**How to use:** Weigh your gold in grams, check the stamp (9K, 14K, 18K, etc.),
and enter today's fine-gold spot price. The result is **melt value** — what the raw
metal is worth before a buyer deducts refining and margin.
"""
)

col1, col2 = st.columns(2)

with col1:
    weight = st.number_input("Weight (grams)", min_value=0.01, value=10.0, step=0.1)
    purity = st.selectbox("Gold purity", list(PURITY_RATIOS.keys()), index=4)

with col2:
    spot_troy_oz = st.number_input(
        "24K spot price (USD per troy oz)",
        min_value=1.0,
        value=2650.0,
        step=10.0,
        help="Check a live gold price feed if you are selling today.",
    )

price_24k_per_g = spot_troy_oz / GRAMS_PER_TROY_OZ
melt = melt_value(weight, purity, price_24k_per_g)
per_gram = melt / weight if weight else 0.0

st.subheader("Results")
st.metric(f"Melt value ({purity}, {weight:g} g)", f"${melt:,.2f}")
st.write(f"**${per_gram:,.2f}** per gram at this purity")

st.markdown("#### Typical buyer offers (% of melt)")
rows = []
for label, rate in BUYER_RATES.items():
    rows.append({"Buyer type": label, "Estimated payout": f"${melt * rate:,.2f}"})
st.table(rows)

st.divider()

st.markdown(
    """
### Before you sell

Sort pieces by karat and weigh separately — mixed lots often get a blended rate
that works against you. Get at least two or three quotes and compare them to melt
minus a reasonable margin (often 10–30% below melt for scrap).

For **live spot prices**, multiple currencies (USD, GBP, EUR), pennyweight and
troy-ounce units, and per-karat tables updated from the market, use this
[scrap gold calculator with live prices](https://mygoldcalc.com/scrap-gold-calculator)
on the web — no sign-up required.
"""
)

st.caption("Educational tool only. Prices move daily; verify with a local buyer or assayer.")
