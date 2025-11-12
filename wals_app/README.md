# WALS Local Explorer

A web-based application for exploring the World Atlas of Language Structures (WALS) dataset on your local computer.

## Features

- **Language Browser**: Browse and search through thousands of languages with detailed information
- **Feature Explorer**: Explore 192 typological features across 11 linguistic domains
- **Interactive Map**: Visualize the geographic distribution of languages using Leaflet
- **Statistics & Visualizations**: View data distributions with interactive charts
- **Advanced Search**: Find languages and features quickly
- **Offline Access**: Works entirely on your local machine once set up
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- The WALS CLDF dataset (optional - app includes demo data)

## Installation

### 1. Navigate to the Application Directory

```bash
cd wals_app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. (Optional) Prepare CLDF Data

If you want to use the full WALS dataset instead of the demo data:

```bash
# Go to the parent directory
cd ..

# Generate CLDF data (requires raw WALS data)
cldfbench wals.makecldf --glottolog /path/to/glottolog

# This will create a 'cldf' directory with all the data
```

**Note**: If you don't have the raw WALS data, the application will run with sample demo data that demonstrates all features.

## Running the Application

### Start the Server

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Open in Browser

Navigate to: **http://localhost:5000**

You should see the WALS Local Explorer home page with statistics and navigation options.

### Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Application Structure

```
wals_app/
├── app.py                  # Main Flask application
├── data_loader.py          # Data loading and query module
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── languages.html     # Language browser
│   ├── language_detail.html  # Individual language page
│   ├── features.html      # Feature browser
│   ├── feature_detail.html   # Individual feature page
│   ├── search.html        # Search page
│   ├── map.html           # Interactive map
│   ├── statistics.html    # Statistics & charts
│   ├── about.html         # About page
│   ├── 404.html           # Not found page
│   └── 500.html           # Error page
└── static/
    ├── css/
    │   └── style.css      # Application styles
    └── js/
        └── (JavaScript files if needed)
```

## Using the Application

### Browse Languages

1. Click **Languages** in the navigation menu
2. Use filters to narrow down by family, macroarea, or search term
3. Click **View** on any language to see detailed information

### Explore Features

1. Click **Features** in the navigation menu
2. Search for specific features
3. Click **View** to see all languages with data for that feature

### Interactive Map

1. Click **Map** in the navigation menu
2. Explore language locations geographically
3. Click markers to see language information

### Search

1. Use the search box in the navigation bar
2. Or visit the Search page for advanced options
3. Search by language name, code, or feature name

### View Statistics

1. Click **Statistics** in the navigation menu
2. View charts showing language distribution by family and macroarea
3. See top language families in tabular format

## Configuration

### Changing the Port

Edit `app.py` and modify the last line:

```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change port here
```

### Using Custom CLDF Data

Edit `data_loader.py` and modify the `WALSDataLoader` initialization:

```python
data_loader = WALSDataLoader(cldf_path='/path/to/your/cldf/directory')
```

### Debug Mode

For production use, disable debug mode in `app.py`:

```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## Data Sources

### With Full CLDF Data

When the `cldf/` directory is present, the application loads:
- Languages from `languages.csv`
- Features from `parameters.csv`
- Value codes from `codes.csv`
- Data points from `values.csv`
- Contributions from `chapters.csv`

### Demo Mode

Without CLDF data, the application uses sample data to demonstrate functionality:
- 5 sample languages (English, Spanish, Mandarin, Arabic, Japanese)
- 3 sample features
- Sample typological values

## Troubleshooting

### Port Already in Use

If port 5000 is already in use:

```bash
# Find and kill the process
lsof -ti:5000 | xargs kill -9

# Or use a different port (see Configuration section)
```

### Missing Dependencies

```bash
pip install -r requirements.txt --upgrade
```

### No Data Showing

1. Check if the `cldf/` directory exists in the parent directory
2. If not, the app will use demo data (this is expected)
3. To get full data, generate CLDF files using `cldfbench`

### Map Not Loading

1. Ensure internet connection (map tiles load from OpenStreetMap)
2. Check browser console for JavaScript errors
3. Try clearing browser cache

## Technologies Used

- **Flask**: Python web framework
- **CLDF/pycldf**: Cross-Linguistic Data Format handling
- **Leaflet**: Interactive maps
- **Chart.js**: Data visualizations
- **HTML/CSS**: Responsive web design

## Contributing

This application was created as a local tool for exploring WALS data. Feel free to:

- Customize the styling in `static/css/style.css`
- Add new features to `app.py`
- Enhance data loading in `data_loader.py`
- Improve templates in the `templates/` directory

## License

This application code is provided as-is for working with WALS data.

The WALS data itself is licensed under **CC-BY-4.0**. Please cite:

> Dryer, Matthew S. & Haspelmath, Martin (eds.) 2013. The World Atlas of Language Structures Online. Leipzig: Max Planck Institute for Evolutionary Anthropology. (Available online at https://wals.info)

## Resources

- **WALS Online**: https://wals.info
- **WALS CLDF Dataset**: https://github.com/cldf-datasets/wals
- **CLDF Specification**: https://cldf.clld.org
- **Flask Documentation**: https://flask.palletsprojects.com/

## Support

For issues with:
- **WALS data**: Visit https://github.com/cldf-datasets/wals/issues
- **This application**: Check the troubleshooting section above

## Version

Version 1.0.0 - Initial Release
