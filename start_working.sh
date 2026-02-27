#!/bin/bash
# Start Fully Functional Transcribe App

echo "🚀 Starting FULLY FUNCTIONAL Transcribe Reels..."

# Kill any existing Streamlit processes
pkill -f "streamlit run" 2>/dev/null
sleep 1

# Activate virtual environment
source venv/bin/activate

# Start the working app
streamlit run transcribe_working.py --server.port 8501
