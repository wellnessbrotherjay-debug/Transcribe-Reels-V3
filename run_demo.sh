#!/bin/bash
# Quick launcher for Streamlit UI Demo

echo "🎨 Starting Streamlit UI Demo..."
echo ""

# Kill any existing Streamlit processes
pkill -f "streamlit run" 2>/dev/null
sleep 1

# Activate virtual environment
source venv/bin/activate

# Check which demo to run
echo "Which demo would you like to run?"
echo "1) Full UI Components Demo"
echo "2) Simple Test (verify all libraries)"
echo "3) Quick Reference Guide"
echo ""
read -p "Enter choice (1-3) or press Enter for default: " choice

case $choice in
    2)
        echo "🧪 Running Simple Test..."
        streamlit run test_ui.py --server.port 8501
        ;;
    3)
        echo "📚 Running Quick Reference..."
        streamlit run ui_quick_reference.py --server.port 8501
        ;;
    *)
        echo "🚀 Running Full UI Demo..."
        streamlit run ui_components_demo.py --server.port 8501
        ;;
esac
