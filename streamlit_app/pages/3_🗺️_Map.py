"""
Interactive Map Page
Visualize the geographic distribution of WALS languages
"""

import streamlit as st
import pandas as pd
import pydeck as pdk
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from streamlit_data_loader import WALSStreamlitLoader

st.set_page_config(page_title="Map - WALS Explorer", page_icon="🗺️", layout="wide")

# Initialize data loader
@st.cache_resource
def get_data_loader():
    return WALSStreamlitLoader()

data_loader = get_data_loader()

# Page header
st.title("🗺️ Geographic Distribution of Languages")
st.markdown("Explore where languages are spoken around the world")

# Sidebar controls
st.sidebar.header("Map Settings")

# Color by option
color_by = st.sidebar.radio(
    "Color markers by:",
    ["Family", "Macroarea"],
    index=1
)

# Get language data with coordinates
languages = data_loader.get_languages_with_coordinates()

if not languages:
    st.warning("No geographic data available. Languages need latitude and longitude coordinates.")
    st.stop()

# Prepare data for map
map_data = []

# Define colors for families/macroareas
if color_by == "Family":
    unique_values = sorted(set(lang['family'] for lang in languages))
else:
    unique_values = sorted(set(lang['macroarea'] for lang in languages))

# Create color map
color_palette = [
    [255, 99, 132],
    [54, 162, 235],
    [255, 206, 86],
    [75, 192, 192],
    [153, 102, 255],
    [255, 159, 64],
    [231, 76, 60],
    [46, 204, 113],
    [52, 152, 219],
    [155, 89, 182],
]

color_map = {}
for i, value in enumerate(unique_values):
    color_map[value] = color_palette[i % len(color_palette)]

# Prepare map data
for lang in languages:
    color_key = lang['family'] if color_by == "Family" else lang['macroarea']
    color = color_map.get(color_key, [128, 128, 128])

    map_data.append({
        'lat': lang['lat'],
        'lon': lang['lon'],
        'name': lang['name'],
        'id': lang['id'],
        'family': lang['family'],
        'macroarea': lang['macroarea'],
        'genus': lang['genus'],
        'iso': lang['iso'],
        'color': color
    })

df = pd.DataFrame(map_data)

# Display legend
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Legend - {color_by}:**")

for value in unique_values[:10]:  # Show first 10
    color = color_map[value]
    st.sidebar.markdown(
        f'<div style="display: flex; align-items: center;">'
        f'<div style="width: 20px; height: 20px; background-color: rgb({color[0]}, {color[1]}, {color[2]}); '
        f'border-radius: 50%; margin-right: 10px;"></div>'
        f'{value}</div>',
        unsafe_allow_html=True
    )

if len(unique_values) > 10:
    st.sidebar.caption(f"... and {len(unique_values) - 10} more")

# Create map
st.subheader(f"Languages by {color_by}")

# PyDeck layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["lon", "lat"],
    get_color="color",
    get_radius=50000,
    pickable=True,
    opacity=0.7,
    stroked=True,
    filled=True,
    radius_scale=1,
    radius_min_pixels=3,
    radius_max_pixels=10,
)

# Set view state
view_state = pdk.ViewState(
    latitude=20,
    longitude=0,
    zoom=1.5,
    pitch=0,
)

# Tooltip
tooltip = {
    "html": "<b>{name}</b><br/>"
            "Code: {id}<br/>"
            "Family: {family}<br/>"
            "Genus: {genus}<br/>"
            "Macroarea: {macroarea}<br/>"
            "ISO: {iso}",
    "style": {
        "backgroundColor": "steelblue",
        "color": "white"
    }
}

# Render map
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_style="mapbox://styles/mapbox/light-v10",
)

st.pydeck_chart(r)

# Statistics
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Languages", f"{len(languages):,}")

with col2:
    if color_by == "Family":
        st.metric("Language Families", len(unique_values))
    else:
        st.metric("Macroareas", len(unique_values))

with col3:
    st.metric("Continents", "6")

# Show data table
with st.expander("📊 View Language Data Table"):
    display_df = pd.DataFrame([
        {
            'Code': lang['id'],
            'Name': lang['name'],
            'Family': lang['family'],
            'Macroarea': lang['macroarea'],
            'Latitude': f"{lang['lat']:.2f}",
            'Longitude': f"{lang['lon']:.2f}",
        }
        for lang in languages
    ])

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # Download button
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="wals_languages_geographic.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d;">
    <p>💡 Tip: Click on markers to see language details | Use mouse to zoom and pan</p>
</div>
""", unsafe_allow_html=True)
