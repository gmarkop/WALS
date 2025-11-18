"""
Feature Geographic Distribution Page
Visualize how feature values are distributed geographically
"""

import streamlit as st
import pandas as pd
import pydeck as pdk
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from streamlit_data_loader import WALSStreamlitLoader

st.set_page_config(page_title="Feature Map - WALS Explorer", page_icon="🌏", layout="wide")

# Initialize data loader
@st.cache_resource
def get_data_loader():
    return WALSStreamlitLoader()

data_loader = get_data_loader()

# Page header
st.title("🌏 Feature Geographic Distribution")
st.markdown("Visualize how typological features are distributed across the world's languages")

# Sidebar - Feature selection
st.sidebar.header("Select Feature")

# Get all features
all_features = data_loader.get_all_features()

if not all_features:
    st.error("No features available in the dataset.")
    st.stop()

# Create feature options
feature_options = {
    f"{feat.get('ID')} - {feat.get('Name')}": feat.get('ID')
    for feat in all_features
}

selected_feature_label = st.sidebar.selectbox(
    "Choose a typological feature:",
    options=list(feature_options.keys()),
    help="Select a feature to see its geographic distribution"
)

selected_feature_id = feature_options[selected_feature_label]

# Get feature details
feature = data_loader.get_feature(selected_feature_id)
codes = data_loader.get_codes_for_feature(selected_feature_id)
values = data_loader.get_values_for_feature(selected_feature_id)

# Display feature information
st.markdown(f"### {feature.get('Name')}")
st.markdown(f"**Feature ID:** `{feature.get('ID')}` | **Chapter:** {feature.get('Chapter_ID', 'N/A')}")

# Get languages with coordinates
languages_with_coords = data_loader.get_languages_with_coordinates()

# Create a map of language_id to coordinates
lang_coords = {lang['id']: lang for lang in languages_with_coords}

# Prepare map data with feature values
map_data = []

# Create color palette for feature values
color_palette = [
    [231, 76, 60],   # Red
    [52, 152, 219],  # Blue
    [46, 204, 113],  # Green
    [241, 196, 15],  # Yellow
    [155, 89, 182],  # Purple
    [230, 126, 34],  # Orange
    [26, 188, 156],  # Turquoise
    [236, 240, 241], # Light gray
    [149, 165, 166], # Gray
    [192, 57, 43],   # Dark red
]

# Map code IDs to colors
code_color_map = {}
for i, code in enumerate(codes):
    code_color_map[code.get('ID')] = color_palette[i % len(color_palette)]

# Also create a name-to-color map for the legend
value_color_map = {}
for i, code in enumerate(codes):
    value_color_map[code.get('Name')] = color_palette[i % len(color_palette)]

# Process values and create map points
languages_with_data = set()
for value in values:
    lang_id = value.get('Language_ID')
    code_id = value.get('Code_ID')

    if lang_id in lang_coords and code_id in code_color_map:
        lang = lang_coords[lang_id]
        color = code_color_map[code_id]

        map_data.append({
            'lat': lang['lat'],
            'lon': lang['lon'],
            'name': lang['name'],
            'id': lang['id'],
            'family': lang['family'],
            'value': value.get('Code_Name', 'Unknown'),
            'color': color
        })
        languages_with_data.add(lang_id)

# Statistics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Languages with Data", len(languages_with_data))

with col2:
    st.metric("Possible Values", len(codes))

with col3:
    coverage = (len(languages_with_data) / len(languages_with_coords) * 100) if languages_with_coords else 0
    st.metric("Geographic Coverage", f"{coverage:.1f}%")

# Display legend
st.sidebar.markdown("---")
st.sidebar.markdown("**Legend - Feature Values:**")

# Sort codes by number for consistent display
sorted_codes = sorted(codes, key=lambda x: int(x.get('Number', 0)))

for code in sorted_codes:
    code_name = code.get('Name')
    color = value_color_map.get(code_name, [128, 128, 128])

    # Count languages with this value
    count = sum(1 for item in map_data if item['value'] == code_name)

    st.sidebar.markdown(
        f'<div style="display: flex; align-items: center; margin-bottom: 8px;">'
        f'<div style="width: 20px; height: 20px; background-color: rgb({color[0]}, {color[1]}, {color[2]}); '
        f'border-radius: 50%; margin-right: 10px; border: 1px solid #ccc;"></div>'
        f'<div><strong>{code_name}</strong> ({count} languages)</div>'
        f'</div>',
        unsafe_allow_html=True
    )

# Show value descriptions if available
with st.expander("ℹ️ View Feature Value Descriptions"):
    for code in sorted_codes:
        st.markdown(f"**{code.get('Number')}. {code.get('Name')}**")
        if code.get('Description'):
            st.markdown(f"{code.get('Description')}")
        else:
            st.markdown("_No description available_")
        st.markdown("---")

# Create map
if map_data:
    st.markdown("---")
    st.subheader("Geographic Distribution")

    df = pd.DataFrame(map_data)

    # PyDeck layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color="color",
        get_radius=50000,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=1,
        radius_min_pixels=4,
        radius_max_pixels=12,
        line_width_min_pixels=1,
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
                f"<strong>{feature.get('Name')}:</strong> {{value}}",
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

    # Analysis section
    st.markdown("---")
    st.subheader("📊 Value Distribution Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # Bar chart of value counts
        value_counts = df['value'].value_counts().reset_index()
        value_counts.columns = ['Value', 'Count']

        st.markdown("**Languages per Value:**")
        st.bar_chart(value_counts.set_index('Value'))

    with col2:
        # Pie chart
        import plotly.express as px

        fig = px.pie(
            value_counts,
            values='Count',
            names='Value',
            title='Distribution of Feature Values',
            color_discrete_sequence=[f'rgb({c[0]}, {c[1]}, {c[2]})' for c in [value_color_map[v] for v in value_counts['Value']]]
        )

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    # Data table
    with st.expander("📋 View Detailed Data Table"):
        display_df = df[['id', 'name', 'family', 'value', 'lat', 'lon']].copy()
        display_df.columns = ['Code', 'Language', 'Family', 'Feature Value', 'Latitude', 'Longitude']

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        # Download button
        csv = display_df.to_csv(index=False)
        st.download_button(
            label=f"📥 Download {feature.get('ID')} Distribution Data",
            data=csv,
            file_name=f"wals_feature_{feature.get('ID')}_distribution.csv",
            mime="text/csv"
        )

    # Geographic patterns analysis
    st.markdown("---")
    st.subheader("🌍 Geographic Patterns")

    # Group by macroarea if possible
    # This would require joining with language data - simplified version
    st.info(
        f"**Observation:** This map shows how **{feature.get('Name')}** varies across "
        f"{len(languages_with_data)} languages worldwide. Look for clustering patterns "
        f"that might indicate areal features or genetic relationships."
    )

    # Top families for each value
    st.markdown("**Top Language Families by Value:**")

    for code in sorted_codes[:5]:  # Show top 5 values
        code_name = code.get('Name')
        languages_with_value = df[df['value'] == code_name]

        if len(languages_with_value) > 0:
            family_counts = languages_with_value['family'].value_counts().head(5)

            st.markdown(f"**{code_name}** ({len(languages_with_value)} languages):")
            for family, count in family_counts.items():
                st.markdown(f"- {family}: {count} languages")
            st.markdown("")

else:
    st.warning(
        f"No geographic data available for feature **{feature.get('Name')}**. "
        "This may be because languages with data for this feature don't have "
        "geographic coordinates."
    )

# Educational notes
st.markdown("---")
st.markdown("### 💡 How to Use This Map")

st.markdown("""
1. **Select a feature** from the sidebar dropdown
2. **View the legend** to understand what each color represents
3. **Hover over markers** on the map to see language details
4. **Look for patterns:**
   - Are certain values clustered geographically? (areal features)
   - Do languages from the same family share values? (genetic features)
   - Are there universal tendencies? (some values more common globally)
5. **Download the data** for further statistical analysis
6. **Compare multiple features** by selecting different features and noting patterns

**Example Questions to Explore:**
- Is word order (SOV, SVO, etc.) clustered geographically?
- Do vowel inventory sizes vary by continent?
- Are certain grammatical features universal or rare?
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d;">
    <p>💡 Tip: Try exploring different features to discover typological patterns across languages</p>
    <p>Patterns that cluster geographically may indicate language contact (areal features)</p>
    <p>Patterns that cluster by family may indicate genetic inheritance</p>
</div>
""", unsafe_allow_html=True)
