"""
Text Preprocessing Module
Handles text tokenization, stop word removal, and other preprocessing tasks.
"""

import re
import string
from typing import List, Dict, Optional
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import warnings

# Suppress NLTK warnings
warnings.filterwarnings('ignore')

class TextPreprocessor:
    """Handles text preprocessing operations."""
    
    def __init__(self, use_stemming: bool = False, custom_stopwords: Optional[List[str]] = None):
        """
        Initialize the text preprocessor.
        
        Args:
            use_stemming: Whether to apply stemming to tokens
            custom_stopwords: Additional stop words to remove
        """
        self.use_stemming = use_stemming
        self.stemmer = PorterStemmer() if use_stemming else None
        
        # Download required NLTK data
        self._download_nltk_data()
        
        # Setup stop words
        self.stop_words = set(stopwords.words('english'))
        if custom_stopwords:
            self.stop_words.update(custom_stopwords)
        
        # Add common document-specific stop words
        document_stopwords = {
            'page', 'document', 'file', 'pdf', 'doc', 'docx', 'txt',
            'copyright', 'rights', 'reserved', 'company', 'inc', 'ltd',
            'www', 'http', 'https', 'com', 'org', 'net'
        }
        self.stop_words.update(document_stopwords)
    
    def _download_nltk_data(self):
        """Download required NLTK data if not already present."""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Downloading NLTK punkt tokenizer...")
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            print("Downloading NLTK stopwords...")
            nltk.download('stopwords', quiet=True)
    
    def clean_text(self, text: str) -> str:
        """
        Enhanced text cleaning while preserving important structural elements.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Preserve important structural elements before cleaning
        preserved_elements = self._preserve_structural_elements(text)
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation and important symbols
        text = re.sub(r'[^\w\s\.\,\!\?\:\;\-\_\$]', ' ', text)
        
        # Keep important numbers for document identification
        # Only remove small standalone numbers that aren't part of important patterns
        text = re.sub(r'\b\d{1,2}\b(?!\d)', '', text)  # Remove small standalone numbers
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Reintegrate preserved elements
        for element in preserved_elements:
            if element not in text:
                text = f"{text} {element}"
        
        return text
    
    def _preserve_structural_elements(self, text: str) -> List[str]:
        """
        Identify and preserve important structural elements from the text.
        
        Args:
            text: Original text
            
        Returns:
            List of preserved elements
        """
        preserved = []
        text_lower = text.lower()
        
        # Preserve document type indicators
        doc_type_patterns = [
            r'invoice\s+(?:number|#|no\.?)\s*:?\s*\w+',
            r'memorandum',
            r'employment\s+contract',
            r'service\s+agreement',
            r'legal\s+notice',
            r'quarterly\s+report',
            r'case\s+(?:number|#)',
            r'plaintiff\s+v\.?\s+defendant',
            r'amount\s+due',
            r'payment\s+terms',
            r'effective\s+date',
            r'signature\s+required'
        ]
        
        for pattern in doc_type_patterns:
            matches = re.findall(pattern, text_lower)
            preserved.extend(matches)
        
        # Preserve currency amounts (important for invoices)
        currency_pattern = r'\$[\d,]+\.?\d*'
        currency_matches = re.findall(currency_pattern, text)
        preserved.extend([match.lower() for match in currency_matches])
        
        # Preserve important structural keywords
        structural_keywords = [
            'invoice', 'memorandum', 'contract', 'agreement', 'legal', 'court',
            'report', 'analysis', 'plaintiff', 'defendant', 'billing', 'payment',
            'quarterly', 'annual', 'executive', 'summary', 'whereas', 'parties',
            'terms', 'conditions', 'signature', 'witness'
        ]
        
        for keyword in structural_keywords:
            if keyword in text_lower:
                preserved.append(keyword)
        
        return list(set(preserved))  # Remove duplicates
    
    def tokenize_text(self, text: str) -> List[str]:
        """
        Tokenize text into individual words.
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of tokens
        """
        try:
            tokens = word_tokenize(text)
            return tokens
        except Exception as e:
            print(f"Tokenization error: {e}")
            # Fallback to simple split
            return text.split()
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Remove stop words from token list.
        
        Args:
            tokens: List of tokens
            
        Returns:
            Filtered tokens
        """
        return [token for token in tokens if token.lower() not in self.stop_words]
    
    def remove_punctuation(self, tokens: List[str]) -> List[str]:
        """
        Remove punctuation from tokens.
        
        Args:
            tokens: List of tokens
            
        Returns:
            Tokens without punctuation
        """
        return [token for token in tokens if token not in string.punctuation]
    
    def filter_short_tokens(self, tokens: List[str], min_length: int = 2) -> List[str]:
        """
        Remove tokens shorter than minimum length.
        
        Args:
            tokens: List of tokens
            min_length: Minimum token length
            
        Returns:
            Filtered tokens
        """
        return [token for token in tokens if len(token) >= min_length]
    
    def stem_tokens(self, tokens: List[str]) -> List[str]:
        """
        Apply stemming to tokens.
        
        Args:
            tokens: List of tokens
            
        Returns:
            Stemmed tokens
        """
        if not self.stemmer:
            return tokens
        
        return [self.stemmer.stem(token) for token in tokens]
    
    def preprocess_text(self, text: str) -> List[str]:
        """
        Complete text preprocessing pipeline.
        
        Args:
            text: Raw text to preprocess
            
        Returns:
            List of processed tokens
        """
        # Clean text
        cleaned_text = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize_text(cleaned_text)
        
        # Remove punctuation
        tokens = self.remove_punctuation(tokens)
        
        # Remove stop words
        tokens = self.remove_stopwords(tokens)
        
        # Filter short tokens
        tokens = self.filter_short_tokens(tokens)
        
        # Apply stemming if enabled
        if self.use_stemming:
            tokens = self.stem_tokens(tokens)
        
        return tokens
    
    def preprocess_documents(self, documents: Dict[str, str]) -> Dict[str, List[str]]:
        """
        Preprocess multiple documents.
        
        Args:
            documents: Dictionary mapping filenames to text content
            
        Returns:
            Dictionary mapping filenames to preprocessed tokens
        """
        preprocessed_docs = {}
        
        print(f"Preprocessing {len(documents)} documents...")
        
        for filename, text in documents.items():
            print(f"Preprocessing: {filename}")
            
            try:
                tokens = self.preprocess_text(text)
                preprocessed_docs[filename] = tokens
                
                # Log statistics
                word_count = len(tokens)
                unique_words = len(set(tokens))
                print(f"  - {word_count} tokens, {unique_words} unique words")
                
            except Exception as e:
                print(f"Error preprocessing {filename}: {e}")
                preprocessed_docs[filename] = []
        
        print(f"Preprocessing complete!")
        return preprocessed_docs
    
    def get_document_features(self, tokens: List[str]) -> Dict[str, any]:
        """
        Extract basic features from preprocessed tokens.
        
        Args:
            tokens: List of preprocessed tokens
            
        Returns:
            Dictionary of features
        """
        if not tokens:
            return {
                'token_count': 0,
                'unique_tokens': 0,
                'avg_token_length': 0,
                'has_numbers': False,
                'text_sample': ""
            }
        
        return {
            'token_count': len(tokens),
            'unique_tokens': len(set(tokens)),
            'avg_token_length': sum(len(token) for token in tokens) / len(tokens),
            'has_numbers': any(char.isdigit() for token in tokens for char in token),
            'text_sample': ' '.join(tokens[:10])  # First 10 tokens
        }

# Example usage
if __name__ == "__main__":
    # Test the preprocessor
    preprocessor = TextPreprocessor(use_stemming=True)
    
    sample_texts = {
        "sample1.txt": "This is a SAMPLE document with various Types of TEXT! It contains numbers like 123 and special characters @#$%.",
        "sample2.txt": "INVOICE Document - Company ABC Inc. Invoice #12345 for services rendered. Total amount: $1,500.00"
    }
    
    print("=== Testing Text Preprocessing ===")
    
    # Test individual text
    text = sample_texts["sample1.txt"]
    print(f"\nOriginal text: {text}")
    
    tokens = preprocessor.preprocess_text(text)
    print(f"Preprocessed tokens: {tokens}")
    
    features = preprocessor.get_document_features(tokens)
    print(f"Features: {features}")
    
    # Test batch processing
    print("\n=== Batch Processing ===")
    processed_docs = preprocessor.preprocess_documents(sample_texts)
    
    for filename, tokens in processed_docs.items():
        print(f"\n{filename}: {tokens[:10]}...")  # Show first 10 tokens 