"""Setup configuration for the package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agentic-fun",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A YouTube video content generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/agentic-fun",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
        "yt-dlp>=2023.12.30",
        "youtube-transcript-api>=0.6.1",
        "openai>=1.12.0",
        "aiohttp>=3.9.1",
        "prefect>=2.14.0",
        "markdown>=3.5.1",
        "jinja2>=3.1.2",
        "reportlab>=4.0.8",
        "pillow>=10.2.0",
        "ultralytics>=8.1.0",
        "pytest>=8.0.0",
        "pytest-asyncio>=0.23.5",
        "pytest-cov>=4.1.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "loguru>=0.7.2",
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0"
    ],
    entry_points={
        'console_scripts': [
            'agentic-fun=com.brykly.cli:main',
        ],
    },
) 