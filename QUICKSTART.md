# 🚀 Papertrail Quick Start Guide

## Installation
```bash
pip install -r requirements.txt
```

## Usage

### 🌐 Web Dashboard (Recommended)
```bash
python main.py --dashboard
# OR
streamlit run dashboard.py
# OR
python launch_dashboard.py
```

### 🖥️ GUI Mode
```bash
python main.py --gui
```

### 💻 Command Line
```bash
python main.py /path/to/documents
python main.py /path/to/documents --organize --stemming
```

## Sample Files
Use the files in `sample_documents/` folder to test the system.

## Features
- 📄 Classifies PDF, TXT, DOCX files
- 🎯 Categories: invoice, memo, legal, report, contract, other
- 📊 Interactive web dashboard with charts
- 📁 Optional file organization by category
- 📥 Export results to CSV/Excel/ZIP

## Need Help?
See the full [README.md](README.md) for detailed documentation. 