"""
Simple UI Test - Verify all libraries are working
Run: streamlit run test_ui.py
"""

import streamlit as st

st.set_page_config(page_title="UI Test", page_icon="✅", layout="wide")

st.title("✅ UI Libraries Test")
st.markdown("Testing all installed libraries...")

# Test 1: Basic Streamlit
st.header("1. Basic Streamlit Components")
st.success("✅ Streamlit working!")

col1, col2, col3 = st.columns(3)
col1.metric("Test", "100", "+5%")
col2.button("Click me")
col3.checkbox("Check me")

# Test 2: Plotly
st.header("2. Plotly")
try:
    import plotly.express as px
    import pandas as pd
    import numpy as np

    df = pd.DataFrame({'x': range(10), 'y': np.random.randn(10)})
    fig = px.line(df, x='x', y='y', title="Test Chart")
    st.plotly_chart(fig, use_container_width=True)
    st.success("✅ Plotly working!")
except Exception as e:
    st.error(f"❌ Plotly error: {e}")

# Test 3: Streamlit Extras
st.header("3. Streamlit Extras")
try:
    from streamlit_extras.colored_header import colored_header
    colored_header(label="Colored Header", description="Test", color_name="violet-70")
    st.success("✅ Streamlit Extras working!")
except Exception as e:
    st.error(f"❌ Streamlit Extras error: {e}")

# Test 4: Option Menu
st.header("4. Navigation Menu")
try:
    from streamlit_option_menu import option_menu
    selected = option_menu("Test Menu", ["A", "B", "C"], icons=["star", "heart", "thumbs-up"])
    st.success(f"✅ Option Menu working! Selected: {selected}")
except Exception as e:
    st.error(f"❌ Option Menu error: {e}")

# Test 5: AgGrid
st.header("5. AgGrid")
try:
    from st_aggrid import AgGrid
    test_df = pd.DataFrame({'Name': ['A', 'B'], 'Value': [1, 2]})
    AgGrid(test_df, height=150)
    st.success("✅ AgGrid working!")
except Exception as e:
    st.error(f"❌ AgGrid error: {e}")

# Test 6: Modal
st.header("6. Modal")
try:
    from streamlit_modal import Modal
    if st.button("Open Test Modal"):
        modal = Modal(key="test", title="Test Modal")
        if modal.is_open():
            with modal.container():
                st.write("Modal content!")
                if st.button("Close"):
                    modal.close()
    st.success("✅ Modal working!")
except Exception as e:
    st.error(f"❌ Modal error: {e}")

# Test 7: Shadcn UI
st.header("7. Shadcn UI")
try:
    from streamlit_shadcn_ui import card
    card(title="Test Card", text="This is a test card")
    st.success("✅ Shadcn UI working!")
except Exception as e:
    st.error(f"❌ Shadcn UI error: {e}")

# Test 8: Lottie
st.header("8. Lottie Animation")
try:
    from streamlit_lottie import st_lottie
    st_lottie("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json", height=100, key="test")
    st.success("✅ Lottie working!")
except Exception as e:
    st.error(f"❌ Lottie error: {e}")

st.markdown("---")
st.header("✅ All Tests Complete!")
st.info("If you see all ✅ marks, your UI libraries are working correctly!")
