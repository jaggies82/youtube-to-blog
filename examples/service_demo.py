"""Example script demonstrating service integration functionality in the package."""
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
from com.brykly.services.openrouter import OpenRouterService
from com.brykly.utils.config import ConfigManager

async def demonstrate_youtube_service():
    """Demonstrate YouTube service functionality."""
    print("\nDemonstrating YouTube service...")
    
    # Initialize configuration
    config_path = os.path.join(os.getcwd(), 'config.yaml')
    config = ConfigManager(config_path)
    
    # Create YouTube service
    service = YouTubeService(config_path)
    
    # Example video URL
    video_url = "https://youtube.com/watch?v=example"
    
    try:
        # Get video information
        print("\nGetting video information...")
        info = await service.get_video_info(video_url)
        print(f"✓ Successfully retrieved video info: {info['title']}")
        
        # Download video
        print("\nDownloading video...")
        output_path = "test_video.mp4"
        await service.download_video(video_url, output_path)
        print(f"✓ Successfully downloaded video to: {output_path}")
    except Exception as e:
        print(f"✗ YouTube service error: {str(e)}")

async def demonstrate_transcript_service():
    """Demonstrate transcript service functionality."""
    print("\nDemonstrating transcript service...")
    
    # Initialize configuration
    config_path = os.path.join(os.getcwd(), 'config.yaml')
    config = ConfigManager(config_path)
    
    # Create transcript service
    service = TranscriptManager(config_path)
    
    # Example video path
    video_path = "test_video.mp4"
    
    try:
        # Extract transcript
        print("\nExtracting transcript...")
        transcript = await service.extract_transcript(video_path)
        print("✓ Successfully extracted transcript")
        
        # Save transcript
        print("\nSaving transcript...")
        output_path = "test_transcript.txt"
        await service.save_transcript(transcript, output_path)
        print(f"✓ Successfully saved transcript to: {output_path}")
    except Exception as e:
        print(f"✗ Transcript service error: {str(e)}")

async def demonstrate_openai_service():
    """Demonstrate OpenAI service functionality."""
    print("\nDemonstrating OpenAI service...")
    
    # Initialize configuration
    config_path = os.path.join(os.getcwd(), 'config.yaml')
    config = ConfigManager(config_path)
    
    # Create OpenAI service
    service = OpenAIService(config_path)
    
    # Example transcript
    transcript = "This is a test transcript for generating a blog post."
    
    try:
        # Generate blog post
        print("\nGenerating blog post...")
        blog_post = await service.generate_blog_post(
            transcript,
            tone="professional",
            style="comprehensive"
        )
        print("✓ Successfully generated blog post")
        
        # Generate metadata
        print("\nGenerating metadata...")
        metadata = await service.generate_metadata(blog_post)
        print("✓ Successfully generated metadata")
    except Exception as e:
        print(f"✗ OpenAI service error: {str(e)}")

async def demonstrate_openrouter_service():
    """Demonstrate OpenRouter service functionality."""
    print("\nDemonstrating OpenRouter service...")
    
    # Initialize configuration
    config_path = os.path.join(os.getcwd(), 'config.yaml')
    config = ConfigManager(config_path)
    
    # Create OpenRouter service
    service = OpenRouterService(config_path)
    
    # Example transcript
    transcript = "This is a test transcript for generating a blog post."
    
    try:
        # Generate blog post (fallback)
        print("\nGenerating blog post (fallback)...")
        blog_post = await service.generate_blog_post(
            transcript,
            tone="professional",
            style="comprehensive"
        )
        print("✓ Successfully generated blog post using OpenRouter")
    except Exception as e:
        print(f"✗ OpenRouter service error: {str(e)}")

async def main():
    """Main function demonstrating service integration features."""
    print("Starting service integration demonstration...")
    
    # Demonstrate YouTube service
    await demonstrate_youtube_service()
    
    # Demonstrate transcript service
    await demonstrate_transcript_service()
    
    # Demonstrate OpenAI service
    await demonstrate_openai_service()
    
    # Demonstrate OpenRouter service
    await demonstrate_openrouter_service()
    
    print("\nService integration demonstration completed!")

if __name__ == "__main__":
    asyncio.run(main()) 