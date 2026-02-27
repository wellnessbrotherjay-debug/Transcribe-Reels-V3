#!/bin/bash
# Clean launch - suppresses all Python warnings at OS level

echo "🚀 Starting Transcribe Reels ENHANCED V2 (Clean Mode)..."

# Kill any existing processes
pkill -f "streamlit run" 2>/dev/null
sleep 2

# Activate virtual environment
source venv/bin/activate

# Set environment variables to suppress ALL warnings
export PYTHONWARNINGS="ignore"
export PYTHONIOENCODING="utf-8"

# Launch with stderr redirected to suppress warning dialogs
python -W ignore -m streamlit run transcribe_enhanced_v2.py --server.port 8501 2>/dev/null
