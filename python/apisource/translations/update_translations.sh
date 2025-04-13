#!/bin/bash

# Navigate to the script's directory
cd "$(dirname "$0")"

# Extract new messages and update messages.pot
~/.local/bin/pybabel extract -F babel.cfg -o messages.pot ..

# Update .po files with new messages
~/.local/bin/pybabel update -i messages.pot -d .

# Compile .po files into .mo files
~/.local/bin/pybabel compile -d .

# Remove the POT-Creation-Date line from messages.pot
sed -i '/^"POT-Creation-Date:/d' messages.pot

# Remove the POT-Creation-Date line from all .po files
find . -name "messages.po" -exec sed -i '/^"POT-Creation-Date:/d' {} +

echo "Translation files updated and compiled successfully."
