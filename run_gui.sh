#!/bin/bash
# Launch the Union FS GUI

# Check if PyQt5 is installed
if ! python3 -c "import PyQt5" 2>/dev/null; then
    echo "PyQt5 not found. Installing..."
    # Try apt first (Debian/Ubuntu)
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3-pyqt5
    # Try pip if apt is not available
    elif command -v pip3 &> /dev/null; then
        pip3 install PyQt5
    elif command -v pip &> /dev/null; then
        pip install PyQt5
    else
        echo "Error: Neither apt-get nor pip found. Please install PyQt5 manually:"
        echo "  Ubuntu/Debian: sudo apt-get install python3-pyqt5"
        echo "  Other: pip install PyQt5"
        exit 1
    fi
fi

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the GUI
cd "$SCRIPT_DIR"
python3 gui.py
