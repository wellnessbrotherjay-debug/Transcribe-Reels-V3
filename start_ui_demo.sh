#!/bin/bash
# Quick Start Script for UI Components Demo

echo "🎨 Starting Streamlit UI Demo..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Activate virtual environment
source venv/bin/activate

# Check if streamlit is installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "❌ Streamlit not found. Installing..."
    pip install streamlit
fi

echo "✅ Libraries loaded!"
echo ""
echo "🚀 Launching demo..."
echo "   URL: http://localhost:8501"
echo "   Press Ctrl+C to stop"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run the demo
streamlit run ui_components_demo.py

# Or run the simple test:
# streamlit run test_ui.py
