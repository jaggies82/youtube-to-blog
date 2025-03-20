"""Example script demonstrating workflow functionality in the package."""
import asyncio
import os
import sys
from pathlib import Path

# Add the package root to the Python path
package_root = Path(__file__).parent.parent
sys.path.append(str(package_root))

from com.brykly.workflow.base import WorkflowStep, BaseWorkflow
from com.brykly.workflow.video import VideoProcessingWorkflow
from com.brykly.workflow.blog import BlogGenerationWorkflow
from com.brykly.utils.config import ConfigManager

async def demonstrate_base_workflow():
    """Demonstrate basic workflow functionality."""
    print("\nDemonstrating base workflow functionality...")
    
    # Create a simple workflow
    workflow = BaseWorkflow()
    
    # Add steps
    step1 = WorkflowStep("step1", "First step")
    step2 = WorkflowStep("step2", "Second step")
    step3 = WorkflowStep("step3", "Third step")
    
    workflow.add_step(step1)
    workflow.add_step(step2)
    workflow.add_step(step3)
    
    # Start workflow
    print("\nStarting workflow...")
    await workflow.start()
    
    # Simulate step execution
    print("\nExecuting steps...")
    await step1.start()
    await asyncio.sleep(1)  # Simulate work
    await step1.complete()
    
    await step2.start()
    await asyncio.sleep(1)  # Simulate work
    await step2.complete()
    
    await step3.start()
    await asyncio.sleep(1)  # Simulate work
    await step3.complete()
    
    # Complete workflow
    await workflow.complete()
    
    # Generate status report
    print("\nWorkflow status report:")
    report = workflow.generate_status_report()
    print(report)

async def demonstrate_video_workflow():
    """Demonstrate video processing workflow."""
    print("\nDemonstrating video processing workflow...")
    
    # Initialize configuration
    config_path = os.path.join(os.getcwd(), 'config.yaml')
    config = ConfigManager(config_path)
    
    # Create video workflow
    workflow = VideoProcessingWorkflow(config_path)
    
    # Example video URL
    video_url = "https://youtube.com/watch?v=example"
    
    try:
        # Execute workflow
        result = await workflow.execute(video_url)
        
        if result['status'] == 'completed':
            print("✓ Video processing completed successfully")
            print(f"Transcript saved to: {result['transcript_path']}")
        else:
            print(f"✗ Video processing failed: {result['error']}")
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")

async def demonstrate_blog_workflow():
    """Demonstrate blog generation workflow."""
    print("\nDemonstrating blog generation workflow...")
    
    # Initialize configuration
    config_path = os.path.join(os.getcwd(), 'config.yaml')
    config = ConfigManager(config_path)
    
    # Create blog workflow
    workflow = BlogGenerationWorkflow(config_path)
    
    # Example transcript path
    transcript_path = "example_transcript.txt"
    
    try:
        # Execute workflow
        result = await workflow.execute(
            transcript_path=transcript_path,
            tone="professional",
            style="comprehensive"
        )
        
        if result['status'] == 'completed':
            print("✓ Blog generation completed successfully")
            print(f"Blog post saved to: {result['blog_path']}")
        else:
            print(f"✗ Blog generation failed: {result['error']}")
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")

async def main():
    """Main function demonstrating workflow features."""
    print("Starting workflow demonstration...")
    
    # Demonstrate base workflow
    await demonstrate_base_workflow()
    
    # Demonstrate video workflow
    await demonstrate_video_workflow()
    
    # Demonstrate blog workflow
    await demonstrate_blog_workflow()
    
    print("\nWorkflow demonstration completed!")

if __name__ == "__main__":
    asyncio.run(main()) 