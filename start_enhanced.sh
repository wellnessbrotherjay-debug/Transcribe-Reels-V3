#!/bin/bash
# Start the Enhanced Transcribe App

echo "🎬 Starting Transcribe Reels Pro (Enhanced UI)..."

# Kill any existing Streamlit processes
pkill -f "streamlit run" 2>/dev/null
sleep 1

# Activate virtual environment
source venv/bin/activate

# Start the enhanced app
streamlit run transcribe_enhanced.py --server.port 8501
