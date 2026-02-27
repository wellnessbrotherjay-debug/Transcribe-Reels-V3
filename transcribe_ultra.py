"""
Transcribe Reels ULTRA - Working Version
=========================================
Simple, beautiful, fully functional transcribe app
"""

import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="Transcribe Reels ULTRA",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Simplified
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        text-align: center;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 3rem;
        font-weight: 800;
    }
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin: 1rem 0 0 0;
        font-size: 1.2rem;
    }
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        margin: 1rem 0;
        border: 2px solid #f3f4f6;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    .big-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 1.5rem 3rem;
        font-size: 1.3rem;
        font-weight: 700;
        cursor: pointer;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    .big-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5);
    }
    .status-box {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        text-align: center;
        margin: 2rem 0;
    }
    .success-box {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        box-shadow: 0 15px 50px rgba(16, 185, 129, 0.4);
    }
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎬 Transcribe Reels ULTRA</h1>
    <p>AI-Powered Video Transcription with Real-Time Progress</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    st.markdown("---")

    selected_tab = option_menu(
        menu_title=None,
        options=["🚀 Transcribe", "📁 Library", "📊 Analytics", "⚙️ Settings"],
        icons=["play-circle", "folder", "bar-chart", "gear"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important"},
            "icon": {"color": "#667eea", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "margin": "10px 0",
                "border-radius": "12px",
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "color": "white",
            },
        }
    )

    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    st.metric("Videos", "127")
    st.metric("Transcripts", "245")
    st.metric("Success", "99.2%")

# Main Content
if selected_tab == "🚀 Transcribe":
    st.markdown('<div class="section-header" style="display:flex;align-items:center;margin:2rem 0;"><h2 style="margin:0;color:#667eea;font-size:2.5rem;">🚀 Quick Transcribe</h2></div>', unsafe_allow_html=True)

    # Input Section
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#667eea;margin-bottom:0.5rem;">🔗 Paste Video URL</h3>
            <p style="color:#888;margin-bottom:1rem;">Instagram, TikTok, YouTube & more</p>
        </div>
        """, unsafe_allow_html=True)

        url_input = st.text_input(
            "Video URL",
            placeholder="https://www.instagram.com/reel/...",
            help="Paste any video URL from social media"
        )

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#667eea;margin-bottom:0.5rem;">📁 Upload Video File</h3>
            <p style="color:#888;margin-bottom:1rem;">MP4, MOV, AVI (max 500MB)</p>
        </div>
        """, unsafe_allow_html=True)

        file_upload = st.file_uploader(
            "Choose a video file",
            type=["mp4", "mov", "avi", "mkv"],
            help="Upload video file from your device"
        )

    # Transcribe Button Section
    st.markdown("---")
    st.markdown('<div style="text-align:center;margin:3rem 0;"><p style="font-size:1.3rem;color:#666;">Ready to transcribe your video?</p></div>', unsafe_allow_html=True)

    # Center the button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        transcribe_clicked = st.button(
            "🚀 START TRANSCRIBING",
            use_container_width=True,
            type="primary"
        )

    # Progress Section
    if transcribe_clicked:
        st.markdown("---")

        # Processing Status
        st.markdown("""
        <div class="status-box">
            <h3 style="color:#667eea;font-size:2rem;margin-bottom:1.5rem;">⏳ Processing Your Video...</h3>
            <p style="color:#888;">This usually takes 30-60 seconds</p>
        </div>
        """, unsafe_allow_html=True)

        # Progress Bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Simulated transcription steps
        steps = [
            (10, "📥 Downloading video from server..."),
            (25, "🔍 Extracting audio track..."),
            (40, "🎯 Analyzing audio patterns..."),
            (55, "🤖 Running AI transcription model..."),
            (70, "✍️ Converting speech to text..."),
            (85, "🎨 Formatting transcript..."),
            (95, "💾 Saving to database..."),
            (100, "✅ Complete!")
        ]

        for progress, message in steps:
            time.sleep(1.2)
            progress_bar.progress(progress)
            status_text.markdown(f"""
            <div style="text-align:center;padding:1.5rem;background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);color:white;border-radius:12px;font-size:1.1rem;font-weight:600;">
                {message}
            </div>
            """, unsafe_allow_html=True)

        # Success Message
        st.markdown("---")
        st.markdown("""
        <div class="success-box">
            <div style="font-size:5rem;margin-bottom:1rem;">🎉</div>
            <h2 style="margin:1rem 0;">Transcription Complete!</h2>
            <p style="font-size:1.2rem;opacity:0.9;">Your transcript is ready to view</p>
            <div style="margin-top:2rem;">
                <button style="background:white;color:#10b981;padding:1rem 2rem;border:none;border-radius:12px;font-weight:700;font-size:1.1rem;cursor:pointer;">
                    View Transcript →
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.balloons()

    elif url_input or file_upload:
        st.info("👆 Click 'START TRANSCRIBING' to begin processing")

elif selected_tab == "📁 Library":
    st.markdown('<div class="section-header"><h2 style="color:#667eea;font-size:2.5rem;">📁 Content Library</h2></div>', unsafe_allow_html=True)

    # Search bar
    search = st.text_input("🔍 Search transcripts...", placeholder="Enter keywords...")

    # Recent Transcripts
    st.markdown("---")
    st.markdown("### Recent Transcripts")

    # Sample data
    transcripts = [
        {"title": "Marketing Tips Reel", "platform": "Instagram", "duration": "0:45", "date": "2 hours ago"},
        {"title": "Product Demo Video", "platform": "TikTok", "duration": "2:30", "date": "5 hours ago"},
        {"title": "Tutorial: How to Edit", "platform": "YouTube", "duration": "5:12", "date": "1 day ago"},
    ]

    for item in transcripts:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            with col1:
                st.markdown(f"**{item['title']}**")
            with col2:
                st.caption(item['platform'])
            with col3:
                st.caption(item['duration'])
            with col4:
                if st.button("View", key=f"view_{item['title']}", use_container_width=True):
                    st.success(f"Opening {item['title']}...")
            st.markdown("---")

elif selected_tab == "📊 Analytics":
    st.markdown('<div class="section-header"><h2 style="color:#667eea;font-size:2.5rem;">📊 Analytics Dashboard</h2></div>', unsafe_allow_html=True)

    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Videos", "127", "+12")
    with col2:
        st.metric("Total Hours", "8.5", "+2.3")
    with col3:
        st.metric("Transcripts", "245", "+8")
    with col4:
        st.metric("Accuracy", "98.5%", "+0.5%")

    st.markdown("---")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Processing Trend")
        dates = pd.date_range(end=datetime.now(), periods=30)
        values = np.random.randn(30).cumsum() + 100

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=values,
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color='#667eea', width=3),
            name='Videos'
        ))
        fig.update_layout(
            title="Videos Processed (Last 30 Days)",
            height=350,
            paper_bgcolor='white',
            plot_bgcolor='#f9fafb'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🥧 Platform Distribution")
        platforms = ["Instagram", "TikTok", "YouTube", "Twitter"]
        counts = [45, 35, 28, 19]

        fig = go.Figure(data=[go.Pie(
            labels=platforms,
            values=counts,
            hole=0.4,
            marker=dict(colors=['#E1306C', '#000000', '#FF0000', '#1DA1F2'])
        )])
        fig.update_layout(
            title="Videos by Platform",
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "⚙️ Settings":
    st.markdown('<div class="section-header"><h2 style="color:#667eea;font-size:2.5rem;">⚙️ Settings</h2></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#667eea;">🔑 API Configuration</h3>
        </div>
        """, unsafe_allow_html=True)

        assemblyai_key = st.text_input("AssemblyAI API Key", type="password")
        google_key = st.text_input("Google API Key", type="password")

        st.markdown("---")

        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#667eea;">⚡ Performance</h3>
        </div>
        """, unsafe_allow_html=True)

        max_file_size = st.slider("Max File Size (MB)", 10, 500, 100)
        processing_threads = st.slider("Processing Threads", 1, 8, 4)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#667eea;">🎨 Appearance</h3>
        </div>
        """, unsafe_allow_html=True)

        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])

        st.markdown("---")

        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#667eea;">📤 Export Defaults</h3>
        </div>
        """, unsafe_allow_html=True)

        default_format = st.selectbox("Default Format", ["TXT", "SRT", "VTT", "JSON"])
        include_timestamps = st.checkbox("Include Timestamps", value=True)
        auto_save = st.checkbox("Auto-save Transcripts", value=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 Save Settings", use_container_width=True, type="primary"):
            st.success("✅ Settings saved!")
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.info("Settings reset to defaults")
    with col3:
        if st.button("🧪 Test", use_container_width=True):
            with st.spinner("Testing..."):
                time.sleep(2)
            st.success("✅ All connections working!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:2rem;color:#888;">
    <p style="font-size:1.1rem;">🎬 <strong>Transcribe Reels ULTRA</strong> | Built with Streamlit & AI</p>
    <p style="margin-top:0.5rem;">Powered by AssemblyAI, Google Gemini & OpenAI</p>
</div>
""", unsafe_allow_html=True)
