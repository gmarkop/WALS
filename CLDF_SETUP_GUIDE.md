# Adding CLDF Data to GitHub - Complete Guide

## Overview

The CLDF (Cross-Linguistic Data Format) data contains the actual WALS database in a standardized format. This guide shows you how to add it to your GitHub repository.

## Important Considerations

⚠️ **File Size Limits:**
- GitHub has a **100 MB** file size limit
- GitHub recommends repositories stay under **1 GB**
- CLDF data can be large (100-500 MB depending on the dataset)

## Method 1: Add CLDF Data Directly (Recommended if Files < 100 MB)

### Step 1: Check if You Have Raw WALS Data

The WALS CLDF data is typically generated from raw database exports. Check if you have a `raw/` directory:

```bash
ls -la raw/ 2>/dev/null || echo "No raw data found"
```

If you don't have raw data, see **Method 2** below.

### Step 2: Install cldfbench (if not installed)

```bash
pip install cldfbench
```

### Step 3: Generate CLDF Data

You need Glottolog data as well:

```bash
# Clone Glottolog (if you don't have it)
git clone https://github.com/glottolog/glottolog.git /tmp/glottolog

# Generate CLDF data
cldfbench wals.makecldf --glottolog /tmp/glottolog
```

This will create a `cldf/` directory with CSV files and metadata.

### Step 4: Check the Size

```bash
du -sh cldf/
```

If it's **under 100 MB**, you can add it directly to GitHub.

### Step 5: Add to Git

```bash
# Add the entire cldf directory
git add cldf/

# Check what will be committed
git status

# Commit
git commit -m "Add CLDF dataset for WALS"

# Push
git push origin your-branch-name
```

## Method 2: Download Pre-Generated CLDF Data from GitHub

The official WALS CLDF repository already has the data:

### Step 1: Clone the Official WALS CLDF Repository

```bash
# In a temporary location
cd /tmp
git clone https://github.com/cldf-datasets/wals.git wals-cldf
```

### Step 2: Copy the CLDF Directory

```bash
# Go back to your repository
cd /path/to/your/WALS

# Copy the cldf directory
cp -r /tmp/wals-cldf/cldf .

# Check the size
du -sh cldf/
```

### Step 3: Add to Your Repository

```bash
# Add to git
git add cldf/

# Commit
git commit -m "Add CLDF dataset from official WALS repository"

# Push
git push origin your-branch-name
```

## Method 3: Use Git LFS for Large Files (If Files > 100 MB)

If your CLDF files are larger than 100 MB, use Git Large File Storage:

### Step 1: Install Git LFS

```bash
# On Ubuntu/Debian
sudo apt-get install git-lfs

# On macOS
brew install git-lfs

# On Windows (with Git for Windows)
# Git LFS is included
```

### Step 2: Initialize Git LFS

```bash
git lfs install
```

### Step 3: Track Large CSV Files

```bash
# Track all CSV files in cldf directory
git lfs track "cldf/*.csv"
git lfs track "cldf/**/*.csv"

# This creates/updates .gitattributes
git add .gitattributes
git commit -m "Configure Git LFS for CLDF files"
```

### Step 4: Add CLDF Files

```bash
git add cldf/
git commit -m "Add CLDF dataset using Git LFS"
git push origin your-branch-name
```

**Note:** GitHub provides 1 GB of free LFS storage per month.

## Method 4: Reference External Storage (Best for Very Large Datasets)

If the data is too large or you don't want it in the repository:

### Option A: Link to Official Repository

Add a note in your README:

```markdown
## CLDF Data

The CLDF data is not included in this repository due to size constraints.

To use the full dataset:

1. Clone the official WALS CLDF repository:
   ```bash
   git clone https://github.com/cldf-datasets/wals.git /tmp/wals-cldf
   cp -r /tmp/wals-cldf/cldf .
   ```

2. Or download from: https://github.com/cldf-datasets/wals/tree/master/cldf
```

### Option B: Use Zenodo or Figshare

Upload the CLDF data to a data repository:

1. Go to https://zenodo.org or https://figshare.com
2. Upload your `cldf/` directory
3. Get a DOI and download URL
4. Add download script to your repository

### Option C: Host on University Storage

If your university provides storage:

1. Upload CLDF directory to university file storage
2. Add download script to repository
3. Share access with students

## Method 5: For Streamlit Cloud Deployment

If you're deploying to Streamlit Cloud and files are too large:

### Option A: Exclude from Git, Generate on First Run

Create `streamlit_app/setup_data.py`:

```python
import os
import subprocess
from pathlib import Path

def setup_cldf_data():
    """Download and setup CLDF data on first run"""
    cldf_path = Path(__file__).parent.parent / 'cldf'

    if not cldf_path.exists():
        print("Downloading CLDF data...")
        # Clone and copy
        subprocess.run([
            'git', 'clone', '--depth', '1',
            'https://github.com/cldf-datasets/wals.git',
            '/tmp/wals-cldf'
        ])
        subprocess.run(['cp', '-r', '/tmp/wals-cldf/cldf', str(cldf_path)])
        print("CLDF data downloaded!")
```

Call this in your `Home.py` before loading data.

### Option B: Use Demo Data Only

For Streamlit Cloud deployment, you might want to use only demo data (which is already included in the code) to keep the repository small.

## Recommended Approach

**For your situation, I recommend:**

1. **If you plan to deploy online (Streamlit Cloud):**
   - Use **Method 5, Option B** (demo data only)
   - This keeps your repository small and deployment fast
   - Perfect for student demonstrations

2. **If you want full data locally:**
   - Use **Method 2** (download from official repo)
   - Check file size
   - If < 100 MB: Add directly to Git (Method 1)
   - If > 100 MB: Use Git LFS (Method 3) or external reference (Method 4)

## Quick Start Script

Save this as `setup_cldf.sh`:

```bash
#!/bin/bash

echo "Setting up CLDF data for WALS..."

# Check if cldf directory already exists
if [ -d "cldf" ]; then
    echo "✓ CLDF directory already exists"
    du -sh cldf/
    exit 0
fi

# Download from official repository
echo "Downloading from official WALS CLDF repository..."
git clone --depth 1 https://github.com/cldf-datasets/wals.git /tmp/wals-cldf

# Copy cldf directory
cp -r /tmp/wals-cldf/cldf .

# Check size
echo "CLDF data size:"
du -sh cldf/

# Check if it's safe to add to git
SIZE=$(du -sb cldf/ | cut -f1)
if [ $SIZE -gt 104857600 ]; then
    echo "⚠️  Warning: CLDF directory is larger than 100 MB"
    echo "Consider using Git LFS or external storage"
else
    echo "✓ Safe to add to Git"
    echo "Run: git add cldf/ && git commit -m 'Add CLDF data'"
fi

# Cleanup
rm -rf /tmp/wals-cldf

echo "Done!"
```

Make it executable and run:

```bash
chmod +x setup_cldf.sh
./setup_cldf.sh
```

## What's in the CLDF Directory?

Once generated/downloaded, you'll have:

```
cldf/
├── StructureDataset-metadata.json  # Main metadata file
├── languages.csv                   # All languages
├── parameters.csv                  # Typological features
├── codes.csv                       # Possible values
├── values.csv                      # Actual data points
├── chapters.csv                    # Contributions
├── sources.bib                     # Bibliography
├── areas.csv                       # Linguistic areas
├── contributors.csv                # Authors
└── ... (other files)
```

## Checking Your Work

After adding CLDF data:

```bash
# Verify files exist
ls -la cldf/

# Check git status
git status

# See what will be pushed
git diff --stat origin/your-branch

# Check repository size
du -sh .git/
```

## Troubleshooting

### "File too large" Error

```
remote: error: File cldf/values.csv is 105.00 MB; this exceeds GitHub's file size limit of 100.00 MB
```

**Solution:** Use Git LFS (Method 3) or external storage (Method 4)

### "Permission denied" When Pushing

**Solution:** You might be exceeding repository size limits. Check:

```bash
du -sh .git/
```

If over 1 GB, consider cleaning up or using external storage.

### Streamlit Cloud Deployment Fails

**Solution:** Streamlit Cloud has memory limits. Use demo data or implement lazy loading.

## Summary

**Simplest approach for you:**

```bash
# Download official CLDF data
git clone --depth 1 https://github.com/cldf-datasets/wals.git /tmp/wals-cldf
cp -r /tmp/wals-cldf/cldf .

# Check size
du -sh cldf/

# Add to git (if < 100 MB)
git add cldf/
git commit -m "Add CLDF dataset"
git push origin claude/create-comprehensive-readme-011CV1b6KsavKWMQjxpMPxEA
```

Need help with any of these steps? Let me know!
