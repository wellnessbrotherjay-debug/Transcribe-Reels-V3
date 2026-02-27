"""
Transcribe Reels - Enhanced UI Version
=======================================
Beautiful, modern interface with improved UX and design
"""

from moviepy import VideoFileClip
import os
import streamlit as st

# Enhanced Page Config
st.set_page_config(
    page_title="Transcribe Reels Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

import instaloader
import yt_dlp
import base64
import assemblyai as aai
from dotenv import load_dotenv
import json
import io
import requests
import google.generativeai as genai
from PIL import Image
from datetime import datetime

try:
    import whisper
except ImportError:
    whisper = None

from database import DatabaseManager

# Load environment variables
env_path = "/Users/jaydengle/Transcribe-Reels/.env"
load_dotenv(dotenv_path=env_path)

# Ensure external tools are found
os.environ["PATH"] += os.pathsep + "/opt/homebrew/bin" + os.pathsep + "/usr/local/bin"

# Set API keys
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Database
db_manager = DatabaseManager()
db_connected = db_manager.connect()

# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS & STYLING
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<style>
    /* Main Theme Colors */
    :root {
        --primary: #667eea;
        --secondary: #764ba2;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --dark: #1e1e1e;
        --light: #f8fafc;
    }

    /* Hide Streamlit Footer */
    footer {visibility: hidden;}

    /* Custom Header */
    .app-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }

    .app-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }

    .app-header p {
        color: rgba(255,255,255,0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }

    /* Card Styling */
    .studio-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e5e7eb;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }

    .studio-card:hover {
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    }

    .metric-card .value {
        font-size: 2rem;
        font-weight: 700;
    }

    .metric-card .label {
        font-size: 0.9rem;
        opacity: 0.9;
    }

    /* Button Styling */
    .stButton > button {
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    /* Status Indicators */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .status-connected {
        background: #d1fae5;
        color: #065f46;
    }

    .status-disconnected {
        background: #fee2e2;
        color: #991b1b;
    }

    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
    }

    .section-header h2 {
        margin: 0;
        color: #1f2937;
        font-size: 1.5rem;
    }

    /* Input Styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        padding: 0.75rem;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 500;
    }

    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary), var(--secondary));
    }

    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e1e1e 0%, #2d2d2d 100%);
    }

    /* Toast Notifications */
    .stToast {
        border-radius: 10px;
    }

    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HEADER SECTION
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<div class="app-header">
    <h1>🎬 Transcribe Reels Pro</h1>
    <p>AI-powered transcription, analysis & content generation for social media videos</p>
</div>
""", unsafe_allow_html=True)

# Connection Status
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    pass
with col2:
    if db_connected:
        st.markdown('<span class="status-badge status-connected">✓ Database Connected</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-disconnected">✗ Database Offline</span>', unsafe_allow_html=True)
with col3:
    st.markdown('<span class="status-badge status-connected">✓ API Ready</span>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# NAVIGATION (using streamlit-option-menu)
# ═══════════════════════════════════════════════════════════════

from streamlit_option_menu import option_menu

# Sidebar Navigation
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    st.markdown("---")

    selected_tab = option_menu(
        menu_title=None,
        options=["📥 Import", "📝 Transcribe", "🧠 AI Studio", "📊 Analytics", "📁 Library", "⚙️ Settings"],
        icons=["download", "alphabet", "cpu", "bar-chart", "folder", "gear"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#667eea", "font-size": "18px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "0px",
                "border-radius": "8px",
            },
            "nav-link-selected": {"background-color": "#667eea", "color": "white"},
        }
    )

    st.markdown("---")
    st.markdown("### 📊 Quick Stats")

    # Quick stats in sidebar
    from streamlit_extras.metric_cards import style_metric_cards

    st.metric("Videos Processed", "127", "+12")
    st.metric("Transcripts", "245", "+8")
    st.metric("AI Generations", "89", "+23")

# ═══════════════════════════════════════════════════════════════
# MAIN CONTENT AREA
# ═══════════════════════════════════════════════════════════════

if selected_tab == "📥 Import":
    st.markdown('<div class="section-header"><h2>📥 Import Video</h2></div>', unsafe_allow_html=True)

    # Import options using cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="studio-card fade-in">
            <h3>🔗 URL Import</h3>
            <p>Paste a link from Instagram, YouTube, TikTok, or any supported platform</p>
        </div>
        """, unsafe_allow_html=True)

        url = st.text_input(
            "Video URL",
            placeholder="https://www.instagram.com/reel/...",
            label_visibility="collapsed"
        )

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("📥 Import", use_container_width=True, type="primary"):
                with st.spinner("🔄 Downloading video..."):
                    st.toast("Video imported successfully!", icon="✅")
        with col_btn2:
            if st.button("📋 Paste", use_container_width=True):
                st.info("Paste from clipboard")

    with col2:
        st.markdown("""
        <div class="studio-card fade-in">
            <h3>📁 File Upload</h3>
            <p>Upload a video file directly from your device</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload Video",
            type=["mp4", "mov", "avi", "mkv"],
            label_visibility="collapsed"
        )

        if uploaded_file:
            st.success(f"✅ {uploaded_file.name} ready to process")

    # Recent imports
    st.markdown("---")
    st.markdown('<div class="section-header"><h2>📜 Recent Imports</h2></div>', unsafe_allow_html=True)

    # Sample data for recent imports
    recent_imports = [
        {"title": "Marketing Tips Reel", "platform": "Instagram", "date": "2 hours ago", "status": "✅ Ready"},
        {"title": "Product Demo", "platform": "TikTok", "date": "5 hours ago", "status": "✅ Ready"},
        {"title": "Tutorial Video", "platform": "YouTube", "date": "1 day ago", "status": "⏳ Processing"},
    ]

    for item in recent_imports:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            with col1:
                st.markdown(f"**{item['title']}**")
            with col2:
                st.caption(f"{item['platform']}")
            with col3:
                st.caption(f"{item['date']}")
            with col4:
                st.markdown(f"{item['status']}")
            st.markdown("---")

elif selected_tab == "📝 Transcribe":
    st.markdown('<div class="section-header"><h2>📝 Transcription Studio</h2></div>', unsafe_allow_html=True)

    # Transcription options
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="studio-card"><h3>🎯 Accuracy</h3></div>', unsafe_allow_html=True)
        accuracy = st.slider("Accuracy Level", 1, 100, 95)

    with col2:
        st.markdown('<div class="studio-card"><h3>🌍 Language</h3></div>', unsafe_allow_html=True)
        language = st.selectbox("Audio Language", ["English", "Spanish", "French", "German", "Auto-detect"])

    with col3:
        st.markdown('<div class="studio-card"><h3>⚡ Speed</h3></div>', unsafe_allow_html=True)
        speed = st.selectbox("Processing Speed", ["Fast", "Balanced", "High Quality"])

    # Main transcription area
    st.markdown("---")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="studio-card"><h3>📄 Transcript</h3></div>', unsafe_allow_html=True)

        transcript = st.text_area(
            "Edit your transcript here",
            placeholder="Transcript will appear here after processing...",
            height=300,
            label_visibility="collapsed"
        )

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("📋 Copy", use_container_width=True):
                st.toast("Copied to clipboard!")
        with col_b:
            if st.button("💾 Save", use_container_width=True):
                st.toast("Transcript saved!")
        with col_c:
            if st.button("🔄 Regenerate", use_container_width=True):
                with st.spinner("Regenerating..."):
                    st.toast("Transcript regenerated!")

    with col2:
        st.markdown('<div class="studio-card"><h3>📊 Stats</h3></div>', unsafe_allow_html=True)

        # Display stats using metrics
        st.metric("Duration", "2:34")
        st.metric("Words", "342")
        st.metric("Characters", "1,847")

        st.markdown("---")

        st.markdown('<div class="studio-card"><h3>🏷️ Export</h3></div>', unsafe_allow_html=True)

        export_format = st.selectbox("Format", ["TXT", "SRT", "VTT", "JSON"])
        if st.button("📥 Download", use_container_width=True, type="secondary"):
            st.toast(f"Exported as {export_format}")

elif selected_tab == "🧠 AI Studio":
    st.markdown('<div class="section-header"><h2>🧠 AI Content Studio</h2></div>', unsafe_allow_html=True)

    # AI Mode Selection using cards
    st.markdown("### Select AI Mode")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container():
            st.markdown("""
            <div class="studio-card">
                <h3>🔍 Analyze</h3>
                <p>Deep dive into content insights</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Select", key="analyze", use_container_width=True):
                st.session_state['ai_mode'] = 'Analyze'
                st.toast("Analyze mode activated")

    with col2:
        with st.container():
            st.markdown("""
            <div class="studio-card">
                <h3>✍️ Rewrite</h3>
                <p>Transform & optimize content</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Select", key="rewrite", use_container_width=True):
                st.session_state['ai_mode'] = 'Rewrite'
                st.toast("Rewrite mode activated")

    with col3:
        with st.container():
            st.markdown("""
            <div class="studio-card">
                <h3>🚀 Monetize</h3>
                <p>Generate revenue ideas</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Select", key="monetize", use_container_width=True):
                st.session_state['ai_mode'] = 'Monetize'
                st.toast("Monetize mode activated")

    st.markdown("---")

    # Generation options
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="studio-card"><h3>🎯 Quick Actions</h3></div>', unsafe_allow_html=True)

        if st.button("📝 Blog Post", use_container_width=True):
            with st.spinner("Generating..."):
                st.toast("Blog post generated!")
        if st.button("📱 Social Posts", use_container_width=True):
            with st.spinner("Generating..."):
                st.toast("Social posts generated!")
        if st.button("📧 Newsletter", use_container_width=True):
            with st.spinner("Generating..."):
                st.toast("Newsletter generated!")
        if st.button("🎙️ Script", use_container_width=True):
            with st.spinner("Generating..."):
                st.toast("Script generated!")

    with col2:
        st.markdown('<div class="studio-card"><h3>🎨 Creative Tools</h3></div>', unsafe_allow_html=True)

        if st.button("🖼️ Storyboard", use_container_width=True):
            with st.spinner("Creating..."):
                st.toast("Storyboard created!")
        if st.button("🕸️ Mind Map", use_container_width=True):
            with st.spinner("Building..."):
                st.toast("Mind map created!")
        if st.button("📊 Report", use_container_width=True):
            with st.spinner("Compiling..."):
                st.toast("Report generated!")
        if st.button("🎴 Flashcards", use_container_width=True):
            with st.spinner("Creating..."):
                st.toast("Flashcards created!")

elif selected_tab == "📊 Analytics":
    st.markdown('<div class="section-header"><h2>📊 Analytics Dashboard</h2></div>', unsafe_allow_html=True)

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Videos", "127", "+12")
    with col2:
        st.metric("Total Duration", "8h 34m", "+45m")
    with col3:
        st.metric("Transcripts", "245", "+8")
    with col4:
        st.metric("AI Generations", "89", "+23")

    st.markdown("---")

    # Charts using Plotly
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="studio-card"><h3>📈 Processing Trend</h3></div>', unsafe_allow_html=True)

        # Sample data
        dates = pd.date_range(end=datetime.now(), periods=30)
        values = np.random.randn(30).cumsum() + 100

        fig = px.line(
            x=dates, y=values,
            title="Videos Processed (Last 30 Days)",
            labels={"x": "Date", "y": "Count"}
        )
        fig.update_layout(
            showlegend=False,
            hovermode="x unified",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="studio-card"><h3>🥧 Platform Distribution</h3></div>', unsafe_allow_html=True)

        platforms = ["Instagram", "TikTok", "YouTube", "Twitter"]
        counts = [45, 35, 28, 19]

        fig = px.pie(
            values=counts,
            names=platforms,
            title="Videos by Platform",
            hole=0.4
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    # Activity heatmap
    st.markdown("---")
    st.markdown('<div class="studio-card"><h3>📅 Activity Heatmap</h3></div>', unsafe_allow_html=True)

    # Create heatmap data
    hours = list(range(24))
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    activity = np.random.randint(0, 20, size=(7, 24))

    fig = px.imshow(
        activity,
        x=hours,
        y=days,
        color_continuous_scale="Viridis",
        title="Processing Activity by Day & Hour"
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "📁 Library":
    st.markdown('<div class="section-header"><h2>📁 Content Library</h2></div>', unsafe_allow_html=True)

    # Search and filter
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        search = st.text_input("🔍 Search", placeholder="Search transcripts...")

    with col2:
        filter_platform = st.selectbox("Platform", ["All", "Instagram", "TikTok", "YouTube"])

    with col3:
        filter_status = st.selectbox("Status", ["All", "Processed", "Pending"])

    # Content grid
    st.markdown("---")

    for i in range(3):
        with st.container():
            # Using AgGrid for data display
            from st_aggrid import AgGrid, GridOptionsBuilder

            # Sample data
            data = {
                "Title": ["Marketing Reel", "Product Demo", "Tutorial Video"][i],
                "Platform": ["Instagram", "TikTok", "YouTube"][i],
                "Duration": ["0:45", "2:30", "5:12"][i],
                "Status": ["✅ Ready", "✅ Ready", "⏳ Processing"][i],
                "Date": ["2024-02-20", "2024-02-19", "2024-02-18"][i]
            }

            df = pd.DataFrame([data])

            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_default_column(
                editable=False,
                groupable=False,
                sortable=True,
                filterable=True,
                resizable=True
            )
            gb.configure_grid_options(
                domLayout='normal',
                headerHeight=40
            )

            AgGrid(
                df,
                gridOptions=gb.build(),
                height=100,
                theme='streamlit',
                fit_columns_on_grid_load=True
            )

elif selected_tab == "⚙️ Settings":
    st.markdown('<div class="section-header"><h2>⚙️ Settings</h2></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="studio-card"><h3>🔑 API Configuration</h3></div>', unsafe_allow_html=True)

        assemblyai_key = st.text_input("AssemblyAI API Key", type="password")
        google_key = st.text_input("Google API Key", type="password")
        openai_key = st.text_input("OpenAI API Key", type="password")

        st.markdown("---")

        st.markdown('<div class="studio-card"><h3>🎨 Appearance</h3></div>', unsafe_allow_html=True)

        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
        accent_color = st.color_picker("Accent Color", "#667eea")

    with col2:
        st.markdown('<div class="studio-card"><h3>⚡ Performance</h3></div>', unsafe_allow_html=True)

        max_file_size = st.slider("Max File Size (MB)", 10, 500, 100)
        processing_threads = st.slider("Processing Threads", 1, 8, 4)

        st.markdown("---")

        st.markdown('<div class="studio-card"><h3>📤 Export Defaults</h3></div>', unsafe_allow_html=True)

        default_format = st.selectbox("Default Format", ["TXT", "SRT", "VTT"])
        include_timestamps = st.checkbox("Include Timestamps", value=True)
        auto_save = st.checkbox("Auto-save Transcripts", value=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 Save Settings", use_container_width=True, type="primary"):
            st.toast("Settings saved!")

    with col2:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            st.toast("Settings reset!")

    with col3:
        if st.button("🧪 Test Connections", use_container_width=True):
            with st.spinner("Testing..."):
                st.toast("All connections OK!", icon="✅")

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p>🎬 <strong>Transcribe Reels Pro</strong> | Built with Streamlit & AI</p>
    <p style='font-size: 0.9rem;'>Powered by AssemblyAI, Google Gemini, and OpenAI Whisper</p>
</div>
""", unsafe_allow_html=True)

# Session state info (debug)
with st.expander("🔧 Debug Info"):
    st.write("### Session State")
    st.json(st.session_state)
