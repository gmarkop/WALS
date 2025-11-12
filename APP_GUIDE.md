# WALS Local Explorer - Quick Start Guide

This guide will help you get the WALS Local Explorer application running on your PC.

## What is WALS Local Explorer?

WALS Local Explorer is a web application that runs on your computer, allowing you to:
- Browse 2,500+ languages from around the world
- Explore 192 typological linguistic features
- View languages on an interactive map
- Search and filter linguistic data
- Generate statistics and visualizations

All of this works offline on your local machine (except for map tiles which require internet).

## Quick Start (5 Minutes)

### Step 1: Ensure Python is Installed

Open a terminal/command prompt and check:

```bash
python3 --version
```

You should see Python 3.7 or higher. If not, install Python from https://www.python.org/downloads/

### Step 2: Navigate to the Application

```bash
cd /path/to/WALS/wals_app
```

Replace `/path/to/WALS` with the actual path where you cloned/downloaded the repository.

### Step 3: Install Requirements

```bash
pip install -r requirements.txt
```

This will install Flask and other necessary libraries. It may take a minute or two.

### Step 4: Run the Application

```bash
python app.py
```

You should see:

```
============================================================
WALS Local Explorer
============================================================
Starting server...
Open your browser and navigate to: http://localhost:5000
Press Ctrl+C to stop the server
============================================================
 * Running on http://0.0.0.0:5000
```

### Step 5: Open in Browser

Open your web browser and go to:

**http://localhost:5000**

You should see the WALS Local Explorer home page!

## What You Can Do

### 1. Browse Languages

- Click **"Languages"** in the top menu
- Use filters to find languages by:
  - Family (e.g., Indo-European, Sino-Tibetan)
  - Macroarea (e.g., Eurasia, Africa)
  - Search term (e.g., "English", "Spanish")
- Click **"View"** on any language to see:
  - Classification information
  - Geographic coordinates
  - All typological features for that language

### 2. Explore Features

- Click **"Features"** in the top menu
- Browse typological features like:
  - "Order of Subject, Object and Verb"
  - "Consonant Inventories"
  - "Vowel Quality Inventories"
- Click **"View"** on any feature to see:
  - Possible values for that feature
  - All languages with data for that feature

### 3. View Interactive Map

- Click **"Map"** in the top menu
- See all languages plotted on a world map
- Click on markers to see language details
- Zoom and pan to explore different regions
- Toggle marker clustering on/off

### 4. Search

- Use the search box in the top right corner
- Or click **"Search"** for advanced options
- Find languages by name or code
- Find features by name

### 5. View Statistics

- Click **"Statistics"** in the top menu
- See charts showing:
  - Language distribution by family
  - Language distribution by macroarea
- View tables with detailed counts

## Demo Mode vs Full Data

### Demo Mode (Default)

By default, the application runs with **sample data** that includes:
- 5 example languages
- 3 example features
- Sample data points

This is perfect for:
- Testing the application
- Understanding how it works
- Demonstrations

You'll see a yellow warning box on the home page indicating demo mode.

### Full Data Mode

To use the complete WALS dataset with 2,500+ languages:

1. Ensure you have the WALS CLDF data in a `cldf/` directory
2. If you don't have it, generate it using:

```bash
cd ..  # Go to parent directory
cldfbench wals.makecldf --glottolog /path/to/glottolog
cd wals_app  # Return to app directory
python app.py  # Restart
```

**Note**: This requires the raw WALS data files and Glottolog.

## Common Tasks

### Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

### Restarting the Server

```bash
python app.py
```

### Changing the Port

If port 5000 is already in use, edit `app.py` and change:

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

to a different port like:

```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

Then access at `http://localhost:8080`

## Troubleshooting

### "Command not found: python"

Try `python3` instead:

```bash
python3 app.py
```

### "Port already in use"

Either:
- Change the port (see above)
- Or find and stop the other application using port 5000

### "Module not found"

Reinstall requirements:

```bash
pip install -r requirements.txt --upgrade
```

### Map Tiles Not Loading

- Check your internet connection (map tiles come from OpenStreetMap)
- Try refreshing the page

### No Languages Showing

This is normal in demo mode - you'll see 5 sample languages. To get all languages, you need the full CLDF dataset.

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.7 or higher
- **RAM**: 512 MB minimum (2 GB recommended for full dataset)
- **Disk Space**:
  - 50 MB for application
  - 500 MB for full CLDF dataset
- **Browser**: Any modern browser (Chrome, Firefox, Safari, Edge)
- **Internet**: Only needed for map tiles (optional)

## Features Overview

| Feature | Description | Demo Mode | Full Data Mode |
|---------|-------------|-----------|----------------|
| Language Browser | Browse all languages | 5 languages | 2,500+ languages |
| Feature Explorer | Explore typological features | 3 features | 192 features |
| Interactive Map | Geographic visualization | ✓ | ✓ |
| Search | Find languages and features | ✓ | ✓ |
| Statistics | Data visualizations | ✓ | ✓ |
| Filtering | By family, area, etc. | ✓ | ✓ |
| Responsive Design | Works on all devices | ✓ | ✓ |

## Next Steps

1. **Explore the demo data** to familiarize yourself with the interface
2. **Try different searches** and filters
3. **View the map** to see geographic distribution
4. **Check statistics** for data visualizations
5. **If you need full data**, follow the instructions above to generate CLDF files

## Getting Full WALS Data

The full WALS dataset is available from:
- **WALS Online**: https://wals.info
- **GitHub**: https://github.com/cldf-datasets/wals

To convert it to CLDF format (required for this app):

```bash
# Clone the repository if you haven't already
git clone https://github.com/cldf-datasets/wals.git
cd wals

# Install cldfbench
pip install cldfbench

# Generate CLDF (requires raw WALS data and Glottolog)
cldfbench wals.makecldf --glottolog /path/to/glottolog

# The 'cldf' directory will be created with all data
# Now run the app:
cd wals_app
python app.py
```

## Need Help?

- Check the **README.md** in the `wals_app` directory for detailed documentation
- Visit the **About** page in the application for information about WALS
- For WALS data issues: https://github.com/cldf-datasets/wals/issues

## Enjoy Exploring!

The WALS dataset contains fascinating information about the world's languages. Explore and discover linguistic patterns across different language families and geographic regions!
