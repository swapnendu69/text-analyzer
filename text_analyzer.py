# Text Analyzer Project - Local Version
# Supports: .txt, .docx, .pdf files

import re
import string
from collections import Counter
import os
import sys

try:
    import PyPDF2
except ImportError:
    print("Installing PyPDF2...")
    os.system("pip install PyPDF2")
    import PyPDF2

try:
    import docx
except ImportError:
    print("Installing python-docx...")
    os.system("pip install python-docx")
    import docx

def read_txt_file(file_path):
    """Read text from .txt file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()

def read_docx_file(file_path):
    """Read text from .docx file"""
    doc = docx.Document(file_path)
    text = []
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)
    return '\n'.join(text)

def read_pdf_file(file_path):
    """Read text from .pdf file"""
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def read_doc_file(file_path):
    """Read text from .doc file"""
    try:
        # Try using antiword if available on system
        import subprocess
        result = subprocess.run(['antiword', file_path], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return "Unable to read .doc file. Please install antiword or convert to .docx format."
    except:
        return "Unable to read .doc file. antiword not available. Please convert to .docx format."

def clean_text(text):
    """Clean and preprocess text for analysis"""
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove numbers and extra whitespace
    text = re.sub(r'\d+', '', text)
    text = ' '.join(text.split())
    return text

def analyze_text(text):
    """Analyze text and return statistics"""
    if not text or text.startswith("Unable to read") or text.startswith("Error"):
        return {
            'lines': 0,
            'words': 0,
            'characters': 0,
            'top_5_words': [],
            'error': text
        }
    
    # Basic statistics
    lines = [line for line in text.split('\n') if line.strip()]
    words = text.split()
    characters = len(text.replace('\n', '').replace('\r', '').replace(' ', ''))
    
    # Clean text for word frequency analysis
    cleaned_text = clean_text(text)
    word_list = [word for word in cleaned_text.split() if len(word) > 1]
    
    # Word frequency
    word_freq = Counter(word_list)
    top_5_words = word_freq.most_common(5)
    
    return {
        'lines': len(lines),
        'words': len(words),
        'characters': characters,
        'top_5_words': top_5_words,
        'error': None
    }

def process_file(file_path):
    """Process file based on its extension"""
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    
    file_extension = file_path.lower().split('.')[-1]
    
    print(f"Processing {file_extension.upper()} file...")
    
    if file_extension == 'txt':
        return read_txt_file(file_path)
    elif file_extension == 'docx':
        return read_docx_file(file_path)
    elif file_extension == 'pdf':
        return read_pdf_file(file_path)
    elif file_extension == 'doc':
        return read_doc_file(file_path)
    else:
        return f"Unsupported file format: {file_extension}"

def display_results(stats, filename):
    """Display analysis results in a formatted way"""
    print("=" * 60)
    print(f"📊 TEXT ANALYSIS REPORT: {filename}")
    print("=" * 60)
    
    if stats['error']:
        print(f"❌ Error: {stats['error']}")
        print("=" * 60)
        return
    
    print(f"📈 Basic Statistics:")
    print(f"   • Number of lines: {stats['lines']:,}")
    print(f"   • Number of words: {stats['words']:,}")
    print(f"   • Number of characters: {stats['characters']:,}")
    
    if stats['top_5_words']:
        print(f"\n🏆 Top 5 Most Frequent Words:")
        for i, (word, count) in enumerate(stats['top_5_words'], 1):
            print(f"   {i}. '{word}' - {count} occurrence(s)")
    else:
        print(f"\nℹ️  No words found for frequency analysis")
    
    print("=" * 60)

def get_file_path():
    """Get file path from user input"""
    while True:
        file_path = input("Enter the path to your file: ").strip()
        if os.path.exists(file_path):
            return file_path
        else:
            print("❌ File not found. Please enter a valid file path.")

def manual_text_input():
    """Get text input manually from user"""
    print("\nEnter your text (press Enter twice to finish):")
    lines = []
    while True:
        try:
            line = input()
            if line == '' and lines and lines[-1] == '':
                break
            lines.append(line)
        except EOFError:
            break
    
    return '\n'.join(lines[:-1]) if len(lines) > 1 else '\n'.join(lines)

def main():
    """Main function to run the text analyzer"""
    print("🎯 TEXT ANALYZER PROJECT")
    print("=" * 40)
    print("Supported formats: .txt, .docx, .pdf")
    print(".doc files have limited support (requires antiword)")
    print("=" * 40)
    
    print("\nChoose an option:")
    print("1. 📁 Analyze a file from path")
    print("2. ⌨️  Enter text manually")
    
    choice = input("\nEnter your choice (1-2): ").strip()
    
    if choice == '1':
        file_path = get_file_path()
        text = process_file(file_path)
        stats = analyze_text(text)
        display_results(stats, os.path.basename(file_path))
        
    elif choice == '2':
        text = manual_text_input()
        stats = analyze_text(text)
        display_results(stats, "Manual Input")
        
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
