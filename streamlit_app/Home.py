"""
WALS Explorer - Streamlit App
A web application for exploring the World Atlas of Language Structures

This is the main entry point for the Streamlit multi-page app.
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from streamlit_data_loader import WALSStreamlitLoader

# Page configuration
st.set_page_config(
    page_title="WALS Explorer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3498db;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stat-number {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .stat-label {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize data loader
@st.cache_resource
def get_data_loader():
    """Initialize and cache the data loader"""
    return WALSStreamlitLoader()

data_loader = get_data_loader()
stats = data_loader.get_statistics()

# Main page content
st.markdown('<h1 class="main-header">🌍 The World Atlas of Language Structures</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Explore typological features of the world\'s languages</p>', unsafe_allow_html=True)

# Show demo mode warning if applicable
if not stats['data_available']:
    st.markdown("""
    <div class="warning-box">
        <h3>📊 Demo Mode</h3>
        <p>Currently running with sample data. To use the full WALS dataset:</p>
        <ol>
            <li>Ensure you have the CLDF data in the <code>cldf/</code> directory</li>
            <li>If you don't have it, run: <code>cldfbench wals.makecldf</code></li>
            <li>Restart the application</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Statistics overview
st.markdown("## 📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{stats['languages']:,}</div>
        <div class="stat-label">Languages</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{stats['features']:,}</div>
        <div class="stat-label">Typological Features</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{stats['values']:,}</div>
        <div class="stat-label">Data Points</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{stats['families']:,}</div>
        <div class="stat-label">Language Families</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# About WALS
st.markdown("## 📖 About WALS")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    The **World Atlas of Language Structures (WALS)** is a comprehensive database of structural
    (phonological, grammatical, lexical) properties of languages gathered from descriptive materials.

    ### Key Features:
    - **2,500+ languages** from diverse language families worldwide
    - **192 typological features** covering phonology, morphology, syntax, and lexicon
    - **Geographic and genealogical information** for each language
    - **Extensive bibliographic references** linked to data points
    """)

with col2:
    st.markdown("""
    ### What You Can Do:
    - 🔍 **Browse Languages**: Explore languages with detailed filtering
    - 📊 **Explore Features**: Discover typological patterns
    - 🗺️ **View Map**: See geographic distribution
    - 📈 **View Statistics**: Analyze data distributions
    - 🔎 **Search**: Find specific languages or features

    ### Navigation:
    Use the sidebar to navigate between different sections of the application.
    """)

st.markdown("---")

# Quick Start Guide
st.markdown("## 🚀 Quick Start")

tab1, tab2, tab3, tab4 = st.tabs(["Languages", "Features", "Map", "Statistics"])

with tab1:
    st.markdown("""
    ### Browse Languages

    Navigate to the **1_🌐_Languages** page from the sidebar to:
    - Browse all languages in the dataset
    - Filter by language family or macroarea
    - Search for specific languages
    - View detailed information for each language
    - See all typological features for a language
    """)

with tab2:
    st.markdown("""
    ### Explore Features

    Visit the **2_📋_Features** page to:
    - Browse all 192 typological features
    - Search for specific features
    - View possible values for each feature
    - See which languages have data for each feature
    - Understand feature distributions
    """)

with tab3:
    st.markdown("""
    ### Interactive Map

    Check out the **3_🗺️_Map** page for:
    - Geographic visualization of all languages
    - Interactive map with language markers
    - Color-coding by language family or macroarea
    - Click markers to see language details
    """)

with tab4:
    st.markdown("""
    ### Statistics & Analysis

    Explore the **4_📊_Statistics** page for:
    - Data distribution charts
    - Language family analysis
    - Macroarea statistics
    - Interactive visualizations
    """)

st.markdown("---")

# Citation
st.markdown("## 📚 Citation")

st.info("""
**If you use WALS data in your research, please cite:**

Dryer, Matthew S. & Haspelmath, Martin (eds.) 2013.
*The World Atlas of Language Structures Online*.
Leipzig: Max Planck Institute for Evolutionary Anthropology.
(Available online at https://wals.info)
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 2rem;">
    <p>WALS Explorer • Built with Streamlit • Data from <a href="https://wals.info" target="_blank">WALS Online</a></p>
    <p>© 2024 • Licensed under CC-BY-4.0</p>
</div>
""", unsafe_allow_html=True)
