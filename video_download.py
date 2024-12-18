import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp as yt
import re  # Import the regex module to clean the string

# Function to update progress bar
def progress_hook(d):
    if d['status'] == 'downloading':
        # Extract percentage of progress and clean the string from any color codes
        percentage = d['_percent_str'].strip().replace('%', '')
        clean_percentage = re.sub(r'\x1b\[[0-9;]*m', '', percentage)  # Remove ANSI escape codes
        try:
            progress_var.set(float(clean_percentage))
        except ValueError:
            pass  # If the conversion fails, ignore the error
    elif d['status'] == 'finished':
        progress_var.set(100)
        messagebox.showinfo("Sucesso", "Vídeo baixado com sucesso!")

# Function to download the video
def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Erro", "Por favor, insira uma URL válida.")
        return
    
    download_dir = './'  # Modify to your desired directory
    
    # Video format options with progress hook
    ydl_opts = {
        'outtmpl': f'{download_dir}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',  # Downloads the best video and audio separately, then combines them
        'progress_hooks': [progress_hook]
    }
    
    # Reset progress bar
    progress_var.set(0)
    
    try:
        with yt.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        messagebox.showerror("Erro", f"Falha no download: {str(e)}")

# UI setup
root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("400x200")

# Label
label = tk.Label(root, text="Insira a URL do vídeo do YouTube:", font=("Arial", 12))
label.pack(pady=10)

# Entry field
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Progress Bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=300)
progress_bar.pack(pady=10)

# Download button
download_btn = tk.Button(root, text="Download", command=download_video, bg="green", fg="white", font=("Arial", 10))
download_btn.pack(pady=10)

# Run the app
root.mainloop()
