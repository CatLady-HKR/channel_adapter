"""
Utility functions for the Channel Adapter API
Common functions used across multiple endpoints
"""
import logging
from typing import Optional, Dict, Any, List
from fastapi import HTTPException

logger = logging.getLogger(__name__)

def parse_custom_headers(custom_headers: Optional[str]) -> Optional[Dict[str, str]]:
    """
    Parse custom headers from string format to dictionary.
    
    Args:
        custom_headers: String in format "key1:value1,key2:value2"
        
    Returns:
        Dictionary of headers or None if parsing fails
    """
    if not custom_headers:
        return None
        
    try:
        headers = dict(item.split(":") for item in custom_headers.split(","))
        return {k.strip(): v.strip() for k, v in headers.items()}
    except Exception:
        logger.warning("Failed to parse custom headers, using defaults")
        return None

def create_standard_response(
    success: bool,
    data: Any = None,
    message: Optional[str] = None,
    error: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a standardized response format.
    
    Args:
        success: Whether the operation was successful
        data: The main data payload
        message: Success message
        error: Error message if any
        
    Returns:
        Standardized response dictionary
    """
    response = {"success": success}
    
    if data is not None:
        response["data"] = data
    if message:
        response["message"] = message
    if error:
        response["error"] = error
        
    return response

def create_forwarding_response(
    original_result: Dict[str, Any],
    forward_result: Dict[str, Any],
    operation_name: str
) -> Dict[str, Any]:
    """
    Create a standardized forwarding response.
    
    Args:
        original_result: Result from the original processing operation
        forward_result: Result from the forwarding operation
        operation_name: Name of the operation for the response key
        
    Returns:
        Standardized forwarding response
    """
    return {
        operation_name: original_result,
        "forward_result": forward_result,
        "success": forward_result.get("success", False)
    }

def create_batch_forwarding_response(
    batch_result: Dict[str, Any],
    forward_results: List[Dict[str, Any]],
    operation_name: str
) -> Dict[str, Any]:
    """
    Create a standardized batch forwarding response.
    
    Args:
        batch_result: Result from the batch processing operation
        forward_results: List of forwarding results
        operation_name: Name of the operation for the response key
        
    Returns:
        Standardized batch forwarding response
    """
    # Extract results from batch operation
    if isinstance(batch_result, dict) and "results" in batch_result:
        total_items = len(batch_result["results"])
    else:
        total_items = 1 if batch_result else 0
    
    successful_forwards = len([r for r in forward_results if r.get("success", False)])
    
    return {
        f"{operation_name}_results": batch_result,
        "forward_results": forward_results,
        "total_items": total_items,
        "successful_forwards": successful_forwards,
        "success": len(forward_results) > 0
    }

def handle_api_error(operation: str, error: Exception) -> HTTPException:
    """
    Handle and format API errors consistently.
    
    Args:
        operation: Name of the operation that failed
        error: The exception that occurred
        
    Returns:
        HTTPException with formatted error message
    """
    error_message = f"{operation} failed: {str(error)}"
    logger.error(f"Error in {operation}: {str(error)}")
    return HTTPException(status_code=500, detail=error_message)

def create_transcription_result_format(
    text: str,
    language: str = "en-US",
    source: str = "manual"
) -> Dict[str, Any]:
    """
    Create a standardized transcription result format.
    
    Args:
        text: The transcribed text
        language: Language code
        source: Source of the transcription
        
    Returns:
        Standardized transcription result
    """
    return {
        "success": True,
        "text": text,
        "language": language,
        "source": source,
        "timestamp": None
    }

def create_text_input_result_format(
    text: str,
    source: str = "ui",
    timestamp: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a standardized text input result format.
    
    Args:
        text: The input text
        source: Source of the text input
        timestamp: Optional timestamp
        
    Returns:
        Standardized text input result
    """
    return {
        "success": True,
        "message": "Text received successfully",
        "text_length": len(text),
        "source": source,
        "received_at": timestamp,
        "processed_text": text.strip()
    }

def extract_successful_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extract only successful results from a list of results.
    
    Args:
        results: List of result dictionaries
        
    Returns:
        List containing only successful results
    """
    return [
        result for result in results 
        if isinstance(result, dict) and result.get("success", False)
    ]

def prepare_batch_results(batch_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Prepare batch results for processing, handling different result formats.
    
    Args:
        batch_result: The batch processing result
        
    Returns:
        List of individual results
    """
    if isinstance(batch_result, dict) and "results" in batch_result:
        return batch_result["results"]
    else:
        return [batch_result] if batch_result else []

def create_tts_forwarding_payload(
    tts_result: Dict[str, Any],
    language: str,
    slow: bool,
    include_metadata: bool = True,
    batch_index: int = 0
) -> Dict[str, Any]:
    """
    Create a forwarding payload for text-to-speech results.
    
    Args:
        tts_result: The TTS conversion result
        language: Language used for TTS
        slow: Whether slow speech was used
        include_metadata: Whether to include metadata
        batch_index: Index in batch processing
        
    Returns:
        Formatted payload for forwarding
    """
    payload = {
        "text_to_voice": tts_result,
        "source": "channel-adapter",
        "timestamp": None
    }
    
    if include_metadata:
        payload["metadata"] = {
            "service": "channel-adapter",
            "version": "2.0.0",
            "processing_type": "text-to-voice-batch",
            "tts_engine": tts_result.get("tts_engine", "gTTS"),
            "language": language,
            "slow": slow,
            "batch_index": batch_index
        }
    
    return payload
