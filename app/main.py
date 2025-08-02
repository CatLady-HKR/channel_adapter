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

# Hardcoded target URL for forwarding
TARGET_URL = "http://host.docker.internal:8003/chat"

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
            "audio data forwarding",
            "session tracking support",
            "voice-to-voice workflow"
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
    language: Optional[str] = "en-US",
    include_metadata: bool = Form(True),
    session_id: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None),
    channel: Optional[str] = Form(None)
):
    """Convert audio file to text and forward result to external API."""
    return await forwarding_service.forward_voice_to_text(
        file, TARGET_URL, language or "en-US", include_metadata, session_id, user_id, channel
    )

@app.post("/voice-to-text-batch-forward/")
async def convert_voice_to_text_batch_and_forward(
    files: List[UploadFile] = File(...),
    language: Optional[str] = "en-US",
    include_metadata: bool = Form(True),
    concurrent_limit: int = Form(3)
):
    """Convert multiple audio files to text and forward results to external API."""
    return await forwarding_service.forward_voice_to_text_batch(
        files, TARGET_URL, language or "en-US", include_metadata, concurrent_limit
    )

@app.post("/forward-transcription/")
async def forward_existing_transcription(
    transcription_text: str = Form(...),
    language: Optional[str] = Form("en-US"),
    source: Optional[str] = Form("manual"),
    custom_headers: Optional[str] = Form(None)
):
    """Forward an existing transcription text to external API."""
    return await forwarding_service.forward_existing_transcription(
        transcription_text, TARGET_URL, language or "en-US", source or "manual", custom_headers
    )

# Text input forwarding endpoints
@app.post("/text-input-forward/")
async def receive_text_from_ui_and_forward(
    text: str = Form(...),
    source: Optional[str] = Form("ui"),
    timestamp: Optional[str] = Form(None),
    include_metadata: bool = Form(True),
    custom_headers: Optional[str] = Form(None),
    session_id: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None),
    channel: Optional[str] = Form(None)
):
    """Receive text input from UI and forward to external API."""
    return await forwarding_service.forward_text_input(
        text, TARGET_URL, source or "ui", timestamp, include_metadata, custom_headers, session_id, user_id, channel
    )

# Text-to-voice forwarding endpoints
@app.post("/text-to-voice-forward/")
async def convert_text_to_voice_and_forward(
    text: str = Form(...),
    language: str = Form("en"),
    slow: bool = Form(False),
    include_audio_data: bool = Form(False),
    include_metadata: bool = Form(True),
    custom_headers: Optional[str] = Form(None)
):
    """Convert text to speech and forward result to external API."""
    return await forwarding_service.forward_text_to_voice(
        text, TARGET_URL, language, slow, include_audio_data, include_metadata, custom_headers
    )

@app.post("/text-to-voice-batch-forward/")
async def convert_text_to_voice_batch_and_forward(
    texts: List[str] = Form(...),
    language: str = Form("en"),
    slow: bool = Form(False),
    include_audio_data: bool = Form(False),
    include_metadata: bool = Form(True),
    concurrent_limit: int = Form(3),
    custom_headers: Optional[str] = Form(None)
):
    """Convert multiple texts to speech and forward results to external API."""
    return await forwarding_service.forward_text_to_voice_batch(
        texts, TARGET_URL, language, slow, include_audio_data, include_metadata, concurrent_limit, custom_headers
    )

# Voice-to-Voice workflow endpoint
@app.post("/voice-to-voice/")
async def voice_to_voice_workflow(
    file: UploadFile = File(...),
    session_id: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None),
    channel: Optional[str] = Form(None),
    language: Optional[str] = "en-US",
    voice_language: str = Form("en"),
    slow: bool = Form(False)
):
    """
    Complete voice-to-voice workflow:
    1. Convert voice file to text
    2. Forward text to external API with session info
    3. Get response and extract text field
    4. Convert response text to voice
    5. Return voice file
    """
    try:
        # Step 1: Convert voice to text
        logger.info(f"Converting voice to text for session {session_id}")
        transcription_result = await voice_to_text_converter.transcribe_audio(file, language or "en-US")
        
        if not transcription_result.get("success", False):
            raise HTTPException(status_code=400, detail="Failed to transcribe audio")
        
        # Add session info to transcription result
        if session_id or user_id or channel:
            transcription_result["session_info"] = {
                "session_id": session_id,
                "user_id": user_id,
                "channel": channel
            }
        
        # Step 2: Forward to external API
        logger.info(f"Forwarding transcription to {TARGET_URL}")
        forward_result = await rest_api_client.forward_transcription_result(
            transcription_result,
            TARGET_URL,
            include_metadata=True
        )
        
        if not forward_result.get("success", False):
            raise HTTPException(status_code=500, detail="Failed to forward transcription to external API")
        
        # Step 3: Extract text from response
        response_data = forward_result.get("response_data", {})
        response_text = None
        
        # Try different common field names for text response
        text_fields = ["text", "response", "message", "reply", "answer", "content", "output"]
        for field in text_fields:
            if field in response_data and response_data[field]:
                response_text = str(response_data[field])
                break
        
        # If no text field found, try to find any string value in the response
        if not response_text:
            for key, value in response_data.items():
                if isinstance(value, str) and len(value.strip()) > 0:
                    response_text = value
                    break
        
        if not response_text:
            raise HTTPException(status_code=500, detail="No text field found in external API response")
        
        logger.info(f"Extracted response text: {response_text[:100]}...")
        
        # Step 4: Convert response text back to voice
        logger.info("Converting response text to voice")
        voice_response = await text_to_voice_converter.convert_to_speech(
            response_text, 
            voice_language, 
            slow
        )
        
        # Step 5: Return the voice file with metadata
        if hasattr(voice_response, 'path'):
            # Return the audio file with additional headers containing workflow info
            return FileResponse(
                voice_response.path,
                media_type="audio/mpeg",
                filename=f"response_{session_id or 'audio'}.mp3",
                headers={
                    "X-Original-Text": transcription_result.get("text", ""),
                    "X-Response-Text": response_text,
                    "X-Session-ID": session_id or "",
                    "X-User-ID": user_id or "",
                    "X-Channel": channel or "",
                    "X-Workflow": "voice-to-voice-complete"
                }
            )
        else:
            return voice_response
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in voice-to-voice workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Voice-to-voice workflow failed: {str(e)}")

# Application lifecycle events
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on application shutdown"""
    logger.info("Shutting down application...")
    await rest_api_client.close()
    logger.info("REST API client closed successfully")


