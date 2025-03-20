"""Example script demonstrating API integration functionality in the package."""
import asyncio
import os
import sys
from pathlib import Path

# Add the package root to the Python path
package_root = Path(__file__).parent.parent
sys.path.append(str(package_root))

from com.brykly.services.openai import OpenAIService
from com.brykly.services.openrouter import OpenRouterService
from com.brykly.services.youtube import YouTubeService
from com.brykly.utils.config import ConfigManager
from com.brykly.utils.logging_config import setup_logging

async def demonstrate_openai_api():
    """Demonstrate OpenAI API integration."""
    print("\nDemonstrating OpenAI API integration...")
    
    # Initialize configuration and logging
    config = ConfigManager('config.yaml')
    logger = setup_logging('openai_demo', {'level': 'INFO'})
    
    # Create OpenAI service
    service = OpenAIService(config)
    
    try:
        # Generate blog post
        print("\nGenerating blog post using OpenAI...")
        transcript = """This is a test transcript.
        It contains multiple lines of text.
        We'll use it to generate a blog post."""
        
        blog_post = await service.generate_blog_post(
            transcript,
            tone="professional",
            style="comprehensive"
        )
        print("✓ Successfully generated blog post")
        print("\nPreview:")
        print(blog_post[:200] + "...")
        
        # Generate metadata
        print("\nGenerating metadata...")
        metadata = await service.generate_metadata(blog_post)
        print("✓ Successfully generated metadata")
        print("Metadata:", metadata)
        
    except Exception as e:
        print(f"✗ OpenAI API error: {str(e)}")

async def demonstrate_openrouter_api():
    """Demonstrate OpenRouter API integration."""
    print("\nDemonstrating OpenRouter API integration...")
    
    # Initialize configuration and logging
    config = ConfigManager('config.yaml')
    logger = setup_logging('openrouter_demo', {'level': 'INFO'})
    
    # Create OpenRouter service
    service = OpenRouterService(config)
    
    try:
        # Generate blog post (fallback)
        print("\nGenerating blog post using OpenRouter...")
        transcript = """This is another test transcript.
        We'll use it to test the OpenRouter API.
        This demonstrates the fallback capability."""
        
        blog_post = await service.generate_blog_post(
            transcript,
            tone="casual",
            style="concise"
        )
        print("✓ Successfully generated blog post")
        print("\nPreview:")
        print(blog_post[:200] + "...")
        
    except Exception as e:
        print(f"✗ OpenRouter API error: {str(e)}")

async def demonstrate_youtube_api():
    """Demonstrate YouTube API integration."""
    print("\nDemonstrating YouTube API integration...")
    
    # Initialize configuration and logging
    config = ConfigManager('config.yaml')
    logger = setup_logging('youtube_demo', {'level': 'INFO'})
    
    # Create YouTube service
    service = YouTubeService(config)
    
    try:
        # Get video information
        video_url = "https://youtube.com/watch?v=example"
        print(f"\nGetting video information for: {video_url}")
        
        info = await service.get_video_info(video_url)
        print("✓ Successfully retrieved video information")
        print("\nVideo details:")
        print(f"Title: {info['title']}")
        print(f"Duration: {info['duration']} seconds")
        print(f"View count: {info['view_count']}")
        print(f"Channel: {info['uploader']}")
        
        # Download video
        print("\nDownloading video...")
        output_path = "test_video.mp4"
        await service.download_video(video_url, output_path)
        print(f"✓ Successfully downloaded video to: {output_path}")
        
        # Clean up
        if os.path.exists(output_path):
            os.remove(output_path)
            print(f"✓ Cleaned up test video file")
        
    except Exception as e:
        print(f"✗ YouTube API error: {str(e)}")

async def demonstrate_api_error_handling():
    """Demonstrate API error handling."""
    print("\nDemonstrating API error handling...")
    
    # Initialize configuration and logging
    config = ConfigManager('config.yaml')
    logger = setup_logging('error_demo', {'level': 'INFO'})
    
    # Test invalid API keys
    print("\nTesting invalid API key handling...")
    try:
        service = OpenAIService(config)
        service.api_key = "invalid_key"
        await service.generate_blog_post("test", "professional", "comprehensive")
        print("✗ Expected error was not raised")
    except Exception as e:
        print(f"✓ Caught expected error: {str(e)}")
    
    # Test rate limiting
    print("\nTesting rate limit handling...")
    try:
        service = OpenAIService(config)
        tasks = []
        for _ in range(10):
            tasks.append(service.generate_blog_post("test", "professional", "comprehensive"))
        await asyncio.gather(*tasks)
        print("✗ Expected rate limit error was not raised")
    except Exception as e:
        print(f"✓ Caught expected error: {str(e)}")
    
    # Test timeout handling
    print("\nTesting timeout handling...")
    try:
        service = YouTubeService(config)
        service.timeout = 0.001  # Set very short timeout
        await service.get_video_info("https://youtube.com/watch?v=example")
        print("✗ Expected timeout error was not raised")
    except Exception as e:
        print(f"✓ Caught expected error: {str(e)}")

async def main():
    """Main function demonstrating API integration features."""
    print("Starting API integration demonstration...")
    
    # Demonstrate OpenAI API
    await demonstrate_openai_api()
    
    # Demonstrate OpenRouter API
    await demonstrate_openrouter_api()
    
    # Demonstrate YouTube API
    await demonstrate_youtube_api()
    
    # Demonstrate error handling
    await demonstrate_api_error_handling()
    
    print("\nAPI integration demonstration completed!")

if __name__ == "__main__":
    asyncio.run(main()) 