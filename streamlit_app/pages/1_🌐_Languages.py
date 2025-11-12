"""
Languages Browser Page
Browse and search WALS languages with detailed filtering
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from streamlit_data_loader import WALSStreamlitLoader

st.set_page_config(page_title="Languages - WALS Explorer", page_icon="🌐", layout="wide")

# Initialize data loader
@st.cache_resource
def get_data_loader():
    return WALSStreamlitLoader()

data_loader = get_data_loader()

# Page header
st.title("🌐 Languages")
st.markdown("Browse and explore languages in the WALS database")

# Sidebar filters
st.sidebar.header("Filters")

# Get filter options
families = ['All'] + data_loader.get_families()
macroareas = ['All'] + data_loader.get_macroareas()

# Filter controls
search_query = st.sidebar.text_input("🔍 Search", placeholder="Language name or code...")
selected_family = st.sidebar.selectbox("Language Family", families)
selected_macroarea = st.sidebar.selectbox("Macroarea", macroareas)

# Get all languages
all_languages = data_loader.get_all_languages()

# Apply filters
filtered_languages = all_languages

if search_query:
    search_lower = search_query.lower()
    filtered_languages = [
        lang for lang in filtered_languages
        if search_lower in lang.get('Name', '').lower() or
           search_lower in lang.get('ID', '').lower()
    ]

if selected_family != 'All':
    filtered_languages = [
        lang for lang in filtered_languages
        if lang.get('Family') == selected_family
    ]

if selected_macroarea != 'All':
    filtered_languages = [
        lang for lang in filtered_languages
        if lang.get('Macroarea') == selected_macroarea
    ]

# Display results count
st.markdown(f"**{len(filtered_languages):,}** languages found")

# Add clear filters button
if st.sidebar.button("Clear All Filters"):
    st.rerun()

# Convert to DataFrame for display
if filtered_languages:
    # Prepare data for table
    table_data = []
    for lang in filtered_languages:
        table_data.append({
            'Code': lang.get('ID', ''),
            'Name': lang.get('Name', ''),
            'Family': lang.get('Family', ''),
            'Genus': lang.get('Genus', ''),
            'Macroarea': lang.get('Macroarea', ''),
            'ISO 639-3': lang.get('ISO639P3code', ''),
        })

    df = pd.DataFrame(table_data)

    # Display with pagination
    items_per_page = st.sidebar.selectbox("Languages per page", [10, 25, 50, 100], index=1)

    total_pages = (len(df) - 1) // items_per_page + 1

    if total_pages > 1:
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        df_display = df.iloc[start_idx:end_idx]
    else:
        df_display = df

    # Display table
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Code": st.column_config.TextColumn("Code", width="small"),
            "Name": st.column_config.TextColumn("Name", width="medium"),
            "Family": st.column_config.TextColumn("Family", width="medium"),
            "Genus": st.column_config.TextColumn("Genus", width="medium"),
            "Macroarea": st.column_config.TextColumn("Macroarea", width="medium"),
            "ISO 639-3": st.column_config.TextColumn("ISO 639-3", width="small"),
        }
    )

    # Language detail section
    st.markdown("---")
    st.subheader("View Language Details")

    # Select language to view
    language_names = [f"{lang.get('Name')} ({lang.get('ID')})" for lang in filtered_languages]
    selected_lang_name = st.selectbox(
        "Select a language to view details:",
        options=language_names,
        key="lang_select"
    )

    if selected_lang_name:
        # Extract language ID
        lang_id = selected_lang_name.split('(')[-1].strip(')')
        language = data_loader.get_language(lang_id)

        if language:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("#### Classification")
                st.markdown(f"**Family:** {language.get('Family', 'Unknown')}")
                st.markdown(f"**Subfamily:** {language.get('Subfamily', '-')}")
                st.markdown(f"**Genus:** {language.get('Genus', 'Unknown')}")
                st.markdown(f"**Macroarea:** {language.get('Macroarea', 'Unknown')}")

            with col2:
                st.markdown("#### Identifiers")
                st.markdown(f"**WALS Code:** `{language.get('ID')}`")
                st.markdown(f"**ISO 639-3:** {language.get('ISO639P3code', '-')}")
                glottocode = language.get('Glottocode', '')
                if glottocode:
                    st.markdown(f"**Glottocode:** [{glottocode}](https://glottolog.org/resource/languoid/id/{glottocode})")
                else:
                    st.markdown("**Glottocode:** -")

            with col3:
                st.markdown("#### Geographic Information")
                st.markdown(f"**Latitude:** {language.get('Latitude', '-')}")
                st.markdown(f"**Longitude:** {language.get('Longitude', '-')}")

            # Feature values
            st.markdown("---")
            st.markdown("#### Typological Features")

            values = data_loader.get_values_for_language(lang_id)

            if values:
                values_data = []
                for value in values:
                    values_data.append({
                        'Feature ID': value.get('Parameter_ID'),
                        'Feature Name': value.get('Feature_Name'),
                        'Value': value.get('Code_Name')
                    })

                values_df = pd.DataFrame(values_data)
                st.dataframe(
                    values_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Feature ID": st.column_config.TextColumn("Feature ID", width="small"),
                        "Feature Name": st.column_config.TextColumn("Feature Name", width="large"),
                        "Value": st.column_config.TextColumn("Value", width="medium"),
                    }
                )

                st.info(f"This language has data for {len(values)} typological features.")
            else:
                st.info("No feature data available for this language.")

else:
    st.info("No languages found matching the selected filters.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d;">
    <p>💡 Tip: Use the sidebar filters to narrow down languages by family or geographic area</p>
</div>
""", unsafe_allow_html=True)
