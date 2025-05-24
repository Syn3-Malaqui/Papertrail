"""
Papertrail Dashboard - Advanced Document Classification Visualization
A comprehensive Streamlit dashboard for viewing classification results and statistics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import glob
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="📄 Papertrail Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-metric {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    .warning-metric {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
    }
    .error-metric {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

def load_classification_data():
    """Load the most recent classification results."""
    try:
        # Look for classification result files
        csv_files = glob.glob("*classification_results*.csv")
        if not csv_files:
            return None, "No classification results found. Please run the classification first."
        
        # Get the most recent file
        latest_file = max(csv_files, key=os.path.getctime)
        
        # Load the data
        df = pd.read_csv(latest_file)
        
        return df, latest_file
    except Exception as e:
        return None, f"Error loading data: {str(e)}"

def create_category_pie_chart(df):
    """Create an interactive pie chart for category distribution."""
    category_counts = df['predicted_category'].value_counts()
    
    # Create pie chart with custom colors
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    
    fig = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        title="📊 Document Category Distribution",
        color_discrete_sequence=colors,
        hole=0.3  # Donut chart
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        font_size=14,
        title_font_size=18,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_confidence_histogram(df):
    """Create a histogram showing confidence distribution."""
    fig = px.histogram(
        df, 
        x='confidence',
        title="🎯 Confidence Score Distribution",
        labels={'confidence': 'Confidence Score', 'count': 'Number of Documents'},
        color_discrete_sequence=['#45B7D1']
    )
    
    fig.update_layout(
        xaxis_title="Confidence Score",
        yaxis_title="Number of Documents",
        title_font_size=18,
        showlegend=False
    )
    
    # Add vertical line for average confidence
    avg_confidence = df['confidence'].mean()
    fig.add_vline(
        x=avg_confidence, 
        line_dash="dash", 
        line_color="red",
        annotation_text=f"Avg: {avg_confidence:.3f}"
    )
    
    return fig

def create_confidence_by_category(df):
    """Create box plot showing confidence distribution by category."""
    fig = px.box(
        df,
        x='predicted_category',
        y='confidence',
        title="📈 Confidence Scores by Category",
        color='predicted_category',
        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    )
    
    fig.update_layout(
        xaxis_title="Document Category",
        yaxis_title="Confidence Score",
        title_font_size=18,
        showlegend=False
    )
    
    return fig

def create_file_count_bar_chart(df):
    """Create bar chart showing file count by category with confidence info."""
    category_stats = df.groupby('predicted_category').agg({
        'confidence': ['count', 'mean'],
        'filename': 'count'
    }).round(3)
    
    category_stats.columns = ['count', 'avg_confidence', 'file_count']
    category_stats = category_stats.reset_index()
    
    fig = px.bar(
        category_stats,
        x='predicted_category',
        y='count',
        title="📁 Document Count by Category",
        color='avg_confidence',
        color_continuous_scale='Viridis',
        text='count'
    )
    
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(
        xaxis_title="Document Category",
        yaxis_title="Number of Documents",
        title_font_size=18,
        coloraxis_colorbar=dict(title="Avg Confidence")
    )
    
    return fig

def display_summary_metrics(df):
    """Display key summary metrics."""
    total_docs = len(df)
    avg_confidence = df['confidence'].mean()
    high_confidence = len(df[df['confidence'] > 0.9])
    perfect_confidence = len(df[df['confidence'] == 1.0])
    categories = df['predicted_category'].nunique()
    
    col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric(
            label="📁 Total Documents",
            value=f"{total_docs:,}",
            delta=None
                )
            
            with col2:
                st.metric(
            label="🎯 Average Confidence",
            value=f"{avg_confidence:.3f}",
            delta=f"{((avg_confidence - 0.8) * 100):+.1f}%" if avg_confidence > 0.8 else None
                )
            
            with col3:
                st.metric(
            label="⭐ High Confidence (>0.9)",
            value=f"{high_confidence:,}",
            delta=f"{(high_confidence/total_docs)*100:.1f}%"
                )
            
            with col4:
                st.metric(
            label="🎖️ Perfect Confidence (1.0)",
            value=f"{perfect_confidence:,}",
            delta=f"{(perfect_confidence/total_docs)*100:.1f}%"
        )
    
    with col5:
        st.metric(
            label="🏷️ Categories Found",
            value=f"{categories}",
            delta=None
        )

def display_category_breakdown(df):
    """Display detailed category breakdown."""
    st.subheader("📋 Category Performance Breakdown")
    
    category_stats = df.groupby('predicted_category').agg({
        'confidence': ['count', 'mean', 'min', 'max', 'std'],
        'text_length': 'mean',
        'word_count': 'mean'
    }).round(3)
    
    category_stats.columns = [
        'Document Count', 'Avg Confidence', 'Min Confidence', 
        'Max Confidence', 'Std Confidence', 'Avg Text Length', 'Avg Word Count'
    ]
    
    # Add percentage column
    category_stats['Percentage'] = (category_stats['Document Count'] / len(df) * 100).round(1)
    
    # Reorder columns
    category_stats = category_stats[['Document Count', 'Percentage', 'Avg Confidence', 
                                   'Min Confidence', 'Max Confidence', 'Std Confidence',
                                   'Avg Text Length', 'Avg Word Count']]
    
    # Style the dataframe
    styled_df = category_stats.style.format({
        'Document Count': '{:.0f}',
        'Percentage': '{:.1f}%',
        'Avg Confidence': '{:.3f}',
        'Min Confidence': '{:.3f}',
        'Max Confidence': '{:.3f}',
        'Std Confidence': '{:.3f}',
        'Avg Text Length': '{:.0f}',
        'Avg Word Count': '{:.0f}'
    }).background_gradient(subset=['Avg Confidence'], cmap='RdYlGn')
    
    st.dataframe(styled_df, use_container_width=True)

def display_low_confidence_files(df, threshold=0.8):
    """Display files with confidence below threshold."""
    low_confidence = df[df['confidence'] < threshold].sort_values('confidence')
    
    if len(low_confidence) > 0:
        st.subheader(f"⚠️ Files with Confidence < {threshold}")
            st.dataframe(
            low_confidence[['filename', 'predicted_category', 'confidence', 'word_count']],
            use_container_width=True
        )
    else:
        st.success(f"🎉 All files have confidence ≥ {threshold}!")

def main():
    """Main dashboard function."""
    
    # Header
    st.markdown('<h1 class="main-header">📄 Papertrail Classification Dashboard</h1>', 
                unsafe_allow_html=True)
    
    # Load data
    df, file_info = load_classification_data()
    
    if df is None:
        st.error(f"❌ {file_info}")
        st.info("💡 Please run the classification first: `python main.py diverse_sample_documents`")
        return
    
    # Sidebar
    st.sidebar.markdown("## 📊 Dashboard Controls")
    st.sidebar.success(f"✅ Data loaded from: `{file_info}`")
    st.sidebar.info(f"📅 Last modified: {datetime.fromtimestamp(os.path.getctime(file_info)).strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Confidence threshold selector
    confidence_threshold = st.sidebar.slider(
        "🎯 Confidence Threshold for Alerts",
        min_value=0.0,
        max_value=1.0,
        value=0.8,
        step=0.05
    )
    
    # Category filter
    categories = ['All'] + sorted(df['predicted_category'].unique().tolist())
    selected_category = st.sidebar.selectbox("🏷️ Filter by Category", categories)
    
    # Filter data if category selected
    filtered_df = df if selected_category == 'All' else df[df['predicted_category'] == selected_category]
    
    # Main content
    st.markdown("---")
    
    # Summary metrics
    display_summary_metrics(filtered_df)
    
    st.markdown("---")
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart
        pie_chart = create_category_pie_chart(filtered_df)
        st.plotly_chart(pie_chart, use_container_width=True)
    
    with col2:
        # Confidence histogram
        conf_hist = create_confidence_histogram(filtered_df)
        st.plotly_chart(conf_hist, use_container_width=True)
    
    # Second row of charts
    col3, col4 = st.columns(2)
    
    with col3:
        # Bar chart
        bar_chart = create_file_count_bar_chart(filtered_df)
        st.plotly_chart(bar_chart, use_container_width=True)
    
    with col4:
        # Box plot
        box_plot = create_confidence_by_category(filtered_df)
        st.plotly_chart(box_plot, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed breakdown
    display_category_breakdown(filtered_df)
    
    st.markdown("---")
    
    # Low confidence alerts
    display_low_confidence_files(filtered_df, confidence_threshold)
    
    st.markdown("---")
    
    # Raw data view
    with st.expander("🔍 View Raw Classification Data"):
        st.dataframe(filtered_df, use_container_width=True)
    
    # Export options
    st.markdown("### 💾 Export Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Download Filtered Data as CSV"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"papertrail_filtered_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📈 Download Summary Stats"):
            summary_stats = filtered_df.groupby('predicted_category').agg({
                'confidence': ['count', 'mean', 'min', 'max', 'std']
            }).round(3)
            csv = summary_stats.to_csv()
            st.download_button(
                label="📥 Download Summary",
                data=csv,
                file_name=f"papertrail_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("🔄 Refresh Data"):
            st.rerun()

if __name__ == "__main__":
    main() 