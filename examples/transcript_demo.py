"""Example script demonstrating transcript management functionality in the package."""
import asyncio
import os
import sys
from pathlib import Path

# Add the package root to the Python path
package_root = Path(__file__).parent.parent
sys.path.append(str(package_root))

from com.brykly.services.transcript import TranscriptManager
from com.brykly.utils.config import ConfigManager

async def demonstrate_transcript_management():
    """Demonstrate transcript management features."""
    print("Starting transcript management demonstration...")
    
    # Initialize configuration
    config_path = os.path.join(os.getcwd(), 'config.yaml')
    config = ConfigManager(config_path)
    
    # Create transcript manager
    transcript_manager = TranscriptManager(config_path)
    
    # Example transcript content
    transcript_content = """[00:00] Introduction
[00:15] Welcome to this video about transcript management.
[00:30] In this video, we'll explore how to handle transcripts effectively.
[01:00] Let's begin with the basics.
[01:30] First, we need to understand the structure.
[02:00] This is a test transcript for demonstration purposes.
[02:30] We'll show various transcript management features.
[03:00] Thank you for watching!"""

    try:
        # Save transcript
        print("\nSaving transcript...")
        transcript_path = await transcript_manager.save_transcript(
            content=transcript_content,
            video_id="test_video_123",
            language="en"
        )
        print(f"✓ Successfully saved transcript to: {transcript_path}")
        
        # Load transcript
        print("\nLoading transcript...")
        loaded_transcript = await transcript_manager.load_transcript(transcript_path)
        print("✓ Successfully loaded transcript")
        print(f"Video ID: {loaded_transcript['video_id']}")
        print(f"Language: {loaded_transcript['language']}")
        
        # Format transcript
        print("\nFormatting transcript...")
        formatted_transcript = await transcript_manager.format_transcript(transcript_content)
        print("✓ Successfully formatted transcript")
        print("Formatted content preview:")
        print(formatted_transcript[:200] + "...")
        
        # Clean transcript
        print("\nCleaning transcript...")
        cleaned_transcript = await transcript_manager.clean_transcript(transcript_content)
        print("✓ Successfully cleaned transcript")
        print("Cleaned content preview:")
        print(cleaned_transcript[:200] + "...")
        
        # Update transcript
        print("\nUpdating transcript...")
        updated_content = transcript_content + "\n[03:30] Additional content added."
        await transcript_manager.update_transcript(transcript_path, updated_content)
        print("✓ Successfully updated transcript")
        
        # List transcripts
        print("\nListing transcripts...")
        transcripts = await transcript_manager.list_transcripts()
        print("Transcripts:")
        for transcript in transcripts:
            print(f"- {transcript['video_id']} ({transcript['language']})")
        
        # Delete transcript
        print("\nDeleting transcript...")
        await transcript_manager.delete_transcript(transcript_path)
        print("✓ Successfully deleted transcript")
        
    except Exception as e:
        print(f"✗ Transcript management error: {str(e)}")
    
    print("\nTranscript management demonstration completed!")

if __name__ == "__main__":
    asyncio.run(demonstrate_transcript_management()) 