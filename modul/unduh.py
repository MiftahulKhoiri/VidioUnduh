import os
import sys
import datetime
import subprocess
from yt_dlp import YoutubeDL
from colorama import init, Fore, Style

init(autoreset=True)

# Ganti nama folder output jika perlu
NAMA_FOLDER = "VidioDownload"
os.makedirs(NAMA_FOLDER, exist_ok=True)

# Progress bar warna-warni
def print_progress_bar(percent, width=32, color=Fore.GREEN, msg=""):
    fill_len = int(width * percent // 100)
    empty_len = width - fill_len
    bar = color + '█' * fill_len + Style.RESET_ALL + '░' * empty_len
    progress = f"{percent:6.2f}%"
    sys.stdout.write(f"\r{bar} {progress} {msg}")
    sys.stdout.flush()
    if percent >= 100:
        print()

def yt_progress_hook(status):
    if status['status'] == 'downloading':
        percent = float(status.get('percent', 0.0))
        speed = status.get('speed', 0)
        eta = status.get('eta', 0)
        color = (
            Fore.RED if percent < 33 else
            Fore.YELLOW if percent < 66 else
            Fore.GREEN if percent < 99.99 else
            Fore.CYAN
        )
        msg = f"Speed: {speed/1024:.1f} KB/s ETA: {eta}s"
        print_progress_bar(percent, width=32, color=color, msg=msg)
    elif status['status'] == 'finished':
        print_progress_bar(100, width=32, color=Fore.CYAN, msg="Done!")

def nama_berkas_hasil(judul, ekstensi):
    """Membuat nama file hasil unduhan agar tidak duplikat dan diberi tanggal lengkap (tanggal-bulan-tahun)."""
    sekarang = datetime.datetime.now()
    tanggal = sekarang.strftime("%d-%m-%Y")  # Tanggal-bulan-tahun
    nama_dasar = f"{judul}_{tanggal}.{ekstensi}"
    urutan = 1
    nama_berkas = nama_dasar
    while os.path.exists(os.path.join(NAMA_FOLDER, nama_berkas)):
        nama_berkas = f"{judul}_{tanggal}_{urutan}.{ekstensi}"
        urutan += 1
    return nama_berkas

def unduh_video_audio_terpisah(alamat, resolusi=None):
    """Mengunduh video dan audio terpisah lalu menggabungkannya dengan ffmpeg."""
    try:
        temp_video = "temp_video.mp4"
        temp_audio = "temp_audio.m4a"
        opsi_video = {
            'format': f"bestvideo[height<={resolusi}]" if resolusi else "bestvideo",
            'outtmpl': temp_video,
            'noplaylist': True,
            'quiet': True,
            'progress_hooks': [yt_progress_hook],
        }
        opsi_audio = {
            'format': "bestaudio",
            'outtmpl': temp_audio,
            'noplaylist': True,
            'quiet': True,
            'progress_hooks': [yt_progress_hook],
        }
        print(Fore.YELLOW + "Mengunduh video...")
        with YoutubeDL(opsi_video) as ydl:
            info = ydl.extract_info(alamat, download=True)
            judul = info.get('title', 'video')
        print(Fore.YELLOW + "Mengunduh audio...")
        with YoutubeDL(opsi_audio) as ydl:
            ydl.download([alamat])
        nama_berkas = nama_berkas_hasil(judul, "mp4")
        hasil_output = os.path.join(NAMA_FOLDER, nama_berkas)
        print(Fore.CYAN + "Menggabungkan video dan audio dengan ffmpeg...")
        perintah = [
            'ffmpeg', '-y',
            '-i', temp_video,
            '-i', temp_audio,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-strict', 'experimental',
            hasil_output
        ]
        proses = subprocess.run(perintah, capture_output=True, text=True)
        if proses.returncode != 0:
            print(Fore.RED + "Terjadi kesalahan saat menggabungkan video dan audio!")
            print(proses.stderr)
            return
        os.remove(temp_video)
        os.remove(temp_audio)
        print(Fore.GREEN + f"Video hasil gabungan disimpan di: {hasil_output}")
    except Exception as e:
        print(Fore.RED + "Gagal mengunduh atau menggabungkan video/audio!")
        print(Fore.RED + f"Detail error: {e}")

def unduh_facebook(alamat, cookies_path=None, resolusi=None):
    """Mengunduh video dari Facebook. Bisa menggunakan cookies jika video private/protected."""
    try:
        opsi = {
            'format': f"bestvideo[height<={resolusi}]+bestaudio/best[height<={resolusi}]" if resolusi else "bestvideo+bestaudio/best",
            'outtmpl': os.path.join(NAMA_FOLDER, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': False,
            'progress_hooks': [yt_progress_hook],
        }
        if cookies_path:
            opsi['cookiefile'] = cookies_path
        with YoutubeDL(opsi) as ydl:
            ydl.download([alamat])
        print(Fore.GREEN + "Download Facebook sukses.")
    except Exception as e:
        print(Fore.RED + f"Download Facebook gagal! {e}")

def unduh_twitter(alamat, cookies_path=None, resolusi=None):
    """Mengunduh video dari Twitter/X. Bisa menggunakan cookies jika video dari akun private/protected."""
    try:
        opsi = {
            'format': f"bestvideo[height<={resolusi}]+bestaudio/best[height<={resolusi}]" if resolusi else "bestvideo+bestaudio/best",
            'outtmpl': os.path.join(NAMA_FOLDER, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': False,
            'progress_hooks': [yt_progress_hook],
        }
        if cookies_path:
            opsi['cookiefile'] = cookies_path
        with YoutubeDL(opsi) as ydl:
            ydl.download([alamat])
        print(Fore.GREEN + "Download Twitter sukses.")
    except Exception as e:
        print(Fore.RED + f"Download Twitter gagal! {e}")
