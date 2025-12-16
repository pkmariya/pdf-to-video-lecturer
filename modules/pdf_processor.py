import pdfplumber
import PyPDF2
from pathlib import Path
from typing import Dict, List
import re

class PDFProcessor:
    """Process and extract content from PDF files"""
    
    def __init__(self):
        self.content = None
    
    def extract_content(self, pdf_path: str) -> Dict:
        """
        Extract text content from PDF using multiple methods
        
        Args: 
            pdf_path: Path to PDF file
            
        Returns: 
            Dictionary containing extracted text and metadata
        """
        print(f"📄 Processing PDF: {pdf_path}")
        
        # Try pdfplumber first (better for complex PDFs)
        text_content, page_contents = self._extract_with_pdfplumber(pdf_path)
        
        # If pdfplumber fails, try PyPDF2
        if not text_content or len(text_content. strip()) < 100:
            print("⚠️ pdfplumber extraction yielded little content, trying PyPDF2...")
            text_content, page_contents = self._extract_with_pypdf2(pdf_path)
        
        # Clean text
        full_text = self._clean_text(text_content)
        
        # Get total pages
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf. pages)
        except:
            total_pages = len(page_contents)
        
        # Calculate metadata
        word_count = len(full_text.split())
        char_count = len(full_text)
        
        print(f"✅ Extracted {word_count} words from {total_pages} pages")
        
        if word_count == 0:
            raise Exception("Could not extract text from PDF.  The PDF might be image-based or password-protected.")
        
        return {
            'text': full_text,
            'pages': page_contents,
            'metadata': {
                'total_pages': total_pages,
                'word_count': word_count,
                'char_count': char_count
            }
        }
    
    def _extract_with_pdfplumber(self, pdf_path: str) -> tuple:
        """Extract text using pdfplumber"""
        try:
            text_content = []
            page_contents = []
            
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    # Extract text
                    page_text = page. extract_text()
                    
                    if page_text:
                        text_content.append(page_text)
                        page_contents.append({
                            'page_number': i + 1,
                            'text': page_text
                        })
                    else:
                        # Try extracting with different settings
                        page_text = page.extract_text(
                            x_tolerance=3,
                            y_tolerance=3
                        )
                        if page_text:
                            text_content.append(page_text)
                            page_contents.append({
                                'page_number': i + 1,
                                'text': page_text
                            })
            
            full_text = "\n\n".join(text_content)
            return full_text, page_contents
            
        except Exception as e: 
            print(f"⚠️ pdfplumber error: {str(e)}")
            return "", []
    
    def _extract_with_pypdf2(self, pdf_path: str) -> tuple:
        """Extract text using PyPDF2 as fallback"""
        try: 
            text_content = []
            page_contents = []
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for i, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    
                    if page_text:
                        text_content.append(page_text)
                        page_contents. append({
                            'page_number': i + 1,
                            'text': page_text
                        })
            
            full_text = "\n\n".join(text_content)
            return full_text, page_contents
            
        except Exception as e:
            print(f"⚠️ PyPDF2 error: {str(e)}")
            return "", []
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re. sub(r'[ \t]+', ' ', text)
        
        # Normalize newlines (max 2 consecutive)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove page numbers and headers/footers (common patterns)
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines: 
            line = line.strip()
            # Skip very short lines that are likely page numbers
            if len(line) > 2:
                cleaned_lines.append(line)
        
        text = '\n'.join(cleaned_lines)
        
        # Remove any remaining weird characters
        text = text.encode('ascii', 'ignore').decode('ascii')
        
        # Final cleanup
        text = text.strip()
        
        return text
    
    def extract_sections(self, text: str) -> List[Dict]:
        """
        Extract sections from text based on headings
        
        Args: 
            text: Full text content
            
        Returns: 
            List of sections with titles and content
        """
        sections = []
        
        # Simple section detection based on common patterns
        lines = text.split('\n')
        current_section = {'title': 'Introduction', 'content': ''}
        
        for line in lines: 
            line = line.strip()
            
            # Check if line is a heading (various patterns)
            if self._is_heading(line):
                if current_section['content']. strip():
                    sections.append(current_section)
                current_section = {'title': line, 'content': ''}
            else:
                current_section['content'] += line + ' '
        
        # Add last section
        if current_section['content'].strip():
            sections. append(current_section)
        
        return sections
    
    def _is_heading(self, line: str) -> bool:
        """Determine if a line is likely a heading"""
        if not line:
            return False
        
        # Check various heading patterns
        heading_patterns = [
            r'^[A-Z\s]{3,}$',  # ALL CAPS
            r'^\d+\. ?\s+[A-Z]',  # Numbered headings (1. Introduction)
            r'^[A-Z][a-z]+: $',  # Title Case with colon
            r'^Chapter\s+\d+',  # Chapter headings
            r'^Section\s+\d+',  # Section headings
        ]
        
        for pattern in heading_patterns:
            if re.match(pattern, line):
                return True
        
        # Short lines in title case
        if len(line) < 60 and len(line.split()) <= 8:
            words = line.split()
            if words and words[0][0].isupper():
                # Check if most words are capitalized
                capitalized = sum(1 for word in words if word and word[0].isupper())
                if capitalized / len(words) > 0.5:
                    return True
        
        return False
    
    def get_text_preview(self, text: str, max_chars: int = 500) -> str:
        """Get a preview of the text"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."