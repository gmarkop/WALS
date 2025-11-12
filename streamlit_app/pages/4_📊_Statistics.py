"""
Statistics Page
View statistics and data visualizations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from streamlit_data_loader import WALSStreamlitLoader

st.set_page_config(page_title="Statistics - WALS Explorer", page_icon="📊", layout="wide")

# Initialize data loader
@st.cache_resource
def get_data_loader():
    return WALSStreamlitLoader()

data_loader = get_data_loader()

# Get detailed statistics
stats = data_loader.get_detailed_statistics()

# Page header
st.title("📊 Dataset Statistics")
st.markdown("Explore data distributions and patterns")

# Overview metrics
st.markdown("## 📈 Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Languages", f"{stats['languages']:,}")

with col2:
    st.metric("Typological Features", f"{stats['features']:,}")

with col3:
    st.metric("Data Points", f"{stats['values']:,}")

with col4:
    st.metric("Language Families", f"{stats['families']:,}")

st.markdown("---")

# Family distribution
st.markdown("## 🌳 Languages by Family")

col1, col2 = st.columns([2, 1])

with col1:
    # Top 15 families bar chart
    family_dist = stats['family_distribution']
    top_families = sorted(family_dist.items(), key=lambda x: x[1], reverse=True)[:15]

    df_families = pd.DataFrame(top_families, columns=['Family', 'Count'])

    fig_families = px.bar(
        df_families,
        x='Count',
        y='Family',
        orientation='h',
        title='Top 15 Language Families',
        labels={'Count': 'Number of Languages', 'Family': 'Language Family'},
        color='Count',
        color_continuous_scale='Blues'
    )

    fig_families.update_layout(
        height=500,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )

    st.plotly_chart(fig_families, use_container_width=True)

with col2:
    st.markdown("### 📋 Top Families")

    # Table of top families
    for i, (family, count) in enumerate(top_families[:10], 1):
        st.markdown(f"**{i}. {family}**")
        st.progress(count / top_families[0][1])
        st.caption(f"{count} languages")

# Macroarea distribution
st.markdown("---")
st.markdown("## 🌍 Languages by Macroarea")

col1, col2 = st.columns(2)

with col1:
    # Pie chart
    macroarea_dist = stats['macroarea_distribution']
    df_macroarea = pd.DataFrame(
        macroarea_dist.items(),
        columns=['Macroarea', 'Count']
    )

    fig_pie = px.pie(
        df_macroarea,
        values='Count',
        names='Macroarea',
        title='Distribution by Macroarea',
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(height=400)

    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Bar chart
    fig_bar = px.bar(
        df_macroarea.sort_values('Count', ascending=False),
        x='Macroarea',
        y='Count',
        title='Languages per Macroarea',
        labels={'Count': 'Number of Languages'},
        color='Count',
        color_continuous_scale='Viridis'
    )

    fig_bar.update_layout(height=400, showlegend=False)

    st.plotly_chart(fig_bar, use_container_width=True)

# Detailed tables
st.markdown("---")
st.markdown("## 📋 Detailed Statistics")

tab1, tab2 = st.tabs(["Language Families", "Macroareas"])

with tab1:
    st.markdown("### All Language Families")

    all_families = sorted(
        stats['family_distribution'].items(),
        key=lambda x: x[1],
        reverse=True
    )

    df_all_families = pd.DataFrame(
        all_families,
        columns=['Language Family', 'Number of Languages']
    )

    st.dataframe(
        df_all_families,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Language Family": st.column_config.TextColumn("Language Family", width="large"),
            "Number of Languages": st.column_config.NumberColumn("Number of Languages", width="medium"),
        }
    )

    # Download button
    csv_families = df_all_families.to_csv(index=False)
    st.download_button(
        label="📥 Download Family Statistics",
        data=csv_families,
        file_name="wals_family_statistics.csv",
        mime="text/csv"
    )

with tab2:
    st.markdown("### All Macroareas")

    all_macroareas = sorted(
        stats['macroarea_distribution'].items(),
        key=lambda x: x[1],
        reverse=True
    )

    df_all_macroareas = pd.DataFrame(
        all_macroareas,
        columns=['Macroarea', 'Number of Languages']
    )

    st.dataframe(
        df_all_macroareas,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Macroarea": st.column_config.TextColumn("Macroarea", width="large"),
            "Number of Languages": st.column_config.NumberColumn("Number of Languages", width="medium"),
        }
    )

    # Download button
    csv_macroareas = df_all_macroareas.to_csv(index=False)
    st.download_button(
        label="📥 Download Macroarea Statistics",
        data=csv_macroareas,
        file_name="wals_macroarea_statistics.csv",
        mime="text/csv"
    )

# Additional insights
st.markdown("---")
st.markdown("## 💡 Insights")

col1, col2, col3 = st.columns(3)

with col1:
    largest_family = max(stats['family_distribution'].items(), key=lambda x: x[1])
    st.info(f"**Largest Family:** {largest_family[0]} with {largest_family[1]} languages")

with col2:
    largest_area = max(stats['macroarea_distribution'].items(), key=lambda x: x[1])
    st.info(f"**Largest Macroarea:** {largest_area[0]} with {largest_area[1]} languages")

with col3:
    avg_per_family = stats['languages'] / stats['families']
    st.info(f"**Avg Languages per Family:** {avg_per_family:.1f}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d;">
    <p>💡 Tip: Download the data tables as CSV for further analysis</p>
</div>
""", unsafe_allow_html=True)
