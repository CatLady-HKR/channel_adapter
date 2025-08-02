"""
REST API client module for forwarding voice-to-text outputs
Handles HTTP requests to external services with transcribed text
"""
import logging
import asyncio
from typing import Dict, Any, Optional, List
import aiohttp
from aiohttp import ClientSession, ClientTimeout, ClientError
import json

# Configure logging
logger = logging.getLogger(__name__)


class RestApiClient:
    """REST API client for forwarding voice-to-text results"""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the REST API client
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = ClientTimeout(total=timeout)
        self.session: Optional[ClientSession] = None
    
    async def _get_session(self) -> ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = ClientSession(timeout=self.timeout)
        return self.session
    
    async def close(self):
        """Close the aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def send_transcription(
        self,
        url: str,
        transcription_data: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
        method: str = "POST"
    ) -> Dict[str, Any]:
        """
        Send transcription data to external REST API
        
        Args:
            url: Target API endpoint URL
            transcription_data: Voice-to-text conversion result
            headers: Optional HTTP headers
            method: HTTP method (POST, PUT, PATCH)
            
        Returns:
            Response data from the external API
        """
        try:
            session = await self._get_session()
            
            # Default headers
            default_headers = {
                "Content-Type": "application/json",
                "User-Agent": "channel-adapter/2.0.0"
            }
            
            # Merge with provided headers
            if headers:
                default_headers.update(headers)
            
            logger.info(f"Sending transcription to {url}")
            logger.debug(f"Payload: {json.dumps(transcription_data, indent=2)}")
            
            async with session.request(
                method.upper(),
                url,
                json=transcription_data,
                headers=default_headers
            ) as response:
                
                response_text = await response.text()
                logger.info(f"API response status: {response.status}")
                
                # Try to parse JSON response
                try:
                    response_data = await response.json()
                except json.JSONDecodeError:
                    response_data = {"raw_response": response_text}
                
                result = {
                    "success": response.status < 400,
                    "status_code": response.status,
                    "response_data": response_data,
                    "url": url,
                    "method": method.upper()
                }
                
                if response.status >= 400:
                    logger.error(f"API call failed: {response.status} - {response_text}")
                    result["error"] = f"HTTP {response.status}: {response_text}"
                else:
                    logger.info("Transcription sent successfully")
                
                return result
                
        except ClientError as e:
            logger.error(f"Client error sending transcription: {str(e)}")
            return {
                "success": False,
                "error": f"Client error: {str(e)}",
                "url": url,
                "method": method.upper()
            }
        except Exception as e:
            logger.error(f"Unexpected error sending transcription: {str(e)}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "url": url,
                "method": method.upper()
            }
    
    async def send_batch_transcriptions(
        self,
        url: str,
        batch_data: List[Dict[str, Any]],
        headers: Optional[Dict[str, str]] = None,
        concurrent_limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Send multiple transcriptions concurrently
        
        Args:
            url: Target API endpoint URL
            batch_data: List of transcription results
            headers: Optional HTTP headers
            concurrent_limit: Maximum concurrent requests
            
        Returns:
            List of response results
        """
        semaphore = asyncio.Semaphore(concurrent_limit)
        
        async def send_single(data: Dict[str, Any]) -> Dict[str, Any]:
            async with semaphore:
                return await self.send_transcription(url, data, headers)
        
        logger.info(f"Sending {len(batch_data)} transcriptions to {url}")
        
        try:
            results = await asyncio.gather(
                *[send_single(data) for data in batch_data],
                return_exceptions=True
            )
            
            # Handle any exceptions in results
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    processed_results.append({
                        "success": False,
                        "error": f"Exception: {str(result)}",
                        "index": i,
                        "url": url
                    })
                else:
                    result["index"] = i
                    processed_results.append(result)
            
            successful = len([r for r in processed_results if r.get("success", False)])
            logger.info(f"Batch sending completed: {successful}/{len(batch_data)} successful")
            
            return processed_results
            
        except Exception as e:
            logger.error(f"Batch sending failed: {str(e)}")
            return [{
                "success": False,
                "error": f"Batch operation failed: {str(e)}",
                "url": url
            }]
    
    async def forward_transcription_result(
        self,
        transcription_result: Dict[str, Any],
        target_url: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        channel: Optional[str] = None,
        include_metadata: bool = True,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Forward a voice-to-text result to external API with optional metadata
        
        Args:
            transcription_result: Result from voice_to_text_converter
            target_url: External API endpoint
            include_metadata: Whether to include conversion metadata
            headers: Optional HTTP headers
            
        Returns:
            API call result
        """
        # Prepare payload
        payload = {
            "text": transcription_result,
            "session_id": session_id,
            "user_id": user_id,
            "channel": channel,
            # "source": "channel-adapter",
            # "timestamp": transcription_result.get("timestamp", None)
        }
        
        if include_metadata:
            payload["metadata"] = {
                "service": "channel-adapter",
                "version": "2.0.0",
                "conversion_engine": "google-speech-recognition",
                "audio_format": transcription_result.get("format", "unknown"),
                "language": transcription_result.get("language", "en-US")
            }
        
        return await self.send_transcription(target_url, payload, headers)
    
    async def forward_text_input_result(
        self,
        text: str,
        text_input_result: Dict[str, Any],
        target_url: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        channel: Optional[str] = None,
        include_metadata: bool = True,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Forward a text-input result to external API
        
        Args:
            text_input_result: Result from text input processing
            target_url: External API endpoint
            include_metadata: Whether to include processing metadata
            headers: Optional HTTP headers
            
        Returns:
            API call result
        """
        # Prepare payload
        payload = {
            "text": text,
            "session_id": session_id,
            "user_id": user_id,
            "channel": channel,
            # "source": "channel-adapter",
            # "timestamp": text_input_result.get("received_at", None)
        }
        
        if include_metadata:
            payload["metadata"] = {
                "service": "channel-adapter",
                "version": "2.0.0",
                "processing_type": "text-input",
                "original_source": text_input_result.get("source", "unknown"),
                "text_length": text_input_result.get("text_length", 0)
            }
        
        return await self.send_transcription(target_url, payload, headers)
    
    async def forward_text_to_voice_result(
        self,
        tts_result: Dict[str, Any],
        target_url: str,
        include_audio_data: bool = False,
        include_metadata: bool = True,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Forward a text-to-voice result to external API
        
        Args:
            tts_result: Result from text-to-voice conversion
            target_url: External API endpoint
            include_audio_data: Whether to include audio file data (base64 encoded)
            include_metadata: Whether to include conversion metadata
            headers: Optional HTTP headers
            
        Returns:
            API call result
        """
        import base64
        
        # Prepare payload
        payload = {
            "text_to_voice": tts_result,
            "source": "channel-adapter",
            "timestamp": None
        }
        
        # Include audio data if requested and available
        if include_audio_data and "file_path" in tts_result:
            try:
                with open(tts_result["file_path"], "rb") as audio_file:
                    audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
                    payload["audio_data"] = {
                        "data": audio_data,
                        "format": "mp3",
                        "encoding": "base64"
                    }
            except Exception as e:
                logger.warning(f"Failed to include audio data: {str(e)}")
        
        if include_metadata:
            payload["metadata"] = {
                "service": "channel-adapter",
                "version": "2.0.0",
                "processing_type": "text-to-voice",
                "tts_engine": tts_result.get("tts_engine", "gTTS"),
                "language": tts_result.get("language", "unknown"),
                "output_format": tts_result.get("output_format", "mp3"),
                "text_length": tts_result.get("text_length", 0),
                "file_size_bytes": tts_result.get("file_size_bytes", 0)
            }
        
        return await self.send_transcription(target_url, payload, headers)


# Global instance for use in the main application
rest_api_client = RestApiClient()


# Cleanup function for proper session closure
async def cleanup_rest_client():
    """Cleanup function to close the REST client session"""
    await rest_api_client.close()
