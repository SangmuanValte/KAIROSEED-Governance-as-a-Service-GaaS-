import streamlit as st
from core.runtime import kairoseed_run
from core.weekly_integration import weekly_intelligence

# --- Page config ---
st.set_page_config(
    page_title="Kairoseed",
    page_icon="🌱",
    layout="centered"
)

# --- Minimal styling ---
st.markdown("""
    <style>
    .main {
        max-width: 500px;
        margin: auto;
    }
    textarea {
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("## 🌱 Kairoseed")
st.caption("A quiet space to notice what is present.")

st.markdown("---")

# --- Input ---
user_input = st.text_area(
    "Write what is present:",
    height=120,
    placeholder="Something you're holding, thinking, or working through..."
)

# --- Buttons ---
col1, col2 = st.columns(2)

with col1:
    run = st.button("Selah Check")

with col2:
    view_week = st.button("Weekly")

st.markdown("---")

# --- Selah Check Output ---
if run:
    if user_input.strip():
        with st.spinner("..."):
            result = kairoseed_run(user_input)

        st.markdown("### Response")
        st.write(result)
    else:
        st.warning("Write something first.")

# --- Weekly Intelligence ---
if view_week:
    with st.spinner("..."):
        weekly = weekly_intelligence()

    st.markdown("### Weekly Themes")
    st.write(weekly)

# --- Footer ---
st.markdown("---")
st.caption("You may pause. You may stop. Nothing is required.")
