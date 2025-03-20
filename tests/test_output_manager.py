"""Tests for the output manager module."""
import pytest
from pathlib import Path
from com.brykly.output_management.output_manager import OutputManager

def test_format_markdown(output_manager, sample_blog_post):
    """Test markdown formatting."""
    formatted_content = output_manager.format(sample_blog_post, "markdown")
    
    assert "# Test Blog Post" in formatted_content
    assert "*Published on 2024-03-20*" in formatted_content
    assert "## Metadata" in formatted_content
    assert "Author: Test Author" in formatted_content
    assert "Tags: test, blog" in formatted_content

def test_format_html(output_manager, sample_blog_post):
    """Test HTML formatting."""
    formatted_content = output_manager.format(sample_blog_post, "html")
    
    assert "<!DOCTYPE html>" in formatted_content
    assert "<title>Test Blog Post</title>" in formatted_content
    assert "Published on 2024-03-20" in formatted_content
    assert "Author: Test Author" in formatted_content
    assert "Tags: test, blog" in formatted_content

def test_save_content(output_manager, sample_blog_post, temp_output_dir):
    """Test content saving."""
    # Update output directory in config
    output_manager.output_config["directory"] = temp_output_dir
    
    # Test saving markdown
    markdown_content = output_manager.format(sample_blog_post, "markdown")
    output_path = Path(temp_output_dir) / "test.md"
    output_manager.save(markdown_content, str(output_path))
    
    assert output_path.exists()
    assert markdown_content == output_path.read_text()

    # Test saving HTML
    html_content = output_manager.format(sample_blog_post, "html")
    output_path = Path(temp_output_dir) / "test.html"
    output_manager.save(html_content, str(output_path))
    assert output_path.exists()
    assert html_content == output_path.read_text()

def test_invalid_format(output_manager, sample_blog_post):
    """Test invalid format handling."""
    with pytest.raises(ValueError) as exc_info:
        output_manager.format(sample_blog_post, "invalid")
    assert "Unsupported format type" in str(exc_info.value)

def test_output_path_generation(output_manager, sample_blog_post):
    """Test output path generation."""
    output_path = output_manager._get_output_path(sample_blog_post, "md")
    assert "test_blog_post_2024-03-20.md" in output_path 