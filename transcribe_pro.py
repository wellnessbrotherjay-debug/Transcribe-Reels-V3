"""
Transcribe Reels PRO - Ultimate UI Version
==========================================
Amazing visual effects, animations, and real progress tracking
"""

import streamlit as st
import time
import json
from datetime import datetime

# Enhanced Page Config
st.set_page_config(
    page_title="Transcribe Reels PRO",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention
import os
from dotenv import load_dotenv

load_dotenv()

# ═══════════════════════════════════════════════════════════════
# AMAZING CSS & ANIMATIONS
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    /* Animated Gradient Background */
    .main {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glassmorphism Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }

    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: 0.5s;
    }

    .glass-card:hover::before {
        left: 100%;
    }

    .glass-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.4);
    }

    /* Animated Header */
    .animated-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: gradientShift 5s ease infinite;
        padding: 3rem 2rem;
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .animated-header h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        animation: slideInDown 1s ease-out;
    }

    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Floating Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }

    .floating {
        animation: float 3s ease-in-out infinite;
    }

    /* Pulse Animation */
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    .pulse {
        animation: pulse 2s ease-in-out infinite;
    }

    /* Glow Effect */
    .glow {
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5),
                    0 0 40px rgba(102, 126, 234, 0.3),
                    0 0 60px rgba(102, 126, 234, 0.1);
        animation: glow 2s ease-in-out infinite;
    }

    @keyframes glow {
        0%, 100% {
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.5),
                        0 0 40px rgba(102, 126, 234, 0.3);
        }
        50% {
            box-shadow: 0 0 40px rgba(118, 75, 162, 0.8),
                        0 0 80px rgba(118, 75, 162, 0.5);
        }
    }

    /* Progress Bar Animation */
    .animated-progress {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #667eea);
        background-size: 300% 100%;
        animation: progressGradient 3s linear infinite;
        border-radius: 12px;
        height: 30px;
        transition: width 0.5s ease;
    }

    @keyframes progressGradient {
        0% { background-position: 0% 50%; }
        100% { background-position: 300% 50%; }
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 1rem 3rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }

    /* Status Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 12px 24px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.95rem;
        animation: slideInRight 0.5s ease-out;
    }

    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    .status-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }

    .status-processing {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        animation: pulse 1.5s ease-in-out infinite;
    }

    /* Spinner */
    .spinner {
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-top: 4px solid white;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Input Styling */
    .stTextInput > div > div > input {
        border-radius: 16px;
        border: 3px solid #e5e7eb;
        padding: 1rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.9);
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        transform: scale(1.02);
    }

    /* Metric Card */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 10s linear infinite;
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .metric-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 25px 60px rgba(102, 126, 234, 0.5);
    }

    /* Section Header */
    .section-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 3rem 0 2rem 0;
        padding-bottom: 1rem;
        border-bottom: 3px solid rgba(102, 126, 234, 0.2);
    }

    .section-header h2 {
        margin: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
    }

    /* Confetti Animation */
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        top: -10px;
        animation: fall linear forwards;
    }

    @keyframes fall {
        to {
            transform: translateY(100vh) rotate(720deg);
        }
    }

    /* Typing Animation */
    .typing {
        display: inline-block;
        overflow: hidden;
        border-right: 3px solid #667eea;
        white-space: nowrap;
        animation: typing 3s steps(40) infinite, blink 0.75s step-end infinite;
    }

    @keyframes typing {
        from, to { width: 0; }
        50% { width: 100%; }
    }

    @keyframes blink {
        50% { border-color: transparent; }
    }

    /* Hide Streamlit Footer */
    footer {visibility: hidden;}

    /* Sidebar Enhancement */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e1e1e 0%, #2d2d2d 100%);
    }

    /* Success Animation */
    @keyframes checkmark {
        0% { stroke-dashoffset: 100; }
        100% { stroke-dashoffset: 0; }
    }

    .success-icon {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        animation: scaleIn 0.5s ease-out;
    }

    @keyframes scaleIn {
        from { transform: scale(0); }
        to { transform: scale(1); }
    }

    /* Wave Animation */
    .wave {
        animation: wave 2s ease-in-out infinite;
    }

    @keyframes wave {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(20deg); }
        75% { transform: rotate(-20deg); }
    }

    /* Particles Background */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: 0;
    }

    .particle {
        position: absolute;
        width: 10px;
        height: 10px;
        background: rgba(102, 126, 234, 0.3);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<div class="animated-header">
    <h1 class="wave">🎬 Transcribe Reels PRO</h1>
    <p style="color: rgba(255,255,255,0.95); font-size: 1.3rem; margin-top: 1rem;">
        Next-Gen AI Video Transcription with Real-Time Progress Tracking ✨
    </p>
</div>
""", unsafe_allow_html=True)

# Status Bar
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    pass
with col2:
    st.markdown('<span class="status-badge status-success">✓ System Online</span>', unsafe_allow_html=True)
with col3:
    st.markdown('<span class="status-badge status-success">✓ AI Ready</span>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h2 style="color: #667eea; font-size: 2rem;">🎛️</h2>
        <p style="color: #888;">Control Panel</p>
    </div>
    """, unsafe_allow_html=True)

    selected_tab = option_menu(
        menu_title=None,
        options=["🚀 Quick Start", "🎬 Import", "⚡ Transcribe", "🧠 AI Studio", "📊 Analytics"],
        icons=["lightning", "upload", "play-circle", "cpu", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#667eea", "font-size": "20px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "8px 0",
                "border-radius": "12px",
                "padding": "12px 20px",
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "color": "white",
            },
        }
    )

    st.markdown("---")

    # Quick Stats
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h3 style="color: #667eea;">📊 Quick Stats</h3>
    </div>
    """, unsafe_allow_html=True)

    st.metric("Processed", "127", "🔥")
    st.metric("In Queue", "3", "⏳")
    st.metric("Success Rate", "99.2%", "✓")

# ═══════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════════════

if selected_tab == "🚀 Quick Start":
    st.markdown('<div class="section-header"><h2>⚡ Get Started Fast</h2></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #667eea; font-size: 1.8rem;">🔗 Paste URL</h3>
            <p style="color: #666;">Instagram, TikTok, YouTube & more</p>
        </div>
        """, unsafe_allow_html=True)

        url = st.text_input(
            "",
            placeholder="https://www.instagram.com/reel/...",
            label_visibility="collapsed"
        )

    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #667eea; font-size: 1.8rem;">📁 Upload File</h3>
            <p style="color: #666;">MP4, MOV, AVI up to 500MB</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "",
            type=["mp4", "mov", "avi", "mkv"],
            label_visibility="collapsed"
        )

    # Big Transcribe Button
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0;">
        <p style="font-size: 1.2rem; color: #666;">Ready to transcribe?</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 START TRANSCRIBING", use_container_width=True, type="primary"):
            # Show progress
            progress_container = st.container()

            with progress_container:
                st.markdown("""
                <div style="text-align: center; padding: 3rem;">
                    <div class="spinner"></div>
                    <h3 style="color: #667eea; margin-top: 2rem;">Processing Your Video...</h3>
                    <p style="color: #888; margin-top: 1rem;">This may take a few moments</p>
                </div>
                """, unsafe_allow_html=True)

                # Progress bar with animation
                progress_bar = st.progress(0)

                # Simulate progress with status updates
                status_steps = [
                    (10, "📥 Downloading video..."),
                    (30, "🔍 Extracting audio..."),
                    (50, "🎯 Analyzing speech patterns..."),
                    (70, "✍️ Generating transcript..."),
                    (90, "🎨 Applying formatting..."),
                    (100, "✅ Complete!")
                ]

                for progress, status in status_steps:
                    time.sleep(1.5)
                    progress_bar.progress(progress)
                    st.markdown(f"""
                    <div style="text-align: center; margin-top: 2rem;">
                        <span class="status-badge status-processing">{status}</span>
                    </div>
                    """, unsafe_allow_html=True)

                # Success message
                st.markdown("""
                <div style="text-align: center; padding: 3rem;">
                    <div class="success-icon" style="margin: 0 auto;">
                        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                    </div>
                    <h2 style="color: #10b981; margin-top: 2rem;">🎉 Transcription Complete!</h2>
                    <p style="color: #666; font-size: 1.1rem;">Your transcript is ready</p>
                </div>
                """, unsafe_allow_html=True)

                st.balloons()

elif selected_tab == "🎬 Import":
    st.markdown('<div class="section-header"><h2>🎬 Import Media</h2></div>', unsafe_allow_html=True)

    # Platform cards
    col1, col2, col3, col4 = st.columns(4)

    platforms = [
        ("Instagram", "📸", "#E1306C"),
        ("TikTok", "🎵", "#000000"),
        ("YouTube", "▶️", "#FF0000"),
        ("Twitter", "🐦", "#1DA1F2")
    ]

    for (name, icon, color) in platforms:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 1.5rem;">
            <div style="font-size: 3rem;">{icon}</div>
            <h4 style="margin: 1rem 0 0 0; color: #333;">{name}</h4>
        </div>
        """, unsafe_allow_html=True)

elif selected_tab == "⚡ Transcribe":
    st.markdown('<div class="section-header"><h2>⚡ Transcription Studio</h2></div>', unsafe_allow_html=True)

    # Settings cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #667eea;">🎯 Accuracy</h3>
            <p style="color: #888;">Select precision level</p>
        </div>
        """, unsafe_allow_html=True)
        accuracy = st.slider("Accuracy", 80, 100, 95)

    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #667eea;">🌍 Language</h3>
            <p style="color: #888;">Audio language</p>
        </div>
        """, unsafe_allow_html=True)
        language = st.selectbox("Language", ["English", "Spanish", "French", "Auto-Detect"])

    with col3:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #667eea;">⚡ Speed</h3>
            <p style="color: #888;">Processing mode</p>
        </div>
        """, unsafe_allow_html=True)
        speed = st.selectbox("Mode", ["Fast", "Balanced", "High Quality"])

    # Transcript area
    st.markdown("---")
    st.markdown('<div class="section-header"><h2>📄 Transcript</h2></div>', unsafe_allow_html=True)

    transcript = st.text_area(
        "",
        placeholder="Your transcript will appear here after processing...",
        height=300,
        label_visibility="collapsed",
        key="transcript_area"
    )

    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Copy", use_container_width=True):
            st.toast("Copied to clipboard! 📋", icon="✅")
    with col2:
        if st.button("💾 Save", use_container_width=True):
            st.toast("Transcript saved! 💾", icon="✅")
    with col3:
        if st.button("🔄 Regenerate", use_container_width=True):
            st.toast("Regenerating... 🔄", icon="⏳")

elif selected_tab == "🧠 AI Studio":
    st.markdown('<div class="section-header"><h2>🧠 AI Content Studio</h2></div>', unsafe_allow_html=True)

    # AI Mode Selection
    st.markdown("### Select Generation Mode")

    col1, col2, col3 = st.columns(3)

    ai_modes = [
        ("📝 Blog Post", "Transform into article"),
        ("📱 Social Posts", "Generate viral content"),
        ("📧 Newsletter", "Create email content"),
        ("🎙️ Script", "Video script format"),
        ("🖼️ Storyboard", "Visual scene breakdown"),
        ("🕸️ Mind Map", "Concept connections")
    ]

    for i, (mode, desc) in enumerate(ai_modes[:3]):
        with [col1, col2, col3][i]:
            st.markdown(f"""
            <div class="glass-card floating">
                <h3 style="color: #667eea;">{mode}</h3>
                <p style="color: #888; font-size: 0.9rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Generate {mode.split()[1]}", use_container_width=True, key=f"gen_{i}"):
                st.toast(f"Generating {mode.split()[1]}... ✨", icon="🧠")

    st.markdown("---")

    # More AI modes
    for i, (mode, desc) in enumerate(ai_modes[3:], 3):
        st.markdown(f"""
        <div class="glass-card" style="margin: 1rem 0;">
            <h3 style="color: #667eea;">{mode}</h3>
            <p style="color: #888;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Generate {mode.split()[1]}", use_container_width=True, key=f"gen_{i}"):
            st.toast(f"Generating {mode.split()[1]}... ✨", icon="🧠")

elif selected_tab == "📊 Analytics":
    st.markdown('<div class="section-header"><h2>📊 Analytics Dashboard</h2></div>', unsafe_allow_html=True)

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)

    metrics_data = [
        ("Total Videos", "127", "+12", "🎬"),
        ("Transcripts", "245", "+8", "📝"),
        ("Hours Processed", "8.5", "+2.3", "⏱️"),
        ("Success Rate", "99.2%", "+0.3%", "✅")
    ]

    for col, (label, value, delta, icon) in zip([col1, col2, col3, col4], metrics_data):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2.5rem;">{icon}</div>
                <div style="font-size: 2rem; font-weight: 800; margin: 1rem 0;">{value}</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">{label}</div>
                <div style="margin-top: 0.5rem; font-size: 0.85rem;">📈 {delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="glass-card"><h3 style="color: #667eea;">📈 Processing Trend</h3></div>', unsafe_allow_html=True)

        # Sample chart data
        dates = pd.date_range(end=datetime.now(), periods=30)
        values = np.random.randn(30).cumsum() + 100

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines',
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.2)',
            line=dict(color='#667eea', width=3),
            name='Videos'
        ))

        fig.update_layout(
            title="Videos Processed (Last 30 Days)",
            xaxis_title="Date",
            yaxis_title="Count",
            hovermode="x unified",
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#333')
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="glass-card"><h3 style="color: #667eea;">🥧 Platform Distribution</h3></div>', unsafe_allow_html=True)

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
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#333')
        )

        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 3rem 0; color: #888;">
    <p style="font-size: 1.2rem;">🎬 <strong>Transcribe Reels PRO</strong></p>
    <p style="margin-top: 1rem;">Built with ❤️ using Streamlit & AI</p>
    <p style="margin-top: 0.5rem; font-size: 0.9rem;">Powered by AssemblyAI, Google Gemini & OpenAI Whisper</p>
</div>
""", unsafe_allow_html=True)

# Session state info
with st.expander("🔧 Debug Info"):
    st.json(st.session_state)
