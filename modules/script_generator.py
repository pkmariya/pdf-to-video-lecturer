from openai import OpenAI
from config. config import Config
from assets.templates.prompts import LECTURER_PROMPT, SCRIPT_REFINEMENT_PROMPT
import re

class ScriptGenerator:
    """Generate lecturer-style scripts from PDF content using AI"""
    
    def __init__(self):
        Config.validate_config()
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
    
    def generate_script(self, content: str, style: str = "engaging", pace: str = "normal") -> str:
        """
        Generate lecture script from content
        
        Args:
            content: PDF text content
            style: Lecture style (engaging, formal, casual)
            pace: Speaking pace (slow, normal, fast)
            
        Returns:
            Generated lecture script (clean, without markers)
        """
        try:
            # Limit content length for API
            max_content_length = 12000
            if len(content) > max_content_length: 
                print(f"⚠️ Content too long ({len(content)} chars), truncating to {max_content_length}")
                content = content[:max_content_length] + "..."
            
            # Prepare the prompt
            prompt = LECTURER_PROMPT.format(
                content=content,
                style=style,
                pace=pace
            )
            
            print("🤖 Generating lecture script with AI...")
            
            # Generate script
            response = self.client. chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert educator who creates natural, engaging video lecture scripts.  You write clean spoken text without any stage directions or markers."
                    },
                    {"role": "user", "content":  prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            script = response.choices[0].message.content
            
            # Clean the script to remove any markers that might have slipped through
            script = self._clean_script(script)
            
            # Refine script for better delivery
            script = self._refine_script(script, pace)
            
            print(f"✅ Generated script:  {len(script)} characters, ~{len(script. split())} words")
            
            return script
            
        except Exception as e:
            raise Exception(f"Error generating script: {str(e)}")
    
    def _clean_script(self, script: str) -> str:
        """Remove any markers, annotations, or stage directions from script"""
        # Remove common markers and annotations
        markers_to_remove = [
            r'\[START\]',
            r'\[END\]',
            r'\[PAUSE\]',
            r'\[pause\]',
            r'\[INTRO\]',
            r'\[CONCLUSION\]',
            r'\[.*?\]',  # Any text in square brackets
            r'\(pause\)',
            r'\(PAUSE\)',
            r'\*pause\*',
            r'\*PAUSE\*',
        ]
        
        for pattern in markers_to_remove: 
            script = re.sub(pattern, '', script, flags=re.IGNORECASE)
        
        # Clean up multiple spaces
        script = re.sub(r'\s+', ' ', script)
        
        # Clean up multiple newlines (keep max 2)
        script = re.sub(r'\n{3,}', '\n\n', script)
        
        # Remove leading/trailing whitespace
        script = script.strip()
        
        return script
    
    def _refine_script(self, script: str, pace: str) -> str:
        """Refine and optimize the generated script"""
        try:
            refinement_prompt = SCRIPT_REFINEMENT_PROMPT.format(
                script=script,
                pace=pace
            )
            
            print("✨ Refining script for optimal delivery...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content":  "You are an expert at refining lecture scripts. You output only clean, natural spoken text without any annotations or stage directions."
                    },
                    {"role": "user", "content": refinement_prompt}
                ],
                temperature=0.5,
                max_tokens=3000
            )
            
            refined_script = response.choices[0].message.content
            
            # Clean again to be absolutely sure
            refined_script = self._clean_script(refined_script)
            
            return refined_script
            
        except Exception as e:
            print(f"⚠️ Refinement failed: {str(e)}, using original script")
            # If refinement fails, return cleaned original script
            return script
    
    def chunk_script(self, script: str, max_chunk_length: int = 500) -> list:
        """
        Split script into chunks for processing
        
        Args:
            script: Full lecture script
            max_chunk_length: Maximum words per chunk
            
        Returns:
            List of script chunks
        """
        sentences = script.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk. split()) + len(sentence.split()) <= max_chunk_length: 
                current_chunk += sentence + ".  "
            else:
                if current_chunk: 
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks