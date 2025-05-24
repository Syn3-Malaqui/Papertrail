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
        """Create an enhanced classification model with format-aware features and comprehensive pattern recognition."""
        print("Creating enhanced classification model with comprehensive training data and format-aware features...")
        
        # Enhanced training data with realistic document patterns - MORE SAMPLES
        sample_texts = [
            # Invoice samples - more comprehensive patterns (12 samples)
            "invoice number 12345 date amount due payment terms billing address customer account total tax net 30 days remittance",
            "invoice billing statement amount due total subtotal sales tax professional services account payable net payment",
            "billing invoice service charges consultation fees hourly rate total amount due payment receipt remittance address",
            "invoice monthly billing period amount total tax due payment terms account number customer billing address",
            "invoice professional services rendered billing period subtotal tax total amount due net 30 payment terms",
            "bill invoice payment due total amount taxes billing customer account receivable payment terms remittance",
            "invoice statement billing amount due subtotal sales tax total payment terms net days customer account",
            "service invoice consultation fees billing address payment due receipt total amount tax professional services",
            "invoice number payment due date billing statement total amount subtotal tax remittance customer account",
            "billing invoice professional services monthly charges consultation fees total amount due net payment terms",
            "invoice statement account payable customer billing address payment due total subtotal sales tax remittance",
            "service invoice hourly consultation billing period total amount due payment terms account number customer",
            
            # Memo samples - internal communications with clear memo structure (15 samples)
            "memorandum to all staff from hr manager regarding policy update effective immediately all employees must",
            "internal memo to department heads from ceo subject quarterly meeting agenda discussion points action items",
            "memo to staff from operations manager subject budget allocation quarterly review meeting planning session",
            "memorandum to employees from human resources policy changes effective date training implementation schedule",
            "internal memo from executive team to department managers regarding strategic planning initiatives coordination",
            "memo to all staff from it director subject new procedures training sessions communication protocols updates",
            "memorandum staff meeting scheduled conference room agenda quarterly review performance metrics best regards",
            "internal memo from management subject policy revision effective date employee handbook training requirements",
            "memo to team from project manager regarding remote work policy hybrid model core hours collaboration",
            "memorandum to all employees announcement organizational changes department restructuring reporting relationships",
            "internal memo from hr director subject new employee onboarding process training mandatory attendance",
            "memo to department heads from ceo regarding budget planning quarterly review strategic objectives performance",
            "memorandum staff announcement from management subject office relocation timeline moving schedule effective date",
            "internal memo to all employees from it department subject system upgrade maintenance scheduled downtime",
            "memo from executive team to managers regarding performance evaluation process annual review procedures timeline",
            
            # Legal samples - varied legal document types (12 samples)
            "legal notice court case superior justice defendant plaintiff breach contract damages attorney proceedings",
            "legal document court filing motion summary judgment defendant response required attorney representation",
            "notice legal proceedings superior court case plaintiff defendant damages relief sought attorney",
            "legal action breach employment contract violation confidentiality agreement damages attorney client",
            "legal notice dispute resolution court superior business litigation plaintiff defendant attorney",
            "court document legal proceedings motion filing defendant response attorney representation required",
            "legal document attorney client privilege confidential communication court proceedings litigation",
            "notice legal action employment dispute court superior defendant plaintiff attorney representation",
            "legal proceedings superior court case number plaintiff versus defendant motion summary judgment attorney",
            "court filing legal document breach contract damages relief attorney representation litigation proceedings",
            "legal notice superior court case plaintiff defendant attorney client litigation dispute resolution",
            "legal action court proceedings motion filing attorney representation defendant response required",
            
            # Report samples - comprehensive business reports (12 samples)
            "quarterly performance report executive summary financial analysis revenue growth profit margin metrics",
            "annual report financial performance revenue expenses profit customer satisfaction market analysis",
            "performance report key indicators revenue growth customer acquisition retention rate analysis",
            "quarterly business report departmental performance sales marketing operations customer service metrics",
            "financial report executive summary analysis revenue expenses profit recommendations strategic planning",
            "market analysis report competitive landscape customer trends revenue forecasting business strategy",
            "quarterly report financial performance operational metrics customer satisfaction employee engagement",
            "performance analysis report key metrics revenue growth profit margin customer acquisition costs",
            "annual financial report executive summary quarterly performance revenue growth profit analysis",
            "business performance report quarterly metrics customer satisfaction revenue growth operational efficiency",
            "financial analysis report quarterly revenue profit margin market share customer acquisition metrics",
            "quarterly performance report business metrics revenue growth customer satisfaction operational analysis",
            
            # Contract samples - various agreement types (12 samples)
            "employment contract agreement parties terms conditions salary benefits effective date signature witness",
            "service agreement provider client terms conditions compensation termination governing law signature",
            "contract agreement entered parties services compensation payment schedule effective date termination",
            "professional services contract consulting agreement terms payment deliverables obligations signature",
            "employment agreement salary benefits terms conditions twelve months notice period signature",
            "service contract software development consulting services monthly fee payment terms signature",
            "agreement contract parties provider client services exhibit attached incorporated signature",
            "consulting contract terms payment schedule deliverables milestones obligations effective date signature",
            "employment contract agreement terms conditions compensation benefits termination notice signature",
            "service agreement provider client professional services payment terms obligations signature",
            "contract agreement parties terms conditions deliverables payment schedule effective date signature",
            "professional services agreement consulting contract terms compensation obligations termination signature",
            
            # Other samples - technical documents and miscellaneous content (12 samples)
            "technical documentation user manual installation guide troubleshooting procedures system requirements version",
            "project proposal business opportunity scope timeline budget resources team assignments specifications",
            "meeting minutes discussion points action items attendees decisions made follow up tasks documentation",
            "user guide software installation configuration setup procedures technical specifications reference manual",
            "technical specification document system requirements design implementation guidelines standards procedures",
            "general correspondence business communication information material documentation prepared by technical team",
            "system configuration guide installation instructions troubleshooting maintenance procedures reference documentation",
            "standard operating procedures quality assurance testing protocols implementation guidelines specifications",
            "technical manual system documentation configuration procedures implementation guidelines reference",
            "user documentation installation guide technical specifications system requirements troubleshooting procedures",
            "project specification technical document implementation guidelines system requirements configuration manual",
            "technical reference guide system documentation configuration procedures implementation specifications manual"
        ]
        
        sample_labels = [
            # Invoice labels (12 samples)
            'invoice', 'invoice', 'invoice', 'invoice', 'invoice', 'invoice', 
            'invoice', 'invoice', 'invoice', 'invoice', 'invoice', 'invoice',
            # Memo labels (15 samples)
            'memo', 'memo', 'memo', 'memo', 'memo', 'memo', 'memo', 'memo', 
            'memo', 'memo', 'memo', 'memo', 'memo', 'memo', 'memo',
            # Legal labels (12 samples)
            'legal', 'legal', 'legal', 'legal', 'legal', 'legal',
            'legal', 'legal', 'legal', 'legal', 'legal', 'legal',
            # Report labels (12 samples)
            'report', 'report', 'report', 'report', 'report', 'report',
            'report', 'report', 'report', 'report', 'report', 'report',
            # Contract labels (12 samples)
            'contract', 'contract', 'contract', 'contract', 'contract', 'contract',
            'contract', 'contract', 'contract', 'contract', 'contract', 'contract',
            # Other labels (12 samples)
            'other', 'other', 'other', 'other', 'other', 'other',
            'other', 'other', 'other', 'other', 'other', 'other'
        ]
        
        # Create enhanced pipeline with optimized feature extraction
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=5000,  # Increased for better feature capture
                ngram_range=(1, 5),  # Include 5-grams for better phrase detection
                stop_words='english',
                lowercase=True,
                min_df=1,  # Include single-occurrence terms
                max_df=0.8,  # Exclude very common terms
                sublinear_tf=True,  # Apply sublinear tf scaling
                use_idf=True,
                norm='l2',  # L2 normalization for better feature scaling
                smooth_idf=True,  # Smooth idf weights
                token_pattern=r'(?u)\b\w\w+\b|[^\w\s]'  # Include punctuation as features
            )),
            ('classifier', MultinomialNB(alpha=0.05))  # Lower smoothing for higher confidence
        ])
        
        # Train the enhanced model
        self.model.fit(sample_texts, sample_labels)
        
        # Create format-specific feature extractors
        self._setup_format_features()
        
        # Save the model
        self.save_model()
        
        print(f"Enhanced model created and saved to {self.model_path}")
        print(f"Model can classify documents into: {self.categories}")
        print("Enhanced features include: format detection, structural analysis, and comprehensive keyword patterns")
    
    def _setup_format_features(self):
        """Setup format-specific feature extraction patterns."""
        
        # Document structure patterns for enhanced classification
        self.structure_patterns = {
            'invoice': [
                r'invoice\s+(?:number|#|no\.?)\s*:?\s*\d+',
                r'amount\s+due',
                r'billing\s+address',
                r'payment\s+terms',
                r'net\s+\d+\s+days?',
                r'subtotal',
                r'sales?\s+tax',
                r'total\s+amount',
                r'remittance',
                r'account\s+(?:number|#)',
                r'\$[\d,]+\.?\d*'
            ],
            'memo': [
                # Strong memo-specific patterns
                r'(?:internal\s+)?memorandum',
                r'internal\s+memo(?:randum)?',
                r'(?:to|from):\s*[A-Za-z\s,]+',
                r'subject:\s*[^\\n]+',
                r'date:\s*[^\\n]+',
                r'(?:re|subject):\s*policy\s+update',
                r'staff\s+(?:members|meeting|announcement)',
                r'department\s+(?:heads?|managers?)',
                r'effective\s+(?:date|immediately)',
                r'all\s+employees?\s+(?:must|should|are)',
                r'meeting\s+(?:agenda|minutes|scheduled)',
                r'policy\s+(?:changes?|updates?|revision)',
                r'(?:hr|human\s+resources)\s+department',
                r'implementation\s+timeline',
                r'compliance\s+(?:deadline|required)',
                r'best\s+regards',
                r'from:\s*[A-Za-z\s,]+(?:manager|director|ceo|cfo)',
                r'dear\s+(?:team|staff|colleagues)'
            ],
            'legal': [
                r'legal\s+(?:notice|document|action)',
                r'court\s+(?:case|filing|proceedings?)',
                r'(?:plaintiff|defendant)',
                r'superior\s+court',
                r'breach\s+(?:of\s+)?contract',
                r'damages?\s+(?:sought|claimed)',
                r'attorney\s+(?:representation|client)',
                r'motion\s+for',
                r'case\s+(?:number|#)',
                r'legal\s+proceedings?'
            ],
            'report': [
                r'(?:quarterly|annual|monthly)\s+report',
                r'executive\s+summary',
                r'financial\s+(?:analysis|performance)',
                r'revenue\s+growth',
                r'profit\s+margin',
                r'performance\s+(?:metrics|indicators)',
                r'market\s+(?:analysis|share)',
                r'key\s+(?:metrics|indicators)',
                r'customer\s+(?:satisfaction|acquisition)',
                r'business\s+(?:performance|strategy)'
            ],
            'contract': [
                r'(?:employment|service|consulting)\s+(?:contract|agreement)',
                r'agreement\s+(?:entered|between)',
                r'parties?\s+(?:agree|acknowledges?)',
                r'terms?\s+(?:and\s+)?conditions?',
                r'effective\s+date',
                r'signature\s*(?:required|block)?',
                r'governing\s+law',
                r'compensation',
                r'termination',
                r'whereas',
                r'provider\s+(?:agrees|shall)',
                r'client\s+(?:agrees|shall)'
            ],
            'other': [
                # Distinct patterns for "other" category (technical docs, manuals, etc.)
                r'technical\s+(?:specification|documentation|manual)',
                r'user\s+(?:manual|guide|documentation)',
                r'meeting\s+minutes',
                r'project\s+(?:proposal|specification)',
                r'system\s+(?:requirements|configuration)',
                r'installation\s+(?:guide|instructions)',
                r'troubleshooting\s+(?:guide|procedures)',
                r'version\s+\d+\.\d+',
                r'reference\s+(?:manual|guide|doc)',
                r'(?:setup|configuration)\s+(?:guide|manual)',
                r'(?:api|software)\s+documentation',
                r'implementation\s+(?:guide|manual)',
                r'(?:quality|testing)\s+(?:procedures|protocols)',
                r'standard\s+operating\s+procedures',
                r'maintenance\s+(?:guide|procedures)',
                r'appendices?\s+for\s+detailed',
                r'document\s+(?:information|prepared\s+by)',
                r'prepared\s+by:\s*[A-Za-z\s]+',
                r'document\s+(?:version|reference)',
                r'(?:general|miscellaneous)\s+(?:information|correspondence)'
            ]
        }
        
        # Keyword weights for different document types
        self.keyword_weights = {
            'invoice': {
                'high': ['invoice', 'billing', 'payment', 'amount', 'due', 'total', 'tax'],
                'medium': ['customer', 'account', 'net', 'terms', 'receipt', 'charges'],
                'low': ['professional', 'services', 'consultation', 'monthly', 'quarterly']
            },
            'memo': {
                'high': ['memo', 'memorandum', 'internal', 'staff', 'policy', 'department'],
                'medium': ['meeting', 'announcement', 'update', 'effective', 'employees', 'team'],
                'low': ['management', 'training', 'procedures', 'communication', 'implementation']
            },
            'legal': {
                'high': ['legal', 'court', 'case', 'plaintiff', 'defendant', 'attorney'],
                'medium': ['notice', 'proceedings', 'motion', 'filing', 'damages', 'breach'],
                'low': ['superior', 'justice', 'litigation', 'representation', 'contract']
            },
            'report': {
                'high': ['report', 'analysis', 'performance', 'quarterly', 'annual'],
                'medium': ['revenue', 'financial', 'metrics', 'summary', 'growth'],
                'low': ['business', 'market', 'customer', 'operational', 'strategic']
            },
            'contract': {
                'high': ['contract', 'agreement', 'parties', 'terms', 'signature'],
                'medium': ['effective', 'services', 'compensation', 'termination', 'governing'],
                'low': ['provider', 'client', 'whereas', 'obligations', 'deliverables']
            },
            'other': {
                'high': ['technical', 'manual', 'documentation', 'specification', 'guide'],
                'medium': ['user', 'system', 'configuration', 'implementation', 'procedures'],
                'low': ['reference', 'installation', 'troubleshooting', 'maintenance', 'version']
            }
        }
        
        # Anti-patterns to reduce false positives
        self.anti_patterns = {
            'memo': [
                # If document has these patterns, it's less likely to be a memo
                r'technical\s+specification',
                r'user\s+manual',
                r'api\s+documentation',
                r'system\s+requirements',
                r'installation\s+guide',
                r'version\s+\d+\.\d+',
                r'troubleshooting\s+procedures'
            ],
            'other': [
                # If document has these patterns, it's less likely to be "other"
                r'(?:internal\s+)?memorandum',
                r'(?:to|from):\s*[A-Za-z\s,]+',
                r'subject:\s*policy',
                r'staff\s+announcement',
                r'department\s+heads?',
                r'all\s+employees\s+must',
                r'effective\s+immediately'
            ]
        }
    
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
        Predict the category of a single document using enhanced features.
        
        Args:
            text: Document text
            
        Returns:
            Tuple of (predicted_category, confidence_score)
        """
        if self.model is None:
            return 'other', 0.0
        
        try:
            # Get base ML model prediction
            base_prediction = self.model.predict([text])[0]
            base_probabilities = self.model.predict_proba([text])[0]
            base_confidence = max(base_probabilities)
            
            # Apply enhanced pattern-based scoring
            enhanced_scores = self._calculate_enhanced_scores(text)
            
            # Combine ML prediction with pattern-based scoring
            final_prediction, final_confidence = self._combine_predictions(
                base_prediction, base_confidence, enhanced_scores
            )
            
            return final_prediction, final_confidence
            
        except Exception as e:
            print(f"Error during prediction: {e}")
            return 'other', 0.0
    
    def _calculate_enhanced_scores(self, text: str) -> Dict[str, float]:
        """Calculate enhanced scores based on document structure and patterns."""
        scores = {category: 0.0 for category in self.categories}
        text_lower = text.lower()
        
        # Check structural patterns with increased weights
        if hasattr(self, 'structure_patterns'):
            for category, patterns in self.structure_patterns.items():
                pattern_matches = 0
                for pattern in patterns:
                    import re
                    if re.search(pattern, text_lower):
                        pattern_matches += 1
                
                # Increased scoring based on pattern matches
                if pattern_matches > 0:
                    scores[category] += min(pattern_matches / len(patterns), 1.0) * 0.6  # Increased from 0.4
        
        # Apply anti-pattern penalties
        if hasattr(self, 'anti_patterns'):
            for category, anti_patterns in self.anti_patterns.items():
                penalty = 0.0
                for pattern in anti_patterns:
                    import re
                    if re.search(pattern, text_lower):
                        penalty += 0.4  # Increased penalty for better distinction
                
                scores[category] -= min(penalty, 0.8)  # Increased cap penalty
        
        # Check keyword weights with increased impact
        if hasattr(self, 'keyword_weights'):
            for category, weight_dict in self.keyword_weights.items():
                keyword_score = 0.0
                
                # High weight keywords - increased impact
                for keyword in weight_dict['high']:
                    if keyword in text_lower:
                        keyword_score += 0.4  # Increased from 0.3
                
                # Medium weight keywords - increased impact
                for keyword in weight_dict['medium']:
                    if keyword in text_lower:
                        keyword_score += 0.3  # Increased from 0.2
                
                # Low weight keywords - increased impact
                for keyword in weight_dict['low']:
                    if keyword in text_lower:
                        keyword_score += 0.15  # Increased from 0.1
                
                scores[category] += min(keyword_score, 0.8)  # Increased cap from 0.6
        
        # Document format analysis
        format_bonus = self._analyze_document_format(text)
        for category, bonus in format_bonus.items():
            scores[category] += bonus
        
        # Special memo vs other distinction logic
        scores = self._apply_memo_other_distinction(text_lower, scores)
        
        return scores
    
    def _analyze_document_format(self, text: str) -> Dict[str, float]:
        """Analyze document format characteristics."""
        format_scores = {category: 0.0 for category in self.categories}
        
        # Check for specific document format indicators
        lines = text.split('\n')
        text_lower = text.lower()
        
        # Invoice format indicators - enhanced detection
        if any('=' * 10 in line for line in lines):  # Header separators
            if any(word in text_lower for word in ['invoice', 'billing', 'amount due']):
                format_scores['invoice'] += 0.3  # Increased from 0.2
        
        # Strong invoice patterns
        if any(pattern in text_lower for pattern in ['invoice number', 'amount due', 'payment terms']):
            format_scores['invoice'] += 0.25
        
        # Contract format indicators - enhanced
        if 'SIGNATURES' in text or 'IN WITNESS WHEREOF' in text:
            format_scores['contract'] += 0.4  # Increased from 0.3
        
        if text.count('================') >= 2:  # Multiple section separators
            if any(word in text_lower for word in ['agreement', 'contract', 'parties']):
                format_scores['contract'] += 0.3  # Increased from 0.2
        
        # Strong contract indicators
        if any(pattern in text_lower for pattern in ['agreement entered', 'parties agree', 'effective date']):
            format_scores['contract'] += 0.25
        
        # Memo format indicators - enhanced
        memo_headers = sum(1 for line in lines if line.strip().upper().startswith(('TO:', 'FROM:', 'SUBJECT:', 'DATE:')))
        if memo_headers >= 2:
            format_scores['memo'] += 0.4  # Strong memo format
        elif memo_headers >= 1:
            format_scores['memo'] += 0.2  # Some memo format
        
        # Strong memo patterns
        if any(pattern in text_lower for pattern in ['memorandum', 'internal memo', 'staff announcement']):
            format_scores['memo'] += 0.3
        
        # Legal document indicators - enhanced
        if any(phrase in text for phrase in ['Superior Court', 'Case No.', 'Plaintiff v.']):
            format_scores['legal'] += 0.4  # Increased from 0.3
        
        # Strong legal patterns
        if any(pattern in text_lower for pattern in ['legal notice', 'court case', 'attorney representation']):
            format_scores['legal'] += 0.25
        
        # Report format indicators - enhanced
        if 'EXECUTIVE SUMMARY' in text.upper() or 'QUARTERLY REPORT' in text.upper():
            format_scores['report'] += 0.4  # Increased from 0.3
        
        # Strong report patterns
        if any(pattern in text_lower for pattern in ['performance report', 'financial analysis', 'revenue growth']):
            format_scores['report'] += 0.25
        
        # Other document indicators - enhanced
        if any(pattern in text_lower for pattern in ['technical documentation', 'user manual', 'system requirements']):
            format_scores['other'] += 0.3
        
        return format_scores
    
    def _combine_predictions(self, base_prediction: str, base_confidence: float, 
                           enhanced_scores: Dict[str, float]) -> Tuple[str, float]:
        """Combine ML prediction with enhanced pattern-based scoring."""
        
        # Optimized weight distribution for better confidence
        ml_weight = 0.55  # Slightly reduced to give more weight to patterns
        pattern_weight = 0.45  # Increased pattern influence
        
        # Create combined scores
        combined_scores = {}
        
        # Get ML model scores for all categories
        for category in self.categories:
            if category == base_prediction:
                ml_score = base_confidence
            else:
                ml_score = 0.03  # Smaller baseline for non-predicted categories
            
            pattern_score = enhanced_scores.get(category, 0.0)
            combined_scores[category] = (ml_weight * ml_score) + (pattern_weight * pattern_score)
        
        # Find the best category
        best_category = max(combined_scores, key=combined_scores.get)
        best_score = combined_scores[best_category]
        
        # Enhanced confidence boosting for clearer classifications
        if best_score > 0.4:  # Lower threshold for boosting
            # Progressive confidence boosting
            if best_score > 0.7:
                # Strong classification - major boost
                confidence_boost = min((best_score - 0.7) * 1.2, 0.25)
            elif best_score > 0.5:
                # Good classification - moderate boost
                confidence_boost = min((best_score - 0.5) * 1.0, 0.2)
            else:
                # Decent classification - minor boost
                confidence_boost = min((best_score - 0.4) * 0.8, 0.15)
            
            final_confidence = min(best_score + confidence_boost, 1.0)
        else:
            final_confidence = best_score
        
        # Additional boost for very clear pattern matches
        pattern_strength = enhanced_scores.get(best_category, 0.0)
        if pattern_strength > 0.6:  # Strong pattern match
            pattern_boost = min(pattern_strength * 0.1, 0.1)
            final_confidence = min(final_confidence + pattern_boost, 1.0)
        
        return best_category, final_confidence
    
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
    
    def _apply_memo_other_distinction(self, text_lower: str, scores: Dict[str, float]) -> Dict[str, float]:
        """Apply special logic to distinguish between memo and other categories."""
        import re
        
        # Strong memo indicators - MUST be business communications
        memo_indicators = [
            r'(?:internal\s+)?memorandum',
            r'memo\s*(?:to|from)',
            r'(?:to|from):\s*[a-z\s,]+(?:manager|director|team|staff|department)',
            r'subject:\s*(?:policy|update|meeting|announcement|implementation)',
            r'all\s+(?:staff|employees)\s+(?:must|should|are|will|need)',
            r'effective\s+(?:immediately|date)',
            r'department\s+(?:heads?|managers?)',
            r'(?:best\s+regards|sincerely),?\s*[a-z\s,]+(?:manager|director)',
            r'please\s+(?:ensure|note|be\s+aware)',
            r'this\s+memo\s+(?:is|serves)',
            r'(?:hr|human\s+resources)\s+(?:department|policy)',
            r'employee\s+(?:handbook|policy|guidelines)'
        ]
        
        # GREATLY EXPANDED other/technical indicators - documents, manuals, specs
        other_indicators = [
            r'technical\s+(?:specification|documentation|manual)',
            r'user\s+(?:manual|guide|documentation)',
            r'system\s+(?:requirements|configuration|specification)',
            r'version\s+\d+\.\d+',
            r'installation\s+(?:guide|instructions|manual)',
            r'document\s+(?:prepared\s+by|information|reference)',
            r'reference\s+(?:manual|guide|doc)',
            r'appendices?\s+for\s+detailed',
            r'standard\s+operating\s+procedures',
            r'document\s+information:',
            r'author:\s*[a-z\s]+',
            r'meeting\s+minutes',
            r'project\s+(?:documentation|specification)',
            r'quality\s+(?:assurance|control)',
            r'troubleshooting\s+(?:guide|procedures)',
            r'configuration\s+(?:parameters|settings)',
            r'this\s+document\s+(?:serves|contains|provides)',
            r'(?:overview|introduction):\s*this\s+document',
            r'procedures\s+(?:and\s+)?guidelines',
            # NEW STRONG INDICATORS for technical documents
            r'api\s+(?:documentation|reference|guide)',
            r'software\s+(?:documentation|manual|guide)',
            r'implementation\s+(?:guide|manual|notes)',
            r'maintenance\s+(?:procedures|guide|manual)',
            r'setup\s+(?:guide|instructions|manual)',
            r'deployment\s+(?:guide|instructions)',
            r'data\s+(?:sheet|specification)',
            r'technical\s+(?:notes|report|summary)',
            r'specification\s+document',
            r'design\s+(?:document|specification)',
            r'requirements\s+(?:document|specification)',
            r'white\s+paper',
            r'research\s+(?:paper|document)',
            r'analysis\s+(?:document|report)',
            r'feasibility\s+(?:study|analysis)',
            r'test\s+(?:plan|procedure|protocol)',
            r'validation\s+(?:procedure|protocol)',
            r'risk\s+(?:assessment|analysis)',
            r'impact\s+(?:analysis|assessment)',
            r'technical\s+(?:brief|overview)',
            r'system\s+(?:architecture|design)',
            r'performance\s+(?:analysis|testing)',
            r'benchmark\s+(?:results|analysis)',
            r'compatibility\s+(?:matrix|guide)',
            r'integration\s+(?:guide|manual)',
            r'migration\s+(?:guide|plan)',
            r'backup\s+(?:procedure|plan)',
            r'recovery\s+(?:procedure|plan)',
            r'security\s+(?:protocol|procedure)',
            r'audit\s+(?:procedure|checklist)',
            r'compliance\s+(?:checklist|guide)',
            r'workflow\s+(?:documentation|guide)',
            r'process\s+(?:documentation|manual)',
            r'operational\s+(?:guide|manual)',
            r'administrative\s+(?:guide|manual)',
            r'reference\s+(?:architecture|implementation)',
            r'best\s+practices\s+(?:guide|document)',
            r'lesson\s+learned',
            r'post\s+mortem',
            r'incident\s+(?:report|analysis)',
            r'root\s+cause\s+analysis'
        ]
        
        memo_score = 0
        other_score = 0
        
        # Count memo indicators
        for pattern in memo_indicators:
            if re.search(pattern, text_lower):
                memo_score += 1
        
        # Count other indicators with MUCH stronger weighting
        for pattern in other_indicators:
            if re.search(pattern, text_lower):
                other_score += 2  # Double weight for "other" indicators
        
        # Apply adjustments with MUCH stronger penalties and boosts
        if memo_score > 0 and other_score == 0:
            # Clear memo document
            scores['memo'] += 0.6  # Increased boost
            scores['other'] -= 0.5  # Increased penalty
        elif other_score > 0 and memo_score == 0:
            # Clear other document - VERY STRONG boost for "other"
            scores['other'] += 0.8  # Increased from 0.6
            scores['memo'] -= 0.7  # Increased penalty from 0.5
        elif memo_score > other_score:
            # More memo indicators
            boost = min((memo_score - other_score) * 0.4, 0.5)  # Increased
            scores['memo'] += boost
            scores['other'] -= boost
        elif other_score > memo_score:
            # More other indicators - VERY STRONG preference for "other"
            boost = min((other_score - memo_score) * 0.5, 0.8)  # Increased significantly
            scores['other'] += boost
            scores['memo'] -= boost * 1.5  # Much stronger penalty for memo
        
        # Check for memo structure (TO/FROM/SUBJECT format)
        memo_structure_patterns = [
            r'to:\s*[a-z\s,]+',
            r'from:\s*[a-z\s,]+',
            r'(?:subject|re):\s*[^\n]+',
            r'date:\s*[^\n]+'
        ]
        
        memo_structure_matches = sum(1 for pattern in memo_structure_patterns 
                                   if re.search(pattern, text_lower))
        
        # ONLY boost memo if there are actual memo structural elements AND no strong technical indicators
        if memo_structure_matches >= 3 and other_score == 0:
            # Strong memo structure with no technical indicators
            scores['memo'] += 0.6  # Increased from 0.5
            scores['other'] -= 0.5  # Increased from 0.4
        elif memo_structure_matches >= 2 and other_score == 0:
            # Moderate memo structure with no technical indicators
            scores['memo'] += 0.4  # Increased from 0.3
            scores['other'] -= 0.3  # Increased from 0.2
        
        # Check for technical document structure - MUCH STRONGER
        technical_patterns = [
            r'document\s+(?:version|reference)',
            r'prepared\s+by:\s*[a-z\s]+',
            r'(?:section|chapter)\s+\d+',
            r'table\s+of\s+contents',
            r'appendix\s+[a-z]',
            r'revision\s+history',
            r'(?:overview|introduction)\s*:?\s*this\s+document',
            # ADDITIONAL technical structure patterns
            r'figure\s+\d+',
            r'table\s+\d+',
            r'equation\s+\d+',
            r'reference\s+\[\d+\]',
            r'see\s+(?:section|chapter|appendix)',
            r'as\s+(?:shown|described)\s+in',
            r'refer\s+to\s+(?:section|chapter|figure|table)',
            r'listed\s+(?:below|above)',
            r'following\s+(?:table|figure|list|steps)',
            r'step\s+\d+',
            r'procedure\s+\d+',
            r'note:\s+',
            r'warning:\s+',
            r'caution:\s+',
            r'important:\s+',
            r'tip:\s+',
            r'example:\s+',
            r'sample:\s+'
        ]
        
        technical_matches = sum(1 for pattern in technical_patterns 
                              if re.search(pattern, text_lower))
        
        if technical_matches >= 2:
            # Strong technical document structure - MASSIVE boost for "other"
            scores['other'] += 0.7  # Increased from 0.4
            scores['memo'] -= 0.6  # Increased from 0.3
        elif technical_matches >= 1:
            # Some technical structure
            scores['other'] += 0.4
            scores['memo'] -= 0.3
        
        # Additional check: If document has ANY business memo keywords but ALSO technical patterns,
        # heavily favor "other" (this should catch our misclassified cases)
        if other_score > 0 and memo_score > 0:
            # Mixed signals, but technical indicators should win
            scores['other'] += 0.6
            scores['memo'] -= 0.8  # Heavy penalty for memo classification
        
        return scores

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