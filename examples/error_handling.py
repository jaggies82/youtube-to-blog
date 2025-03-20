"""Example script demonstrating error handling in the package."""
import asyncio
import os
import sys
from pathlib import Path

# Add the package root to the Python path
package_root = Path(__file__).parent.parent
sys.path.append(str(package_root))

from com.brykly.workflow.video import VideoProcessingWorkflow
from com.brykly.workflow.blog import BlogGenerationWorkflow
from com.brykly.utils.config import ConfigManager

async def handle_video_processing_error(video_url):
    """Demonstrate error handling in video processing."""
    print(f"\nProcessing video: {video_url}")
    try:
        workflow = VideoProcessingWorkflow("config.yaml")
        result = await workflow.execute(video_url)
        
        if result['status'] == 'completed':
            print("✓ Video processed successfully")
            return result['transcript_path']
        else:
            print(f"✗ Video processing failed: {result['error']}")
            return None
    except Exception as e:
        print(f"✗ Unexpected error during video processing: {str(e)}")
        return None

async def handle_blog_generation_error(transcript_path):
    """Demonstrate error handling in blog generation."""
    if not transcript_path:
        print("✗ Cannot generate blog post: No transcript available")
        return None
        
    print(f"\nGenerating blog post from transcript: {transcript_path}")
    try:
        workflow = BlogGenerationWorkflow("config.yaml")
        result = await workflow.execute(
            transcript_path=transcript_path,
            tone="professional",
            style="comprehensive"
        )
        
        if result['status'] == 'completed':
            print("✓ Blog post generated successfully")
            return result['blog_path']
        else:
            print(f"✗ Blog generation failed: {result['error']}")
            return None
    except Exception as e:
        print(f"✗ Unexpected error during blog generation: {str(e)}")
        return None

async def main():
    """Main function demonstrating error handling."""
    # Initialize configuration
    config_path = os.path.join(os.getcwd(), 'config.yaml')
    config = ConfigManager(config_path)
    
    print("Starting error handling demonstration...")
    
    # Test cases with potential errors
    test_cases = [
        "https://youtube.com/watch?v=invalid",  # Invalid video URL
        "https://youtube.com/watch?v=dQw4w9WgXcQ",  # Valid video URL
        "https://youtube.com/watch?v=another_invalid"  # Another invalid URL
    ]
    
    for video_url in test_cases:
        print(f"\n{'='*50}")
        print(f"Testing with URL: {video_url}")
        
        # Process video
        transcript_path = await handle_video_processing_error(video_url)
        
        # Generate blog post if transcript is available
        if transcript_path:
            blog_path = await handle_blog_generation_error(transcript_path)
            if blog_path:
                print(f"✓ Final blog post saved to: {blog_path}")
    
    print("\nError handling demonstration completed!")

if __name__ == "__main__":
    asyncio.run(main()) 