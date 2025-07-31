# Channel Adapter API

## Description
A comprehensive FastAPI service that provides bidirectional conversion between voice and text, plus text input handling. The service supports **voice-to-text** (speech recognition), **text-to-voice** (speech synthesis), and **text input processing** with advanced configuration options and multiple audio formats.

## Features
- 🎵 **Voice-to-Text Conversion**: Transform audio files into text using advanced speech recognition
- 🗣️ **Text-to-Voice Synthesis**: Convert text into natural-sounding speech using Google Text-to-Speech (gTTS)
- 📝 **Text Input Processing**: Receive and process text input from UI and other sources
- 🌍 **Multi-language Support**: Configurable language recognition and synthesis
- 🎛️ **Voice Customization**: Adjustable speech speed and language selection with gTTS
- 📦 **Batch Processing**: Process multiple files or texts simultaneously
- 🔄 **Multiple Audio Formats**: Support for WAV, MP3, FLAC, M4A, OGG, AAC input; MP3 output via gTTS
- 🐳 **Docker Ready**: Fully containerized application with easy deployment
- 📊 **Modular Architecture**: Separate modules for voice-to-text and text-to-voice functionality
- 🚀 **High Performance**: Async processing with FastAPI
- 📝 **Comprehensive API**: RESTful endpoints with detailed documentation
- 🔧 **Cloud-based TTS**: Reliable Google Text-to-Speech integration with high-quality audio
- 📊 **Health Monitoring**: Built-in health check endpoints

## API Endpoints

### Core Information
- `GET /` - API information and available features
- `GET /health` - Health check endpoint
- `GET /formats/` - Get supported audio formats and languages
- `GET /voices/` - Get available voices for text-to-speech
- `GET /voices/info/` - Get voice configuration options

### Text Input Endpoints
- `POST /text-input/` - Receive text input from UI or other sources

### Voice-to-Text Endpoints
- `POST /voice-to-text/` - Convert single audio file to text
- `POST /voice-to-text/batch/` - Convert multiple audio files to text

### Text-to-Voice Endpoints  
- `POST /text-to-voice/` - Convert text to speech audio file (returns audio file)
- `POST /text-to-voice/info/` - Convert text to speech and return conversion info only
- `POST /text-to-voice/batch/` - Convert multiple texts to speech

### Legacy Endpoints (Backward Compatibility)
- `POST /transcribe/` - Legacy voice-to-text conversion
- `POST /transcribe-batch/` - Legacy batch voice-to-text conversion

### API Documentation
Once the service is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Quick Start

### Using Docker Compose (Recommended)
```bash
# Build and start the service
docker-compose up --build

# The API will be available at http://localhost:8000
```

### Using Docker
```bash
# Build the Docker image
docker build -t channel-adapter .

# Run the container
docker run -p 8000:8000 channel-adapter
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Usage Examples

### Text Input Processing
```bash
# Simple text input from UI
curl -X POST "http://localhost:8000/text-input/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=Hello from the UI&source=web_interface"

# Text input with timestamp
curl -X POST "http://localhost:8000/text-input/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=User message&source=mobile_app&timestamp=2025-07-30T16:27:00Z"
```

### Voice-to-Text Conversion
```bash
# Single file transcription
curl -X POST "http://localhost:8000/voice-to-text/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_audio_file.wav" \
  -F "language=en-US"

# Batch file transcription  
curl -X POST "http://localhost:8000/voice-to-text/batch/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@audio1.wav" \
  -F "files=@audio2.mp3" \
  -F "language=en-US"
```

### Text-to-Voice Conversion
```bash
# Convert text to speech (downloads MP3 file)
curl -X POST "http://localhost:8000/text-to-voice/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=Hello world, this is a test&language=en&slow=false" \
  --output speech.mp3

# Get conversion info without downloading
curl -X POST "http://localhost:8000/text-to-voice/info/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=Hello world&language=en&slow=false"

# Batch text-to-voice conversion
curl -X POST "http://localhost:8000/text-to-voice/batch/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "texts=Hello world&texts=How are you today&language=en&slow=false"

# Get available voices (legacy espeak voices)
curl -X GET "http://localhost:8000/voices/" \
  -H "accept: application/json"
```

### Python Client Examples
```python
import requests

# Text Input Processing
data = {
    'text': 'Hello from Python client',
    'source': 'python_app',
    'timestamp': '2025-07-30T16:27:00Z'
}
response = requests.post('http://localhost:8000/text-input/', data=data)
result = response.json()
print(f"Text processed: {result['success']}, Length: {result['text_length']}")

# Voice-to-Text
with open('audio_file.wav', 'rb') as f:
    files = {'file': f}
    data = {'language': 'en-US'}
    response = requests.post('http://localhost:8000/voice-to-text/', files=files, data=data)
    result = response.json()
    print(f"Transcribed text: {result['text']}")

# Text-to-Voice using gTTS
data = {
    'text': 'Hello, this is a test using Google Text-to-Speech.',
    'language': 'en',
    'slow': False
}
response = requests.post('http://localhost:8000/text-to-voice/', data=data)
with open('output_speech.mp3', 'wb') as f:
    f.write(response.content)
print("Speech audio saved as output_speech.mp3")

# Get text-to-voice info without downloading file
response = requests.post('http://localhost:8000/text-to-voice/info/', data=data)
result = response.json()
print(f"Conversion successful: {result['success']}")
print(f"File size: {result['file_size_bytes']} bytes")
print(f"TTS Engine: {result['tts_engine']}")

# Batch text-to-voice conversion
batch_data = {
    'texts': ['Hello world', 'How are you today?', 'This is batch processing'],
    'language': 'en',
    'slow': False
}
response = requests.post('http://localhost:8000/text-to-voice/batch/', data=batch_data)
result = response.json()
print(f"Batch conversion: {result['successful_conversions']}/{result['total_texts']} successful")

# Get available voices
response = requests.get('http://localhost:8000/voices/')
voices = response.json()
print(f"Available voices: {len(voices.get('voices', []))}")
```

## Supported Languages
The service supports all languages available in:
- **Voice-to-Text**: Google Speech Recognition API
- **Text-to-Voice**: Google Text-to-Speech (gTTS) API

Common languages include:
- `en` - English (gTTS) / `en-US`, `en-GB` - English (Speech Recognition)
- `es` - Spanish (gTTS) / `es-ES` - Spanish (Speech Recognition)
- `fr` - French (gTTS) / `fr-FR` - French (Speech Recognition)
- `de` - German (gTTS) / `de-DE` - German (Speech Recognition)
- `it` - Italian (gTTS) / `it-IT` - Italian (Speech Recognition)
- `pt` - Portuguese (gTTS) / `pt-BR` - Portuguese (Speech Recognition)
- `ja` - Japanese (gTTS) / `ja-JP` - Japanese (Speech Recognition)
- `ko` - Korean (gTTS) / `ko-KR` - Korean (Speech Recognition)
- `zh` - Chinese (gTTS) / `zh-CN` - Chinese (Speech Recognition)
- And many more...

**Note**: gTTS uses simpler language codes (e.g., 'en', 'es'), while Speech Recognition uses locale-specific codes (e.g., 'en-US', 'es-ES').

## Response Format

### Successful Transcription
```json
{
  "success": true,
  "filename": "audio_file.wav",
  "text": "This is the transcribed text from the audio file.",
  "language": "en-US"
}
```

### Error Response
```json
{
  "detail": "Could not understand the audio. Please ensure the audio is clear and contains speech."
}
```

### Batch Response
```json
{
  "results": [
    {
      "success": true,
      "filename": "audio1.wav",
      "text": "First audio transcription",
      "language": "en-US"
    },
    {
      "success": false,
      "filename": "audio2.mp3",
      "error": "Could not understand audio"
    }
  ]
}
```

### Text-to-Voice Info Response (gTTS)
```json
{
  "success": true,
  "message": "Text-to-speech conversion successful",
  "text_length": 54,
  "language": "en",
  "slow": false,
  "file_size_bytes": 17856,
  "tts_engine": "gTTS",
  "output_format": "mp3"
}
```

### Text-to-Voice Batch Response
```json
{
  "success": true,
  "total_texts": 3,
  "successful_conversions": 3,
  "failed_conversions": 0,
  "tts_engine": "gTTS",
  "results": [
    {
      "success": true,
      "index": 0,
      "text": "Hello world",
      "text_length": 11,
      "file_size_bytes": 10854,
      "language": "en",
      "slow": false
    }
  ]
}
```

## Testing
Use the provided test client to test the API:

```bash
# From within the container or local environment
python app/test_client.py
```

Or test manually:
1. Place test audio files in the `test_audio/` directory
2. Use curl commands or the Swagger UI at `http://localhost:8000/docs`

## Configuration

### Environment Variables
- `PYTHONPATH` - Python path for module imports
- `UVICORN_HOST` - Host address (default: 0.0.0.0)
- `UVICORN_PORT` - Port number (default: 8000)

### Audio Quality Tips
For best transcription results:
- Use clear, high-quality audio recordings
- Minimize background noise
- Ensure speech is clearly audible
- Use supported audio formats
- Consider using mono audio at 16kHz sample rate

## Development

### Project Structure
```
voice2text/
├── app/
│   ├── main.py                  # Main FastAPI application (simplified)
│   ├── voice_to_text.py         # Voice-to-text conversion module
│   ├── text2voice.py            # Text-to-voice conversion module
│   ├── test_client.py           # Basic test client
│   └── test_comprehensive.py    # Comprehensive test suite
├── test_audio/                  # Directory for test audio files
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
├── Makefile                     # Development commands
├── requirements.txt             # Python dependencies
└── README.md                   # This file
```

### Adding New Features
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Troubleshooting

### Common Issues
1. **Audio format not supported**: Ensure your audio file is in a supported format (WAV, MP3, FLAC, M4A, OGG, AAC)
2. **Poor transcription quality**: Check audio quality and try adjusting the language parameter
3. **Text-to-voice fails**: Ensure internet connectivity for Google Text-to-Speech (gTTS) API
4. **gTTS language errors**: Use proper gTTS language codes (e.g., 'en', 'es', 'fr' instead of 'en-US')
5. **API errors**: Check logs for detailed error messages
6. **Docker build issues**: Ensure Docker has sufficient resources allocated

### Logs
View application logs:
```bash
# Docker Compose
docker-compose logs -f voice2text-api

# Docker
docker logs <container_id>
```

## Performance Considerations
- For production use, consider implementing rate limiting
- Monitor memory usage with large audio files
- **gTTS requires internet connectivity** for cloud-based text-to-speech conversion
- Consider caching generated audio files to reduce API calls
- Monitor gTTS API usage and quotas for high-volume applications
- Implement proper error handling and retry mechanisms for network-dependent operations

## License
This project is open source and available under the MIT License.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Requirements
- Docker and Docker Compose
- Internet connectivity (required for Google Text-to-Speech API)
- Audio files in supported formats: WAV, MP3, FLAC, M4A, OGG, AAC
- Python 3.11+ (for local development)
