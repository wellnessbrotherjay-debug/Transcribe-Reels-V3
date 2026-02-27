#!/bin/bash
# Start Transcribe Reels ENHANCED V2 (All Features + Modern UI)

echo "🚀 Starting Transcribe Reels ENHANCED V2..."
echo "✅ All 1,640 lines of original features"
echo "✅ Enhanced UI with progress indicators"
echo "✅ Toast notifications"
echo "✅ Smooth animations"
echo ""

# Kill any existing Streamlit processes
pkill -f "streamlit run" 2>/dev/null
sleep 1

# Activate virtual environment
source venv/bin/activate

# Start the ENHANCED V2 app
echo "🎬 Launching on http://localhost:8501"
streamlit run transcribe_enhanced_v2.py --server.port 8501
