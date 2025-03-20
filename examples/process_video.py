"""Example script demonstrating how to use the Agentic Fun package."""
import asyncio
import os
from pathlib import Path

from com.brykly.workflow.video import VideoProcessingWorkflow
from com.brykly.workflow.blog import BlogGenerationWorkflow
from com.brykly.utils.config import ConfigManager

async def main():
    """Main function demonstrating the workflow."""
    # Initialize configuration
    config_path = os.path.join(os.getcwd(), 'config.yaml')
    config = ConfigManager(config_path)
    
    # Example YouTube video URL
    video_url = "https://www.youtube.com/watch?v=example"
    
    # Process video and extract transcript
    print("Starting video processing workflow...")
    video_workflow = VideoProcessingWorkflow(config_path)
    video_result = await video_workflow.execute(video_url)
    
    if video_result['status'] == 'completed':
        transcript_path = video_result['transcript_path']
        print(f"Transcript extracted successfully: {transcript_path}")
        
        # Generate blog post from transcript
        print("\nStarting blog generation workflow...")
        blog_workflow = BlogGenerationWorkflow(config_path)
        blog_result = await blog_workflow.execute(
            transcript_path=transcript_path,
            tone="professional",
            style="comprehensive"
        )
        
        if blog_result['status'] == 'completed':
            print(f"Blog post generated successfully: {blog_result['blog_path']}")
        else:
            print(f"Blog generation failed: {blog_result['error']}")
    else:
        print(f"Video processing failed: {video_result['error']}")

if __name__ == "__main__":
    asyncio.run(main()) 