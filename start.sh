#!/bin/bash
# One-click launcher - starts the main UI demo

# Kill any existing Streamlit processes
pkill -f "streamlit run" 2>/dev/null
sleep 1

# Activate and start
source venv/bin/activate
streamlit run ui_components_demo.py --server.port 8501
