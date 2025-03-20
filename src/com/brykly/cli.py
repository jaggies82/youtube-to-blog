"""Command-line interface for the application."""

import argparse
import sys
from pathlib import Path
from typing import Optional
from .core.app import App
from .utils.logger import Logger

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='YouTube Content Generator')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('--mode', choices=['quick', 'detailed'], default='quick',
                      help='Processing mode (quick or detailed)')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--debug', action='store_true',
                      help='Enable debug logging')
    return parser.parse_args()

def main() -> Optional[int]:
    """Main entry point."""
    args = parse_args()
    logger = Logger()
    
    try:
        # Get the default config path if not provided
        if not args.config:
            args.config = str(Path(__file__).parent / "config" / "config.yaml")
        
        app = App(config_path=args.config)
        app.initialize_paths()
        
        # Process the video
        output_files = app.process_video(args.url, args.mode)
        
        if output_files:
            logger.info("Successfully generated blog post!")
            for format_name, filepath in output_files.items():
                logger.info(f"Saved {format_name} to: {filepath}")
        else:
            logger.error("Failed to generate blog post")
            return 1
        
        return 0
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 