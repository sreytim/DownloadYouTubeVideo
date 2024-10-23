# I choose to do case 2 and 7

import tkinter as tk
from tkinter import ttk
from tkinter import  messagebox
import os
import threading
import yt_dlp


def download_video():
    url = entry_url.get()
    download_type = download_option.get()
    path = "downloads"  # Get custom path or default to 'downloads'
    
    if not os.path.exists(path):
        os.makedirs(path)

    if url:
        try:
            if download_type == "MP4":
                ydl_opts = {
                    'format': 'best[ext=mp4]/mp4',  # Download combined video and audio in MP4 format
                    'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
                    'progress_hooks': [yt_dlp_progress_hook],
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                status_label.config(text="MP4 video download complete!")

            elif download_type == "MP3":
                ydl_opts = {
                    'format': 'bestaudio[ext=m4a]/mp3',  # Download combined audio in MP3 or M4A format
                    'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
                    'progress_hooks': [yt_dlp_progress_hook],
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                status_label.config(text="MP3 audio download complete!")
                

        except Exception as e:
            status_label.config(text=f"Error: {e}")
    else:
        messagebox.showerror("Invalid Input", "Please enter a valid YouTube URL")


def yt_dlp_progress_hook(d):
    if d['status'] == 'finished':
        progress_var.set(100)  # Complete download
        progress_label.config(text="Download complete!")
    elif d['status'] == 'downloading':
        percentage = d['downloaded_bytes'] / d['total_bytes'] * 100
        progress_var.set(percentage)
        progress_label.config(text=f"Downloading... {int(percentage)}%")


def start_download_thread():
        threading.Thread(target=download_video).start()

# Create the main application window
root = tk.Tk()
root.title("YouTube Downloader with Enhanced Features")
root.geometry("600x400")

# Create a label and entry widget for the video URL
url_label = tk.Label(root, text="Enter YouTube URL:")
url_label.pack(pady=10)
entry_url = tk.Entry(root, width=50)
entry_url.pack(pady=5)

# Create a label to display video thumbnail
thumbnail_label = tk.Label(root)
thumbnail_label.pack(pady=10)

# Create download options (MP4 or MP3)
download_option = tk.StringVar(value="MP4")
download_mp4_radio = tk.Radiobutton(root, text="Download MP4 (Video)", variable=download_option, value="MP4")
download_mp3_radio = tk.Radiobutton(root, text="Download MP3 (Audio)", variable=download_option, value="MP3")
download_mp4_radio.pack(pady=5)
download_mp3_radio.pack(pady=5)

# Create a download button
download_button = tk.Button(root, text="Download Video", command=lambda: start_download_thread())
download_button.pack(pady=10)


# Create a progress bar and label
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, fill=tk.X, padx=20)
progress_label = tk.Label(root, text="")
progress_label.pack(pady=5)

# Create a status label to show download status
status_label = tk.Label(root, text="")
status_label.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()