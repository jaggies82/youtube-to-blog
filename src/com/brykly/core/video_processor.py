"""Video processing module."""

import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
from loguru import logger

@dataclass
class VideoMetadata:
    """Video metadata container."""
    title: str
    description: str
    duration: int
    upload_date: str
    channel: str
    transcript: Optional[str] = None
    transcript_language: Optional[str] = None
    is_auto_generated: bool = False

class VideoProcessor:
    """Handles YouTube video processing."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the video processor."""
        self.config = config
        self.preferred_languages = config.get('transcript', {}).get('preferred_languages', ['en'])
    
    def validate_url(self, url: str) -> bool:
        """Validate YouTube URL format."""
        return 'youtube.com' in url or 'youtu.be' in url
    
    def _get_transcript(self, video_id: str) -> Optional[tuple[str, str, bool]]:
        """Get transcript for a video, trying multiple languages if needed.
        
        Returns:
            Tuple of (transcript_text, language_code, is_auto_generated)
            or None if no transcript is available.
        """
        try:
            # First try to get manual captions
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=self.preferred_languages)
            return ' '.join([entry['text'] for entry in transcript_list]), transcript_list[0]['lang'], False
        except (TranscriptsDisabled, NoTranscriptFound):
            try:
                # If no manual captions, try auto-generated ones
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=self.preferred_languages)
                return ' '.join([entry['text'] for entry in transcript_list]), transcript_list[0]['lang'], True
            except Exception as e:
                logger.warning(f"Failed to get transcript for video {video_id}: {str(e)}")
                return None
    
    def extract_metadata(self, url: str) -> VideoMetadata:
        """Extract video metadata and transcript."""
        if not self.validate_url(url):
            raise ValueError("Invalid YouTube URL")
        
        # Extract video info using yt-dlp
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False  # Changed to False to get full metadata
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    raise ValueError("Failed to extract video information")
                
                # Get transcript if available
                transcript_result = self._get_transcript(info['id'])
                transcript = None
                transcript_language = None
                is_auto_generated = False
                
                if transcript_result:
                    transcript, transcript_language, is_auto_generated = transcript_result
                    if is_auto_generated:
                        logger.info(f"Using auto-generated transcript in {transcript_language}")
                    else:
                        logger.info(f"Using manual transcript in {transcript_language}")
                
                # Extract and validate required fields
                title = info.get('title')
                if not title:
                    raise ValueError("Video title not found")
                
                return VideoMetadata(
                    title=title,
                    description=info.get('description', 'No description available'),
                    duration=info.get('duration', 0),
                    upload_date=info.get('upload_date', datetime.now().strftime('%Y%m%d')),
                    channel=info.get('channel', 'Unknown channel'),
                    transcript=transcript,
                    transcript_language=transcript_language,
                    is_auto_generated=is_auto_generated
                )
        except Exception as e:
            raise ValueError(f"Failed to process video: {str(e)}") 