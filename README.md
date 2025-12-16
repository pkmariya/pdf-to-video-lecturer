# 🎓 PDF to Teaching Video Lecturer

Transform your PDF documents into engaging video lectures with AI-powered narration and interactive Q&A capabilities.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 📄 **PDF Processing**: Extract and structure content from any PDF document
- 🎓 **AI-Powered Script Generation**: Convert PDF content into natural, lecturer-style narration using GPT-4
- 🎥 **Automatic Video Creation**: Generate teaching videos with synchronized text-to-speech and visuals
- 💬 **Interactive Q&A**:  Ask questions about the lecture content and get AI-powered answers
- 🎨 **Customizable Options**: Choose voice settings, speaking pace, and video styles
- 📱 **User-Friendly Interface**: Clean, intuitive Streamlit UI

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- FFmpeg (for video processing)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/pkmariya/pdf-to-video-lecturer.git
cd pdf-to-video-lecturer
```

2. **Install dependencies**
```bash
pip install -r requirements. txt
```

3. **Install FFmpeg**

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

4. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key: 
```env
OPENAI_API_KEY=your_actual_api_key_here
```

5. **Create data directories**
```bash
mkdir -p data/uploads data/videos data/vectordb
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 Usage Guide

### Step 1: Upload PDF
1. Click the "Browse files" button in the sidebar
2. Select a PDF file (max 50MB)
3. Click "Process PDF" to extract content

### Step 2: Generate Video
1. Review the extracted content preview
2. Click "Generate Lecture Script" to create AI narration
3. Review the generated script (optional)
4. Click "Generate Video" to create the teaching video
5. Wait for processing (may take several minutes)

### Step 3: Watch & Learn
1. Navigate to the "Watch & Learn" tab
2. Play the generated video
3. View the synchronized transcript
4. Download video or transcript if needed

### Step 4: Ask Questions
1. Go to the "Ask Questions" tab
2. Type your question in the chat input
3. Get AI-powered answers based on the lecture content
4. Continue the conversation with follow-up questions

## 🎨 Customization Options

### Voice Settings
- **TTS Service**: Choose between gTTS (free), Azure TTS, or ElevenLabs
- **Speaking Pace**: Adjust to Slow, Normal, or Fast

### Video Settings
- **Simple Text**: Clean text on white background
- **Slides with Background**: Colored background with styled text
- **Animated Text**: Enhanced visual presentation

## 🏗️ Project Structure

```
pdf-to-video-lecturer/
├── app.py                      # Main Streamlit application
├── requirements. txt            # Python dependencies
├── README.md                   # This file
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── config/
│   └── config.py              # Configuration management
├── modules/
│   ├── __init__.py
│   ├── pdf_processor.py       # PDF extraction
│   ├── script_generator.py    # AI script generation
│   ├── video_generator.py     # Video creation
│   ├── qa_engine.py          # Q&A system
│   └── utils.py              # Helper functions
├── assets/
│   ├── styles.css            # Custom styling
│   └── templates/
│       └── prompts.py        # AI prompt templates
└── data/
    ├── uploads/              # Uploaded PDFs
    ├── videos/               # Generated videos
    └── vectordb/             # Vector database storage
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | - | Yes |
| `OPENAI_MODEL` | GPT model to use | gpt-4 | No |
| `TTS_SERVICE` | Text-to-speech service | gtts | No |
| `MAX_PDF_SIZE_MB` | Maximum PDF size | 50 | No |
| `CHUNK_SIZE` | Text chunk size for embeddings | 1000 | No |
| `CHUNK_OVERLAP` | Overlap between chunks | 200 | No |

### Advanced TTS Options

**Azure TTS** (Optional):
```env
AZURE_TTS_KEY=your_azure_key
AZURE_TTS_REGION=eastus
```

**ElevenLabs** (Optional):
```env
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=default_voice_id
```

## 📊 Technical Details

### Technologies Used

- **Frontend**: Streamlit
- **AI/ML**: 
  - OpenAI GPT-4 for script generation and Q&A
  - LangChain for RAG implementation
  - ChromaDB for vector storage
- **PDF Processing**: pdfplumber
- **Video Generation**: MoviePy
- **Text-to-Speech**: gTTS (default), Azure TTS, ElevenLabs

### How It Works

1. **PDF Processing**:  Extracts text using pdfplumber, preserving structure
2. **Script Generation**: GPT-4 transforms content into engaging lecture narration
3. **TTS Conversion**: Converts script to natural speech audio
4. **Video Creation**: MoviePy combines audio with visual slides
5. **Q&A System**: Uses RAG (Retrieval Augmented Generation) to answer questions based on PDF content

## 🔍 Troubleshooting

### Common Issues

**"OPENAI_API_KEY is required"**
- Make sure you've created a `.env` file and added your API key

**"Error generating video"**
- Ensure FFmpeg is installed and accessible in your PATH
- Check that you have enough disk space

**"PDF processing failed"**
- Verify the PDF is not corrupted or password-protected
- Try a different PDF to isolate the issue

**Video generation is slow**
- Large PDFs take longer to process
- Consider using a faster TTS service like Azure or ElevenLabs

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Streamlit for the amazing web framework
- MoviePy for video processing capabilities
- LangChain for RAG implementation

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ by [pkmariya](https://github.com/pkmariya)**