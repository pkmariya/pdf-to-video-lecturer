#!/usr/bin/env python3
"""Test PDF extraction"""

from modules.pdf_processor import PDFProcessor
import sys

def test_pdf(pdf_path):
    print(f"\n{'='*60}")
    print(f"Testing PDF: {pdf_path}")
    print(f"{'='*60}\n")
    
    try:
        processor = PDFProcessor()
        content = processor.extract_content(pdf_path)
        
        print(f"✅ SUCCESS!")
        print(f"📄 Total Pages: {content['metadata']['total_pages']}")
        print(f"📝 Word Count: {content['metadata']['word_count']}")
        print(f"🔤 Character Count: {content['metadata']['char_count']}")
        print(f"\n📖 Content Preview (first 500 chars):")
        print("-" * 60)
        print(content['text'][:500])
        print("-" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__": 
    if len(sys.argv) < 2:
        print("Usage: python test_pdf_extraction.py <path_to_pdf>")
        sys.exit(1)
    
    pdf_path = sys. argv[1]
    test_pdf(pdf_path)