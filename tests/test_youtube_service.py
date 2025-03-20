"""Tests for the YouTube service module."""
import pytest
from unittest.mock import AsyncMock, patch
from pathlib import Path

from com.brykly.external_integration.youtube import YouTubeAdapter

@pytest.fixture
def youtube_service(test_config_file):
    """Create a YouTube service instance for testing."""
    return YouTubeAdapter(config_path=test_config_file)

@pytest.mark.asyncio
async def test_get_video_info(youtube_service):
    """Test getting video information."""
    with patch('yt_dlp.YoutubeDL') as mock_ydl:
        mock_ydl.return_value.extract_info = AsyncMock(return_value={
            'title': 'Test Video',
            'description': 'Test Description',
            'duration': 120,
            'view_count': 1000,
            'uploader': 'Test Channel'
        })
        
        info = await youtube_service.get_video_info('https://youtube.com/watch?v=test')
        assert info['title'] == 'Test Video'
        assert info['description'] == 'Test Description'
        assert info['duration'] == 120
        assert info['view_count'] == 1000
        assert info['uploader'] == 'Test Channel'

@pytest.mark.asyncio
async def test_download_video(youtube_service):
    """Test downloading a video."""
    with patch('yt_dlp.YoutubeDL') as mock_ydl:
        mock_ydl.return_value.download = AsyncMock()
        output_path = 'output.mp4'
        result = await youtube_service.download_video('https://youtube.com/watch?v=test', output_path)
        assert result == output_path
        assert Path(output_path).exists()

@pytest.mark.asyncio
async def test_get_video_info_error(youtube_service):
    """Test error handling in get_video_info."""
    test_error = Exception('Test error')
    youtube_service._mock_error = test_error
    with pytest.raises(Exception) as exc_info:
        await youtube_service.get_video_info('https://youtube.com/watch?v=test')
    assert str(exc_info.value) == 'Test error' 