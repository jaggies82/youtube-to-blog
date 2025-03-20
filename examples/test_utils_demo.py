"""Example script demonstrating testing utilities in the package."""
import asyncio
import os
import sys
from pathlib import Path

# Add the package root to the Python path
package_root = Path(__file__).parent.parent
sys.path.append(str(package_root))

from com.brykly.utils.testing import (
    MockYouTubeService,
    MockTranscriptManager,
    MockOpenAIService,
    MockOpenRouterService,
    MockStorageManager,
    MockConfigManager,
    TestAsyncContextManager
)

async def demonstrate_mock_youtube_service():
    """Demonstrate mock YouTube service functionality."""
    print("\nDemonstrating mock YouTube service...")
    
    # Create mock service
    service = MockYouTubeService()
    
    # Configure mock responses
    service.set_video_info({
        'title': 'Test Video',
        'description': 'Test Description',
        'duration': 120,
        'view_count': 1000,
        'uploader': 'Test Channel'
    })
    
    # Test video info retrieval
    video_url = "https://youtube.com/watch?v=test"
    info = await service.get_video_info(video_url)
    print("Video info test:")
    print(f"✓ Title: {info['title']}")
    print(f"✓ Duration: {info['duration']} seconds")
    print(f"✓ Views: {info['view_count']}")
    
    # Test video download
    output_path = "test_video.mp4"
    await service.download_video(video_url, output_path)
    print(f"✓ Mock video download completed")

async def demonstrate_mock_transcript_manager():
    """Demonstrate mock transcript manager functionality."""
    print("\nDemonstrating mock transcript manager...")
    
    # Create mock manager
    manager = MockTranscriptManager()
    
    # Configure mock responses
    manager.set_transcript("This is a test transcript.\nIt has multiple lines.\nEnd of transcript.")
    
    # Test transcript extraction
    video_path = "test_video.mp4"
    transcript = await manager.extract_transcript(video_path)
    print("Transcript test:")
    print(f"✓ Extracted transcript length: {len(transcript)}")
    
    # Test transcript saving
    output_path = "test_transcript.txt"
    await manager.save_transcript(transcript, output_path)
    print(f"✓ Mock transcript save completed")

async def demonstrate_mock_openai_service():
    """Demonstrate mock OpenAI service functionality."""
    print("\nDemonstrating mock OpenAI service...")
    
    # Create mock service
    service = MockOpenAIService()
    
    # Configure mock responses
    service.set_blog_post("# Test Blog Post\n\nThis is a mock blog post.\n\n## Section 1\n\nTest content.")
    service.set_metadata({
        'word_count': 100,
        'reading_time': 5,
        'keywords': ['test', 'mock', 'blog']
    })
    
    # Test blog post generation
    transcript = "Test transcript"
    blog_post = await service.generate_blog_post(transcript, "professional", "comprehensive")
    print("Blog post test:")
    print(f"✓ Generated blog post length: {len(blog_post)}")
    
    # Test metadata generation
    metadata = await service.generate_metadata(blog_post)
    print("Metadata test:")
    print(f"✓ Word count: {metadata['word_count']}")
    print(f"✓ Reading time: {metadata['reading_time']} minutes")

async def demonstrate_mock_storage_manager():
    """Demonstrate mock storage manager functionality."""
    print("\nDemonstrating mock storage manager...")
    
    # Create mock manager
    manager = MockStorageManager()
    
    # Configure mock responses
    manager.set_file_content("test.txt", "Test file content")
    manager.set_directory_listing(["file1.txt", "file2.txt", "file3.txt"])
    
    # Test file operations
    print("File operations test:")
    content = await manager.read_file("test.txt")
    print(f"✓ Read file content: {content}")
    
    await manager.write_file("new.txt", "New content")
    print("✓ Mock file write completed")
    
    files = await manager.list_directory("test_dir")
    print(f"✓ Listed {len(files)} files in directory")

async def demonstrate_test_context_manager():
    """Demonstrate test context manager functionality."""
    print("\nDemonstrating test context manager...")
    
    async with TestAsyncContextManager() as context:
        # Test setup phase
        print("✓ Context setup completed")
        
        # Simulate test operations
        await asyncio.sleep(0.1)
        print("✓ Test operations completed")
        
        # Test cleanup will happen automatically
    print("✓ Context cleanup completed")

async def main():
    """Main function demonstrating testing utilities."""
    print("Starting testing utilities demonstration...")
    
    try:
        # Demonstrate mock services
        await demonstrate_mock_youtube_service()
        await demonstrate_mock_transcript_manager()
        await demonstrate_mock_openai_service()
        await demonstrate_mock_storage_manager()
        
        # Demonstrate test context manager
        await demonstrate_test_context_manager()
        
    except Exception as e:
        print(f"✗ Error during demonstration: {str(e)}")
    
    print("\nTesting utilities demonstration completed!")

if __name__ == "__main__":
    asyncio.run(main()) 