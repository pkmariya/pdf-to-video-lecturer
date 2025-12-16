from openai import OpenAI
from config.config import Config
from typing import List
import re

class QAEngine:
    """Simplified Q&A system using OpenAI directly (no LangChain dependencies)"""
    
    def __init__(self):
        Config.validate_config()
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.content = None
        self.chunks = []
    
    def initialize_vectorstore(self, content: str):
        """
        Initialize with PDF content
        
        Args: 
            content: Full text content from PDF
        """
        try: 
            self.content = content
            # Split content into chunks
            self.chunks = self._split_text(content, chunk_size=Config.CHUNK_SIZE, overlap=Config.CHUNK_OVERLAP)
            print(f"✅ Initialized Q&A with {len(self.chunks)} chunks")
            
        except Exception as e:
            raise Exception(f"Error initializing Q&A system: {str(e)}")
    
    def _split_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        # Clean text
        text = re.sub(r'\s+', ' ', text).strip()
        
        words = text.split()
        chunks = []
        
        i = 0
        while i < len(words):
            # Get chunk
            chunk_words = words[i:i + chunk_size]
            chunk = ' '.join(chunk_words)
            chunks.append(chunk)
            
            # Move forward with overlap
            i += chunk_size - overlap
            
            if i >= len(words):
                break
        
        return chunks
    
    def answer_question(self, question: str, chat_history:  list = None) -> str:
        """
        Answer a question based on the PDF content
        
        Args:
            question: User's question
            chat_history: Previous chat history (list of tuples)
            
        Returns:
            Answer to the question
        """
        try: 
            if not self.content:
                raise Exception("Q&A system not initialized. Please process a PDF first.")
            
            # Get relevant context
            context = self._get_relevant_context(question)
            
            # Format chat history
            history_text = ""
            if chat_history and len(chat_history) > 0:
                # Include last 3 exchanges for context
                recent_history = chat_history[-3:] if len(chat_history) > 3 else chat_history
                for q, a in recent_history: 
                    history_text += f"Student: {q}\nAssistant: {a}\n\n"
            
            # Create system prompt
            system_prompt = """You are a helpful and knowledgeable teaching assistant. Your role is to: 
1. Answer questions clearly and accurately based on the lecture content
2. Provide explanations that are easy to understand
3. Use examples when helpful
4. If something isn't covered in the lecture, politely say so
5. Encourage curiosity and deeper learning
6. Be supportive and patient"""
            
            # Create user prompt
            user_prompt = f"""Based on the following lecture content, please answer the student's question. 

Lecture Content:
{context}

{f'Previous Conversation:{history_text}' if history_text else ''}

Student's Question: {question}

Please provide a clear, helpful answer based on the lecture content."""
            
            # Get answer from GPT
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content":  system_prompt},
                    {"role": "user", "content":  user_prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            answer = response.choices[0].message.content
            return answer
            
        except Exception as e: 
            return f"I apologize, but I encountered an error: {str(e)}\n\nPlease try rephrasing your question."
    
    def _get_relevant_context(self, question: str, max_chunks: int = 4) -> str:
        """Get relevant context for the question using keyword matching"""
        if not self.chunks:
            return self.content[: 3000]  # Fallback to first 3000 chars
        
        # Extract keywords from question
        question_lower = question.lower()
        question_words = set(re.findall(r'\b\w+\b', question_lower))
        
        # Remove common stop words
        stop_words = {'what', 'when', 'where', 'who', 'why', 'how', 'is', 'are', 'was', 
                      'were', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                      'to', 'for', 'of', 'with', 'by', 'from', 'about', 'can', 'does', 
                      'do', 'will', 'would', 'should', 'could', 'tell', 'me', 'please'}
        question_words = question_words - stop_words
        
        # Score each chunk based on keyword overlap
        scored_chunks = []
        for chunk in self.chunks:
            chunk_lower = chunk.lower()
            chunk_words = set(re.findall(r'\b\w+\b', chunk_lower))
            
            # Calculate overlap score
            overlap = len(question_words & chunk_words)
            
            # Bonus for exact phrase matches
            bonus = 0
            for word in question_words:
                if len(word) > 3 and word in chunk_lower:
                    bonus += 2
            
            total_score = overlap + bonus
            scored_chunks.append((total_score, chunk))
        
        # Sort by score and get top chunks
        scored_chunks.sort(reverse=True, key=lambda x: x[0])
        
        # Get top chunks
        relevant_chunks = [chunk for score, chunk in scored_chunks[:max_chunks] if score > 0]
        
        # If no relevant chunks found, use first few chunks
        if not relevant_chunks: 
            relevant_chunks = self.chunks[:max_chunks]
        
        # Combine chunks
        context = "\n\n".join(relevant_chunks)
        
        # Limit context length
        max_context_length = 4000
        if len(context) > max_context_length: 
            context = context[:max_context_length] + "..."
        
        return context
    
    def get_relevant_context(self, question: str, k: int = 3) -> list:
        """
        Get relevant context chunks for a question
        
        Args:
            question: User's question
            k: Number of chunks to return
            
        Returns: 
            List of relevant text chunks
        """
        if not self.chunks:
            return []
        
        context = self._get_relevant_context(question, max_chunks=k)
        return [context]