"""
Main FastAPI application for Voice-Text conversion service
Combines voice-to-text and text-to-voice functionality
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import logging

# Import our custom modules
from app.voice_to_text import voice_to_text_converter
from app.text_to_voice import text_to_voice_converter
from app.rest_api_client import rest_api_client
from app.forwarding import get_forwarding_service
from app.utils import create_text_input_result_format, handle_api_error

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="channel adapter",
    description="A comprehensive FastAPI service for voice-to-text and text-to-voice conversions",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize forwarding service
forwarding_service = get_forwarding_service(voice_to_text_converter, text_to_voice_converter, rest_api_client)

# Root and health endpoints
@app.get("/")
async def root():
    return {
        "message": "channel adapter",
        "version": "2.0.0",
        "status": "running",
        "features": [
            "voice-to-text conversion",
            "text-to-voice synthesis",
            "text input processing",
            "batch processing",
            "multiple audio formats",
            "configurable voice parameters",
            "REST API forwarding",
            "external service integration",
            "text input forwarding",
            "text-to-voice forwarding",
            "audio data forwarding"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "channel-adapter"}

# Text input endpoint
@app.post("/text-input/")
async def receive_text_from_ui(
    text: str = Form(...),
    source: Optional[str] = Form("ui"),
    timestamp: Optional[str] = Form(None)
):
    """Receive text input from UI or other sources."""
    try:
        # Log the received text
        logger.info(f"Received text from {source}: {text[:100]}...")
        
        # Use utility function to create response
        response = create_text_input_result_format(text, source or "ui", timestamp)
        return response
        
    except Exception as e:
        raise handle_api_error("text input processing", e)

# Voice to Text endpoints
@app.post("/voice-to-text/")
async def convert_voice_to_text(
    file: UploadFile = File(...),
    language: Optional[str] = "en-US"
):
    """Convert audio file to text using speech recognition."""
    return await voice_to_text_converter.transcribe_audio(file, language or "en-US")

@app.post("/voice-to-text/batch/")
async def convert_voice_to_text_batch(
    files: List[UploadFile] = File(...),
    language: Optional[str] = "en-US"
):
    """Convert multiple audio files to text."""
    return await voice_to_text_converter.transcribe_batch(files, language or "en-US")

# Text to Voice endpoints
@app.post("/text-to-voice/")                                                        
async def convert_text_to_voice(
    text: str = Form(...),
    language: str = Form("en"),
    slow: bool = Form(False)
):
    """Convert text to speech using Google Text-to-Speech (gTTS)."""
    return await text_to_voice_converter.convert_to_speech(text, language, slow)

@app.post("/text-to-voice/info/")
async def convert_text_to_voice_info(
    text: str = Form(...),
    language: str = Form("en"),
    slow: bool = Form(False)
):
    """Convert text to speech info using Google Text-to-Speech (gTTS) without downloading file."""
    return await text_to_voice_converter.convert_to_speech_info(text, language, slow)

@app.post("/text-to-voice/batch/")
async def convert_text_to_voice_batch(
    texts: List[str] = Form(...),
    language: str = Form("en"),
    slow: bool = Form(False)
):
    """Convert multiple texts to speech using Google Text-to-Speech (gTTS)."""
    return await text_to_voice_converter.convert_batch_to_speech(texts, language, slow)

# REST API forwarding endpoints
@app.post("/voice-to-text-forward/")
async def convert_voice_to_text_and_forward(
    file: UploadFile = File(...),
    target_url: str = Form(...),
    language: Optional[str] = "en-US",
    include_metadata: bool = Form(True)
):
    """Convert audio file to text and forward result to external API."""
    return await forwarding_service.forward_voice_to_text(
        file, target_url, language or "en-US", include_metadata
    )

@app.post("/voice-to-text-batch-forward/")
async def convert_voice_to_text_batch_and_forward(
    files: List[UploadFile] = File(...),
    target_url: str = Form(...),
    language: Optional[str] = "en-US",
    include_metadata: bool = Form(True),
    concurrent_limit: int = Form(3)
):
    """Convert multiple audio files to text and forward results to external API."""
    return await forwarding_service.forward_voice_to_text_batch(
        files, target_url, language or "en-US", include_metadata, concurrent_limit
    )

@app.post("/forward-transcription/")
async def forward_existing_transcription(
    transcription_text: str = Form(...),
    target_url: str = Form(...),
    language: Optional[str] = Form("en-US"),
    source: Optional[str] = Form("manual"),
    custom_headers: Optional[str] = Form(None)
):
    """Forward an existing transcription text to external API."""
    return await forwarding_service.forward_existing_transcription(
        transcription_text, target_url, language or "en-US", source or "manual", custom_headers
    )

# Text input forwarding endpoints
@app.post("/text-input-forward/")
async def receive_text_from_ui_and_forward(
    text: str = Form(...),
    target_url: str = Form(...),
    source: Optional[str] = Form("ui"),
    timestamp: Optional[str] = Form(None),
    include_metadata: bool = Form(True),
    custom_headers: Optional[str] = Form(None)
):
    """Receive text input from UI and forward to external API."""
    return await forwarding_service.forward_text_input(
        text, target_url, source or "ui", timestamp, include_metadata, custom_headers
    )

# Text-to-voice forwarding endpoints
@app.post("/text-to-voice-forward/")
async def convert_text_to_voice_and_forward(
    text: str = Form(...),
    target_url: str = Form(...),
    language: str = Form("en"),
    slow: bool = Form(False),
    include_audio_data: bool = Form(False),
    include_metadata: bool = Form(True),
    custom_headers: Optional[str] = Form(None)
):
    """Convert text to speech and forward result to external API."""
    return await forwarding_service.forward_text_to_voice(
        text, target_url, language, slow, include_audio_data, include_metadata, custom_headers
    )

@app.post("/text-to-voice-batch-forward/")
async def convert_text_to_voice_batch_and_forward(
    texts: List[str] = Form(...),
    target_url: str = Form(...),
    language: str = Form("en"),
    slow: bool = Form(False),
    include_audio_data: bool = Form(False),
    include_metadata: bool = Form(True),
    concurrent_limit: int = Form(3),
    custom_headers: Optional[str] = Form(None)
):
    """Convert multiple texts to speech and forward results to external API."""
    return await forwarding_service.forward_text_to_voice_batch(
        texts, target_url, language, slow, include_audio_data, include_metadata, concurrent_limit, custom_headers
    )

# Application lifecycle events
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on application shutdown"""
    logger.info("Shutting down application...")
    await rest_api_client.close()
    logger.info("REST API client closed successfully")


