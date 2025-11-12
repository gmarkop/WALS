"""
Features Explorer Page
Browse and explore typological features in WALS
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from streamlit_data_loader import WALSStreamlitLoader

st.set_page_config(page_title="Features - WALS Explorer", page_icon="📋", layout="wide")

# Initialize data loader
@st.cache_resource
def get_data_loader():
    return WALSStreamlitLoader()

data_loader = get_data_loader()

# Page header
st.title("📋 Typological Features")
st.markdown("Explore linguistic features across languages")

# Sidebar filters
st.sidebar.header("Filters")

search_query = st.sidebar.text_input("🔍 Search", placeholder="Feature name or code...")

# Get all features
all_features = data_loader.get_all_features()

# Apply search filter
filtered_features = all_features

if search_query:
    search_lower = search_query.lower()
    filtered_features = [
        feat for feat in filtered_features
        if search_lower in feat.get('Name', '').lower() or
           search_lower in feat.get('ID', '').lower()
    ]

# Display results count
st.markdown(f"**{len(filtered_features):,}** features found")

# Convert to DataFrame for display
if filtered_features:
    table_data = []
    for feat in filtered_features:
        table_data.append({
            'Feature ID': feat.get('ID', ''),
            'Feature Name': feat.get('Name', ''),
            'Chapter': feat.get('Chapter_ID', ''),
        })

    df = pd.DataFrame(table_data)

    # Display with pagination
    items_per_page = st.sidebar.selectbox("Features per page", [10, 20, 30, 50], index=1)

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
            "Feature ID": st.column_config.TextColumn("Feature ID", width="small"),
            "Feature Name": st.column_config.TextColumn("Feature Name", width="large"),
            "Chapter": st.column_config.TextColumn("Chapter", width="small"),
        }
    )

    # Feature detail section
    st.markdown("---")
    st.subheader("View Feature Details")

    # Select feature to view
    feature_names = [f"{feat.get('ID')} - {feat.get('Name')}" for feat in filtered_features]
    selected_feat_name = st.selectbox(
        "Select a feature to view details:",
        options=feature_names,
        key="feat_select"
    )

    if selected_feat_name:
        # Extract feature ID
        feat_id = selected_feat_name.split(' - ')[0]
        feature = data_loader.get_feature(feat_id)

        if feature:
            st.markdown(f"### {feature.get('Name')}")
            st.markdown(f"**Feature ID:** `{feature.get('ID')}`")
            st.markdown(f"**Chapter:** {feature.get('Chapter_ID', 'N/A')}")

            # Get possible values
            st.markdown("---")
            st.markdown("#### Possible Values")

            codes = data_loader.get_codes_for_feature(feat_id)

            if codes:
                codes_data = []
                for code in codes:
                    codes_data.append({
                        'Number': code.get('Number'),
                        'Value': code.get('Name'),
                        'Description': code.get('Description', '')
                    })

                codes_df = pd.DataFrame(codes_data)
                st.dataframe(
                    codes_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Number": st.column_config.NumberColumn("Number", width="small"),
                        "Value": st.column_config.TextColumn("Value", width="medium"),
                        "Description": st.column_config.TextColumn("Description", width="large"),
                    }
                )
            else:
                st.info("No value codes defined for this feature.")

            # Get languages with this feature
            st.markdown("---")
            st.markdown("#### Languages with Data")

            values = data_loader.get_values_for_feature(feat_id)

            if values:
                st.info(f"**{len(values)}** languages have data for this feature")

                # Show value distribution
                value_counts = {}
                for value in values:
                    code_name = value.get('Code_Name', 'Unknown')
                    value_counts[code_name] = value_counts.get(code_name, 0) + 1

                # Create distribution chart
                dist_df = pd.DataFrame([
                    {'Value': k, 'Count': v}
                    for k, v in sorted(value_counts.items(), key=lambda x: x[1], reverse=True)
                ])

                st.markdown("**Value Distribution:**")
                st.bar_chart(dist_df.set_index('Value'))

                # Show sample languages
                st.markdown("**Sample Languages (first 100):**")

                values_data = []
                for value in values[:100]:
                    values_data.append({
                        'Language Code': value.get('Language_ID'),
                        'Language Name': value.get('Language_Name'),
                        'Value': value.get('Code_Name')
                    })

                values_df = pd.DataFrame(values_data)
                st.dataframe(
                    values_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Language Code": st.column_config.TextColumn("Code", width="small"),
                        "Language Name": st.column_config.TextColumn("Language", width="medium"),
                        "Value": st.column_config.TextColumn("Value", width="medium"),
                    }
                )

                if len(values) > 100:
                    st.caption(f"Showing first 100 of {len(values)} languages")
            else:
                st.info("No language data available for this feature.")

else:
    st.info("No features found matching the search query.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d;">
    <p>💡 Tip: Click on a feature to see its possible values and distribution across languages</p>
</div>
""", unsafe_allow_html=True)
