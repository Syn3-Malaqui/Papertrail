"""
Papertrail Interactive Dashboard
A Streamlit-based web dashboard for document classification results.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys
import tempfile
import zipfile
import shutil
from datetime import datetime
from typing import Dict, Any, Optional
import base64

# Add src to path for imports
sys.path.append('src')
from src.parser import DocumentParser
from src.preprocess import TextPreprocessor
from src.predict import DocumentClassifier
from main import PapertrailPipeline

# Page configuration
st.set_page_config(
    page_title="📄 Papertrail Dashboard",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    .stDownloadButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

def create_download_link(file_path: str, link_text: str, file_name: str = None) -> str:
    """Create a download link for a file."""
    if not os.path.exists(file_path):
        return "File not found"
    
    with open(file_path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    
    if file_name is None:
        file_name = os.path.basename(file_path)
    
    href = f'<a href="data:application/octet-stream;base64,{encoded}" download="{file_name}" style="text-decoration: none; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; padding: 0.5rem 1rem; border-radius: 5px;">{link_text}</a>'
    return href

def create_zip_from_organized_folders(organized_folder: str) -> str:
    """Create a zip file from organized folders."""
    zip_path = os.path.join(tempfile.gettempdir(), f"papertrail_organized_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(organized_folder):
            for file in files:
                file_path = os.path.join(root, file)
                # Create relative path for the zip
                relative_path = os.path.relpath(file_path, organized_folder)
                zipf.write(file_path, relative_path)
    
    return zip_path

def plot_distribution_chart(df: pd.DataFrame) -> go.Figure:
    """Create an interactive pie chart of document type distribution."""
    category_counts = df['predicted_category'].value_counts()
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=category_counts.index,
        values=category_counts.values,
        hole=0.4,
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
        textinfo='label+percent',
        textposition='auto',
        marker=dict(
            colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'],
            line=dict(color='#FFFFFF', width=2)
        )
    )])
    
    fig.update_layout(
        title={
            'text': "📊 Document Type Distribution",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#2F3542'}
        },
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.01
        ),
        margin=dict(t=60, b=20, l=20, r=120),
        height=400
    )
    
    return fig

def plot_confidence_distribution(df: pd.DataFrame) -> go.Figure:
    """Create a histogram of confidence scores."""
    fig = px.histogram(
        df, 
        x='confidence',
        nbins=20,
        title="🎯 Confidence Score Distribution",
        labels={'confidence': 'Confidence Score', 'count': 'Number of Documents'},
        color_discrete_sequence=['#667eea']
    )
    
    fig.update_layout(
        title_x=0.5,
        title_font_size=18,
        height=350
    )
    
    return fig

def create_detailed_table(df: pd.DataFrame) -> pd.DataFrame:
    """Create a detailed, searchable table."""
    # Round confidence scores
    df_display = df.copy()
    df_display['confidence'] = df_display['confidence'].round(3)
    
    # Add emoji icons for categories
    category_icons = {
        'invoice': '📄',
        'memo': '📝',
        'legal': '⚖️',
        'report': '📊',
        'contract': '📋',
        'other': '📂'
    }
    
    df_display['category_icon'] = df_display['predicted_category'].map(category_icons)
    df_display['display_category'] = df_display['category_icon'] + ' ' + df_display['predicted_category'].str.title()
    
    # Reorder columns for better display
    columns_order = ['filename', 'display_category', 'confidence', 'word_count', 'text_length']
    df_display = df_display[columns_order]
    
    # Rename columns for better display
    df_display.columns = ['📄 Filename', '📂 Category', '🎯 Confidence', '📝 Words', '📏 Length']
    
    return df_display

def main():
    """Main dashboard application."""
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>📄 Papertrail Document Classification Dashboard</h1>
            <p>Intelligent document analysis with interactive visualizations</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for file upload and processing
    st.sidebar.markdown("## 🔧 Processing Options")
    
    # Folder selection
    folder_path = st.sidebar.text_input(
        "📁 Document Folder Path:",
        placeholder="Enter folder path containing documents...",
        help="Enter the full path to the folder containing your documents"
    )
    
    # Processing options
    st.sidebar.markdown("### ⚙️ Advanced Options")
    use_stemming = st.sidebar.checkbox("🌱 Enable stemming", value=False, help="Apply word stemming for better text analysis")
    organize_files = st.sidebar.checkbox("📁 Organize files by category", value=False, help="Create organized folders for each document type")
    
    # Process button
    process_button = st.sidebar.button("🚀 Process Documents", type="primary")
    
    # Initialize session state
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    
    # Process documents when button is clicked
    if process_button and folder_path:
        if not os.path.exists(folder_path):
            st.sidebar.error("❌ Folder path does not exist!")
        else:
            with st.spinner("🔄 Processing documents... This may take a few minutes."):
                try:
                    # Initialize pipeline
                    pipeline = PapertrailPipeline(
                        use_stemming=use_stemming,
                        move_files=organize_files
                    )
                    
                    # Process documents
                    result = pipeline.process_folder(folder_path, "dashboard_results.csv")
                    
                    if result['success']:
                        st.session_state.results = result
                        st.session_state.processing_complete = True
                        st.sidebar.success("✅ Processing completed successfully!")
                    else:
                        st.sidebar.error(f"❌ Processing failed: {result['error']}")
                        
                except Exception as e:
                    st.sidebar.error(f"❌ Error: {str(e)}")
    
    # Main dashboard content
    if st.session_state.processing_complete and st.session_state.results:
        result = st.session_state.results
        
        # Load results data
        if os.path.exists("dashboard_results.csv"):
            df = pd.read_csv("dashboard_results.csv")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="📁 Total Files",
                    value=result['stats']['total_files_found']
                )
            
            with col2:
                st.metric(
                    label="✅ Successfully Processed",
                    value=result['stats']['successfully_classified']
                )
            
            with col3:
                avg_confidence = df['confidence'].mean()
                st.metric(
                    label="🎯 Avg Confidence",
                    value=f"{avg_confidence:.3f}"
                )
            
            with col4:
                high_confidence = len(df[df['confidence'] > 0.7])
                st.metric(
                    label="⭐ High Confidence",
                    value=f"{high_confidence}/{len(df)}"
                )
            
            # Charts row
            chart_col1, chart_col2 = st.columns([2, 1])
            
            with chart_col1:
                # Distribution pie chart
                fig_pie = plot_distribution_chart(df)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with chart_col2:
                # Confidence distribution
                fig_conf = plot_confidence_distribution(df)
                st.plotly_chart(fig_conf, use_container_width=True)
            
            # Searchable table
            st.markdown("## 📋 Document Details")
            
            # Search functionality
            search_term = st.text_input(
                "🔍 Search documents:",
                placeholder="Search by filename or category...",
                help="Search for specific documents by name or filter by category"
            )
            
            # Category filter
            categories = ['All'] + sorted(df['predicted_category'].unique().tolist())
            selected_category = st.selectbox("📂 Filter by category:", categories)
            
            # Apply filters
            filtered_df = df.copy()
            
            if search_term:
                filtered_df = filtered_df[
                    filtered_df['filename'].str.contains(search_term, case=False, na=False) |
                    filtered_df['predicted_category'].str.contains(search_term, case=False, na=False)
                ]
            
            if selected_category != 'All':
                filtered_df = filtered_df[filtered_df['predicted_category'] == selected_category]
            
            # Display filtered table
            display_df = create_detailed_table(filtered_df)
            st.dataframe(
                display_df,
                use_container_width=True,
                height=400,
                hide_index=True
            )
            
            # Download section
            st.markdown("## 📥 Download Results")
            
            download_col1, download_col2, download_col3 = st.columns(3)
            
            with download_col1:
                # Download CSV report
                if os.path.exists("dashboard_results.csv"):
                    with open("dashboard_results.csv", "rb") as file:
                        st.download_button(
                            label="📊 Download CSV Report",
                            data=file.read(),
                            file_name=f"papertrail_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
            
            with download_col2:
                # Download detailed report (Excel-like)
                excel_buffer = pd.ExcelWriter("detailed_report.xlsx", engine='openpyxl')
                df.to_excel(excel_buffer, sheet_name='Classification Results', index=False)
                
                # Add summary sheet
                summary_data = {
                    'Metric': ['Total Files Found', 'Successfully Processed', 'Average Confidence', 'High Confidence Count'],
                    'Value': [
                        result['stats']['total_files_found'],
                        result['stats']['successfully_classified'],
                        f"{df['confidence'].mean():.3f}",
                        len(df[df['confidence'] > 0.7])
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(excel_buffer, sheet_name='Summary', index=False)
                excel_buffer.close()
                
                with open("detailed_report.xlsx", "rb") as file:
                    st.download_button(
                        label="📈 Download Excel Report",
                        data=file.read(),
                        file_name=f"papertrail_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            
            with download_col3:
                # Download organized folders as zip
                if organize_files and result['stats']['files_moved'] > 0:
                    # Find the organized folder
                    organized_folder = None
                    if 'organized_documents' in os.listdir('.'):
                        organized_folder = './organized_documents'
                    else:
                        # Look for organized_documents in the processed folder
                        for root, dirs, files in os.walk('.'):
                            if 'organized_documents' in dirs:
                                organized_folder = os.path.join(root, 'organized_documents')
                                break
                    
                    if organized_folder and os.path.exists(organized_folder):
                        zip_path = create_zip_from_organized_folders(organized_folder)
                        with open(zip_path, "rb") as file:
                            st.download_button(
                                label="🗂️ Download Organized Folders",
                                data=file.read(),
                                file_name=f"papertrail_organized_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                                mime="application/zip"
                            )
                else:
                    st.info("📝 Enable 'Organize files by category' to download organized folders")
            
            # Additional insights
            st.markdown("## 📈 Insights & Statistics")
            
            insight_col1, insight_col2 = st.columns(2)
            
            with insight_col1:
                st.markdown("### 📊 Category Breakdown")
                category_stats = df['predicted_category'].value_counts()
                for category, count in category_stats.items():
                    percentage = (count / len(df)) * 100
                    st.write(f"**{category.title()}**: {count} documents ({percentage:.1f}%)")
            
            with insight_col2:
                st.markdown("### 🎯 Confidence Analysis")
                high_conf = len(df[df['confidence'] > 0.8])
                medium_conf = len(df[(df['confidence'] > 0.5) & (df['confidence'] <= 0.8)])
                low_conf = len(df[df['confidence'] <= 0.5])
                
                st.write(f"**High Confidence (>0.8)**: {high_conf} documents")
                st.write(f"**Medium Confidence (0.5-0.8)**: {medium_conf} documents")
                st.write(f"**Low Confidence (≤0.5)**: {low_conf} documents")
        
        else:
            st.error("❌ Results file not found. Please process documents first.")
    
    else:
        # Welcome message and instructions
        st.markdown("""
        ## 👋 Welcome to Papertrail Dashboard!
        
        This interactive dashboard helps you analyze and classify your documents with powerful visualizations and insights.
        
        ### 🚀 Getting Started:
        1. **Enter folder path** in the sidebar containing your PDF, TXT, or DOCX files
        2. **Choose options** like stemming and file organization
        3. **Click 'Process Documents'** to start the analysis
        4. **Explore results** with interactive charts and searchable tables
        5. **Download reports** in various formats
        
        ### 📊 Features:
        - **Interactive pie charts** showing document type distribution
        - **Searchable table** with filtering capabilities
        - **Confidence score analysis** to assess prediction reliability
        - **Multiple download formats** (CSV, Excel, ZIP)
        - **Real-time processing** with progress indicators
        
        ### 📁 Supported File Types:
        - 📄 **PDF files** (text-based)
        - 📝 **Word documents** (.docx)
        - 📄 **Text files** (.txt)
        
        **Ready to get started?** Enter your document folder path in the sidebar! 👉
        """)
        
        # Sample visualization for demo
        st.markdown("### 📊 Sample Dashboard Preview")
        sample_data = {
            'Category': ['Invoice', 'Memo', 'Legal', 'Report', 'Contract'],
            'Count': [15, 8, 12, 6, 9]
        }
        sample_df = pd.DataFrame(sample_data)
        
        fig_sample = px.pie(
            sample_df,
            values='Count',
            names='Category',
            title="Sample Document Distribution",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        )
        fig_sample.update_layout(height=300)
        st.plotly_chart(fig_sample, use_container_width=True)

if __name__ == "__main__":
    main() 