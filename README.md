# Video Downloader

A simple video downloader with MP3 conversion support. Download videos and audio from YouTube, Twitter, TikTok, Reddit, and many other platforms.

![Python](https://img.shields.io/badge/Python-3.7+-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Platform](https://img.shields.io/badge/Platform-Windows-blue)

## Features

- 🎬 Download videos from multiple platforms
- 🎵 Convert audio to MP3 automatically  
- 🌙 Modern dark theme interface
- ⚡ Fast and reliable downloads
- 📦 Self-contained (includes FFmpeg)

## Installation & Usage

### Download Source Code
1. Click the green "Code" button above
2. Select "Download ZIP" 
3. Extract the ZIP file
4. Follow the setup instructions below

### Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the application
python video_downloader.py
```

### Building Your Own Executable (Optional)
If you want to create a standalone .exe file:
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable with FFmpeg included
pyinstaller --onefile --windowed --name "VideoDownloader" --add-binary "ffmpeg.exe;." video_downloader.py
```

## How to Use

1. Run `python video_downloader.py`
2. Paste a video URL in the input field
3. Choose **⭐ auto** for video or **🎵 audio** for MP3
4. Select your download folder
5. Click **📥 paste** to start download

## Supported Platforms

- YouTube (youtube.com, youtu.be)
- Twitter/X (twitter.com, x.com) 
- TikTok (tiktok.com)
- Reddit (reddit.com)
- And many more...

## Requirements

- Python 3.7 or higher
- Windows 10/11
- Internet connection
- FFmpeg (included in repository)

## File Structure

```
video-downloader/
├── video_downloader.py    # Main application
├── requirements.txt       # Python dependencies  
├── ffmpeg.exe            # Audio conversion tool
├── build_exe.bat         # Build executable script
└── setup_ffmpeg.bat      # FFmpeg setup helper
```

## Troubleshooting

**MP3 conversion not working?**
- Make sure `ffmpeg.exe` is in the same folder as the Python script
- Run `setup_ffmpeg.bat` to verify FFmpeg setup

**Download failing?**
- Check your internet connection
- Some sites may block downloads - this is normal
- Try a different video URL

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter issues, please [open an issue](https://github.com/Armata-AI/video-downloader/issues) on GitHub.

---

**Made with ❤️ by Armata AI**