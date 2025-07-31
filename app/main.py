"""
Main FastAPI application for Voice-Text conversion service
Combines voice-to-text and text-to-voice functionality
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import logging
import os
import tempfile
from gtts import gTTS

# Import our custom modules
from app.voice_to_text import voice_to_text_converter
from app.text2voice import text_to_voice_converter

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
            "batch processing",
            "multiple audio formats",
            "configurable voice parameters"
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
        
        # Process the text (you can add your processing logic here)
        response = {
            "success": True,
            "message": "Text received successfully",
            "text_length": len(text),
            "source": source,
            "received_at": timestamp,
            "processed_text": text.strip()
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing text input: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process text: {str(e)}")

# Voice to Text endpoints
@app.post("/voice-to-text/")
async def convert_voice_to_text(
    file: UploadFile = File(...),
    language: Optional[str] = "en-US"
):
    """Convert audio file to text using speech recognition."""
    return await voice_to_text_converter.transcribe_audio(file, language)

@app.post("/voice-to-text/batch/")
async def convert_voice_to_text_batch(
    files: List[UploadFile] = File(...),
    language: Optional[str] = "en-US"
):
    """Convert multiple audio files to text."""
    return await voice_to_text_converter.transcribe_batch(files, language)

# Text to Voice endpoints
@app.post("/text-to-voice/")                                                        
async def convert_text_to_voice(
    text: str = Form(...),
    language: str = Form("en"),
    slow: bool = Form(False)
):
    """Convert text to speech using Google Text-to-Speech (gTTS)."""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_filename = temp_file.name
        
        # Generate speech using gTTS
        tts = gTTS(text=text, lang=language, slow=slow)
        tts.save(temp_filename)
        
        # Check if file was created and has content
        if os.path.exists(temp_filename) and os.path.getsize(temp_filename) > 0:
            filename = f"speech_{hash(text[:50])}.mp3"
            
            return FileResponse(
                path=temp_filename,
                filename=filename,
                media_type="audio/mpeg",
                headers={
                    "X-TTS-Engine": "gTTS",
                    "X-Language": language,
                    "X-Slow": str(slow),
                    "X-Text-Length": str(len(text))
                }
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to generate audio file")
            
    except Exception as e:
        logger.error(f"Error in gTTS conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"gTTS conversion failed: {str(e)}")

@app.post("/text-to-voice/gtts/")
async def convert_text_to_voice_gtts(
    text: str = Form(...),
    language: str = Form("en"),
    slow: bool = Form(False)
):
    """Convert text to speech using Google Text-to-Speech (gTTS)."""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_filename = temp_file.name
        
        # Generate speech using gTTS
        tts = gTTS(text=text, lang=language, slow=slow)
        tts.save(temp_filename)
        
        # Check if file was created and has content
        if os.path.exists(temp_filename) and os.path.getsize(temp_filename) > 0:
            filename = f"gtts_speech_{hash(text[:50])}.mp3"
            
            return FileResponse(
                path=temp_filename,
                filename=filename,
                media_type="audio/mpeg",
                headers={
                    "X-TTS-Engine": "gTTS",
                    "X-Language": language,
                    "X-Slow": str(slow),
                    "X-Text-Length": str(len(text))
                }
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to generate audio file")
            
    except Exception as e:
        logger.error(f"Error in gTTS conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"gTTS conversion failed: {str(e)}")

@app.post("/text-to-voice/info/")
async def convert_text_to_voice_info(
    text: str = Form(...),
    language: str = Form("en"),
    slow: bool = Form(False)
):
    """Convert text to speech info using Google Text-to-Speech (gTTS) without downloading file."""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_filename = temp_file.name
        
        # Generate speech using gTTS
        tts = gTTS(text=text, lang=language, slow=slow)
        tts.save(temp_filename)
        
        # Check if file was created and has content
        if os.path.exists(temp_filename) and os.path.getsize(temp_filename) > 0:
            file_size = os.path.getsize(temp_filename)
            
            # Clean up the temporary file since we're not returning it
            os.unlink(temp_filename)
            
            return {
                "success": True,
                "message": "Text-to-speech conversion successful",
                "text_length": len(text),
                "language": language,
                "slow": slow,
                "file_size_bytes": file_size,
                "tts_engine": "gTTS",
                "output_format": "mp3"
            }
        else:
            # Clean up the temporary file
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
            raise HTTPException(status_code=500, detail="Failed to generate audio file")
            
    except Exception as e:
        logger.error(f"Error in gTTS conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"gTTS conversion failed: {str(e)}")

@app.post("/text-to-voice/batch/")
async def convert_text_to_voice_batch(
    texts: List[str] = Form(...),
    language: str = Form("en"),
    slow: bool = Form(False)
):
    """Convert multiple texts to speech using Google Text-to-Speech (gTTS)."""
    results = []
    
    try:
        for i, text in enumerate(texts):
            try:
                # Create a temporary file for each text
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                    temp_filename = temp_file.name
                
                # Generate speech using gTTS
                tts = gTTS(text=text, lang=language, slow=slow)
                tts.save(temp_filename)
                
                # Check if file was created and has content
                if os.path.exists(temp_filename) and os.path.getsize(temp_filename) > 0:
                    file_size = os.path.getsize(temp_filename)
                    filename = f"batch_speech_{i}_{hash(text[:30])}.mp3"
                    
                    results.append({
                        "success": True,
                        "index": i,
                        "text": text[:100] + "..." if len(text) > 100 else text,
                        "text_length": len(text),
                        "file_path": temp_filename,
                        "filename": filename,
                        "file_size_bytes": file_size,
                        "language": language,
                        "slow": slow
                    })
                else:
                    # Clean up failed file
                    if os.path.exists(temp_filename):
                        os.unlink(temp_filename)
                    results.append({
                        "success": False,
                        "index": i,
                        "text": text[:100] + "..." if len(text) > 100 else text,
                        "error": "Failed to generate audio file"
                    })
                    
            except Exception as e:
                results.append({
                    "success": False,
                    "index": i,
                    "text": text[:100] + "..." if len(text) > 100 else text,
                    "error": str(e)
                })
        
        successful_results = [r for r in results if r["success"]]
        failed_results = [r for r in results if not r["success"]]
        
        return {
            "success": True,
            "total_texts": len(texts),
            "successful_conversions": len(successful_results),
            "failed_conversions": len(failed_results),
            "tts_engine": "gTTS",
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error in batch gTTS conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch gTTS conversion failed: {str(e)}")

# Voice information endpoints
@app.get("/voices/")
async def get_available_voices():
    """Get list of available voices on the system."""
    return text_to_voice_converter.get_available_voices()

@app.get("/voices/info/")
async def get_voice_info():
    """Get information about voice configuration options."""
    return {
        "supported_rates": ["slow", "normal", "fast", "very_fast"],
        "supported_volumes": ["quiet", "normal", "loud"],
        "supported_formats": ["wav", "mp3"],
        "max_text_length": 5000,
        "max_batch_size": {
            "voice_to_text": 10,
            "text_to_voice": 5
        }
    }

# Utility endpoints
@app.get("/formats/")
async def get_supported_formats():
    """Get supported audio formats for input and output."""
    return {
        "input_formats": [".wav", ".mp3", ".flac", ".m4a", ".ogg", ".aac"],
        "output_formats": ["wav", "mp3"],
        "languages": [
            {"code": "en-US", "name": "English (US)"},
            {"code": "en-GB", "name": "English (UK)"},
            {"code": "es-ES", "name": "Spanish (Spain)"},
            {"code": "fr-FR", "name": "French (France)"},
            {"code": "de-DE", "name": "German (Germany)"},
            {"code": "it-IT", "name": "Italian (Italy)"},
            {"code": "pt-BR", "name": "Portuguese (Brazil)"},
            {"code": "ja-JP", "name": "Japanese"},
            {"code": "ko-KR", "name": "Korean"},
            {"code": "zh-CN", "name": "Chinese (Simplified)"}
        ]
    }

# Legacy endpoints for backward compatibility
@app.post("/transcribe/")
async def legacy_transcribe(
    file: UploadFile = File(...),
    language: Optional[str] = "en-US"
):
    """Legacy endpoint for voice-to-text conversion (backward compatibility)."""
    return await voice_to_text_converter.transcribe_audio(file, language)

@app.post("/transcribe-batch/")
async def legacy_transcribe_batch(
    files: List[UploadFile] = File(...),
    language: Optional[str] = "en-US"
):
    """Legacy endpoint for batch voice-to-text conversion (backward compatibility)."""
    return await voice_to_text_converter.transcribe_batch(files, language)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
