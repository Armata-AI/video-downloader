#!/usr/bin/env python3
"""
Universal Video Downloader - Dark Theme GUI Version
Downloads MP4 videos and MP3 audio from various platforms with a modern dark GUI interface.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
from pathlib import Path
import yt_dlp
from urllib.parse import urlparse
import re


class VideoDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Downloader")
        self.root.geometry("700x650")
        self.root.resizable(True, True)
        
        # Dark theme colors inspired by Cobolt tools
        self.colors = {
            'bg': '#1a1a1a',           # Dark background
            'card_bg': '#2d2d2d',      # Card/panel background
            'input_bg': '#3a3a3a',     # Input field background
            'text': '#ffffff',         # White text
            'text_secondary': '#b3b3b3', # Gray secondary text
            'accent': '#4a9eff',       # Blue accent
            'accent_hover': '#357abd', # Darker blue on hover
            'success': '#4ade80',      # Green for success
            'border': '#404040'        # Border color
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['bg'])
        
        # Variables
        self.output_dir = tk.StringVar(value=str(Path.cwd() / "downloads"))
        self.quality = tk.StringVar(value="best")
        self.downloading = False
        
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        # Configure ttk styles for dark theme
        style = ttk.Style()
        
        # Configure frame styles
        style.configure('Dark.TFrame', background=self.colors['bg'])
        style.configure('Card.TFrame', background=self.colors['card_bg'], relief='flat')
        
        # Configure label styles
        style.configure('Title.TLabel', 
                       background=self.colors['bg'], 
                       foreground=self.colors['text'],
                       font=('Arial', 24, 'bold'))
        style.configure('Heading.TLabel', 
                       background=self.colors['bg'], 
                       foreground=self.colors['text'],
                       font=('Arial', 12, 'bold'))
        style.configure('Dark.TLabel', 
                       background=self.colors['bg'], 
                       foreground=self.colors['text_secondary'],
                       font=('Arial', 10))
        style.configure('Card.TLabel', 
                       background=self.colors['card_bg'], 
                       foreground=self.colors['text_secondary'],
                       font=('Arial', 10))
        
        # Configure entry styles
        style.configure('Dark.TEntry',
                       fieldbackground=self.colors['input_bg'],
                       background=self.colors['input_bg'],
                       foreground=self.colors['text'],
                       bordercolor=self.colors['border'],
                       lightcolor=self.colors['border'],
                       darkcolor=self.colors['border'],
                       relief='flat',
                       borderwidth=1)
        style.map('Dark.TEntry',
                 focuscolor=[('!focus', self.colors['border']),
                           ('focus', self.colors['accent'])])
        
        # Configure button styles
        style.configure('Accent.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       font=('Arial', 12, 'bold'),
                       relief='flat',
                       borderwidth=0)
        style.map('Accent.TButton',
                 background=[('active', self.colors['accent_hover']),
                           ('pressed', self.colors['accent_hover'])])
        
        style.configure('Dark.TButton',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text'],
                       font=('Arial', 10),
                       relief='flat',
                       borderwidth=1,
                       bordercolor=self.colors['border'])
        style.map('Dark.TButton',
                 background=[('active', self.colors['input_bg']),
                           ('pressed', self.colors['input_bg'])])
        
        # Configure radiobutton styles
        style.configure('Dark.TRadiobutton',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text'],
                       focuscolor=self.colors['accent'],
                       font=('Arial', 10))
        
        # Configure progressbar styles
        style.configure('Dark.Horizontal.TProgressbar',
                       background=self.colors['accent'],
                       troughcolor=self.colors['input_bg'],
                       lightcolor=self.colors['accent'],
                       darkcolor=self.colors['accent'])
    
    def setup_ui(self):
        # Main container with dark background
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Configure grid weights
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Central logo/icon area (mimicking cobolt's centered design)
        header_frame = tk.Frame(main_container, bg=self.colors['bg'])
        header_frame.pack(pady=(0, 40))
        
        # Title with modern styling
        title_label = ttk.Label(header_frame, text="🎬", style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(header_frame, text="Video Downloader", style='Title.TLabel')
        subtitle_label.pack()
        
        # Main card container (like cobolt's central input area)
        card_container = tk.Frame(main_container, bg=self.colors['bg'])
        card_container.pack(fill='both', expand=True)
        card_container.columnconfigure(0, weight=1)
        card_container.rowconfigure(1, weight=1)
        
        # URL input card (main focal point)
        url_card = tk.Frame(card_container, bg=self.colors['card_bg'], relief='flat', bd=0)
        url_card.pack(fill='x', pady=(0, 30))
        
        # URL input with placeholder-like styling
        url_inner = tk.Frame(url_card, bg=self.colors['card_bg'])
        url_inner.pack(fill='x', padx=25, pady=25)
        
        self.url_entry = tk.Entry(url_inner, 
                                 bg=self.colors['input_bg'], 
                                 fg=self.colors['text_secondary'],
                                 font=('Arial', 14),
                                 relief='flat',
                                 bd=0,
                                 insertbackground=self.colors['text'])
        self.url_entry.pack(fill='x', ipady=15, padx=5)
        
        # Add placeholder text
        self.url_entry.insert(0, "paste the link here")
        self.url_entry.bind('<FocusIn>', self.on_url_focus_in)
        self.url_entry.bind('<FocusOut>', self.on_url_focus_out)
        
        # Options card (like cobolt's option buttons)
        options_card = tk.Frame(card_container, bg=self.colors['card_bg'], relief='flat', bd=0)
        options_card.pack(fill='x', pady=(0, 30))
        
        options_inner = tk.Frame(options_card, bg=self.colors['card_bg'])
        options_inner.pack(fill='x', padx=25, pady=20)
        
        # Quality buttons (styled like cobolt's option buttons)
        quality_frame = tk.Frame(options_inner, bg=self.colors['card_bg'])
        quality_frame.pack(fill='x', pady=(0, 15))
        
        self.quality_buttons = []
        qualities = [('⭐ auto', 'best'), ('🎵 audio', 'audio'), ('🔇 mute', 'worst')]
        
        for i, (text, value) in enumerate(qualities):
            btn = tk.Button(quality_frame, 
                           text=text,
                           bg=self.colors['input_bg'] if value == 'best' else self.colors['card_bg'],
                           fg=self.colors['text'],
                           font=('Arial', 10),
                           relief='flat',
                           bd=0,
                           command=lambda v=value: self.set_quality(v))
            btn.pack(side='left', padx=(0, 10), pady=5, ipadx=15, ipady=8)
            self.quality_buttons.append((btn, value))
        
        # Output directory
        output_frame = tk.Frame(options_inner, bg=self.colors['card_bg'])
        output_frame.pack(fill='x', pady=(0, 15))
        output_frame.columnconfigure(0, weight=1)
        
        ttk.Label(output_frame, text="Download folder:", style='Card.TLabel').pack(anchor='w', pady=(0, 5))
        
        output_input_frame = tk.Frame(output_frame, bg=self.colors['card_bg'])
        output_input_frame.pack(fill='x')
        output_input_frame.columnconfigure(0, weight=1)
        
        self.output_entry = tk.Entry(output_input_frame,
                                    textvariable=self.output_dir,
                                    bg=self.colors['input_bg'],
                                    fg=self.colors['text'],
                                    font=('Arial', 10),
                                    relief='flat',
                                    bd=0,
                                    insertbackground=self.colors['text'])
        self.output_entry.pack(side='left', fill='x', expand=True, ipady=8, padx=(0, 10))
        
        browse_btn = tk.Button(output_input_frame,
                              text="Browse",
                              bg=self.colors['input_bg'],
                              fg=self.colors['text'],
                              font=('Arial', 10),
                              relief='flat',
                              bd=0,
                              command=self.browse_output_dir)
        browse_btn.pack(side='right', padx=5, pady=5, ipadx=10, ipady=5)
        
        # Download button (like cobolt's main action button)
        download_frame = tk.Frame(options_inner, bg=self.colors['card_bg'])
        download_frame.pack(fill='x')
        
        self.download_btn = tk.Button(download_frame,
                                     text="📥 paste",
                                     bg=self.colors['accent'],
                                     fg='white',
                                     font=('Arial', 12, 'bold'),
                                     relief='flat',
                                     bd=0,
                                     command=self.start_download)
        self.download_btn.pack(side='right', padx=5, pady=5, ipadx=20, ipady=10)
        
        # Progress and status card
        status_card = tk.Frame(card_container, bg=self.colors['card_bg'], relief='flat', bd=0)
        status_card.pack(fill='both', expand=True)
        
        status_inner = tk.Frame(status_card, bg=self.colors['card_bg'])
        status_inner.pack(fill='both', expand=True, padx=25, pady=25)
        status_inner.columnconfigure(0, weight=1)
        status_inner.rowconfigure(2, weight=1)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_inner, mode='indeterminate', style='Dark.Horizontal.TProgressbar')
        self.progress.pack(fill='x', pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(status_inner, text="Ready to download", style='Card.TLabel')
        self.status_label.pack(anchor='w', pady=(0, 15))
        
        # Log area with dark theme
        log_frame = tk.Frame(status_inner, bg=self.colors['input_bg'], relief='flat', bd=0)
        log_frame.pack(fill='both', expand=True)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame,
                               bg=self.colors['input_bg'],
                               fg=self.colors['text_secondary'],
                               font=('Consolas', 9),
                               wrap='word',
                               relief='flat',
                               bd=0,
                               selectbackground=self.colors['accent'],
                               insertbackground=self.colors['text'])
        
        scrollbar = tk.Scrollbar(log_frame, orient='vertical', command=self.log_text.yview,
                                bg=self.colors['input_bg'], troughcolor=self.colors['input_bg'])
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky='nsew', padx=(15, 0), pady=15)
        scrollbar.grid(row=0, column=1, sticky='ns', pady=15)
        
        # Bind Enter key to URL entry
        self.url_entry.bind('<Return>', lambda e: self.start_download())
        
        # Focus on URL entry
        self.url_entry.focus()
        
    def on_url_focus_in(self, event):
        if self.url_entry.get() == "paste the link here":
            self.url_entry.delete(0, tk.END)
            self.url_entry.config(fg=self.colors['text'])
            
    def on_url_focus_out(self, event):
        if not self.url_entry.get():
            self.url_entry.insert(0, "paste the link here")
            self.url_entry.config(fg=self.colors['text_secondary'])
            
    def set_quality(self, quality):
        self.quality.set(quality)
        # Update button styling
        for btn, value in self.quality_buttons:
            if value == quality:
                btn.config(bg=self.colors['accent'], fg='white')
            else:
                btn.config(bg=self.colors['input_bg'], fg=self.colors['text'])
        
    def browse_output_dir(self):
        directory = filedialog.askdirectory(initialdir=self.output_dir.get())
        if directory:
            self.output_dir.set(directory)
            
    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def is_valid_url(self, url):
        url_pattern = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None
    
    def get_ffmpeg_path(self):
        """Try to find FFmpeg executable"""
        # Check if running as executable
        if getattr(sys, 'frozen', False):
            # Running as exe, check for bundled ffmpeg
            exe_dir = Path(sys.executable).parent
            ffmpeg_exe = exe_dir / 'ffmpeg.exe'
            if ffmpeg_exe.exists():
                return str(ffmpeg_exe)
        else:
            # Running as script, check local folder
            script_dir = Path(__file__).parent
            ffmpeg_exe = script_dir / 'ffmpeg.exe'
            if ffmpeg_exe.exists():
                return str(ffmpeg_exe)
        
        # Check system PATH for ffmpeg
        import shutil
        ffmpeg_system = shutil.which('ffmpeg')
        if ffmpeg_system:
            return ffmpeg_system
            
        return None
    
    def show_ffmpeg_warning(self):
        """Show user-friendly warning about MP3 conversion"""
        warning_msg = (
            "Audio will be downloaded in the best available format (usually M4A).\n\n"
            "For MP3 conversion, FFmpeg is required but not found.\n"
            "The audio file will still work in most media players.\n\n"
            "To get MP3 files, install the complete version with FFmpeg included."
        )
        messagebox.showwarning("MP3 Conversion Unavailable", warning_msg)
        
    def get_ydl_opts(self, url):
        output_path = Path(self.output_dir.get())
        output_path.mkdir(exist_ok=True)
        
        # Check if audio quality is selected for MP3 extraction
        if self.quality.get() == 'audio':
            # Check if FFmpeg is available
            ffmpeg_path = self.get_ffmpeg_path()
            
            if ffmpeg_path:
                # FFmpeg available - can convert to MP3
                return {
                    'outtmpl': str(output_path / '%(title)s.%(ext)s'),
                    'format': 'bestaudio[ext=mp3]/bestaudio[acodec=mp3]/bestaudio',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                        'nopostoverwrites': False,
                    }],
                    'ffmpeg_location': ffmpeg_path,
                    'writeinfojson': False,
                    'writesubtitles': False,
                    'writeautomaticsub': False,
                }
            else:
                # No FFmpeg - download best audio format available
                self.log_message("⚠️ FFmpeg not found - downloading in best available audio format")
                return {
                    'outtmpl': str(output_path / '%(title)s.%(ext)s'),
                    'format': 'bestaudio/best',
                    'writeinfojson': False,
                    'writesubtitles': False,
                    'writeautomaticsub': False,
                }
        
        # Default video format options
        base_opts = {
            'outtmpl': str(output_path / '%(title)s.%(ext)s'),
            'format': 'best[ext=mp4]/best',
            'writeinfojson': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
        }
        
        domain = urlparse(url).netloc.lower()
        
        if 'youtube.com' in domain or 'youtu.be' in domain:
            base_opts.update({
                'format': 'best[height<=1080][ext=mp4]/best[ext=mp4]/best',
            })
        elif 'twitter.com' in domain or 'x.com' in domain:
            base_opts.update({
                'format': 'best[ext=mp4]/best',
            })
        elif 'reddit.com' in domain:
            base_opts.update({
                'format': 'best[ext=mp4]/best',
            })
        elif 'tiktok.com' in domain:
            base_opts.update({
                'format': 'best[ext=mp4]/best',
            })
        
        return base_opts
        
    def download_video(self):
        url = self.url_entry.get().strip()
        
        # Clear placeholder text
        if url == "paste the link here":
            url = ""
        
        if not url:
            messagebox.showerror("Error", "Please enter a video URL")
            return
            
        if not self.is_valid_url(url):
            messagebox.showerror("Error", f"Invalid URL: {url}")
            return
            
        try:
            self.status_label.config(text="Downloading...")
            self.progress.start()
            self.log_message(f"Starting download from: {url}")
            
            ydl_opts = self.get_ydl_opts(url)
            
            # Custom hook to capture progress
            def progress_hook(d):
                if d['status'] == 'downloading':
                    if 'filename' in d:
                        filename = os.path.basename(d['filename'])
                        self.status_label.config(text=f"Downloading: {filename}")
                elif d['status'] == 'finished':
                    filename = os.path.basename(d['filename'])
                    self.log_message(f"Finished downloading: {filename}")
            
            ydl_opts['progress_hooks'] = [progress_hook]
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            self.log_message("✅ Download completed successfully!")
            self.status_label.config(text="Download completed!")
            self.download_btn.config(text="✅ Done", bg=self.colors['success'])
            
            # Reset button after 3 seconds
            self.root.after(3000, lambda: self.download_btn.config(text="📥 paste", bg=self.colors['accent']))
            
        except yt_dlp.DownloadError as e:
            error_msg = f"Download error: {str(e)}"
            self.log_message(f"❌ {error_msg}")
            messagebox.showerror("Download Error", error_msg)
            self.status_label.config(text="Download failed")
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.log_message(f"❌ {error_msg}")
            messagebox.showerror("Error", error_msg)
            self.status_label.config(text="Download failed")
            
        finally:
            self.progress.stop()
            self.download_btn.config(state='normal')
            self.downloading = False
            
    def start_download(self):
        if self.downloading:
            return
            
        self.downloading = True
        self.download_btn.config(state='disabled')
        
        # Run download in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self.download_video)
        thread.daemon = True
        thread.start()


def main():
    root = tk.Tk()
    app = VideoDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()