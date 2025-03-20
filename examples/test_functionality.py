"""Test script to verify the package's core functionality."""
import asyncio
import os
import sys
from pathlib import Path

# Add the package root to the Python path
package_root = Path(__file__).parent.parent
sys.path.append(str(package_root))

from com.brykly.services.youtube import YouTubeService
from com.brykly.services.transcript import TranscriptManager
from com.brykly.services.openai import OpenAIService
from com.brykly.utils.config import ConfigManager

async def test_youtube_service(config_path):
    """Test YouTube service functionality."""
    print("\nTesting YouTube Service...")
    service = YouTubeService(config_path)
    
    # Test video info extraction
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Example video
    try:
        info = await service.get_video_info(video_url)
        print(f"✓ Successfully extracted video info: {info['title']}")
    except Exception as e:
        print(f"✗ Failed to extract video info: {str(e)}")

async def test_transcript_service(config_path):
    """Test transcript service functionality."""
    print("\nTesting Transcript Service...")
    service = TranscriptManager(config_path)
    
    # Test transcript extraction
    video_path = "test_video.mp4"  # Example video path
    try:
        transcript = await service.extract_transcript(video_path)
        print("✓ Successfully extracted transcript")
    except Exception as e:
        print(f"✗ Failed to extract transcript: {str(e)}")

async def test_openai_service(config_path):
    """Test OpenAI service functionality."""
    print("\nTesting OpenAI Service...")
    service = OpenAIService(config_path)
    
    # Test blog post generation
    transcript = "This is a test transcript for generating a blog post."
    try:
        blog_post = await service.generate_blog_post(
            transcript,
            tone="professional",
            style="comprehensive"
        )
        print("✓ Successfully generated blog post")
    except Exception as e:
        print(f"✗ Failed to generate blog post: {str(e)}")

async def main():
    """Main function to run all tests."""
    # Initialize configuration
    config_path = os.path.join(os.getcwd(), 'config.yaml')
    config = ConfigManager(config_path)
    
    print("Starting functionality tests...")
    
    # Run tests
    await test_youtube_service(config_path)
    await test_transcript_service(config_path)
    await test_openai_service(config_path)
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 