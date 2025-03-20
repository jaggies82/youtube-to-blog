"""Output management module."""

import os
from datetime import datetime
from typing import Dict, Any
from pathlib import Path
import markdown
import jinja2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .content_generator import BlogPost
import json
import re

class OutputManager:
    """Handles saving blog posts in different formats."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the output manager."""
        self.config = config
        self.base_output_dir = Path(config['output']['directory'])
        self.base_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a unique directory for this run
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = self.base_output_dir / timestamp
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for different content types
        self.blog_dir = self.output_dir / "blog"
        self.metadata_dir = self.output_dir / "metadata"
        self.blog_dir.mkdir(exist_ok=True)
        self.metadata_dir.mkdir(exist_ok=True)
        
        # Load templates from package directory
        package_dir = Path(__file__).parent.parent
        self.templates = {}
        for format_name, template_path in config['output']['templates'].items():
            template_dir = package_dir / Path(template_path).parent
            template_name = Path(template_path).name
            self.templates[format_name] = jinja2.Environment(
                loader=jinja2.FileSystemLoader(template_dir),
                autoescape=True
            ).get_template(template_name)
    
    def _sanitize_filename(self, title: str) -> str:
        """Sanitize the title for use in filenames."""
        # Remove special characters and replace spaces with underscores
        sanitized = re.sub(r'[^\w\s-]', '', title)
        sanitized = re.sub(r'[-\s]+', '_', sanitized)
        return sanitized.lower().strip('_')
    
    def _get_filename(self, blog_post: BlogPost, format: str, is_metadata: bool = False) -> str:
        """Generate filename for the blog post or metadata."""
        date_str = datetime.now().strftime("%Y%m%d")
        title_slug = self._sanitize_filename(blog_post.title)
        prefix = "metadata" if is_metadata else "blog_post"
        return f"{prefix}_{title_slug}_{date_str}.{format}"
    
    def save_metadata(self, blog_post: BlogPost) -> str:
        """Save metadata in JSON format."""
        filename = self._get_filename(blog_post, "json", is_metadata=True)
        filepath = self.metadata_dir / filename
        
        metadata = {
            "title": blog_post.title,
            "seo_tags": blog_post.seo_tags,
            "actionable_takeaways": blog_post.actionable_takeaways,
            "generated_at": datetime.now().isoformat()
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            return str(filepath)
        except Exception as e:
            raise RuntimeError(f"Failed to save metadata: {str(e)}")
    
    def save_markdown(self, blog_post: BlogPost) -> str:
        """Save blog post as Markdown."""
        filename = self._get_filename(blog_post, "md")
        filepath = self.blog_dir / filename
        
        try:
            content = self.templates['markdown'].render(
                title=blog_post.title,
                content=blog_post.content
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return str(filepath)
        except Exception as e:
            raise RuntimeError(f"Failed to save markdown: {str(e)}")
    
    def save_html(self, blog_post: BlogPost) -> str:
        """Save blog post as HTML."""
        filename = self._get_filename(blog_post, "html")
        filepath = self.blog_dir / filename
        
        try:
            # Convert markdown to HTML
            html_content = markdown.markdown(blog_post.content)
            
            content = self.templates['html'].render(
                title=blog_post.title,
                content=html_content
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return str(filepath)
        except Exception as e:
            raise RuntimeError(f"Failed to save HTML: {str(e)}")
    
    def save_pdf(self, blog_post: BlogPost) -> str:
        """Save blog post as PDF."""
        filename = self._get_filename(blog_post, "pdf")
        filepath = self.blog_dir / filename
        
        try:
            # Render content using template
            content = self.templates['pdf'].render(
                title=blog_post.title,
                content=blog_post.content
            )
            
            # Create PDF
            c = canvas.Canvas(str(filepath), pagesize=letter)
            width, height = letter
            
            # Add title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, blog_post.title)
            
            # Add content
            c.setFont("Helvetica", 12)
            y = height - 100
            for line in content.split('\n'):
                if y < 50:  # Start new page if near bottom
                    c.showPage()
                    y = height - 50
                c.drawString(50, y, line)
                y -= 20
            
            c.save()
            return str(filepath)
        except Exception as e:
            raise RuntimeError(f"Failed to save PDF: {str(e)}")
    
    def save_all_formats(self, blog_post: BlogPost) -> Dict[str, str]:
        """Save blog post in all configured formats."""
        results = {}
        
        # Save metadata first
        results['metadata'] = self.save_metadata(blog_post)
        
        # Save blog content in different formats
        for format in self.config['output']['formats']:
            if format == 'markdown':
                results['markdown'] = self.save_markdown(blog_post)
            elif format == 'html':
                results['html'] = self.save_html(blog_post)
            elif format == 'pdf':
                results['pdf'] = self.save_pdf(blog_post)
        
        return results 