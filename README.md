# YouTube to Blog Post Generator

A Python application that converts YouTube videos into well-structured, SEO-friendly blog posts using AI. The application processes YouTube video URLs and generates detailed blog content in multiple formats (Markdown, HTML, PDF) with key takeaways and SEO tags.

## Features

- **Multiple Processing Modes**:
  - Quick Summary Mode: Generate concise blog post summaries
  - Detailed Review Mode: Create comprehensive, long-form blog posts with additional context

- **AI-Powered Content Generation**:
  - Intelligent content structuring
  - SEO-optimized titles and tags
  - Actionable takeaways
  - Engaging introductions and conclusions

- **Multiple Output Formats**:
  - Markdown
  - HTML (with responsive styling)
  - PDF
  - JSON metadata

- **Configurable Settings**:
  - Customizable API endpoints
  - Adjustable content generation parameters
  - Flexible output directory structure

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtube-to-blog.git
cd youtube-to-blog
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the application:
   - Copy `config.yaml.example` to `config.yaml`
   - Add your OpenRouter API key and other configuration settings

## Usage

### Command Line Interface

Basic usage:
```bash
python -m src.com.brykly.cli "YOUR_YOUTUBE_URL"
```

With detailed mode:
```bash
python -m src.com.brykly.cli "YOUR_YOUTUBE_URL" --mode detailed
```

### Output Structure

Generated content is saved in the following structure:
```
output/
├── YYYYMMDD_HHMMSS/
│   ├── blog/
│   │   ├── blog_post_[title]_YYYYMMDD.md
│   │   ├── blog_post_[title]_YYYYMMDD.html
│   │   └── blog_post_[title]_YYYYMMDD.pdf
│   └── metadata/
│       └── metadata_[title]_YYYYMMDD.json
```

## Configuration

Edit `config.yaml` to customize:
- API endpoints and keys
- Content generation parameters
- Output formats and directory structure
- Logging settings

## Development

### Project Structure

```
src/
├── com/
│   └── brykly/
│       ├── core/
│       │   ├── content_generator.py
│       │   ├── output_manager.py
│       │   └── video_processor.py
│       ├── templates/
│       │   ├── blog_post.md.j2
│       │   ├── blog_post.html.j2
│       │   └── blog_post.pdf.j2
│       └── cli.py
├── config.yaml
└── requirements.txt
```

### Running Tests

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python and OpenRouter API
- Uses Jinja2 for templating
- Markdown and HTML generation support
- PDF generation with ReportLab 