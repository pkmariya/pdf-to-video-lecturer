from gtts import gTTS
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path
from config.config import Config
import tempfile
import textwrap

class VideoGenerator: 
    """Generate teaching videos with TTS and visuals"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def generate_video(
        self,
        script: str,
        title: str,
        style: str = "simple_text",
        tts_service: str = "gtts"
    ) -> str:
        """
        Generate video from script
        
        Args: 
            script: Lecture script text
            title: Video title
            style: Visual style
            tts_service: TTS service to use
            
        Returns:
            Path to generated video file
        """
        try: 
            # Generate audio
            audio_path = self._generate_audio(script, tts_service)
            
            # Generate visuals
            video_clips = self._generate_visuals(script, title, style, audio_path)
            
            # Combine into final video
            video_path = self._create_final_video(video_clips, audio_path, title)
            
            return video_path
            
        except Exception as e:
            raise Exception(f"Error generating video: {str(e)}")
    
    def _generate_audio(self, script: str, tts_service: str) -> str:
        """Generate audio from script using TTS"""
        try: 
            audio_path = Path(self.temp_dir) / "lecture_audio.mp3"
            
            if tts_service == "gtts": 
                tts = gTTS(text=script, lang='en', slow=False)
                tts.save(str(audio_path))
            else:
                # Fallback to gTTS
                tts = gTTS(text=script, lang='en', slow=False)
                tts.save(str(audio_path))
            
            return str(audio_path)
            
        except Exception as e:
            raise Exception(f"Error generating audio:  {str(e)}")
    
    def _generate_visuals(self, script: str, title: str, style: str, audio_path: str) -> list:
        """Generate visual elements for video"""
        try:
            # Get audio duration
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration
            audio_clip.close()
            
            # Split script into segments
            segments = self._split_script_into_segments(script, duration)
            
            clips = []
            
            # Create title slide (3 seconds)
            title_clip = self._create_title_slide(title, 3)
            clips.append(title_clip)
            
            # Create content slides
            remaining_duration = duration - 3
            time_per_segment = remaining_duration / len(segments) if segments else remaining_duration
            
            for segment in segments:
                segment_clip = self._create_content_slide(segment, time_per_segment, style)
                clips.append(segment_clip)
            
            return clips
            
        except Exception as e:
            raise Exception(f"Error generating visuals: {str(e)}")
    
    def _create_title_slide(self, title: str, duration: float) -> VideoClip:
        """Create title slide"""
        # Create image with title
        img = Image.new('RGB', (1920, 1080), color=(25, 25, 112))
        draw = ImageDraw.Draw(img)
        
        # Try to use a nice font, fallback to default
        try: 
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        except:
            font = ImageFont.load_default()
        
        # Wrap title text
        wrapped_title = textwrap.fill(title, width=30)
        
        # Get text bbox and center it
        bbox = draw.textbbox((0, 0), wrapped_title, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((1920 - text_width) / 2, (1080 - text_height) / 2)
        
        draw.text(position, wrapped_title, fill=(255, 255, 255), font=font)
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Create clip
        clip = ImageClip(img_array).set_duration(duration)
        
        return clip
    
    def _create_content_slide(self, text: str, duration: float, style: str) -> VideoClip:
        """Create content slide with text"""
        # Create image
        if style == "simple_text": 
            bg_color = (255, 255, 255)
            text_color = (0, 0, 0)
        elif style == "slides_with_background":
            bg_color = (240, 248, 255)
            text_color = (0, 0, 139)
        else:
            bg_color = (245, 245, 245)
            text_color = (50, 50, 50)
        
        img = Image.new('RGB', (1920, 1080), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Font
        try:
            font = ImageFont. truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans. ttf", 48)
        except:
            font = ImageFont.load_default()
        
        # Wrap text
        wrapped_text = textwrap.fill(text, width=50)
        
        # Draw text
        draw.text((100, 200), wrapped_text, fill=text_color, font=font)
        
        # Convert to numpy array
        img_array = np. array(img)
        
        # Create clip
        clip = ImageClip(img_array).set_duration(duration)
        
        return clip
    
    def _split_script_into_segments(self, script: str, total_duration: float) -> list:
        """Split script into time-appropriate segments"""
        # Split by paragraphs or sentences
        paragraphs = script.split('\n\n')
        
        # If too few paragraphs, split by sentences
        if len(paragraphs) < 3:
            sentences = script.split('. ')
            # Group sentences into segments
            segments = []
            current_segment = ""
            
            for sentence in sentences:
                if len(current_segment.split()) < 50: 
                    current_segment += sentence + ". "
                else:
                    segments.append(current_segment.strip())
                    current_segment = sentence + ". "
            
            if current_segment:
                segments.append(current_segment. strip())
            
            return segments
        
        return paragraphs
    
    def _create_final_video(self, video_clips: list, audio_path: str, title: str) -> str:
        """Combine clips and audio into final video"""
        try:
            # Concatenate video clips
            final_video = concatenate_videoclips(video_clips, method="compose")
            
            # Add audio
            audio = AudioFileClip(audio_path)
            final_video = final_video.set_audio(audio)
            
            # Save video
            output_path = Path(Config.VIDEO_DIR) / f"{title}_lecture.mp4"
            final_video.write_videofile(
                str(output_path),
                fps=24,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=str(Path(self.temp_dir) / 'temp-audio.m4a'),
                remove_temp=True
            )
            
            # Close clips
            final_video.close()
            audio.close()
            
            return str(output_path)
            
        except Exception as e: 
            raise Exception(f"Error creating final video: {str(e)}")