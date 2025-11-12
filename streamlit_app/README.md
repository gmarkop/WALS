# WALS Explorer - Streamlit App

A Streamlit web application for exploring the World Atlas of Language Structures (WALS) dataset. Perfect for deploying online for students and researchers.

## Features

- 🌐 **Language Browser**: Search and filter 2,500+ languages
- 📋 **Feature Explorer**: Explore 192 typological features
- 🗺️ **Interactive Map**: Geographic visualization with PyDeck
- 📊 **Statistics**: Interactive charts and data visualizations
- 📱 **Responsive Design**: Works on all devices
- ☁️ **Cloud-Ready**: Easy deployment to Streamlit Cloud, Heroku, or other platforms

## Quick Start (Local)

### 1. Install Dependencies

```bash
cd streamlit_app
pip install -r requirements.txt
```

### 2. Run the App

```bash
streamlit run Home.py
```

The app will open in your browser at `http://localhost:8501`

## Deployment Options

### Option 1: Streamlit Cloud (Recommended for Students)

**Streamlit Cloud is FREE and perfect for educational use!**

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add Streamlit WALS app"
   git push
   ```

2. **Go to [share.streamlit.io](https://share.streamlit.io)**

3. **Sign in with GitHub**

4. **Click "New app"**

5. **Configure your app:**
   - Repository: `your-username/WALS`
   - Branch: `main` (or your branch name)
   - Main file path: `streamlit_app/Home.py`

6. **Click "Deploy"**

Your app will be live in a few minutes with a URL like:
`https://your-username-wals-app.streamlit.app`

#### Advantages:
- ✅ **Free** for public repositories
- ✅ Automatic HTTPS
- ✅ Easy updates (just push to GitHub)
- ✅ No server management
- ✅ Perfect for sharing with students

### Option 2: Heroku

1. **Install Heroku CLI**

2. **Create `Procfile`:**
   ```
   web: sh setup.sh && streamlit run Home.py
   ```

3. **Create `setup.sh`:**
   ```bash
   mkdir -p ~/.streamlit/
   echo "[server]
   headless = true
   port = $PORT
   enableCORS = false
   " > ~/.streamlit/config.toml
   ```

4. **Deploy:**
   ```bash
   heroku create wals-explorer
   git push heroku main
   ```

### Option 3: Docker

1. **Create `Dockerfile`:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY streamlit_app/ /app/
   RUN pip install -r requirements.txt
   EXPOSE 8501
   CMD ["streamlit", "run", "Home.py"]
   ```

2. **Build and run:**
   ```bash
   docker build -t wals-app .
   docker run -p 8501:8501 wals-app
   ```

## App Structure

```
streamlit_app/
├── Home.py                      # Main entry point
├── streamlit_data_loader.py     # Data loading module
├── requirements.txt             # Python dependencies
├── README.md                   # This file
├── .streamlit/
│   └── config.toml             # Streamlit configuration
└── pages/
    ├── 1_🌐_Languages.py       # Languages browser
    ├── 2_📋_Features.py         # Features explorer
    ├── 3_🗺️_Map.py             # Interactive map
    └── 4_📊_Statistics.py       # Statistics & charts
```

## Data Modes

### Demo Mode (Default)
- Runs with sample data (5 languages, 3 features)
- Perfect for testing and demonstrations
- No setup required

### Full Data Mode
- Requires CLDF dataset in `../cldf/` directory
- 2,679 languages, 192 features
- Full WALS database

To use full data:
1. Generate CLDF files: `cldfbench wals.makecldf`
2. Ensure `cldf/` directory is in the parent folder
3. Restart the app

## Configuration

### Customize Theme

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor="#3498db"        # Primary accent color
backgroundColor="#ffffff"      # Background color
secondaryBackgroundColor="#f0f2f6"  # Sidebar color
textColor="#262730"           # Text color
font="sans serif"             # Font family
```

### Adjust Port

Edit `.streamlit/config.toml`:

```toml
[server]
port = 8502  # Change port here
```

## Features Details

### 1. Languages Browser
- Search by name or code
- Filter by family or macroarea
- View detailed language information
- See all typological features for each language
- Pagination for large datasets

### 2. Features Explorer
- Browse all typological features
- Search by feature name
- View possible values for each feature
- See value distribution across languages
- Interactive charts

### 3. Interactive Map
- Geographic visualization using PyDeck
- Color by family or macroarea
- Click markers for language details
- Zoom and pan functionality
- Export data as CSV

### 4. Statistics
- Overview metrics
- Family distribution charts
- Macroarea pie charts
- Downloadable data tables
- Interactive Plotly visualizations

## Performance Tips

### For Large Datasets

1. **Use caching** (already implemented with `@st.cache_resource` and `@st.cache_data`)

2. **Implement pagination** (already included)

3. **Limit initial displays:**
   ```python
   # Show first 100 items by default
   display_data = data[:100]
   ```

4. **Use data sampling for charts:**
   ```python
   # Sample for faster rendering
   sample = df.sample(n=1000) if len(df) > 1000 else df
   ```

## Troubleshooting

### Import Errors

If you see import errors, ensure you're in the correct directory:
```bash
cd streamlit_app
streamlit run Home.py
```

### Port Already in Use

Change the port in `.streamlit/config.toml` or run:
```bash
streamlit run Home.py --server.port 8502
```

### Map Not Loading

Ensure `pydeck` is installed:
```bash
pip install pydeck
```

### Memory Issues

For very large datasets, increase memory limits in `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 200
```

## Sharing with Students

### Option 1: Streamlit Cloud URL
Deploy to Streamlit Cloud and share the URL:
```
https://your-app.streamlit.app
```

### Option 2: Share the Code
Students can run locally:
```bash
git clone https://github.com/your-username/WALS.git
cd WALS/streamlit_app
pip install -r requirements.txt
streamlit run Home.py
```

### Option 3: Embed in Learning Management System
Add the Streamlit Cloud URL to your LMS (Canvas, Moodle, etc.)

## Educational Use

This app is perfect for:
- **Linguistics courses**: Explore language typology
- **Research projects**: Analyze cross-linguistic patterns
- **Student assignments**: Interactive data exploration
- **Presentations**: Live demonstrations of linguistic diversity
- **Independent study**: Self-paced learning

## License

This application code is provided for working with WALS data.

**WALS data is licensed under CC-BY-4.0.**

### Citation

When using WALS data, please cite:

> Dryer, Matthew S. & Haspelmath, Martin (eds.) 2013. *The World Atlas of Language Structures Online*. Leipzig: Max Planck Institute for Evolutionary Anthropology. (Available online at https://wals.info)

## Resources

- **WALS Online**: https://wals.info
- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Cloud**: https://share.streamlit.io
- **CLDF Specification**: https://cldf.clld.org
- **GitHub Repository**: https://github.com/cldf-datasets/wals

## Support

For issues:
- **WALS data**: https://github.com/cldf-datasets/wals/issues
- **Streamlit**: https://discuss.streamlit.io
- **This app**: Check the troubleshooting section above

## Version

Version 1.0.0 - Initial Release

## Updates

To update the app after deployment:

**Streamlit Cloud:**
Just push to GitHub - updates automatically!

**Local:**
```bash
git pull
pip install -r requirements.txt --upgrade
streamlit run Home.py
```

---

**Built with ❤️ using Streamlit • Perfect for linguistics education**
