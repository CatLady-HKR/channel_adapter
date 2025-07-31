"""
Text to Voice conversion module
Handles text-to-speech synthesis and audio generation
"""
import pyttsx3
import io
import tempfile
import os
import logging
from typing import Dict, Any, Optional
from fastapi import HTTPException
from fastapi.responses import FileResponse
import asyncio
from concurrent.futures import ThreadPoolExecutor
import wave

logger = logging.getLogger(__name__)

# Supported output formats
SUPPORTED_OUTPUT_FORMATS = {'wav', 'mp3'}

# Voice configuration options
VOICE_RATES = {
    'slow': 150,
    'normal': 200,
    'fast': 250,
    'very_fast': 300
}

VOICE_VOLUMES = {
    'quiet': 0.3,
    'normal': 0.7,
    'loud': 1.0
}

class TextToVoiceConverter:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=3)
    
    def _initialize_engine(self, voice_id: Optional[str] = None, rate: str = 'normal', volume: str = 'normal') -> pyttsx3.Engine:
        """Initialize the TTS engine with specified parameters."""
        engine = pyttsx3.init()
        
        # Set rate (speed)
        engine.setProperty('rate', VOICE_RATES.get(rate, 200))
        
        # Set volume
        engine.setProperty('volume', VOICE_VOLUMES.get(volume, 0.7))
        
        # Set voice if specified
        if voice_id:
            voices = engine.getProperty('voices')
            for voice in voices:
                if voice_id in voice.id or voice_id.lower() in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
        
        return engine
    
    def _synthesize_speech(self, text: str, output_path: str, voice_id: Optional[str] = None, 
                          rate: str = 'normal', volume: str = 'normal') -> bool:
        """Synchronous speech synthesis function."""
        try:
            engine = self._initialize_engine(voice_id, rate, volume)
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            return True
        except Exception as e:
            logger.error(f"Error in speech synthesis: {str(e)}")
            return False
    
    async def convert_text_to_speech(self, text: str, voice_id: Optional[str] = None, 
                                   rate: str = 'normal', volume: str = 'normal', 
                                   output_format: str = 'wav') -> Dict[str, Any]:
        """
        Convert text to speech audio file.
        
        Args:
            text: Text to convert to speech
            voice_id: Voice identifier (optional)
            rate: Speech rate (slow, normal, fast, very_fast)
            volume: Speech volume (quiet, normal, loud)
            output_format: Output audio format (wav, mp3)
            
        Returns:
            Dictionary containing conversion results and file path
        """
        if not text or not text.strip():
            raise HTTPException(status_code=400, detail="No text provided")
        
        if len(text) > 5000:
            raise HTTPException(status_code=400, detail="Text too long. Maximum 5000 characters allowed.")
        
        if output_format not in SUPPORTED_OUTPUT_FORMATS:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported output format. Supported formats: {', '.join(SUPPORTED_OUTPUT_FORMATS)}"
            )
        
        if rate not in VOICE_RATES:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid rate. Supported rates: {', '.join(VOICE_RATES.keys())}"
            )
        
        if volume not in VOICE_VOLUMES:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid volume. Supported volumes: {', '.join(VOICE_VOLUMES.keys())}"
            )
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{output_format}') as temp_file:
                temp_path = temp_file.name
            
            # Run speech synthesis in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            success = await loop.run_in_executor(
                self.executor, 
                self._synthesize_speech, 
                text, temp_path, voice_id, rate, volume
            )
            
            if not success:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                raise HTTPException(status_code=500, detail="Failed to generate speech audio")
            
            # Verify file was created and has content
            if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                raise HTTPException(status_code=500, detail="Generated audio file is empty")
            
            logger.info(f"Successfully generated speech audio for text length: {len(text)}")
            
            return {
                "success": True,
                "text": text[:100] + "..." if len(text) > 100 else text,
                "text_length": len(text),
                "voice_id": voice_id,
                "rate": rate,
                "volume": volume,
                "output_format": output_format,
                "file_path": temp_path,
                "file_size": os.path.getsize(temp_path),
                "type": "text_to_voice"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in text-to-speech conversion: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error occurred")
    
    def get_available_voices(self) -> Dict[str, Any]:
        """Get list of available voices on the system."""
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            
            voice_list = []
            for voice in voices:
                voice_info = {
                    "id": voice.id,
                    "name": voice.name,
                    "languages": getattr(voice, 'languages', []),
                    "gender": getattr(voice, 'gender', 'unknown')
                }
                voice_list.append(voice_info)
            
            return {
                "success": True,
                "voices": voice_list,
                "total_voices": len(voice_list),
                "supported_rates": list(VOICE_RATES.keys()),
                "supported_volumes": list(VOICE_VOLUMES.keys()),
                "supported_formats": list(SUPPORTED_OUTPUT_FORMATS)
            }
            
        except Exception as e:
            logger.error(f"Error getting available voices: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "supported_rates": list(VOICE_RATES.keys()),
                "supported_volumes": list(VOICE_VOLUMES.keys()),
                "supported_formats": list(SUPPORTED_OUTPUT_FORMATS)
            }
    
    async def convert_batch_text_to_speech(self, texts: list[str], voice_id: Optional[str] = None,
                                         rate: str = 'normal', volume: str = 'normal',
                                         output_format: str = 'wav') -> Dict[str, Any]:
        """
        Convert multiple texts to speech audio files.
        
        Args:
            texts: List of texts to convert
            voice_id: Voice identifier (optional)
            rate: Speech rate
            volume: Speech volume
            output_format: Output audio format
            
        Returns:
            Dictionary containing batch conversion results
        """
        if not texts:
            raise HTTPException(status_code=400, detail="No texts provided")
        
        if len(texts) > 5:
            raise HTTPException(status_code=400, detail="Maximum 5 texts allowed per batch")
        
        results = []
        
        for i, text in enumerate(texts):
            try:
                result = await self.convert_text_to_speech(text, voice_id, rate, volume, output_format)
                result["index"] = i
                results.append(result)
            except HTTPException as e:
                results.append({
                    "success": False,
                    "index": i,
                    "text": text[:50] + "..." if len(text) > 50 else text,
                    "error": e.detail,
                    "type": "text_to_voice"
                })
            except Exception as e:
                results.append({
                    "success": False,
                    "index": i,
                    "text": text[:50] + "..." if len(text) > 50 else text,
                    "error": "Unexpected error occurred",
                    "type": "text_to_voice"
                })
        
        return {"results": results, "type": "text_to_voice_batch"}

# Global instance
text_to_voice_converter = TextToVoiceConverter()