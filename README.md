# 📄 Papertrail - Document Classification System

An intelligent document classification system that automatically categorizes PDF, TXT, and DOCX files using machine learning.

## 🚀 Features

- **📁 Multi-format Support**: Processes PDF, TXT, and DOCX files
- **🔍 Intelligent Classification**: Uses ML to categorize documents (invoice, memo, legal, report, contract, other)
- **🧼 Advanced Text Preprocessing**: NLTK-powered tokenization, stop word removal, and stemming
- **📊 Detailed Results**: Exports classification results to CSV with confidence scores
- **📁 Auto-organization**: Optional file organization into category folders
- **🌐 Interactive Web Dashboard**: Modern web interface with real-time visualizations- **🖥️ Multiple Interfaces**: Web dashboard, GUI, and command-line interfaces- **⚡ Batch Processing**: Recursively processes entire directory structures

## 🌐 Interactive Dashboard FeaturesThe new web dashboard provides:- **📊 Interactive Pie Charts**: Visual distribution of document types with hover details- **🔍 Searchable Data Table**: Filter and search through results in real-time- **📈 Confidence Analysis**: Histogram showing prediction reliability- **📥 Multiple Download Options**: CSV, Excel, and ZIP downloads- **📋 Real-time Statistics**: Live metrics and processing summaries- **🎨 Modern UI**: Clean, responsive design that works on all devices## 📋 CategoriesThe system can classify documents into these categories:
- **📄 Invoice**: Bills, payment requests, financial documents
- **📝 Memo**: Internal communications, announcements
- **⚖️ Legal**: Contracts, legal documents, court papers
- **📊 Report**: Analysis reports, summaries, findings
- **📋 Contract**: Agreements, service contracts, employment documents
- **📂 Other**: General documents that don't fit other categories

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/papertrail.git
   cd papertrail
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data** (automatic on first run):
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

## 🎯 Quick Start### Web Dashboard (Recommended)```bashstreamlit run dashboard.py# ORpython main.py --dashboard```### GUI Mode```bashpython main.py --gui```### Command Line Mode```bash# Basic usagepython main.py /path/to/documents# With optionspython main.py /path/to/documents --stemming --organize --output results.csv```### Interactive Mode```bashpython main.py```

## 📖 Usage Examples

### Basic Document Classification
```bash
# Classify all documents in a folder
python main.py ./sample_documents

# Output: classification_results.csv
```

### Advanced Usage
```bash
# Enable stemming and file organization
python main.py ./documents --stemming --organize --output detailed_results.csv
```

### Programmatic Usage
```python
from src.parser import DocumentParser
from src.preprocess import TextPreprocessor
from src.predict import DocumentClassifier

# Create pipeline
parser = DocumentParser()
preprocessor = TextPreprocessor(use_stemming=True)
classifier = DocumentClassifier()

# Process documents
documents = parser.parse_documents("./documents")
preprocessed = preprocessor.preprocess_documents(documents)
text_docs = classifier.preprocess_for_prediction(preprocessed)
predictions = classifier.predict_documents(text_docs)

# Save results
classifier.save_results_csv(predictions, "results.csv")
```

## 🏗️ Project Structure

```
papertrail/
├── src/
│   ├── parser.py          # Document parsing and text extraction
│   ├── preprocess.py      # Text preprocessing and tokenization
│   └── predict.py         # ML model and classification
├── models/
│   └── classifier.pkl     # Trained ML model (auto-generated)
├── main.py               # Main application entry point
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔧 Command Line Options

```
usage: main.py [-h] [--output OUTPUT] [--stemming] [--organize] [--gui] [folder]

Papertrail Document Classification System

positional arguments:
  folder                Folder path containing documents to classify

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output CSV file path (default: classification_results.csv)
  --stemming            Enable stemming in text preprocessing
  --organize            Organize files into category folders after classification
  --gui                 Launch GUI mode
```

## 📊 Output Format

The system generates a CSV file with the following columns:

| Column | Description |
|--------|-------------|
| `filename` | Original filename |
| `predicted_category` | Predicted document category |
| `confidence` | Prediction confidence score (0-1) |
| `text_length` | Number of characters in document |
| `word_count` | Number of words in document |
| `prob_invoice` | Probability of being an invoice |
| `prob_memo` | Probability of being a memo |
| `prob_legal` | Probability of being a legal document |
| `prob_report` | Probability of being a report |
| `prob_contract` | Probability of being a contract |
| `prob_other` | Probability of being other category |

## 🧠 Model Details

- **Algorithm**: Naive Bayes with TF-IDF vectorization
- **Features**: 1000 most important terms, unigrams and bigrams
- **Preprocessing**: Tokenization, stop word removal, optional stemming
- **Training**: Pre-trained on synthetic document samples (expandable)

## 🔄 Extending the System

### Adding New Categories
1. Update `categories` list in `src/predict.py`
2. Add training samples in `create_dummy_model()`
3. Retrain the model

### Custom Preprocessing
```python
# Add custom stop words
preprocessor = TextPreprocessor(
    use_stemming=True,
    custom_stopwords=['company_specific', 'term']
)
```

### Custom Model
```python
# Replace the model in src/predict.py
from sklearn.ensemble import RandomForestClassifier

# In DocumentClassifier.create_dummy_model():
self.model = Pipeline([
    ('tfidf', TfidfVectorizer(...)),
    ('classifier', RandomForestClassifier())
])
```

## 🐛 Troubleshooting

### Common Issues

1. **NLTK Data Not Found**:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

2. **PDF Parsing Errors**:
   - Ensure PDFs are text-based (not scanned images)
   - Try different PDF files to isolate the issue

3. **Memory Issues with Large Files**:
   - Process files in smaller batches
   - Increase system memory allocation

### Error Messages

- `FileNotFoundError`: Check file paths and permissions
- `ModuleNotFoundError`: Install missing dependencies with pip
- `PDFSyntaxError`: Corrupted or encrypted PDF files

## 📈 Performance Tips

1. **Use stemming** for better text normalization
2. **Process smaller batches** for large document sets
3. **Pre-filter files** by size or type if needed
4. **Train custom models** for domain-specific documents

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Commit changes: `git commit -am 'Add feature'`
5. Push to branch: `git push origin feature-name`
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **pdfminer.six** for PDF text extraction
- **python-docx** for Word document processing
- **NLTK** for natural language processing
- **scikit-learn** for machine learning capabilities

## 📞 Support

For questions, issues, or feature requests:
- Create an issue on GitHub
- Check the troubleshooting section above
- Review the documentation and examples

---

**Happy Document Classification! 📄✨** 