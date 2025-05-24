"""
Papertrail - Document Classification System
Main entry point for the document classification pipeline.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

# Import our custom modules
sys.path.append('src')
from src.parser import DocumentParser
from src.preprocess import TextPreprocessor
from src.predict import DocumentClassifier

# GUI imports (optional)
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("Warning: tkinter not available. GUI mode disabled.")


class PapertrailPipeline:
    """Main pipeline orchestrator for document classification."""
    
    def __init__(self, use_stemming: bool = False, move_files: bool = False):
        """
        Initialize the pipeline.
        
        Args:
            use_stemming: Whether to use stemming in preprocessing
            move_files: Whether to organize files into category folders
        """
        self.parser = DocumentParser()
        self.preprocessor = TextPreprocessor(use_stemming=use_stemming)
        self.classifier = DocumentClassifier()
        self.move_files = move_files
        
        # Statistics
        self.stats = {
            'total_files_found': 0,
            'successfully_parsed': 0,
            'successfully_classified': 0,
            'files_moved': 0
        }
    
    def process_folder(self, folder_path: str, output_csv: str = "classification_results.csv") -> Dict[str, Any]:
        """
        Process all documents in a folder through the complete pipeline.
        
        Args:
            folder_path: Path to folder containing documents
            output_csv: Path for output CSV file
            
        Returns:
            Dictionary containing processing results and statistics
        """
        print("=" * 60)
        print("🚀 PAPERTRAIL DOCUMENT CLASSIFICATION PIPELINE")
        print("=" * 60)
        
        try:
            # Step 1: Parse documents
            print("\n📁 Step 1: Finding and parsing documents...")
            documents = self.parser.parse_documents(folder_path)
            self.stats['total_files_found'] = len(self.parser.find_documents(folder_path))
            self.stats['successfully_parsed'] = len(documents)
            
            if not documents:
                print("❌ No documents found or successfully parsed!")
                return {'success': False, 'error': 'No documents parsed', 'stats': self.stats}
            
            # Step 2: Preprocess text
            print("\n🧼 Step 2: Preprocessing text...")
            preprocessed_docs = self.preprocessor.preprocess_documents(documents)
            
            # Convert back to text for prediction
            text_docs = self.classifier.preprocess_for_prediction(preprocessed_docs)
            
            # Step 3: Classify documents
            print("\n🔍 Step 3: Classifying documents...")
            predictions = self.classifier.predict_documents(text_docs)
            self.stats['successfully_classified'] = len(predictions)
            
            # Step 4: Save results
            print("\n📊 Step 4: Saving results...")
            self.classifier.save_results_csv(predictions, output_csv)
            
            # Step 5: Optional file organization
            if self.move_files:
                print("\n📁 Step 5: Organizing files by category...")
                self.organize_files(folder_path, predictions)
            
            # Final summary
            self.print_final_summary(predictions)
            
            return {
                'success': True,
                'predictions': predictions,
                'stats': self.stats,
                'output_csv': output_csv
            }
            
        except Exception as e:
            error_msg = f"Pipeline error: {str(e)}"
            print(f"❌ {error_msg}")
            return {'success': False, 'error': error_msg, 'stats': self.stats}
    
    def organize_files(self, base_folder: str, predictions: Dict[str, Dict[str, Any]]):
        """
        Organize files into folders based on their predicted categories.
        Enhanced to handle all supported file formats and provide comprehensive feedback.
        
        Args:
            base_folder: Original folder containing the files
            predictions: Dictionary of prediction results
        """
        try:
            # Create organized folder structure
            organized_folder = os.path.join(base_folder, "organized_documents")
            os.makedirs(organized_folder, exist_ok=True)
            
            # Create category folders
            categories = set(result['predicted_category'] for result in predictions.values())
            for category in categories:
                category_folder = os.path.join(organized_folder, category)
                os.makedirs(category_folder, exist_ok=True)
            
            print(f"📁 Created category folders: {', '.join(sorted(categories))}")
            
            # Track organization statistics
            moved_count = 0
            format_stats = {}
            category_stats = {category: 0 for category in categories}
            
            # Move files
            for filename, result in predictions.items():
                source_path = None
                
                # Find the original file (check both direct path and in parsed_files)
                possible_paths = [
                    os.path.join(base_folder, filename),  # Direct in base folder
                ]
                
                # Add all paths from parsed_files that match the filename
                for file_path in self.parser.parsed_files:
                    if os.path.basename(file_path) == filename:
                        possible_paths.append(file_path)
                
                # Find the actual existing file
                for path in possible_paths:
                    if os.path.exists(path):
                        source_path = path
                        break
                
                if source_path and os.path.exists(source_path):
                    category = result['predicted_category']
                    destination = os.path.join(organized_folder, category, filename)
                    
                    try:
                        # Create destination directory if it doesn't exist
                        os.makedirs(os.path.dirname(destination), exist_ok=True)
                        
                        # Move the file
                        shutil.move(source_path, destination)
                        moved_count += 1
                        
                        # Track statistics
                        file_ext = os.path.splitext(filename)[1].lower()
                        format_stats[file_ext] = format_stats.get(file_ext, 0) + 1
                        category_stats[category] += 1
                        
                        confidence = result['confidence']
                        confidence_icon = "🟢" if confidence > 0.7 else "🟡" if confidence > 0.5 else "🟠"
                        print(f"  {confidence_icon} Moved {filename} -> {category}/ (confidence: {confidence:.3f})")
                        
                    except Exception as e:
                        print(f"  ❌ Failed to move {filename}: {e}")
                else:
                    print(f"  ⚠️  Source file not found for {filename}")
            
            self.stats['files_moved'] = moved_count
            
            # Print comprehensive organization summary
            print(f"\n✅ Successfully organized {moved_count} files into categories")
            print(f"📂 Organized files location: {organized_folder}")
            
            if format_stats:
                print(f"\n📊 Files organized by format:")
                format_icons = {
                    '.pdf': '📄', '.docx': '📝', '.txt': '📋', '.doc': '📄', 
                    '.html': '🌐', '.htm': '🌐', '.rtf': '📄', '.odt': '📄', 
                    '.pptx': '📊', '.ppt': '📊', '.xlsx': '📊', '.xls': '📊'
                }
                for fmt, count in sorted(format_stats.items()):
                    icon = format_icons.get(fmt, '📄')
                    print(f"   {icon} {fmt.upper()}: {count} files")
            
            if category_stats:
                print(f"\n🗂️  Files organized by category:")
                for category, count in sorted(category_stats.items()):
                    if count > 0:
                        print(f"   📁 {category}: {count} files")
            
        except Exception as e:
            print(f"❌ Error organizing files: {e}")
            import traceback
            traceback.print_exc()
    
    def print_final_summary(self, predictions: Dict[str, Dict[str, Any]]):
        """Print a summary of the processing results."""
        print("\n" + "=" * 60)
        print("📋 PROCESSING SUMMARY")
        print("=" * 60)
        
        print(f"📁 Total files found: {self.stats['total_files_found']}")
        print(f"✅ Successfully parsed: {self.stats['successfully_parsed']}")
        print(f"🔍 Successfully classified: {self.stats['successfully_classified']}")
        
        if self.move_files:
            print(f"📦 Files organized: {self.stats['files_moved']}")
        
        # Category breakdown
        if predictions:
            categories = {}
            high_confidence = 0
            
            for result in predictions.values():
                category = result['predicted_category']
                categories[category] = categories.get(category, 0) + 1
                
                if result['confidence'] > 0.7:
                    high_confidence += 1
            
            print(f"\n📊 Category Distribution:")
            for category, count in sorted(categories.items()):
                print(f"   {category}: {count} documents")
            
            avg_confidence = sum(r['confidence'] for r in predictions.values()) / len(predictions)
            print(f"\n🎯 Average confidence: {avg_confidence:.3f}")
            print(f"⭐ High confidence predictions (>0.7): {high_confidence}/{len(predictions)}")


def gui_mode():
    """Run the application in GUI mode using tkinter."""
    if not GUI_AVAILABLE:
        print("❌ GUI mode not available. tkinter is not installed.")
        return
    
    def select_folder_and_process():
        folder_path = filedialog.askdirectory(title="Select folder containing documents")
        if folder_path:
            try:
                # Show processing dialog
                processing_window = tk.Toplevel(root)
                processing_window.title("Processing...")
                processing_window.geometry("300x100")
                tk.Label(processing_window, text="Processing documents...\nPlease wait.").pack(pady=20)
                processing_window.update()
                
                # Process documents
                pipeline = PapertrailPipeline(
                    use_stemming=stem_var.get(),
                    move_files=move_var.get()
                )
                
                result = pipeline.process_folder(folder_path)
                processing_window.destroy()
                
                # Show results
                if result['success']:
                    message = f"✅ Processing completed successfully!\n\n"
                    message += f"📁 Files found: {result['stats']['total_files_found']}\n"
                    message += f"✅ Successfully processed: {result['stats']['successfully_classified']}\n"
                    message += f"📊 Results saved to: {result['output_csv']}"
                    
                    if pipeline.move_files:
                        message += f"\n📦 Files organized: {result['stats']['files_moved']}"
                    
                    messagebox.showinfo("Success", message)
                else:
                    messagebox.showerror("Error", f"❌ Processing failed:\n{result['error']}")
                    
            except Exception as e:
                if 'processing_window' in locals():
                    processing_window.destroy()
                messagebox.showerror("Error", f"❌ An error occurred:\n{str(e)}")
    
    # Create GUI
    root = tk.Tk()
    root.title("Papertrail - Document Classifier")
    root.geometry("400x300")
    
    # Title
    title_label = tk.Label(root, text="📄 Papertrail Document Classifier", 
                          font=("Arial", 16, "bold"))
    title_label.pack(pady=20)
    
    # Options
    options_frame = tk.Frame(root)
    options_frame.pack(pady=10)
    
    stem_var = tk.BooleanVar()
    stem_check = tk.Checkbutton(options_frame, text="🌱 Use stemming in preprocessing", 
                               variable=stem_var)
    stem_check.pack(anchor='w')
    
    move_var = tk.BooleanVar()
    move_check = tk.Checkbutton(options_frame, text="📁 Organize files by category", 
                               variable=move_var)
    move_check.pack(anchor='w')
    
    # Instructions
    instructions = tk.Label(root, 
                           text="Click below to select a folder containing\nPDF, TXT, or DOCX files to classify",
                           justify=tk.CENTER)
    instructions.pack(pady=10)
    
    # Select folder button
    select_button = tk.Button(root, text="📁 Select Folder & Process", 
                             command=select_folder_and_process,
                             bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                             padx=20, pady=10)
    select_button.pack(pady=20)
    
    # Status
    status_label = tk.Label(root, text="Ready to process documents", 
                           fg="gray")
    status_label.pack(pady=10)
    
    root.mainloop()


def cli_mode():
    """Run the application in command-line mode."""
    parser = argparse.ArgumentParser(description="Papertrail Document Classification System")
    parser.add_argument("folder", nargs='?', help="Folder path containing documents to classify")
    parser.add_argument("--output", "-o", default="classification_results.csv",
                        help="Output CSV file path (default: classification_results.csv)")
    parser.add_argument("--stemming", action="store_true",
                        help="Enable stemming in text preprocessing")
    parser.add_argument("--organize", action="store_true",
                        help="Organize files into category folders after classification")
    parser.add_argument("--gui", action="store_true",
                        help="Launch GUI mode")
    parser.add_argument("--dashboard", action="store_true",
                        help="Launch web dashboard after classification")
    
    args = parser.parse_args()
    
    # GUI mode
    if args.gui:
        gui_mode()
        return

    # Dashboard mode
    if args.dashboard:
        try:
            import subprocess
            import sys
            print("🚀 Launching Papertrail Dashboard...")
            subprocess.run([sys.executable, "launch_dashboard.py"])
        except Exception as e:
            print(f"❌ Error launching dashboard: {e}")
            print("💡 Try running: python launch_dashboard.py")
        return

    # Get folder path
    folder_path = args.folder
    if not folder_path:
        if GUI_AVAILABLE:
            try:
                root = tk.Tk()
                root.withdraw()  # Hide main window
                folder_path = filedialog.askdirectory(title="Select folder containing documents")
                root.destroy()
            except:
                pass
        
        if not folder_path:
            folder_path = input("📁 Enter folder path containing documents: ").strip()
    
    if not folder_path or not os.path.exists(folder_path):
        print("❌ Invalid folder path provided!")
        return
    
    # Process documents
    pipeline = PapertrailPipeline(
        use_stemming=args.stemming,
        move_files=args.organize if args.organize else True  # Default to True, override only if explicitly set
    )
    
    print(f"\n🚀 Processing documents in: {folder_path}")
    print(f"📊 Results will be saved to: {args.output}")
    print(f"📁 Files will be organized into category folders: {'Yes' if pipeline.move_files else 'No'}")
    if pipeline.move_files:
        print(f"   📂 Organized files will be in: {os.path.join(folder_path, 'organized_documents')}")
    print()
    
    result = pipeline.process_folder(folder_path, args.output)
    
    if result['success']:
        print(f"\n🎉 Processing completed successfully!")
        print(f"📊 Results saved to: {args.output}")
        
        # Ask if user wants to view dashboard
        try:
            response = input("\n🚀 Would you like to view the results in the dashboard? (y/n): ").lower()
            if response == 'y':
                import subprocess
                import sys
                subprocess.run([sys.executable, "launch_dashboard.py"])
        except KeyboardInterrupt:
            print("\nSkipping dashboard launch.")
        except Exception as e:
            print(f"Dashboard launch failed: {e}")
            print("💡 You can manually launch it with: python launch_dashboard.py")
    else:
        print(f"\n❌ Processing failed: {result['error']}")


def main():
    """Main entry point."""
    print("🚀 Welcome to Papertrail - Document Classification System!")
    print("   Automatically classify PDF, TXT, and DOCX files\n")
    
    # Check if GUI mode was requested via arguments
    if len(sys.argv) > 1 and "--gui" in sys.argv:
        gui_mode()
    elif len(sys.argv) == 1:
        # No arguments - ask user for mode preference
        if GUI_AVAILABLE:
            choice = input("Choose interface mode:\n  1. 🖥️  GUI Mode\n  2. 💻 Command Line Mode\n  Enter choice (1 or 2): ").strip()
            
            if choice == "1":
                gui_mode()
            else:
                cli_mode()
        else:
            print("GUI not available. Using command line mode.")
            cli_mode()
    else:
        # Arguments provided - use CLI mode
        cli_mode()


if __name__ == "__main__":
    main() 