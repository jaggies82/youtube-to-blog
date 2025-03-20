"""Core application module."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from .video_processor import VideoProcessor
from .content_generator import ContentGenerator
from .output_manager import OutputManager
from ..utils.logger import Logger

class App:
    """Core application class."""
    
    def __init__(self, config_path: str = 'config.yaml'):
        """Initialize the application."""
        self.config_path = config_path
        self.config = self._load_config()
        self.logger = Logger()
        
        # Initialize components
        self.video_processor = VideoProcessor(self.config)
        self.content_generator = ContentGenerator(self.config)
        self.output_manager = OutputManager(self.config)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration: {str(e)}")
    
    def initialize_paths(self) -> None:
        """Initialize application directories."""
        paths = self.config.get('paths', {})
        for path_name, path_value in paths.items():
            path = Path(path_value)
            path.mkdir(parents=True, exist_ok=True)
    
    def process_video(self, url: str, mode: str = 'quick') -> Optional[Dict[str, str]]:
        """Process a YouTube video and generate blog content."""
        try:
            # Extract video metadata
            self.logger.info(f"Processing video: {url}")
            metadata = self.video_processor.extract_metadata(url)
            self.logger.info(f"Extracted metadata for: {metadata.title}")
            
            # Generate content based on mode
            if mode == 'quick':
                blog_post = self.content_generator.generate_quick_summary(metadata)
            else:
                blog_post = self.content_generator.generate_detailed_review(metadata)
            
            self.logger.info("Generated blog post content")
            
            # Save in configured formats
            output_files = self.output_manager.save_all_formats(blog_post)
            self.logger.info(f"Saved blog post in formats: {', '.join(output_files.keys())}")
            
            return output_files
            
        except Exception as e:
            self.logger.error(f"Error processing video: {str(e)}")
            raise 