"""Video processing module."""

import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class VideoMetadata:
    """Video metadata container."""
    title: str
    description: str
    duration: int
    upload_date: str
    channel: str
    transcript: Optional[str] = None

class VideoProcessor:
    """Handles YouTube video processing."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the video processor."""
        self.config = config
    
    def validate_url(self, url: str) -> bool:
        """Validate YouTube URL format."""
        return 'youtube.com' in url or 'youtu.be' in url
    
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
                transcript = None
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(info['id'])
                    transcript = ' '.join([entry['text'] for entry in transcript_list])
                except Exception:
                    pass  # Transcript not available
                
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
                    transcript=transcript
                )
        except Exception as e:
            raise ValueError(f"Failed to process video: {str(e)}") 