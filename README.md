# Channel Adapt- 🔗 **REST API Forwarding**: Automatically forward transcription results to external APIs
- 📝 **Text Input Forwarding**: Forward UI text inputs to external services
- 🎵 **Audio Result Forwarding**: Forward text-to-voice results with optional audio data
- 🌐 **External Service Integration**: Connect with webhooks and third-party services
- ⚡ **Concurrent Processing**: Parallel API calls for batch operations
- 📦 **Batch Forwarding**: Process and forward multiple items concurrently
# Channel Adapter API

## Description
A comprehensive FastAPI service that provides bidirectional conversion between voice and text, plus text input handling with REST API forwarding capabilities. The service supports **voice-to-text** (speech recognition), **text-to-voice** (speech synthesis), **text input processing**, and **external service integration** with advanced configuration options and multiple audio formats.

## 🚀 Current Version: 2.0.0
**Complete Integration Hub with Modular Architecture** - The Channel Adapter now serves as a full-featured integration hub with:
- ✅ **13 REST API Endpoints** covering all conversion and forwarding scenarios including voice-to-voice workflow
- ✅ **Modular Architecture** with dedicated modules for voice processing and external integrations  
- ✅ **Enhanced REST API Client** with session tracking, batch processing, and concurrent request handling
- ✅ **Session Tracking System** with session_id, user_id, and channel support across all forwarding endpoints
- ✅ **Voice-to-Voice Workflow** complete conversational pipeline with external API integration
- ✅ **Comprehensive Forwarding System** for all processing types with metadata enrichment
- ✅ **Base64 Audio Encoding** for including audio data in API forwarding
- ✅ **Concurrent Processing** with configurable limits for batch operations
- ✅ **Custom Headers Support** for external API integration flexibility

## 🏗️ **Architecture Improvements (v2.0.0)**
**50% Code Reduction & Enhanced Maintainability:**
- **Simplified main.py**: Reduced from 400+ lines to ~228 lines (50% reduction)
- **Modular Design**: Separated concerns into dedicated modules (utils.py, forwarding.py)
- **Reusable Components**: Common functions centralized for better code reuse
- **Standardized Patterns**: Consistent error handling and response formatting
- **Better Testability**: Isolated modules are easier to unit test and maintain
- **Developer Experience**: Much cleaner codebase that's easier to understand and extend

## Features
- 🎵 **Voice-to-Text Conversion**: Transform audio files into text using advanced speech recognition
- 🗣️ **Text-to-Voice Synthesis**: Convert text into natural-sounding speech using Google Text-to-Speech (gTTS)
- 📝 **Text Input Processing**: Receive and process text input from UI and other sources
- 🌍 **Multi-language Support**: Configurable language recognition and synthesis
- 🎛️ **Voice Customization**: Adjustable speech speed and language selection with gTTS
- 📦 **Batch Processing**: Process multiple files or texts simultaneously
- 🔄 **Multiple Audio Formats**: Support for WAV, MP3, FLAC, M4A, OGG, AAC input; MP3 output via gTTS
- 🐳 **Docker Ready**: Fully containerized application with easy deployment
- 📊 **Modular Architecture**: Separated voice-to-text and text-to-voice modules for better maintainability
- 🔗 **REST API Forwarding**: Automatically forward transcription results to external APIs
- 📝 **Text Input Forwarding**: Forward UI text inputs to external services  
- 🎵 **Audio Result Forwarding**: Forward text-to-voice results with optional audio data
- 🌐 **External Service Integration**: Connect with webhooks and third-party services
- ⚡ **Concurrent Processing**: Parallel API calls for batch operations
- 📦 **Batch Forwarding**: Process and forward multiple items concurrently
- 🔄 **Base64 Audio Encoding**: Include audio data in forwarded payloads
- 👥 **Session Tracking**: Complete session management with session_id, user_id, and channel support
- 🔄 **Voice-to-Voice Workflow**: Complete conversational pipeline with external API integration
- 🚀 **High Performance**: Async processing with FastAPI
- 📝 **Clean API Design**: Focused RESTful endpoints with clear documentation
- 🔧 **Cloud-based TTS**: Reliable Google Text-to-Speech integration with high-quality audio
- 📊 **Health Monitoring**: Built-in health check endpoints

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
- 📊 **Modular Architecture**: Separated voice-to-text and text-to-voice modules for better maintainability
- � **REST API Forwarding**: Automatically forward transcription results to external APIs
- 🌐 **External Service Integration**: Connect with webhooks and third-party services
- ⚡ **Concurrent Processing**: Parallel API calls for batch operations
- �🚀 **High Performance**: Async processing with FastAPI
- 📝 **Clean API Design**: Focused RESTful endpoints with clear documentation
- 🔧 **Cloud-based TTS**: Reliable Google Text-to-Speech integration with high-quality audio
- 📊 **Health Monitoring**: Built-in health check endpoints

## API Endpoints

### Core Information
- `GET /` - API information and available features
- `GET /health` - Health check endpoint

### Text Input Processing
- `POST /text-input/` - Receive text input from UI or other sources

### Voice-to-Text Conversion
- `POST /voice-to-text/` - Convert single audio file to text
- `POST /voice-to-text/batch/` - Convert multiple audio files to text

### Text-to-Voice Conversion  
- `POST /text-to-voice/` - Convert text to speech audio file (returns audio file)
- `POST /text-to-voice/info/` - Convert text to speech and return conversion info only
- `POST /text-to-voice/batch/` - Convert multiple texts to speech

### Voice-to-Voice Workflow
- `POST /voice-to-voice/` - Complete voice-to-voice workflow with external API integration

### REST API Forwarding
- `POST /voice-to-text-forward/` - Convert audio to text and forward result to external API (supports session tracking)
- `POST /voice-to-text-batch-forward/` - Convert multiple audio files and forward results to external API  
- `POST /forward-transcription/` - Forward existing transcription text to external API
- `POST /text-input-forward/` - Receive text input and forward to external API (supports session tracking)
- `POST /text-to-voice-forward/` - Convert text to speech and forward result to external API
- `POST /text-to-voice-batch-forward/` - Convert multiple texts to speech and forward results to external API

#### 🔍 **Session Tracking Parameters**
The following endpoints support session tracking with optional parameters:
- **`session_id`**: Unique identifier for the conversation/session
- **`user_id`**: Identifier for the user making the request  
- **`channel`**: Source channel (e.g., "web_app", "mobile", "api", "bot")

**Supported Endpoints:**
- `POST /voice-to-text-forward/` - Session info included in transcription result
- `POST /text-input-forward/` - Session info included in text input result

**Session Info Format:**
```json
{
  "session_info": {
    "session_id": "session_123",
    "user_id": "user_456", 
    "channel": "web_app"
  }
}
```

#### 🎙️ **Voice-to-Voice Workflow**
The `/voice-to-voice/` endpoint provides a complete conversational workflow:

**Process Flow:**
1. **Voice Input** → Receives audio file with session tracking
2. **Speech-to-Text** → Converts audio to text using Google Speech Recognition
3. **API Forward** → Sends transcription + session info to `localhost:8003`
4. **Response Processing** → Extracts text from external API response
5. **Text-to-Speech** → Converts response text to audio using gTTS
6. **Voice Output** → Returns MP3 audio file with workflow metadata

**Parameters:**
- `file` (required): Audio file (WAV, MP3, FLAC, M4A, OGG, AAC)
- `session_id` (optional): Conversation session identifier
- `user_id` (optional): User identifier  
- `channel` (optional): Source channel (e.g., "voice_chat", "phone")
- `language` (optional): Speech recognition language (default: "en-US")
- `voice_language` (optional): TTS language (default: "en")
- `slow` (optional): Slow speech flag for TTS (default: false)

**Response Headers:**
- `X-Original-Text`: The transcribed input text
- `X-Response-Text`: The extracted response text
- `X-Session-ID`: Session identifier
- `X-User-ID`: User identifier
- `X-Channel`: Channel identifier
- `X-Workflow`: "voice-to-voice-complete"

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
```

### Voice-to-Voice Workflow
```bash
# Complete voice-to-voice conversation workflow
curl -X POST "http://localhost:8000/voice-to-voice/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@input_audio.wav" \
  -F "session_id=conv_123" \
  -F "user_id=user_456" \
  -F "channel=voice_chat" \
  -F "language=en-US" \
  -F "voice_language=en" \
  -F "slow=false" \
  --output response_audio.mp3

# The response will be an MP3 file with headers containing workflow info
# Headers: X-Original-Text, X-Response-Text, X-Session-ID, etc.
```

### REST API Forwarding
```bash
# Convert audio to text and forward to external API
curl -X POST "http://localhost:8000/voice-to-text-forward/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audio.wav" \
  -F "target_url=https://your-api.com/webhook" \
  -F "language=en-US" \
  -F "include_metadata=true" \
  -F "session_id=session_123" \
  -F "user_id=user_456" \
  -F "channel=web_app"

# Forward existing transcription text
curl -X POST "http://localhost:8000/forward-transcription/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "transcription_text=Hello world&target_url=https://your-api.com/webhook&language=en-US"

# Batch audio conversion with forwarding
curl -X POST "http://localhost:8000/voice-to-text-batch-forward/" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@audio1.wav" \
  -F "files=@audio2.mp3" \
  -F "target_url=https://your-api.com/webhook" \
  -F "language=en-US" \
  -F "concurrent_limit=3"

# Forward text input to external API
curl -X POST "http://localhost:8000/text-input-forward/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=Hello from UI&target_url=https://your-api.com/webhook&source=web_interface&session_id=session_123&user_id=user_456&channel=web_app"

# Convert text to voice and forward result
curl -X POST "http://localhost:8000/text-to-voice-forward/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=Hello world&target_url=https://your-api.com/webhook&language=en&include_audio_data=true"

# Batch text-to-voice with forwarding
curl -X POST "http://localhost:8000/text-to-voice-batch-forward/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "texts=Hello world&texts=How are you&target_url=https://your-api.com/webhook&language=en"
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

# REST API Forwarding Examples
# Convert audio to text and forward to external API
with open('audio_file.wav', 'rb') as f:
    files = {'file': f}
    data = {
        'target_url': 'https://your-api.com/webhook',
        'language': 'en-US',
        'include_metadata': True,
        'session_id': 'session_123',
        'user_id': 'user_456',
        'channel': 'python_client'
    }
    response = requests.post('http://localhost:8000/voice-to-text-forward/', files=files, data=data)
    result = response.json()
    print(f"Transcription: {result['transcription']['text']}")
    print(f"Forward success: {result['forward_result']['success']}")
    print(f"Session info: {result['transcription'].get('session_info', {})}")

# Forward existing transcription
data = {
    'transcription_text': 'This is existing transcription text',
    'target_url': 'https://your-api.com/webhook',
    'language': 'en-US',
    'source': 'manual'
}
response = requests.post('http://localhost:8000/forward-transcription/', data=data)
result = response.json()
print(f"Forward success: {result['success']}")

# Batch audio conversion with forwarding
files = [
    ('files', open('audio1.wav', 'rb')),
    ('files', open('audio2.wav', 'rb'))
]
data = {
    'target_url': 'https://your-api.com/webhook',
    'language': 'en-US',
    'concurrent_limit': 3
}
response = requests.post('http://localhost:8000/voice-to-text-batch-forward/', files=files, data=data)
result = response.json()
print(f"Successful forwards: {result['successful_forwards']}/{result['total_transcriptions']}")

# Text input forwarding
data = {
    'text': 'Hello from Python client',
    'target_url': 'https://your-api.com/webhook',
    'source': 'python_app',
    'include_metadata': True,
    'session_id': 'session_123',
    'user_id': 'user_456',
    'channel': 'python_client'
}
response = requests.post('http://localhost:8000/text-input-forward/', data=data)
result = response.json()
print(f"Text input forward success: {result['success']}")
print(f"Session info: {result['text_input'].get('session_info', {})}")

# Text-to-voice forwarding
data = {
    'text': 'Hello, this is a test message',
    'target_url': 'https://your-api.com/webhook',
    'language': 'en',
    'include_audio_data': True,  # Include base64 encoded audio
    'include_metadata': True
}
response = requests.post('http://localhost:8000/text-to-voice-forward/', data=data)
result = response.json()
print(f"TTS forward success: {result['success']}")
print(f"Generated audio size: {result['text_to_voice']['file_size_bytes']} bytes")

# Batch text-to-voice forwarding
data = {
    'texts': ['Hello world', 'How are you?', 'Goodbye'],
    'target_url': 'https://your-api.com/webhook',
    'language': 'en',
    'include_metadata': True,
    'concurrent_limit': 2
}
response = requests.post('http://localhost:8000/text-to-voice-batch-forward/', data=data)
result = response.json()
print(f"Batch TTS forwards: {result['successful_forwards']}/{result['total_conversions']}")

# Voice-to-Voice Workflow Example
with open('input_audio.wav', 'rb') as f:
    files = {'file': f}
    data = {
        'session_id': 'conv_123',
        'user_id': 'user_456', 
        'channel': 'python_client',
        'language': 'en-US',
        'voice_language': 'en',
        'slow': False
    }
    response = requests.post('http://localhost:8000/voice-to-voice/', files=files, data=data)
    
    # Save the response audio
    with open('response_audio.mp3', 'wb') as audio_file:
        audio_file.write(response.content)
    
    # Access workflow metadata from headers
    print(f"Original text: {response.headers.get('X-Original-Text', '')}")
    print(f"Response text: {response.headers.get('X-Response-Text', '')}")
    print(f"Session ID: {response.headers.get('X-Session-ID', '')}")
    print(f"Workflow: {response.headers.get('X-Workflow', '')}")
    print("Voice response saved as response_audio.mp3")
```

## Supported Languages & Formats

### Audio Input Formats
Supported formats: WAV, MP3, FLAC, M4A, OGG, AAC

### Languages
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

### Project Structure (v2.0.0 - Modular Architecture)
```
channel_adapter/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Simplified FastAPI app (~228 lines, 12 endpoints)
│   ├── utils.py                 # Common utility functions & helpers
│   ├── forwarding.py            # Dedicated forwarding service module
│   ├── voice_to_text.py         # Voice-to-text conversion module
│   ├── text_to_voice.py         # Text-to-voice conversion module (gTTS)
│   ├── rest_api_client.py       # Enhanced REST API client with session tracking and batch processing
│   ├── test_client.py           # Basic test client (if exists)
│   └── test_comprehensive.py    # Comprehensive test suite (if exists)
├── test_audio/                  # Directory for test audio files
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
├── requirements.txt             # Python dependencies
└── README.md                   # This file
```

### 🎯 **Modular Architecture Benefits (v2.0.0)**
- **Clean Separation of Concerns**: Each module has a specific responsibility
- **50% Code Reduction**: main.py simplified from 400+ to ~228 lines
- **Reusable Components**: Common functions centralized in utils.py
- **Dedicated Forwarding Service**: All forwarding logic isolated in forwarding.py
- **Standardized Error Handling**: Consistent error patterns across all endpoints
- **Easy Maintenance**: Modular design makes updates and testing much simpler

### 📦 **Module Responsibilities**
- **`main.py`**: FastAPI app configuration and simplified endpoint definitions
- **`utils.py`**: Common utilities (header parsing, response formatting, error handling)
- **`forwarding.py`**: ForwardingService class with all REST API forwarding logic
- **`voice_to_text.py`**: Voice-to-text conversion using Google Speech Recognition
- **`text_to_voice.py`**: Text-to-voice synthesis using Google Text-to-Speech (gTTS)
- **`rest_api_client.py`**: Enhanced HTTP client for external API integrations with session tracking and batch processing

### Adding New Features
The modular architecture makes extending the Channel Adapter much simpler:

#### 🔧 **Adding New Endpoints:**
1. **Simple Endpoints**: Add directly to `main.py` using existing converters
2. **Forwarding Endpoints**: Add new methods to `ForwardingService` in `forwarding.py`
3. **Utility Functions**: Add common helpers to `utils.py` for reuse across endpoints

#### 📝 **Code Quality Standards:**
- **Single Responsibility**: Each module handles one specific concern
- **DRY Principle**: Common logic is centralized in utility functions  
- **Error Handling**: Use `handle_api_error()` for consistent error responses
- **Response Formatting**: Use utility functions for standardized responses
- **Type Safety**: Proper type hints and Optional handling throughout

#### 🌐 **REST API Client Enhancements (v2.0.0)**

The `rest_api_client.py` module has been significantly enhanced with advanced features:

**🔧 Core Features:**
- **Session Management**: Persistent aiohttp sessions with automatic session handling
- **Advanced Error Handling**: Comprehensive exception handling with detailed error responses
- **Batch Processing**: Concurrent request processing with configurable limits
- **Custom Headers**: Full support for custom HTTP headers in API calls
- **Multiple HTTP Methods**: Support for POST, PUT, PATCH operations

**📊 Key Methods:**
- `send_transcription()`: Core method for sending data to external APIs
- `send_batch_transcriptions()`: Concurrent processing of multiple requests with semaphore control
- `forward_transcription_result()`: Enhanced with session tracking (session_id, user_id, channel)
- `forward_text_input_result()`: New method for forwarding text input with session metadata
- `forward_text_to_voice_result()`: Forward TTS results with optional base64 audio data inclusion

**⚡ Performance Features:**
- **Connection Pooling**: Reusable aiohttp sessions for improved performance
- **Concurrent Limits**: Configurable semaphore control for batch operations (default: 5 concurrent requests)
- **Timeout Management**: Configurable request timeouts (default: 30 seconds)
- **Session Persistence**: Automatic session lifecycle management

**🔒 Session Tracking Integration:**
All forwarding methods now support comprehensive session tracking:
```python
# Session tracking in transcription forwarding
await rest_api_client.forward_transcription_result(
    transcription_result,
    target_url,
    session_id="conv_123",
    user_id="user_456", 
    channel="web_app",
    include_metadata=True
)

# Session tracking in text input forwarding  
await rest_api_client.forward_text_input_result(
    text_input_result,
    target_url,
    session_id="conv_123",
    user_id="user_456",
    channel="mobile_app",
    include_metadata=True
)
```

**📦 Payload Structure:**
Enhanced payloads now include session information and comprehensive metadata:
```json
{
  "text": "transcribed content",
  "session_id": "conv_123",
  "user_id": "user_456", 
  "channel": "web_app",
  "source": "channel-adapter",
  "timestamp": "2025-08-02T10:30:00Z",
  "metadata": {
    "service": "channel-adapter",
    "version": "2.0.0",
    "conversion_engine": "google-speech-recognition",
    "audio_format": "wav",
    "language": "en-US"
  }
}
```

#### 🧪 **Development Workflow:**
1. Fork the repository
2. Create a feature branch
3. Make changes using the modular patterns:
   - Add utilities to `utils.py` if needed
   - Extend `ForwardingService` for new forwarding features
   - Keep `main.py` endpoints simple and focused
4. Test thoroughly using the modular test structure
5. Submit a pull request

#### 📊 **Before/After Code Comparison:**

**Before (v1.x - Monolithic):**
```python
@app.post("/voice-to-text-forward/")  # 50+ lines each
async def convert_voice_to_text_and_forward(...):
    try:
        # Header parsing logic (repeated 6+ times)
        headers = None
        if custom_headers:
            try:
                headers = dict(item.split(":") for item in custom_headers.split(","))
                # ... more parsing logic
            except Exception:
                logger.warning("Failed to parse...")
        
        # Conversion logic
        transcription_result = await voice_to_text_converter.transcribe_audio(...)
        
        # Forwarding logic
        forward_result = await rest_api_client.forward_transcription_result(...)
        
        # Response formatting (inconsistent patterns)
        return {
            "transcription": transcription_result,
            "forward_result": forward_result,
            "success": forward_result.get("success", False)
        }
    except Exception as e:
        logger.error(f"Error in voice-to-text forwarding: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Voice-to-text forwarding failed: {str(e)}")
```

**After (v2.0 - Modular):**
```python
@app.post("/voice-to-text-forward/")  # 3 lines each
async def convert_voice_to_text_and_forward(...):
    return await forwarding_service.forward_voice_to_text(
        file, target_url, language or "en-US", include_metadata
    )
```

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
docker-compose logs -f channel-adapter-api

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

### 🏎️ **v2.0 Performance Benefits:**
- **Reduced Memory Footprint**: Modular architecture loads only necessary components
- **Better Error Isolation**: Module-specific error handling prevents cascading failures
- **Improved Maintainability**: Faster debugging and updates with isolated concerns
- **Enhanced Testability**: Unit testing individual modules improves reliability
- **Code Reusability**: Shared utilities reduce redundant code execution

## 📈 **Technical Achievements (v2.0.0)**

### Code Quality Improvements
- **50% Code Reduction**: main.py simplified from 400+ to 228 lines
- **Eliminated Code Duplication**: Header parsing, error handling, and response formatting centralized
- **Consistent Patterns**: Standardized approach across all 13 endpoints
- **Type Safety**: Proper Optional type handling and parameter validation
- **Enhanced REST Client**: Comprehensive session tracking and batch processing capabilities

### Architecture Enhancements  
- **Separation of Concerns**: Clear module boundaries with single responsibilities
- **Dependency Injection**: ForwardingService pattern for better testability
- **Utility Functions**: Reusable components in utils.py reduce redundancy
- **Error Handling**: Centralized error management with consistent responses
- **Session Management**: Persistent HTTP sessions with lifecycle management

### Integration Capabilities
- **Session Tracking**: Complete session lifecycle management across all forwarding operations
- **Concurrent Processing**: Configurable semaphore control for batch operations
- **Voice-to-Voice Workflow**: End-to-end conversational pipeline with external API integration
- **Advanced Payloads**: Rich metadata inclusion with session information and processing details
- **Connection Pooling**: Optimized HTTP client with persistent session reuse

### Developer Experience
- **Easier Maintenance**: Modular structure makes updates simpler and safer
- **Better Testing**: Isolated modules can be unit tested independently  
- **Clear Documentation**: Each module has well-defined purpose and interface
- **Extensibility**: Adding new features follows established patterns

### Runtime Benefits
- **Memory Efficiency**: Shared utilities reduce memory footprint
- **Error Resilience**: Module isolation prevents cascading failures
- **Performance**: Reduced code paths and optimized common operations
- **Debugging**: Clear module boundaries make issue isolation faster

## License
This project is open source and available under the MIT License.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Requirements
- Docker and Docker Compose
- Internet connectivity (required for Google Text-to-Speech API)
- Audio files in supported formats: WAV, MP3, FLAC, M4A, OGG, AAC
- Python 3.11+ (for local development)
