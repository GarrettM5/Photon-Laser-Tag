#!/bin/bash

echo "--- Starting Photon Laser Tag Installer ---"

# Update package lists
sudo apt-get update

# Install Python3, Pip, and Tkinter (GUI)
echo "--- Installing Python and System Dependencies ---"
sudo apt-get install -y python3 python3-pip python3-tk libpq-dev

# Install Python Libraries
# psycopg2-binary: for PostgreSQL
# Pillow: for handling the jpg splash screen image
# pygame: for audio playback and timer functionality
echo "--- Installing Python Libraries ---"
pip3 install psycopg2-binary Pillow pygame --break-system-packages

echo "--- Installation Complete ---"
echo "To run the game: python3 src/main.py"
