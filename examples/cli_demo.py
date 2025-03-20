"""Example script demonstrating command-line interface functionality in the package."""
import os
import sys
import argparse
import asyncio
from pathlib import Path

# Add the package root to the Python path
package_root = Path(__file__).parent.parent
sys.path.append(str(package_root))

from com.brykly.workflow.video import VideoProcessingWorkflow
from com.brykly.workflow.blog import BlogGenerationWorkflow
from com.brykly.utils.config import ConfigManager
from com.brykly.utils.logging_config import setup_logging

def setup_argparse():
    """Set up command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description='Agentic Fun CLI - Process YouTube videos and generate blog posts'
    )
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Process video command
    video_parser = subparsers.add_parser('process-video', help='Process a YouTube video')
    video_parser.add_argument('url', help='YouTube video URL')
    video_parser.add_argument('--output', '-o', help='Output directory for processed files')
    
    # Generate blog command
    blog_parser = subparsers.add_parser('generate-blog', help='Generate a blog post from transcript')
    blog_parser.add_argument('transcript', help='Path to transcript file')
    blog_parser.add_argument('--tone', '-t', default='professional', help='Blog post tone')
    blog_parser.add_argument('--style', '-s', default='comprehensive', help='Blog post style')
    blog_parser.add_argument('--output', '-o', help='Output directory for blog post')
    
    # Configuration options
    parser.add_argument('--config', '-c', default='config.yaml', help='Path to configuration file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    return parser

async def process_video(args, config, logger):
    """Process a YouTube video."""
    try:
        workflow = VideoProcessingWorkflow(args.config)
        logger.info(f"Processing video: {args.url}")
        
        result = await workflow.execute(args.url)
        
        if result['status'] == 'completed':
            logger.info("Video processing completed successfully")
            print(f"✓ Video processed successfully")
            print(f"Transcript saved to: {result['transcript_path']}")
            return result['transcript_path']
        else:
            logger.error(f"Video processing failed: {result['error']}")
            print(f"✗ Video processing failed: {result['error']}")
            return None
            
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}", exc_info=True)
        print(f"✗ Error: {str(e)}")
        return None

async def generate_blog(args, config, logger):
    """Generate a blog post from transcript."""
    try:
        workflow = BlogGenerationWorkflow(args.config)
        logger.info(f"Generating blog post from transcript: {args.transcript}")
        
        result = await workflow.execute(
            transcript_path=args.transcript,
            tone=args.tone,
            style=args.style
        )
        
        if result['status'] == 'completed':
            logger.info("Blog post generation completed successfully")
            print(f"✓ Blog post generated successfully")
            print(f"Blog post saved to: {result['blog_path']}")
        else:
            logger.error(f"Blog post generation failed: {result['error']}")
            print(f"✗ Blog post generation failed: {result['error']}")
            
    except Exception as e:
        logger.error(f"Error generating blog post: {str(e)}", exc_info=True)
        print(f"✗ Error: {str(e)}")

async def main():
    """Main function implementing the command-line interface."""
    # Set up argument parsing
    parser = setup_argparse()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize configuration
    try:
        config = ConfigManager(args.config)
    except Exception as e:
        print(f"✗ Error loading configuration: {str(e)}")
        return
    
    # Setup logging
    log_config = {
        'level': 'DEBUG' if args.verbose else 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file': 'logs/cli.log'
    }
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Setup logger
    logger = setup_logging('cli', log_config)
    
    try:
        if args.command == 'process-video':
            transcript_path = await process_video(args, config, logger)
            
            # If video processing succeeded and user wants to generate blog post
            if transcript_path and input("\nGenerate blog post from transcript? [y/N] ").lower() == 'y':
                args.transcript = transcript_path
                await generate_blog(args, config, logger)
                
        elif args.command == 'generate-blog':
            await generate_blog(args, config, logger)
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        print("\n✗ Operation cancelled")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        print(f"✗ Unexpected error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 