#!/bin/bash
# Start Transcribe Reels PRO (Ultimate UI)

echo "🚀 Starting Transcribe Reels PRO..."

# Kill any existing Streamlit processes
pkill -f "streamlit run" 2>/dev/null
sleep 1

# Activate virtual environment
source venv/bin/activate

# Start the PRO app
streamlit run transcribe_pro.py --server.port 8501
