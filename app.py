import streamlit as st
import os
from pathlib import Path
from modules.pdf_processor import PDFProcessor
from modules.script_generator import ScriptGenerator
from modules.video_generator import VideoGenerator
from modules.qa_engine import QAEngine
from modules.utils import setup_directories, clean_old_files
from config.config import Config
import time

# Page configuration
st.set_page_config(
    page_title="PDF to Teaching Video Lecturer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_file = Path("assets/styles.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f. read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize session state
if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False
if 'video_generated' not in st.session_state:
    st.session_state.video_generated = False
if 'pdf_content' not in st.session_state:
    st.session_state.pdf_content = None
if 'video_path' not in st.session_state:
    st.session_state.video_path = None
if 'script' not in st.session_state:
    st.session_state. script = None
if 'qa_engine' not in st.session_state:
    st.session_state.qa_engine = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Setup directories
setup_directories()

# Header
st.title("🎓 PDF to Teaching Video Lecturer")
st.markdown("Transform your PDF documents into engaging video lectures with AI-powered narration and interactive Q&A")

# Sidebar
with st.sidebar:
    st.header("📤 Upload PDF")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help=f"Maximum file size: {Config.MAX_PDF_SIZE_MB}MB"
    )
    
    st.divider()
    
    st.header("⚙️ Settings")
    
    # Voice settings
    st.subheader("Voice Options")
    tts_service = st.selectbox(
        "TTS Service",
        ["gTTS (Free)", "Azure TTS", "ElevenLabs"],
        help="Select text-to-speech service"
    )
    
    speaking_pace = st.select_slider(
        "Speaking Pace",
        options=["Slow", "Normal", "Fast"],
        value="Normal"
    )
    
    # Video settings
    st.subheader("Video Options")
    video_style = st.selectbox(
        "Video Style",
        ["Simple Text", "Slides with Background", "Animated Text"],
        help="Visual style for the generated video"
    )
    
    st.divider()
    
    # Status
    st.header("📊 Status")
    if st.session_state.pdf_processed:
        st.success("✅ PDF Processed")
    if st.session_state.video_generated:
        st.success("✅ Video Generated")
    
    st.divider()
    
    # Reset button
    if st.button("🔄 Reset All", use_container_width=True):
        st.session_state.pdf_processed = False
        st. session_state.video_generated = False
        st.session_state.pdf_content = None
        st. session_state.video_path = None
        st.session_state.script = None
        st. session_state.qa_engine = None
        st.session_state.chat_history = []
        clean_old_files()
        st.rerun()

# Main content tabs
tab1, tab2, tab3 = st.tabs(["📄 Generate Video", "🎥 Watch & Learn", "💬 Ask Questions"])

# Tab 1: Generate Video
with tab1:
    st.header("Generate Teaching Video from PDF")
    
    if uploaded_file is not None:
        # Display PDF info
        col1, col2 = st. columns([2, 1])
        
        with col1:
            st. info(f"📁 **File:** {uploaded_file.name}")
            st.info(f"📊 **Size:** {uploaded_file.size / 1024:.2f} KB")
        
        # with col2:
        #     if st.button("🔍 Process PDF", use_container_width=True, type="primary"):
        #         try:
        #             with st.spinner("Processing PDF..."):
        #                 # Save uploaded file
        #                 pdf_path = Path(Config.UPLOAD_DIR) / uploaded_file.name
        #                 with open(pdf_path, "wb") as f:
        #                     f.write(uploaded_file. getbuffer())
                        
        #                 # Process PDF
        #                 processor = PDFProcessor()
        #                 pdf_content = processor.extract_content(str(pdf_path))
                        
        #                 st.session_state.pdf_content = pdf_content
        #                 st.session_state.pdf_processed = True
                        
        #                 st.success("✅ PDF processed successfully!")
        #                 st.rerun()
                        
        #         except Exception as e: 
        #             st.error(f"❌ Error processing PDF: {str(e)}")
        
        # In app.py, find the "Process PDF" button section and replace with: 

        with col2:
            if st.button("🔍 Process PDF", use_container_width=True, type="primary"):
                try:
                    with st.spinner("Processing PDF..."):
                        # Save uploaded file
                        pdf_path = Path(Config.UPLOAD_DIR) / uploaded_file.name
                        with open(pdf_path, "wb") as f:
                            f.write(uploaded_file. getbuffer())
                        
                        st.info(f"📁 Saved to: {pdf_path}")
                        
                        # Process PDF
                        processor = PDFProcessor()
                        pdf_content = processor.extract_content(str(pdf_path))
                        
                        # Validate content
                        if not pdf_content['text'] or pdf_content['metadata']['word_count'] == 0:
                            st.error("❌ No text could be extracted from this PDF. The PDF might be:")
                            st.error("- Image-based (scanned document without OCR)")
                            st.error("- Password protected")
                            st.error("- Corrupted or in an unsupported format")
                            st.info("💡 Try converting the PDF to a text-based format first.")
                        else:
                            st.session_state.pdf_content = pdf_content
                            st.session_state.pdf_processed = True
                            
                            st.success(f"✅ PDF processed successfully!  Extracted {pdf_content['metadata']['word_count']} words.")
                            st.rerun()
                        
                except Exception as e:
                    st.error(f"❌ Error processing PDF: {str(e)}")
                    import traceback
                    with st.expander("Show error details"):
                        st.code(traceback.format_exc())
        
        # Show PDF preview if processed
        if st.session_state.pdf_processed and st.session_state.pdf_content:
            st.divider()
            st.subheader("📖 PDF Content Preview")
            
            with st.expander("View Extracted Content", expanded=False):
                content = st.session_state.pdf_content
                st.markdown(f"**Total Pages:** {content['metadata']['total_pages']}")
                st.markdown(f"**Word Count:** {content['metadata']['word_count']}")
                st. text_area(
                    "Content Preview",
                    content['text'][:2000] + "..." if len(content['text']) > 2000 else content['text'],
                    height=300
                )
            
            st.divider()
            
            # Generate script
            if not st.session_state.video_generated:
                if st.button("✨ Generate Lecture Script", use_container_width=True, type="primary"):
                    try:
                        with st.spinner("Generating lecturer-style script with AI..."):
                            script_gen = ScriptGenerator()
                            script = script_gen.generate_script(
                                st.session_state.pdf_content['text'],
                                style="engaging",
                                pace=speaking_pace. lower()
                            )
                            
                            st.session_state. script = script
                            st. success("✅ Script generated successfully!")
                            st.rerun()
                            
                    except Exception as e:
                        st. error(f"❌ Error generating script: {str(e)}")
            
            # Show script if generated
            if st.session_state.script:
                st. subheader("📝 Generated Lecture Script")
                with st.expander("View Script", expanded=True):
                    st.text_area("Script", st.session_state. script, height=400)
                
                st.divider()
                
                # Generate video
                if not st.session_state.video_generated:
                    if st. button("🎬 Generate Video", use_container_width=True, type="primary"):
                        try:
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            status_text.text("🎤 Converting script to speech...")
                            progress_bar.progress(25)
                            
                            video_gen = VideoGenerator()
                            
                            status_text.text("🎥 Creating video with visuals...")
                            progress_bar.progress(50)
                            
                            video_path = video_gen.generate_video(
                                script=st.session_state.script,
                                title=uploaded_file.name. replace('.pdf', ''),
                                style=video_style. lower().replace(' ', '_'),
                                tts_service=tts_service.split()[0]. lower()
                            )
                            
                            status_text.text("🎨 Adding final touches...")
                            progress_bar.progress(75)
                            
                            st.session_state.video_path = video_path
                            st.session_state.video_generated = True
                            
                            progress_bar.progress(100)
                            status_text.text("✅ Video generated successfully!")
                            
                            time.sleep(1)
                            st.rerun()
                            
                        except Exception as e: 
                            st.error(f"❌ Error generating video: {str(e)}")
    else:
        st.info("👆 Please upload a PDF file from the sidebar to get started")

# Tab 2: Watch & Learn
with tab2:
    st.header("Watch Your Generated Lecture")
    
    if st.session_state.video_generated and st.session_state.video_path:
        col1, col2 = st. columns([2, 1])
        
        with col1:
            st.subheader("🎥 Video Player")
            if os.path.exists(st.session_state.video_path):
                video_file = open(st.session_state.video_path, 'rb')
                video_bytes = video_file.read()
                st.video(video_bytes)
                
                # Download button
                st.download_button(
                    label="⬇️ Download Video",
                    data=video_bytes,
                    file_name=f"lecture_{uploaded_file.name.replace('.pdf', '')}.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )
            else:
                st.error("Video file not found!")
        
        with col2:
            st. subheader("📄 Transcript")
            if st.session_state.script:
                st. text_area(
                    "Lecture Transcript",
                    st.session_state.script,
                    height=500
                )
                
                # Download transcript
                st.download_button(
                    label="⬇️ Download Transcript",
                    data=st.session_state.script,
                    file_name=f"transcript_{uploaded_file.name.replace('.pdf', '')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    else:
        st.info("📹 No video generated yet. Please go to the 'Generate Video' tab to create your lecture video.")

# Tab 3: Ask Questions
with tab3:
    st.header("Interactive Q&A about Your Lecture")
    
    if st.session_state.pdf_processed and st.session_state.pdf_content:
        # Initialize QA engine if not already done
        if st.session_state.qa_engine is None:
            with st.spinner("Initializing Q&A system..."):
                try:
                    qa_engine = QAEngine()
                    qa_engine.initialize_vectorstore(st.session_state.pdf_content['text'])
                    st.session_state.qa_engine = qa_engine
                    st.success("✅ Q&A system ready!")
                except Exception as e:
                    st.error(f"❌ Error initializing Q&A: {str(e)}")
        
        if st.session_state.qa_engine:
            # Chat interface
            st.subheader("💬 Ask me anything about the lecture content")
            
            # Display chat history
            chat_container = st.container()
            with chat_container:
                for i, (question, answer) in enumerate(st.session_state.chat_history):
                    with st.chat_message("user"):
                        st.write(question)
                    with st.chat_message("assistant"):
                        st.write(answer)
            
            # Input for new question
            user_question = st.chat_input("Type your question here...")
            
            if user_question:
                try:
                    # Display user question
                    with st. chat_message("user"):
                        st.write(user_question)
                    
                    # Generate answer
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            answer = st.session_state.qa_engine.answer_question(
                                user_question,
                                st. session_state.chat_history
                            )
                            st.write(answer)
                    
                    # Update chat history
                    st.session_state. chat_history.append((user_question, answer))
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            
            # Clear chat history button
            if st.session_state.chat_history:
                if st.button("🗑️ Clear Chat History"):
                    st.session_state.chat_history = []
                    st.rerun()
    else:
        st.info("📚 Please process a PDF first to enable the Q&A system.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🎓 PDF to Teaching Video Lecturer | Powered by AI</p>
    <p style='font-size: 0.8em;'>Transform your documents into engaging learning experiences</p>
</div>
""", unsafe_allow_html=True)