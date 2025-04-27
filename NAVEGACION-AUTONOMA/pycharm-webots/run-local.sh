#!/bin/bash

# https://www.youtube.com/watch?v=t6ZSB5cGZdQ

# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install numpy opencv-python

echo "Virtual environment created and activated successfully"
echo "Use 'deactivate' to exit the virtual environment"


