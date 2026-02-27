#!/bin/bash
# Start Transcribe Reels ENHANCED V2 (Silent Mode - No Warning Popups)

echo "🚀 Starting Transcribe Reels ENHANCED V2 (Silent Mode)..."
echo "✅ All 1,640 lines of original features"
echo "✅ Enhanced UI with progress indicators"
echo "✅ Toast notifications"
echo "✅ Smooth animations"
echo "✅ Warning popups suppressed"
echo ""

# Kill any existing Streamlit processes
pkill -f "streamlit run" 2>/dev/null
sleep 1

# Activate virtual environment
source venv/bin/activate

# Redirect stderr to suppress warnings, but keep stdout for Streamlit
streamlit run transcribe_enhanced_v2.py --server.port 8501 2>/dev/null
