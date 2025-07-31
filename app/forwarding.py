"""
Forwarding operations module for Channel Adapter API
Handles all REST API forwarding logic
"""
import logging
from typing import Optional, Dict, Any, List
from fastapi import UploadFile

from app.utils import (
    parse_custom_headers,
    create_forwarding_response,
    create_batch_forwarding_response,
    extract_successful_results,
    prepare_batch_results,
    create_tts_forwarding_payload,
    handle_api_error
)

logger = logging.getLogger(__name__)

class ForwardingService:
    """Service class for handling all forwarding operations"""
    
    def __init__(self, voice_to_text_converter, text_to_voice_converter, rest_api_client):
        self.voice_to_text_converter = voice_to_text_converter
        self.text_to_voice_converter = text_to_voice_converter
        self.rest_api_client = rest_api_client
    
    async def forward_voice_to_text(
        self,
        file: UploadFile,
        target_url: str,
        language: str = "en-US",
        include_metadata: bool = True
    ) -> Dict[str, Any]:
        """Convert audio file to text and forward result to external API."""
        try:
            # Convert voice to text
            transcription_result = await self.voice_to_text_converter.transcribe_audio(file, language)
            
            # Forward the result to external API
            forward_result = await self.rest_api_client.forward_transcription_result(
                transcription_result, 
                target_url, 
                include_metadata
            )
            
            return create_forwarding_response(
                transcription_result,
                forward_result,
                "transcription"
            )
            
        except Exception as e:
            raise handle_api_error("voice-to-text forwarding", e)
    
    async def forward_voice_to_text_batch(
        self,
        files: List[UploadFile],
        target_url: str,
        language: str = "en-US",
        include_metadata: bool = True,
        concurrent_limit: int = 3
    ) -> Dict[str, Any]:
        """Convert multiple audio files to text and forward results to external API."""
        try:
            # Convert all audio files to text
            batch_transcription_result = await self.voice_to_text_converter.transcribe_batch(files, language)
            
            # Prepare individual transcription results for forwarding
            transcription_results = prepare_batch_results(batch_transcription_result)
            successful_transcriptions = extract_successful_results(transcription_results)
            
            if successful_transcriptions:
                forward_results = await self.rest_api_client.send_batch_transcriptions(
                    target_url,
                    successful_transcriptions,
                    concurrent_limit=concurrent_limit
                )
            else:
                forward_results = []
            
            return create_batch_forwarding_response(
                batch_transcription_result,
                forward_results,
                "transcription"
            )
            
        except Exception as e:
            raise handle_api_error("batch voice-to-text forwarding", e)
    
    async def forward_existing_transcription(
        self,
        transcription_text: str,
        target_url: str,
        language: str = "en-US",
        source: str = "manual",
        custom_headers: Optional[str] = None
    ) -> Dict[str, Any]:
        """Forward an existing transcription text to external API."""
        try:
            headers = parse_custom_headers(custom_headers)
            
            # Create transcription result format
            from app.utils import create_transcription_result_format
            transcription_result = create_transcription_result_format(
                transcription_text, language, source
            )
            
            # Forward to external API
            forward_result = await self.rest_api_client.forward_transcription_result(
                transcription_result,
                target_url,
                include_metadata=True,
                headers=headers
            )
            
            return create_forwarding_response(
                transcription_result,
                forward_result,
                "transcription"
            )
            
        except Exception as e:
            raise handle_api_error("transcription forwarding", e)
    
    async def forward_text_input(
        self,
        text: str,
        target_url: str,
        source: str = "ui",
        timestamp: Optional[str] = None,
        include_metadata: bool = True,
        custom_headers: Optional[str] = None
    ) -> Dict[str, Any]:
        """Receive text input and forward to external API."""
        try:
            headers = parse_custom_headers(custom_headers)
            
            # Process the text input first
            logger.info(f"Received text from {source}: {text[:100]}...")
            
            from app.utils import create_text_input_result_format
            text_input_result = create_text_input_result_format(text, source, timestamp)
            
            # Forward to external API
            forward_result = await self.rest_api_client.forward_text_input_result(
                text_input_result,
                target_url,
                include_metadata,
                headers
            )
            
            return create_forwarding_response(
                text_input_result,
                forward_result,
                "text_input"
            )
            
        except Exception as e:
            raise handle_api_error("text input forwarding", e)
    
    async def forward_text_to_voice(
        self,
        text: str,
        target_url: str,
        language: str = "en",
        slow: bool = False,
        include_audio_data: bool = False,
        include_metadata: bool = True,
        custom_headers: Optional[str] = None
    ) -> Dict[str, Any]:
        """Convert text to speech and forward result to external API."""
        try:
            headers = parse_custom_headers(custom_headers)
            
            # Convert text to voice (get info, not audio file)
            tts_result = await self.text_to_voice_converter.convert_to_speech_info(text, language, slow)
            
            # If we need audio data, also generate the actual audio file
            if include_audio_data:
                audio_response = await self.text_to_voice_converter.convert_to_speech(text, language, slow)
                if hasattr(audio_response, 'path'):
                    tts_result["file_path"] = audio_response.path
            
            # Forward to external API
            forward_result = await self.rest_api_client.forward_text_to_voice_result(
                tts_result,
                target_url,
                include_audio_data,
                include_metadata,
                headers
            )
            
            return create_forwarding_response(
                tts_result,
                forward_result,
                "text_to_voice"
            )
            
        except Exception as e:
            raise handle_api_error("text-to-voice forwarding", e)
    
    async def forward_text_to_voice_batch(
        self,
        texts: List[str],
        target_url: str,
        language: str = "en",
        slow: bool = False,
        include_audio_data: bool = False,
        include_metadata: bool = True,
        concurrent_limit: int = 3,
        custom_headers: Optional[str] = None
    ) -> Dict[str, Any]:
        """Convert multiple texts to speech and forward results to external API."""
        try:
            headers = parse_custom_headers(custom_headers)
            
            # Convert all texts to speech (batch processing)
            batch_tts_result = await self.text_to_voice_converter.convert_batch_to_speech(texts, language, slow)
            
            # Prepare individual TTS results for forwarding
            tts_results = prepare_batch_results(batch_tts_result)
            successful_conversions = extract_successful_results(tts_results)
            
            if successful_conversions:
                # Create forwarding payloads
                forward_payloads = [
                    create_tts_forwarding_payload(
                        tts_result, language, slow, include_metadata, tts_result.get("index", 0)
                    )
                    for tts_result in successful_conversions
                ]
                
                forward_results = await self.rest_api_client.send_batch_transcriptions(
                    target_url,
                    forward_payloads,
                    headers,
                    concurrent_limit
                )
            else:
                forward_results = []
            
            return create_batch_forwarding_response(
                batch_tts_result,
                forward_results,
                "text_to_voice"
            )
            
        except Exception as e:
            raise handle_api_error("batch text-to-voice forwarding", e)

# Global instance to be used in main.py
forwarding_service = None

def get_forwarding_service(voice_to_text_converter, text_to_voice_converter, rest_api_client):
    """Get or create the global forwarding service instance"""
    global forwarding_service
    if forwarding_service is None:
        forwarding_service = ForwardingService(voice_to_text_converter, text_to_voice_converter, rest_api_client)
    return forwarding_service
