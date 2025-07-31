"""
Voice to Text conversion module
Handles audio file processing and speech recognition
"""
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os
import logging
from typing import Dict, Any, Optional
from fastapi import UploadFile, HTTPException

logger = logging.getLogger(__name__)

# Supported audio formats
SUPPORTED_AUDIO_FORMATS = {'.wav', '.mp3', '.flac', '.m4a', '.ogg', '.aac'}

class VoiceToTextConverter:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def convert_to_wav(self, input_path: str, output_path: str) -> bool:
        """Convert audio file to WAV format for speech recognition."""
        try:
            audio = AudioSegment.from_file(input_path)
            # Convert to mono and set sample rate to 16kHz for better recognition
            audio = audio.set_channels(1).set_frame_rate(16000)
            audio.export(output_path, format="wav")
            return True
        except Exception as e:
            logger.error(f"Error converting audio: {str(e)}")
            return False
    
    async def transcribe_audio(self, file: UploadFile, language: str = "en-US") -> Dict[str, Any]:
        """
        Transcribe audio file to text.
        
        Args:
            file: Uploaded audio file
            language: Language code for recognition (default: en-US)
            
        Returns:
            Dictionary containing transcription results
        """
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in SUPPORTED_AUDIO_FORMATS:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file format. Supported formats: {', '.join(SUPPORTED_AUDIO_FORMATS)}"
            )
        
        try:
            # Create temporary files
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_input:
                # Write uploaded file to temporary file
                content = await file.read()
                temp_input.write(content)
                temp_input.flush()
                
                # Convert to WAV if necessary
                if file_extension != '.wav':
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_wav:
                        if not self.convert_to_wav(temp_input.name, temp_wav.name):
                            raise HTTPException(status_code=500, detail="Failed to convert audio file")
                        audio_file_path = temp_wav.name
                else:
                    audio_file_path = temp_input.name
                
                # Perform speech recognition
                with sr.AudioFile(audio_file_path) as source:
                    # Adjust for ambient noise
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.record(source)
                    
                    try:
                        # Use Google Speech Recognition
                        text = self.recognizer.recognize_google(audio, language=language)
                        logger.info(f"Successfully transcribed audio file: {file.filename}")
                        return {
                            "success": True,
                            "filename": file.filename,
                            "text": text,
                            "language": language,
                            "type": "voice_to_text"
                        }
                        
                    except sr.UnknownValueError:
                        logger.warning(f"Could not understand audio in file: {file.filename}")
                        raise HTTPException(
                            status_code=400, 
                            detail="Could not understand the audio. Please ensure the audio is clear and contains speech."
                        )
                        
                    except sr.RequestError as e:
                        logger.error(f"Speech recognition service error: {str(e)}")
                        raise HTTPException(
                            status_code=503, 
                            detail=f"Speech recognition service unavailable: {str(e)}"
                        )
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error processing file {file.filename}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error occurred")
        
        finally:
            # Clean up temporary files
            try:
                if 'temp_input' in locals():
                    os.unlink(temp_input.name)
                if 'temp_wav' in locals() and file_extension != '.wav':
                    os.unlink(temp_wav.name)
            except Exception as e:
                logger.warning(f"Failed to clean up temporary files: {str(e)}")
    
    async def transcribe_batch(self, files: list[UploadFile], language: str = "en-US") -> Dict[str, Any]:
        """
        Transcribe multiple audio files to text.
        
        Args:
            files: List of uploaded audio files
            language: Language code for recognition
            
        Returns:
            Dictionary containing batch transcription results
        """
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")
        
        if len(files) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 files allowed per batch")
        
        results = []
        
        for file in files:
            try:
                # Process each file individually
                result = await self.transcribe_audio(file, language)
                results.append(result)
            except HTTPException as e:
                results.append({
                    "success": False,
                    "filename": file.filename,
                    "error": e.detail,
                    "type": "voice_to_text"
                })
            except Exception as e:
                results.append({
                    "success": False,
                    "filename": file.filename,
                    "error": "Unexpected error occurred",
                    "type": "voice_to_text"
                })
        
        return {"results": results, "type": "voice_to_text_batch"}

# Global instance
voice_to_text_converter = VoiceToTextConverter()
