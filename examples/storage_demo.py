"""Example script demonstrating file storage functionality in the package."""
import os
import sys
import shutil
from pathlib import Path

# Add the package root to the Python path
package_root = Path(__file__).parent.parent
sys.path.append(str(package_root))

from com.brykly.output_management.storage import StorageManager
from com.brykly.utils.config import ConfigManager

def create_test_files():
    """Create test files for demonstration."""
    # Create test directories
    os.makedirs('test_output', exist_ok=True)
    os.makedirs('test_temp', exist_ok=True)
    
    # Create test files
    with open('test_temp/test_video.mp4', 'w') as f:
        f.write('Test video content')
    
    with open('test_temp/test_transcript.txt', 'w') as f:
        f.write('Test transcript content')
    
    with open('test_temp/test_blog.md', 'w') as f:
        f.write('Test blog content')

def demonstrate_storage():
    """Demonstrate various storage management features."""
    print("Starting storage management demonstration...")
    
    # Initialize configuration
    config_path = os.path.join(os.getcwd(), 'config.yaml')
    config = ConfigManager(config_path)
    
    # Create test files
    create_test_files()
    
    # Initialize storage manager
    storage = StorageManager(config)
    
    # Demonstrate file operations
    print("\nDemonstrating file operations:")
    
    # Move file from temp to output
    print("\nMoving file from temp to output:")
    temp_file = 'test_temp/test_video.mp4'
    output_file = 'test_output/video.mp4'
    try:
        storage.move_file(temp_file, output_file)
        print(f"✓ Successfully moved {temp_file} to {output_file}")
    except Exception as e:
        print(f"✗ Failed to move file: {str(e)}")
    
    # Copy file
    print("\nCopying file:")
    source_file = 'test_temp/test_transcript.txt'
    target_file = 'test_output/transcript.txt'
    try:
        storage.copy_file(source_file, target_file)
        print(f"✓ Successfully copied {source_file} to {target_file}")
    except Exception as e:
        print(f"✗ Failed to copy file: {str(e)}")
    
    # Read file content
    print("\nReading file content:")
    try:
        content = storage.read_file(target_file)
        print(f"✓ Successfully read file content: {content[:50]}...")
    except Exception as e:
        print(f"✗ Failed to read file: {str(e)}")
    
    # Write file content
    print("\nWriting file content:")
    new_content = "Updated test content"
    try:
        storage.write_file(target_file, new_content)
        print("✓ Successfully wrote new content to file")
    except Exception as e:
        print(f"✗ Failed to write file: {str(e)}")
    
    # List directory contents
    print("\nListing directory contents:")
    try:
        files = storage.list_directory('test_output')
        print("Files in output directory:")
        for file in files:
            print(f"- {file}")
    except Exception as e:
        print(f"✗ Failed to list directory: {str(e)}")
    
    # Clean up temporary files
    print("\nCleaning up temporary files:")
    try:
        storage.cleanup_temp_files()
        print("✓ Successfully cleaned up temporary files")
    except Exception as e:
        print(f"✗ Failed to clean up files: {str(e)}")
    
    # Clean up test directories
    print("\nCleaning up test directories:")
    try:
        shutil.rmtree('test_output')
        shutil.rmtree('test_temp')
        print("✓ Successfully cleaned up test directories")
    except Exception as e:
        print(f"✗ Failed to clean up directories: {str(e)}")
    
    print("\nStorage management demonstration completed!")

if __name__ == "__main__":
    demonstrate_storage() 