"""
UI Components Quick Reference - Copy & Paste Examples
======================================================
A handy reference for common UI patterns with all installed libraries.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid
from streamlit_modal import Modal

# ========================================================================
# NAVIGATION
# ========================================================================

# Sidebar Navigation
selected = option_menu(
    menu_title="Main Menu",
    options=["Home", "Data", "Settings", "About"],
    icons=["house", "database", "gear", "info"],
    menu_icon="cast",
    default_index=0,
)

# Horizontal Navigation
selected2 = option_menu(
    None,
    ["Item 1", "Item 2", "Item 3"],
    icons=["star", "heart", "thumbs-up"],
    orientation="horizontal",
)

# ========================================================================
# CHARTS (Plotly)
# ========================================================================

# Line Chart
fig = px.line(df, x='date', y='value', title='Trend Over Time')
st.plotly_chart(fig, use_container_width=True)

# Bar Chart
fig = px.bar(df, x='category', y='count', color='category')
st.plotly_chart(fig)

# Scatter Plot
fig = px.scatter(df, x='x', y='y', color='group', size='size')
st.plotly_chart(fig)

# Pie Chart
fig = px.pie(df, values='count', names='category')
st.plotly_chart(fig)

# Heatmap
fig = px.imshow(df.corr(), text_auto=True)
st.plotly_chart(fig)

# ========================================================================
# DATA TABLES
# ========================================================================

# Simple DataFrame
st.dataframe(df, use_container_width=True)

# Static Table
st.table(df.head())

# AgGrid (Advanced Table)
from st_aggrid import GridOptionsBuilder

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(editable=True, groupable=True)
grid_options = gb.build()

AgGrid(
    df,
    gridOptions=grid_options,
    editable=True,
    height=400,
    theme='streamlit',
)

# ========================================================================
# METRICS & CARDS
# ========================================================================

# Single Metric
st.metric("Revenue", "$12,345", "+15%")

# Metric Columns
col1, col2, col3 = st.columns(3)
col1.metric("Users", "1,234", "+5%")
col2.metric("Sales", "$5,678", "+12%")
col3.metric("Growth", "23%", "+2%")

# Feature Card (from streamlit-extras)
from streamlit_extras.card import card

card(
    title="Card Title",
    text="Card description goes here.",
    image="https://example.com/image.jpg"
)

# ========================================================================
# FORMS & INPUTS
# ========================================================================

# Text Input
name = st.text_input("Enter your name")

# Number Input
age = st.number_input("Age", min_value=0, max_value=120)

# Select Box
option = st.selectbox("Choose one", ["Option A", "Option B", "Option C"])

# Multi Select
options = st.multiselect("Select options", ["A", "B", "C", "D"])

# Slider
value = st.slider("Value", min_value=0, max_value=100, value=50)

# Date Picker
date = st.date_input("Pick a date")

# File Uploader
file = st.file_uploader("Upload file", type=['csv', 'txt', 'pdf'])

# Checkbox
agree = st.checkbox("I agree to the terms")

# Radio Button
choice = st.radio("Choose", ["Option 1", "Option 2"])

# Text Area
message = st.text_area("Message", height=150)

# Form with Submit Button
with st.form("my_form"):
    st.write("Form content")
    text = st.text_input("Text")
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.success(f"Submitted: {text}")

# ========================================================================
# LAYOUTS
# ========================================================================

# Columns
col1, col2 = st.columns(2)
with col1:
    st.write("Column 1")
with col2:
    st.write("Column 2")

# Three Columns
col1, col2, col3 = st.columns(3)

# Tabs
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
with tab1:
    st.write("Content 1")
with tab2:
    st.write("Content 2")
with tab3:
    st.write("Content 3")

# Expander/Accordion
with st.expander("Click to expand"):
    st.write("Hidden content")

# Container
with st.container():
    st.write("Container content")

# ========================================================================
# MODALS & DIALOGS
# ========================================================================

# Modal Dialog
from streamlit_modal import Modal

modal = Modal(
    key="demo_modal",
    title="My Modal",
    padding="20px",
    max_width="500px"
)

if st.button("Open Modal"):
    modal.open()

if modal.is_open():
    with modal.container():
        st.write("Modal content here")
        if st.button("Close"):
            modal.close()

# ========================================================================
# STATUS MESSAGES
# ========================================================================

st.info("ℹ️ Information message")
st.success("✅ Success message")
st.warning("⚠️ Warning message")
st.error("❌ Error message")

# With exception handling
try:
    # Your code
    pass
except Exception as e:
    st.error(f"Error: {e}")

# ========================================================================
# PROGRESS & SPINNERS
# ========================================================================

# Progress Bar
progress = st.progress(0)
for i in range(100):
    progress.progress(i + 1)

# Spinner
with st.spinner('Loading...'):
    import time
    time.sleep(2)
st.success('Done!')

# Status (beta/experimental)
st.status("Processing...")

# ========================================================================
# MEDIA
# ========================================================================

# Image
st.image("path/to/image.jpg", caption="Image Caption")

# Audio
st.audio("path/to/audio.mp3")

# Video
st.video("path/to/video.mp4")

# Camera Input
picture = st.camera_input("Take a picture")

# ========================================================================
# STYLING & THEMING
# ========================================================================

# Markdown Styling
st.markdown("""
# Heading 1
## Heading 2
**Bold text**
*Italic text*
- List item 1
- List item 2
`inline code`
""")

# Custom CSS
st.markdown("""
<style>
    .big-font {
        font-size:20px !important;
        font-weight:bold;
    }
</style>
<span class="big-font">Styled Text</span>
""", unsafe_allow_html=True)

# Colored Header (from streamlit-extras)
from streamlit_extras.colored_header import colored_header

colored_header(
    label="My Header",
    description="Description here",
    color_name="violet-70"
)

# Badges
from streamlit_extras.badges import badge

badge(type="github", name="myrepo")
badge(type="pypi", name="mypackage")

# ========================================================================
# ADVANCED COMPONENTS
# ========================================================================

# Toggle Switch (from streamlit-extras)
from streamlit_extras.toggle_switch import st_toggle_switch

switch = st_toggle_switch(
    label="Enable feature",
    key="switch1",
    default_active=True
)

# Annotated Text
from streamlit_extras.annotated_text import annotated_text

annotated_text(
    "This is ",
    ("important", "highlight", "#faa"),
    " text!",
)

# Metrics with Styling
from streamlit_extras.metric_cards import style_metric_cards

col1.metric("Users", "1,234", "+5%")
col2.metric("Sales", "$5,678", "+12%")
style_metric_cards(
    background_color="#1e1e1e",
    border_left_color="#667eea"
)

# Toast Notification
from streamlit_extras.notify import st_notify

st_notify(
    message="Notification text",
    type="success",
    duration=3
)

# ========================================================================
# DATA DISPLAY
# ========================================================================

# JSON Display
st.json({"key": "value", "number": 123})

# Code Display
st.code("""
def hello():
    print("Hello World!")
""", language="python")

# DataFrame with Styling
st.dataframe(
    df.style.format({'Price': '${:.2f}'}),
    use_container_width=True
)

# ========================================================================
# STATE MANAGEMENT
# ========================================================================

# Initialize State
if 'count' not in st.session_state:
    st.session_state.count = 0

# Update State
if st.button("Increment"):
    st.session_state.count += 1

# Display State
st.write(f"Count: {st.session_state.count}")

# Clear State
if st.button("Reset"):
    st.session_state.clear()

# ========================================================================
# USEFUL PATTERNS
# ========================================================================

# Page Config (Must be first Streamlit command)
st.set_page_config(
    page_title="My App",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Two-Line Button Pattern
if st.button("Click me"):
    st.balloons()  # Celebration animation
    # Or:
    st.snow()      # Snow animation

# Confirmation Pattern
if st.button("Delete"):
    if st.checkbox("Are you sure?"):
        # Delete action
        st.success("Deleted!")

# Download Button
from io import StringIO

buffer = StringIO()
df.to_csv(buffer, index=False)
st.download_button(
    label="Download CSV",
    data=buffer.getvalue(),
    file_name="data.csv",
    mime="text/csv"
)

# ========================================================================
# TIPS & TRICKS
# ========================================================================

# Tip 1: Use @st.cache_data for expensive computations
@st.cache_data(ttl=3600)
def load_data():
    return pd.read_csv("large_file.csv")

# Tip 2: Use container for better layout
with st.container():
    st.write("Better grouped content")

# Tip 3: Add separators
st.markdown("---")

# Tip 4: Use columns for side-by-side content
left, right = st.columns([2, 1])  # 2:1 ratio

# Tip 5: Lazy load expensive components
if st.checkbox("Show Advanced"):
    st.write("Advanced content...")

# Tip 6: Use expander for optional details
with st.expander("See details"):
    st.write("Detailed explanation...")

# Tip 7: Add sections with markdown
st.markdown("## Section Title")

# Tip 8: Group related controls
with st.sidebar:
    st.header("Settings")
    option1 = st.checkbox("Option 1")
    option2 = st.slider("Option 2")

# ========================================================================
# END OF REFERENCE
# ========================================================================

st.write("---")
st.markdown("*Reference guide loaded successfully! 🎉*")
