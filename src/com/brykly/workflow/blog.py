"""Blog generation workflow module."""

import logging
from pathlib import Path
from typing import Dict, Any

from ..external_integration.openai import OpenAIAdapter
from ..external_integration.openrouter import OpenRouterAdapter
from ..output_management.blog import BlogManager
from ..output_management.storage import StorageManager
from .base import BaseWorkflow

logger = logging.getLogger(__name__)

class BlogGenerationWorkflow(BaseWorkflow):
    """Workflow for generating blog posts from transcripts."""
    
    def __init__(self, config_path: str = 'config.yaml'):
        super().__init__(config_path)
        self.openai_service = OpenAIAdapter(config_path)
        self.openrouter_service = OpenRouterAdapter(config_path)
        self.blog_manager = BlogManager(config_path)
        self.storage_manager = StorageManager(config_path)
    
    async def execute(
        self,
        transcript_path: str,
        tone: str = 'professional',
        style: str = 'comprehensive'
    ) -> Dict[str, Any]:
        """Execute the blog generation workflow."""
        try:
            await self.start()
            
            # Step 1: Load transcript
            load_step = self.add_step(
                "load_transcript",
                "Loading transcript from file"
            )
            load_step.start()
            transcript_data = await self.blog_manager.load_transcript(transcript_path)
            load_step.complete({'transcript_data': transcript_data})
            
            # Step 2: Generate blog post
            generate_step = self.add_step(
                "generate_blog_post",
                "Generating blog post content"
            )
            generate_step.start()
            try:
                blog_content = await self.openai_service.generate_blog_post(
                    transcript_data['transcript'],
                    tone=tone,
                    style=style
                )
            except Exception as e:
                logger.warning(f"OpenAI generation failed, falling back to OpenRouter: {str(e)}")
                blog_content = await self.openrouter_service.generate_blog_post(
                    transcript_data['transcript'],
                    tone=tone,
                    style=style
                )
            generate_step.complete({'blog_content': blog_content})
            
            # Step 3: Save blog post
            save_step = self.add_step(
                "save_blog_post",
                "Saving blog post to file"
            )
            save_step.start()
            blog_path = await self.blog_manager.save_blog_post(
                blog_content,
                transcript_data['metadata']
            )
            save_step.complete({'blog_path': blog_path})
            
            # Step 4: Generate metadata
            metadata_step = self.add_step(
                "generate_metadata",
                "Generating blog post metadata"
            )
            metadata_step.start()
            await self.blog_manager.generate_metadata(blog_content)
            metadata_step.complete()
            
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
            logger.error(f"Error in blog generation workflow: {str(e)}")
            await self.fail(e)
            raise 