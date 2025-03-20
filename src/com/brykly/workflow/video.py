"""Video processing workflow module."""

import logging
from pathlib import Path
from typing import Dict, Any

from ..external_integration.youtube import YouTubeAdapter
from ..output_management.transcript import TranscriptManager
from ..output_management.storage import StorageManager
from .base import BaseWorkflow

logger = logging.getLogger(__name__)

class VideoProcessingWorkflow(BaseWorkflow):
    """Workflow for processing YouTube videos and generating transcripts."""
    
    def __init__(self, config_path: str = 'config.yaml'):
        super().__init__(config_path)
        self.youtube_service = YouTubeAdapter(config_path)
        self.transcript_manager = TranscriptManager(config_path)
        self.storage_manager = StorageManager(config_path)
    
    async def execute(self, video_url: str) -> Dict[str, Any]:
        """Execute the video processing workflow."""
        try:
            await self.start()
            
            # Step 1: Extract video information
            info_step = self.add_step(
                "extract_video_info",
                "Extracting video information from YouTube"
            )
            info_step.start()
            video_info = await self.youtube_service.get_video_info(video_url)
            info_step.complete({'video_info': video_info})
            
            # Step 2: Download video
            download_step = self.add_step(
                "download_video",
                "Downloading video from YouTube"
            )
            download_step.start()
            video_path = await self.youtube_service.download_video(video_url)
            download_step.complete({'video_path': video_path})
            
            # Step 3: Extract transcript
            transcript_step = self.add_step(
                "extract_transcript",
                "Extracting transcript from video"
            )
            transcript_step.start()
            transcript = await self.transcript_manager.extract_transcript(video_path)
            transcript_step.complete({'transcript': transcript})
            
            # Step 4: Save transcript
            save_step = self.add_step(
                "save_transcript",
                "Saving transcript to file"
            )
            save_step.start()
            transcript_path = await self.transcript_manager.save_transcript(
                transcript,
                video_info
            )
            save_step.complete({'transcript_path': transcript_path})
            
            # Step 5: Cleanup
            cleanup_step = self.add_step(
                "cleanup",
                "Cleaning up temporary files"
            )
            cleanup_step.start()
            await self.storage_manager.cleanup_temp_files()
            cleanup_step.complete()
            
            await self.complete()
            return self.get_status_report()
            
        except Exception as e:
            logger.error(f"Error in video processing workflow: {str(e)}")
            await self.fail(e)
            raise 