"""
Economic News Analysis Dashboard
Interactive visualization of LLM-categorized real news articles
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Economic News Analyzer",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Economic News Analysis Dashboard")
st.markdown("### Real-time Economic News Categorization using LLM")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/categorized_real_articles.csv')
        return df
    except FileNotFoundError:
        st.error("❌ Data file not found! Please run the scraping and categorization scripts first.")
        st.stop()

df = load_data()

# Sidebar
st.sidebar.header("📌 Project Information")
st.sidebar.markdown("""
**Economic News LLM Analyzer**

This dashboard displays real economic news articles that were:
1. 🔍 Scraped from real news sources
2. 🤖 Categorized using GPT-3.5 LLM
3. 📊 Visualized for analysis

**Total Articles:** {total}
**Sources:** {sources}
**Categories:** {categories}
""".format(
    total=len(df),
    sources=df['source'].nunique(),
    categories=df['llm_category'].nunique()
))

st.sidebar.markdown("---")
st.sidebar.markdown("**Filter Options:**")

# Filters in sidebar
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=sorted(df['llm_category'].unique()),
    default=sorted(df['llm_category'].unique())
)

selected_sources = st.sidebar.multiselect(
    "Select Sources",
    options=sorted(df['source'].unique()),
    default=sorted(df['source'].unique())
)

# Filter dataframe
filtered_df = df[
    (df['llm_category'].isin(selected_categories)) &
    (df['source'].isin(selected_sources))
]

# Main dashboard
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📰 Total Articles", len(filtered_df))

with col2:
    st.metric("📁 Categories", filtered_df['llm_category'].nunique())

with col3:
    st.metric("🌐 Sources", filtered_df['source'].nunique())

with col4:
    st.metric("🤖 LLM Model", "GPT-3.5")

st.markdown("---")

# Charts row
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Category Distribution")
    
    category_counts = filtered_df['llm_category'].value_counts()
    
    fig = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        title="Articles by Category",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🌐 Source Distribution")
    
    source_counts = filtered_df['source'].value_counts().head(10)
    
    fig = px.bar(
        x=source_counts.values,
        y=source_counts.index,
        orientation='h',
        title="Top 10 News Sources",
        labels={'x': 'Number of Articles', 'y': 'Source'},
        color=source_counts.values,
        color_continuous_scale='Blues'
    )
    fig.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Category breakdown
st.subheader("📈 Category Breakdown")

category_col1, category_col2 = st.columns(2)

with category_col1:
    category_counts_df = filtered_df['llm_category'].value_counts().reset_index()
    category_counts_df.columns = ['Category', 'Count']
    category_counts_df['Percentage'] = (category_counts_df['Count'] / len(filtered_df) * 100).round(1)
    
    st.dataframe(
        category_counts_df,
        use_container_width=True,
        hide_index=True
    )

with category_col2:
    fig = px.bar(
        category_counts_df,
        x='Category',
        y='Count',
        title='Articles per Category',
        color='Count',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Articles table
st.subheader("📋 Article Details")

# Search box
search_term = st.text_input("🔍 Search articles by title or description:", "")

if search_term:
    display_df = filtered_df[
        filtered_df['title'].str.contains(search_term, case=False, na=False) |
        filtered_df['description'].str.contains(search_term, case=False, na=False)
    ]
else:
    display_df = filtered_df

# Display articles
st.markdown(f"**Showing {len(display_df)} articles:**")

for idx, row in display_df.iterrows():
    with st.expander(f"🔹 {row['title'][:100]}..."):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**Title:** {row['title']}")
            st.markdown(f"**Description:** {row['description']}")
            if pd.notna(row['link']) and row['link']:
                st.markdown(f"**Link:** [{row['link']}]({row['link']})")
        
        with col2:
            st.markdown(f"**Category:** `{row['llm_category']}`")
            st.markdown(f"**Source:** {row['source']}")
            if pd.notna(row['date']):
                st.markdown(f"**Date:** {row['date']}")

st.markdown("---")

# Footer
st.markdown("""
### 🎯 About This Project

This dashboard demonstrates a production-ready economic news analysis pipeline:

1. **Real Data Collection**: Web scraping from multiple news sources (Guardian, Google News, etc.)
2. **LLM Categorization**: Automated classification using OpenAI GPT-3.5
3. **Interactive Visualization**: Streamlit dashboard for exploring results

**Technologies Used:**
- Python, Pandas, BeautifulSoup
- OpenAI API (GPT-3.5)
- Streamlit, Plotly
- Web Scraping, RSS Feeds

**Project Structure:**
- `scrape_real_news.py` - Collects articles from multiple sources
- `categorize_real_articles.py` - LLM-based categorization
- `dashboard.py` - Interactive visualization (this page!)

---
*Built as a portfolio project demonstrating data science, LLM integration, and web development skills.*
""")
