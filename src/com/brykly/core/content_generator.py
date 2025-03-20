"""Content generation module."""

from typing import Dict, Any, Optional
from dataclasses import dataclass
import json
import requests
from .video_processor import VideoMetadata
import re

@dataclass
class BlogPost:
    """Blog post container."""
    title: str
    content: str
    seo_tags: list[str]
    actionable_takeaways: list[str]

class ContentGenerator:
    """Handles content generation using OpenRouter."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the content generator."""
        self.config = config
        self.api_key = config['api']['openai']['api_key']
        if not self.api_key or self.api_key == "your_openrouter_api_key_here":
            raise ValueError("Please set your OpenRouter API key in the config.yaml file")
        
        self.api_url = config['api']['openai']['api_url']
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/yourusername/agenticFunProject",  # Replace with your actual repo URL
            "Content-Type": "application/json"
        }
    
    def _make_api_request(self, prompt: str) -> str:
        """Make a request to OpenRouter API."""
        payload = {
            "model": self.config['api']['openai']['model'],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.config['api']['openai']['temperature'],
            "max_tokens": self.config['api']['openai']['max_tokens']
        }
        
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()['choices'][0]['message']['content']
    
    def _clean_section_markers(self, text: str) -> str:
        """Remove section markers from text."""
        # Remove [Section] markers
        text = re.sub(r'\[(Title|Content|Tags|Takeaways)\]\s*', '', text)
        # Remove numbered lists
        text = re.sub(r'^\d+\.\s*', '', text, flags=re.MULTILINE)
        return text.strip()
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse the response from the API."""
        try:
            # Split the response into sections
            sections = response.split('\n\n')
            
            # Extract title (first line)
            title = self._clean_section_markers(sections[0].strip())
            
            # Extract content (main body)
            content = '\n\n'.join(sections[1:-2])
            content = self._clean_section_markers(content)
            
            # Extract tags and takeaways (last two sections)
            tags_section = sections[-2] if len(sections) >= 2 else ""
            takeaways_section = sections[-1] if len(sections) >= 1 else ""
            
            # Parse tags and takeaways
            tags = [self._clean_section_markers(tag.strip()) for tag in tags_section.split(',') if tag.strip()]
            takeaways = [self._clean_section_markers(takeaway.strip()) for takeaway in takeaways_section.split('\n') if takeaway.strip()]
            
            return {
                "title": title,
                "content": content,
                "seo_tags": tags,
                "actionable_takeaways": takeaways
            }
        except Exception:
            # If parsing fails, return a simple structure
            return {
                "title": "Blog Post",
                "content": response,
                "seo_tags": [],
                "actionable_takeaways": []
            }
    
    def generate_quick_summary(self, metadata: VideoMetadata) -> BlogPost:
        """Generate a quick summary of the video."""
        prompt = f"""Create a concise blog post summary of this YouTube video:
Title: {metadata.title}
Description: {metadata.description}
Channel: {metadata.channel}

Please write a detailed blog post in the following format:

[Title]
Write a compelling title here.

[Content]
Write a comprehensive blog post that includes:
1. An engaging introduction that hooks the reader
2. A detailed summary of the main points and insights
3. Real examples and practical applications
4. A conclusion that ties everything together
5. A "Key Takeaways" section at the end with 3-5 actionable insights

[Tags]
List 3-5 relevant SEO tags, separated by commas.

[Takeaways]
List 3-5 actionable takeaways, one per line."""

        result = self._make_api_request(prompt)
        parsed = self._parse_response(result)
        
        return BlogPost(
            title=parsed.get('title', metadata.title),
            content=parsed.get('content', result),
            seo_tags=parsed.get('seo_tags', ["youtube", "summary", metadata.channel]),
            actionable_takeaways=parsed.get('actionable_takeaways', ["Watch the video for more details"])
        )
    
    def generate_detailed_review(self, metadata: VideoMetadata) -> BlogPost:
        """Generate a detailed review of the video."""
        prompt = f"""Create a comprehensive, long-form blog post about this YouTube video:
Title: {metadata.title}
Description: {metadata.description}
Channel: {metadata.channel}
Transcript: {metadata.transcript if metadata.transcript else 'No transcript available'}

Please write a detailed blog post in the following format:

[Title]
Write a compelling, SEO-friendly title here.

[Content]
Write a comprehensive blog post that includes:
1. An engaging introduction that hooks the reader and sets up the key themes
2. Multiple sections covering different aspects of the content:
   - Main concepts and theories
   - Real-world examples and applications
   - Personal insights and reflections
   - Practical tips and strategies
3. In-depth analysis of key points with supporting evidence
4. Connections to broader themes and implications
5. A strong conclusion that summarizes the main points
6. A "Key Takeaways" section at the end with 5-7 actionable insights

Make the content engaging, well-structured, and easy to follow. Use subheadings to break up the content and make it more readable.

[Tags]
List 5-7 relevant SEO tags, separated by commas.

[Takeaways]
List 5-7 actionable takeaways, one per line."""

        result = self._make_api_request(prompt)
        parsed = self._parse_response(result)
        
        return BlogPost(
            title=parsed.get('title', metadata.title),
            content=parsed.get('content', result),
            seo_tags=parsed.get('seo_tags', ["youtube", "review", "analysis", metadata.channel]),
            actionable_takeaways=parsed.get('actionable_takeaways', ["Watch the video for more details"])
        ) 