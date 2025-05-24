"""
Document Parser Module
Handles finding and extracting text from PDF, TXT, and DOCX files.
"""

import os
import glob
from pathlib import Path
from typing import List, Dict, Optional

# PDF parsing
from pdfminer.high_level import extract_text as pdf_extract_text
from pdfminer.pdfparser import PDFSyntaxError

# DOCX parsing
from docx import Document

class DocumentParser:
    """Handles document discovery and text extraction."""
    
    SUPPORTED_EXTENSIONS = ['.pdf', '.txt', '.docx']
    
    def __init__(self):
        self.parsed_files = []
        self.errors = []
    
    def find_documents(self, folder_path: str) -> List[str]:
        """
        Recursively find all supported document files in the given folder.
        
        Args:
            folder_path: Path to the folder to search
            
        Returns:
            List of file paths
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")
        
        file_paths = []
        
        for ext in self.SUPPORTED_EXTENSIONS:
            pattern = os.path.join(folder_path, '**', f'*{ext}')
            files = glob.glob(pattern, recursive=True)
            file_paths.extend(files)
        
        return sorted(file_paths)
    
    def extract_text_from_pdf(self, file_path: str) -> Optional[str]:
        """Extract text from PDF file."""
        try:
            text = pdf_extract_text(file_path)
            return text.strip() if text else None
        except (PDFSyntaxError, Exception) as e:
            self.errors.append(f"PDF parsing error for {file_path}: {str(e)}")
            return None
    
    def extract_text_from_docx(self, file_path: str) -> Optional[str]:
        """Extract text from DOCX file."""
        try:
            doc = Document(file_path)
            paragraphs = [paragraph.text for paragraph in doc.paragraphs]
            text = '\n'.join(paragraphs)
            return text.strip() if text else None
        except Exception as e:
            self.errors.append(f"DOCX parsing error for {file_path}: {str(e)}")
            return None
    
    def extract_text_from_txt(self, file_path: str) -> Optional[str]:
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                text = file.read()
            return text.strip() if text else None
        except Exception as e:
            self.errors.append(f"TXT parsing error for {file_path}: {str(e)}")
            return None
    
    def extract_text(self, file_path: str) -> Optional[str]:
        """
        Extract text from a file based on its extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Extracted text or None if failed
        """
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_ext == '.docx':
            return self.extract_text_from_docx(file_path)
        elif file_ext == '.txt':
            return self.extract_text_from_txt(file_path)
        else:
            self.errors.append(f"Unsupported file type: {file_ext}")
            return None
    
    def parse_documents(self, folder_path: str) -> Dict[str, str]:
        """
        Parse all documents in a folder and return a mapping of filenames to text.
        
        Args:
            folder_path: Path to the folder containing documents
            
        Returns:
            Dictionary mapping filenames to extracted text
        """
        self.parsed_files = []
        self.errors = []
        
        file_paths = self.find_documents(folder_path)
        results = {}
        
        print(f"Found {len(file_paths)} documents to process...")
        
        for file_path in file_paths:
            print(f"Processing: {os.path.basename(file_path)}")
            
            text = self.extract_text(file_path)
            if text:
                filename = os.path.basename(file_path)
                results[filename] = text
                self.parsed_files.append(file_path)
            else:
                print(f"Failed to extract text from: {file_path}")
        
        if self.errors:
            print(f"\nEncountered {len(self.errors)} errors during parsing:")
            for error in self.errors:
                print(f"  - {error}")
        
        print(f"\nSuccessfully parsed {len(results)} documents.")
        return results

# Example usage
if __name__ == "__main__":
    parser = DocumentParser()
    
    # Test with a sample directory
    test_folder = input("Enter folder path to test (or press Enter for current directory): ").strip()
    if not test_folder:
        test_folder = "."
    
    try:
        documents = parser.parse_documents(test_folder)
        
        if documents:
            print("\n--- Sample Results ---")
            for filename, text in list(documents.items())[:2]:  # Show first 2 files
                print(f"\nFile: {filename}")
                print(f"Text preview: {text[:200]}...")
        else:
            print("No documents found or successfully parsed.")
            
    except Exception as e:
        print(f"Error: {e}") 