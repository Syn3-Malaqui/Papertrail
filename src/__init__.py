"""
Papertrail Document Classification System
Source package for document parsing, preprocessing, and classification.
"""

__version__ = "1.0.0"
__author__ = "Papertrail Team"
__description__ = "Intelligent document classification system"

from .parser import DocumentParser
from .preprocess import TextPreprocessor
from .predict import DocumentClassifier

__all__ = ['DocumentParser', 'TextPreprocessor', 'DocumentClassifier'] 