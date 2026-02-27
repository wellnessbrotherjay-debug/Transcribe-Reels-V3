#!/bin/bash
# Start Transcribe Reels ULTRA

echo "🚀 Starting Transcribe Reels ULTRA..."

# Kill any existing Streamlit processes
pkill -f "streamlit run" 2>/dev/null
sleep 1

# Activate virtual environment
source venv/bin/activate

# Start the ULTRA app
streamlit run transcribe_ultra.py --server.port 8501
