"""
Document Classification Prediction Module
Handles ML model loading, vectorization, and prediction.
"""

import os
import pickle
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import warnings

warnings.filterwarnings('ignore')

class DocumentClassifier:
    """Handles document classification using ML models."""
    
    def __init__(self, model_path: str = "models/classifier.pkl"):
        """
        Initialize the document classifier.
        
        Args:
            model_path: Path to the trained model file
        """
        self.model_path = model_path
        self.model = None
        self.vectorizer = None
        self.categories = ['invoice', 'memo', 'legal', 'report', 'contract', 'other']
        
        # Try to load existing model
        self.load_model()
        
        # If no model exists, create a dummy one
        if self.model is None:
            self.create_dummy_model()
    
    def create_dummy_model(self):
        """Create a dummy model for demonstration purposes."""
        print("Creating improved classification model with comprehensive training data...")
        
        # Create comprehensive training data with realistic examples
        sample_texts = [
            # Invoice samples - financial billing documents
            "invoice payment due amount total tax billing address customer account number remit net days",
            "bill invoice date amount due payment terms billing subtotal sales tax professional services",
            "invoice total amount tax payment billing customer account receivable thirty days receipt",
            "monthly invoice services rendered billing period subtotal tax total due payment terms",
            "invoice number date bill customer description quantity rate amount subtotal tax total",
            "service invoice professional consultation billing address payment due receipt remittance",
            
            # Memo samples - internal communications and policy updates
            "memorandum staff members policy update effective date implementation department heads",
            "internal memo regarding meeting agenda discussion points action items staff announcement",
            "memo budget allocation department meeting notes quarterly planning review session",
            "memorandum policy changes effective immediately all employees human resources department",
            "internal memo meeting scheduled conference room agenda items quarterly review staff",
            "memo regarding remote work policy hybrid model core hours collaboration equipment stipend",
            "memorandum announcement new procedures training sessions communication tools project management",
            "internal memo from management regarding updated policies effective date implementation",
            
            # Legal samples - court documents, notices, legal proceedings
            "legal notice court case defendant plaintiff breach contract damages attorney",
            "legal document court superior justice notice proceedings defendant response required",
            "legal action commenced breach employment contract violation non disclosure agreement",
            "notice legal proceedings court case plaintiff defendant damages injunctive relief",
            "legal notice employment dispute court superior business affairs defendant",
            "legal document attorney client privilege confidential communication court proceedings",
            
            # Report samples - analysis, findings, performance metrics
            "quarterly performance report executive summary financial analysis revenue growth metrics",
            "report analysis findings conclusions recommendations data results performance indicators",
            "annual report financial performance revenue profit margin customer satisfaction market share",
            "quarterly report departmental performance sales marketing operations customer service",
            "performance report key metrics revenue growth profit margin customer acquisition retention",
            "financial report executive summary quarterly analysis revenue expenses profit recommendations",
            
            # Contract samples - agreements, terms, parties, signatures
            "service agreement provider client terms conditions compensation termination governing law",
            "contract agreement parties terms conditions signature effective date witness",
            "employment contract salary benefits terms conditions agreement twelve months notice",
            "service contract software development technical consulting services monthly fee",
            "agreement entered provider client services outlined exhibit attached incorporated",
            "contract terms payment schedule deliverables obligations effective date signature",
            
            # Other samples - general documents, correspondence, miscellaneous
            "general document information text content miscellaneous correspondence communication",
            "letter correspondence communication general information document material content",
            "notes information general content document text material miscellaneous data",
            "general correspondence letter communication information document content material",
            "miscellaneous document general information content text material data notes"
        ]
        
        sample_labels = [
            # Invoice labels
            'invoice', 'invoice', 'invoice', 'invoice', 'invoice', 'invoice',
            # Memo labels  
            'memo', 'memo', 'memo', 'memo', 'memo', 'memo', 'memo', 'memo',
            # Legal labels
            'legal', 'legal', 'legal', 'legal', 'legal', 'legal',
            # Report labels
            'report', 'report', 'report', 'report', 'report', 'report',
            # Contract labels
            'contract', 'contract', 'contract', 'contract', 'contract', 'contract',
            # Other labels
            'other', 'other', 'other', 'other', 'other'
        ]
        
                # Create pipeline with improved TF-IDF vectorizer and Naive Bayes classifier
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=2000,  # Increased for better feature capture
                ngram_range=(1, 3),  # Include trigrams for better context
                stop_words='english',
                lowercase=True,
                min_df=1,  # Include single-occurrence terms
                max_df=0.8  # Exclude very common terms
            )),
            ('classifier', MultinomialNB(alpha=0.01))  # Lower smoothing for better discrimination
        ])
        
        # Train the dummy model
        self.model.fit(sample_texts, sample_labels)
        
        # Save the model
        self.save_model()
        
        print(f"Dummy model created and saved to {self.model_path}")
        print(f"Model can classify documents into: {self.categories}")
    
    def load_model(self) -> bool:
        """
        Load the trained model from file.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print(f"Model loaded successfully from {self.model_path}")
                return True
            except Exception as e:
                print(f"Error loading model: {e}")
                return False
        else:
            print(f"Model file not found: {self.model_path}")
            return False
    
    def save_model(self):
        """Save the current model to file."""
        try:
            # Create models directory if it doesn't exist
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.model, f)
            print(f"Model saved to {self.model_path}")
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def preprocess_for_prediction(self, preprocessed_docs: Dict[str, List[str]]) -> Dict[str, str]:
        """
        Convert preprocessed tokens back to text for TF-IDF vectorization.
        
        Args:
            preprocessed_docs: Dictionary mapping filenames to token lists
            
        Returns:
            Dictionary mapping filenames to text strings
        """
        text_docs = {}
        for filename, tokens in preprocessed_docs.items():
            text_docs[filename] = ' '.join(tokens)
        return text_docs
    
    def predict_single(self, text: str) -> Tuple[str, float]:
        """
        Predict the category of a single document.
        
        Args:
            text: Document text
            
        Returns:
            Tuple of (predicted_category, confidence_score)
        """
        if self.model is None:
            return 'other', 0.0
        
        try:
            # Get prediction and probabilities
            prediction = self.model.predict([text])[0]
            probabilities = self.model.predict_proba([text])[0]
            confidence = max(probabilities)
            
            return prediction, confidence
        except Exception as e:
            print(f"Error during prediction: {e}")
            return 'other', 0.0
    
    def predict_documents(self, documents: Dict[str, str]) -> Dict[str, Dict[str, any]]:
        """
        Predict categories for multiple documents.
        
        Args:
            documents: Dictionary mapping filenames to text content
            
        Returns:
            Dictionary mapping filenames to prediction results
        """
        if self.model is None:
            print("No model available for prediction!")
            return {}
        
        predictions = {}
        
        print(f"Classifying {len(documents)} documents...")
        
        for filename, text in documents.items():
            print(f"Classifying: {filename}")
            
            try:
                predicted_category, confidence = self.predict_single(text)
                
                # Get all class probabilities for detailed analysis
                probabilities = self.model.predict_proba([text])[0]
                classes = self.model.classes_
                
                # Create probability dictionary
                prob_dict = dict(zip(classes, probabilities))
                
                predictions[filename] = {
                    'predicted_category': predicted_category,
                    'confidence': confidence,
                    'probabilities': prob_dict,
                    'text_length': len(text),
                    'word_count': len(text.split())
                }
                
                print(f"  -> {predicted_category} (confidence: {confidence:.3f})")
                
            except Exception as e:
                print(f"Error classifying {filename}: {e}")
                predictions[filename] = {
                    'predicted_category': 'other',
                    'confidence': 0.0,
                    'probabilities': {},
                    'text_length': 0,
                    'word_count': 0
                }
        
        print("Classification complete!")
        return predictions
    
    def create_results_dataframe(self, predictions: Dict[str, Dict[str, any]]) -> pd.DataFrame:
        """
        Create a pandas DataFrame from prediction results.
        
        Args:
            predictions: Dictionary of prediction results
            
        Returns:
            DataFrame with prediction results
        """
        rows = []
        
        for filename, result in predictions.items():
            row = {
                'filename': filename,
                'predicted_category': result['predicted_category'],
                'confidence': result['confidence'],
                'text_length': result['text_length'],
                'word_count': result['word_count']
            }
            
            # Add probability columns
            for category in self.categories:
                prob_key = f'prob_{category}'
                row[prob_key] = result['probabilities'].get(category, 0.0)
            
            rows.append(row)
        
        return pd.DataFrame(rows)
    
    def save_results_csv(self, predictions: Dict[str, Dict[str, any]], output_path: str = "classification_results.csv"):
        """
        Save prediction results to CSV file.
        
        Args:
            predictions: Dictionary of prediction results
            output_path: Path to save the CSV file
        """
        try:
            df = self.create_results_dataframe(predictions)
            df.to_csv(output_path, index=False)
            print(f"Results saved to {output_path}")
            
            # Print summary statistics
            print("\n=== Classification Summary ===")
            print(f"Total documents classified: {len(df)}")
            print("\nCategory distribution:")
            print(df['predicted_category'].value_counts())
            print(f"\nAverage confidence: {df['confidence'].mean():.3f}")
            print(f"High confidence predictions (>0.7): {len(df[df['confidence'] > 0.7])}")
            
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def get_model_info(self) -> Dict[str, any]:
        """Get information about the current model."""
        if self.model is None:
            return {"status": "No model loaded"}
        
        try:
            info = {
                "model_type": type(self.model).__name__,
                "categories": list(self.model.classes_),
                "feature_count": len(self.model.named_steps['tfidf'].get_feature_names_out()),
                "model_path": self.model_path
            }
            return info
        except Exception as e:
            return {"status": f"Error getting model info: {e}"}

# Example usage
if __name__ == "__main__":
    # Test the classifier
    classifier = DocumentClassifier()
    
    # Test sample documents
    sample_docs = {
        "invoice_001.pdf": "Invoice #12345 Amount Due: $1,500.00 Payment Terms: Net 30 Billing Address Customer Account",
        "memo_meeting.txt": "Memo: Weekly Team Meeting Agenda: Project Updates, Budget Discussion, Action Items",
        "contract_service.docx": "Service Agreement between Company A and Company B Terms and Conditions Effective Date Signature",
        "report_quarterly.pdf": "Quarterly Performance Report Executive Summary Financial Analysis Revenue Growth Metrics"
    }
    
    print("=== Testing Document Classification ===")
    
    # Get model info
    model_info = classifier.get_model_info()
    print(f"Model Info: {model_info}")
    
    # Make predictions
    predictions = classifier.predict_documents(sample_docs)
    
    # Show detailed results
    print("\n=== Detailed Results ===")
    for filename, result in predictions.items():
        print(f"\n{filename}:")
        print(f"  Category: {result['predicted_category']}")
        print(f"  Confidence: {result['confidence']:.3f}")
        print(f"  Top probabilities:")
        sorted_probs = sorted(result['probabilities'].items(), key=lambda x: x[1], reverse=True)
        for category, prob in sorted_probs[:3]:
            print(f"    {category}: {prob:.3f}")
    
    # Save results
    classifier.save_results_csv(predictions, "test_classification_results.csv") 