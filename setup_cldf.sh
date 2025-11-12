#!/bin/bash

# CLDF Data Setup Script for WALS
# This script downloads CLDF data from the official WALS repository

set -e  # Exit on error

echo "=========================================="
echo "WALS CLDF Data Setup"
echo "=========================================="
echo ""

# Check if cldf directory already exists
if [ -d "cldf" ]; then
    echo "✓ CLDF directory already exists"
    echo "Current size:"
    du -sh cldf/
    echo ""
    read -p "Do you want to replace it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing CLDF data"
        exit 0
    fi
    echo "Removing existing cldf directory..."
    rm -rf cldf/
fi

# Download from official repository
echo "Downloading CLDF data from official WALS repository..."
echo "(This may take a few minutes)"
echo ""

git clone --depth 1 https://github.com/cldf-datasets/wals.git /tmp/wals-cldf

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to download WALS repository"
    exit 1
fi

# Copy cldf directory
echo "Copying CLDF files..."
cp -r /tmp/wals-cldf/cldf .

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to copy CLDF files"
    exit 1
fi

echo "✓ CLDF data downloaded successfully!"
echo ""

# Check size
echo "CLDF directory size:"
du -sh cldf/
echo ""

# Count files
echo "Files in CLDF directory:"
ls -1 cldf/ | wc -l
echo ""

# Check if it's safe to add to git
SIZE=$(du -sb cldf/ | cut -f1)
SIZE_MB=$((SIZE / 1024 / 1024))

echo "Total size: ${SIZE_MB} MB"
echo ""

if [ $SIZE -gt 104857600 ]; then
    echo "⚠️  WARNING: CLDF directory is larger than 100 MB!"
    echo "GitHub has a 100 MB file size limit."
    echo ""
    echo "Options:"
    echo "1. Use Git LFS (git lfs track 'cldf/*.csv')"
    echo "2. Keep data locally only (add 'cldf/' to .gitignore)"
    echo "3. Use external storage (see CLDF_SETUP_GUIDE.md)"
    echo ""
    echo "For Streamlit Cloud deployment, consider using demo data only."
else
    echo "✓ Size is safe for GitHub (under 100 MB)"
    echo ""
    echo "To add to Git, run:"
    echo "  git add cldf/"
    echo "  git commit -m 'Add CLDF dataset'"
    echo "  git push"
fi

# Cleanup
echo ""
echo "Cleaning up temporary files..."
rm -rf /tmp/wals-cldf

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Test the apps with: ./run_wals_app.sh or ./run_streamlit_app.sh"
echo "2. (Optional) Add to Git if size is acceptable"
echo "3. Deploy to Streamlit Cloud for student access"
