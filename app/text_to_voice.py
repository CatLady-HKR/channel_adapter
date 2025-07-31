"""
Text-to-Voice conversion module using Google Text-to-Speech (gTTS)
Handles text-to-speech conversion with various output options
"""
import tempfile
import os
import logging
from typing import List, Dict, Any
from gtts import gTTS
from fastapi import HTTPException
from fastapi.responses import FileResponse

# Configure logging
logger = logging.getLogger(__name__)


class TextToVoiceConverter:
    """Text-to-Voice converter using Google Text-to-Speech (gTTS)"""
    
    def __init__(self):
        """Initialize the text-to-voice converter"""
        self.tts_engine = "gTTS"
        self.output_format = "mp3"
    
    async def convert_to_speech(
        self, 
        text: str, 
        language: str = "en", 
        slow: bool = False
    ) -> FileResponse:
        """
        Convert text to speech and return as FileResponse
        
        Args:
            text: Text to convert to speech
            language: Language code for gTTS (e.g., 'en', 'es', 'fr')
            slow: Whether to use slow speech
            
        Returns:
            FileResponse with the generated MP3 audio file
        """
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
    
    async def convert_to_speech_info(
        self, 
        text: str, 
        language: str = "en", 
        slow: bool = False
    ) -> Dict[str, Any]:
        """
        Convert text to speech and return info about the conversion without file
        
        Args:
            text: Text to convert to speech
            language: Language code for gTTS
            slow: Whether to use slow speech
            
        Returns:
            Dictionary with conversion information
        """
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
    
    async def convert_batch_to_speech(
        self, 
        texts: List[str], 
        language: str = "en", 
        slow: bool = False
    ) -> Dict[str, Any]:
        """
        Convert multiple texts to speech
        
        Args:
            texts: List of texts to convert to speech
            language: Language code for gTTS
            slow: Whether to use slow speech
            
        Returns:
            Dictionary with batch conversion results
        """
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


# Create a global instance for use in the main application
text_to_voice_converter = TextToVoiceConverter()
