# Video Downloader

A simple, modern video downloader with MP3 conversion support. Download videos and audio from YouTube, Twitter, TikTok, Reddit, and many other platforms.

![Video Downloader](https://img.shields.io/badge/Platform-Windows-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Python](https://img.shields.io/badge/Python-3.7+-blue)

## Features

- 🎬 **Multi-platform support**: YouTube, Twitter/X, TikTok, Reddit, and more
- 🎵 **MP3 audio conversion**: Automatic conversion from video to high-quality MP3
- 🌙 **Modern dark theme**: Beautiful, modern interface inspired by professional tools
- 📦 **Self-contained**: No additional software installation required
- ⚡ **Fast downloads**: Optimized for speed and reliability
- 📱 **Simple interface**: Just paste, click, and download

## Download & Installation

### Option 1: Ready-to-use Executable (Recommended)

1. Go to [Releases](https://github.com/AwesomeCodeCreator/video-downloader/releases/latest)
2. Download `VideoDownloader.exe`
3. Run it - that's it! No installation needed.

### Option 2: With Installer (Creates shortcuts)

1. Download the release ZIP from [Releases](https://github.com/AwesomeCodeCreator/video-downloader/releases/latest)
2. Extract the ZIP file
3. Run `Video_Downloader_Installer.bat`
4. Follow the prompts for automatic installation with desktop shortcuts

### Option 3: Run from Source

```bash
git clone https://github.com/AwesomeCodeCreator/video-downloader.git
cd video-downloader
pip install -r requirements.txt
python video_downloader.py
```

## Usage

1. **Launch** the application
2. **Paste** a video URL in the input field
3. **Choose** between video download or audio (MP3) conversion
4. **Select** your download folder
5. **Click** download and wait for completion!

### Supported Formats
- **Video**: MP4 (best quality available)
- **Audio**: MP3 (192kbps, high quality)

### Supported Platforms
- YouTube (youtube.com, youtu.be)
- Twitter/X (twitter.com, x.com)
- TikTok (tiktok.com)
- Reddit (reddit.com)
- And many more supported by yt-dlp

## Screenshots

*Coming soon - will add interface screenshots*

## Requirements

### For Executable Version
- Windows 10/11
- Internet connection
- That's it! Everything else is included.

### For Source Version
- Python 3.7+
- FFmpeg (for MP3 conversion)
- Dependencies listed in `requirements.txt`

## Technical Details

- Built with Python and tkinter for the GUI
- Uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video downloading
- FFmpeg integration for audio conversion
- Self-contained executable built with PyInstaller

## Building from Source

```bash
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name "VideoDownloader" video_downloader.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues, please [open an issue](https://github.com/AwesomeCodeCreator/video-downloader/issues) on GitHub.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the powerful downloading capabilities
- [FFmpeg](https://ffmpeg.org/) for audio conversion
- The open-source community for inspiration and tools

---

**Made with ❤️ by AwesomeCodeCreator**