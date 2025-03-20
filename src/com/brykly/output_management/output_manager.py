from pathlib import Path
from typing import Any, Dict, Optional
import markdown
from jinja2 import Environment, FileSystemLoader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from ..config.configuration_manager import ConfigurationManager
from ..utils.logger import Logger

class OutputManager:
    """Manages output formatting and storage."""

    def __init__(self, config_manager: Optional[ConfigurationManager] = None):
        """Initialize the output manager.
        
        Args:
            config_manager: Optional configuration manager instance. If not provided,
                          a new instance will be created.
        """
        self.config_manager = config_manager or ConfigurationManager()
        self.logger = Logger()
        self.output_config = self.config_manager.get_output_config()
        self._setup_templates()

    def _setup_templates(self) -> None:
        """Setup Jinja2 templates."""
        template_dir = Path(__file__).parent.parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))

    def format(self, blog_post: Dict[str, Any], format_type: str) -> str:
        """Format blog post content into specified format."""
        try:
            if format_type == "markdown":
                return self._format_markdown(blog_post)
            elif format_type == "html":
                return self._format_html(blog_post)
            elif format_type == "pdf":
                return self._format_pdf(blog_post)
            else:
                raise ValueError(f"Unsupported format type: {format_type}")
        except Exception as e:
            self.logger.error(f"Failed to format content: {str(e)}")
            raise

    def save(self, formatted_content: str, output_path: str) -> None:
        """Save formatted content to file."""
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(formatted_content)
            
            self.logger.info(f"Content saved to {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to save content: {str(e)}")
            raise

    def _format_markdown(self, blog_post: Dict[str, Any]) -> str:
        """Format content as Markdown."""
        template = self.env.get_template(self.output_config["templates"]["markdown"])
        return template.render(**blog_post)

    def _format_html(self, blog_post: Dict[str, Any]) -> str:
        """Format content as HTML."""
        template = self.env.get_template(self.output_config["templates"]["html"])
        return template.render(**blog_post)

    def _format_pdf(self, blog_post: Dict[str, Any]) -> str:
        """Format content as PDF."""
        output_path = self._get_output_path(blog_post, "pdf")
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        # Add title
        title = Paragraph(blog_post["title"], styles["Heading1"])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Add content
        content = Paragraph(blog_post["content"], styles["Normal"])
        story.append(content)
        
        # Build PDF
        doc.build(story)
        return output_path

    def _get_output_path(self, blog_post: Dict[str, Any], format_type: str) -> str:
        """Generate output file path based on configuration."""
        output_dir = Path(self.output_config["directory"])
        file_naming = self.output_config["file_naming"]
        
        # Replace placeholders in file naming pattern
        filename = file_naming.format(
            title=blog_post["title"].lower().replace(" ", "_"),
            date=blog_post["metadata"].get("date", "unknown")
        )
        
        return str(output_dir / f"{filename}.{format_type}") 