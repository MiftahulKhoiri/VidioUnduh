import os
import sys
import datetime
import subprocess
from yt_dlp import YoutubeDL
from colorama import init, Fore, Style

init(autoreset=True)
NAMA_FOLDER = "VidioDownload"
os.makedirs(NAMA_FOLDER, exist_ok=True)

def tanggal_hari_ini():
    return datetime.datetime.now().strftime("%d-%m-%Y")

def safe_filename(name):
    return "".join(c for c in name if c.isalnum() or c in " ._-").rstrip()

def nama_file_unik(judul, ekstensi, tanggal):
    judul = safe_filename(judul)
    nama_dasar = f"{judul}_{tanggal}.{ekstensi}"
    nama_file = nama_dasar
    idx = 1
    while os.path.exists(os.path.join(NAMA_FOLDER, nama_file)):
        if idx == 1:
            nama_file = f"{judul}_{tanggal} (copy).{ekstensi}"
        else:
            nama_file = f"{judul}_{tanggal} (copy {idx}).{ekstensi}"
        idx += 1
    return nama_file

def cek_file_dan_konfirmasi(judul, ekstensi, tanggal):
    nama_file = f"{safe_filename(judul)}_{tanggal}.{ekstensi}"
    path_file = os.path.join(NAMA_FOLDER, nama_file)
    if os.path.exists(path_file):
        jawab = input(
            f"{Fore.YELLOW}File sudah ada: {nama_file}. Lanjutkan download dan simpan dengan nama baru? (y/n): "
        ).lower().strip()
        if jawab == "y":
            return nama_file_unik(judul, ekstensi, tanggal)
        else:
            print(Fore.CYAN + "Download dibatalkan.")
            return None
    else:
        return nama_file

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

def unduh_video_audio_terpisah(alamat, resolusi=None):
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
        tanggal = tanggal_hari_ini()
        nama_file = cek_file_dan_konfirmasi(judul, "mp4", tanggal)
        if not nama_file:
            os.remove(temp_video)
            os.remove(temp_audio)
            return  # Batal
        hasil_output = os.path.join(NAMA_FOLDER, nama_file)
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
    try:
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(alamat, download=False)
            judul = info.get('title', 'facebook_video')
            ekstensi = info.get('ext', 'mp4')
        tanggal = tanggal_hari_ini()
        nama_file = cek_file_dan_konfirmasi(judul, ekstensi, tanggal)
        if not nama_file:
            return  # Batal
        hasil_output = os.path.join(NAMA_FOLDER, nama_file)
        opsi = {
            'format': f"bestvideo[height<={resolusi}]+bestaudio/best[height<={resolusi}]" if resolusi else "bestvideo+bestaudio/best",
            'outtmpl': hasil_output,
            'noplaylist': True,
            'quiet': False,
            'progress_hooks': [yt_progress_hook],
        }
        if cookies_path:
            opsi['cookiefile'] = cookies_path
        with YoutubeDL(opsi) as ydl:
            ydl.download([alamat])
        print(Fore.GREEN + f"Download Facebook sukses. File: {hasil_output}")
    except Exception as e:
        print(Fore.RED + f"Download Facebook gagal! {e}")

def unduh_twitter(alamat, cookies_path=None, resolusi=None):
    try:
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(alamat, download=False)
            judul = info.get('title', 'twitter_video')
            ekstensi = info.get('ext', 'mp4')
        tanggal = tanggal_hari_ini()
        nama_file = cek_file_dan_konfirmasi(judul, ekstensi, tanggal)
        if not nama_file:
            return  # Batal
        hasil_output = os.path.join(NAMA_FOLDER, nama_file)
        opsi = {
            'format': f"bestvideo[height<={resolusi}]+bestaudio/best[height<={resolusi}]" if resolusi else "bestvideo+bestaudio/best",
            'outtmpl': hasil_output,
            'noplaylist': True,
            'quiet': False,
            'progress_hooks': [yt_progress_hook],
        }
        if cookies_path:
            opsi['cookiefile'] = cookies_path
        with YoutubeDL(opsi) as ydl:
            ydl.download([alamat])
        print(Fore.GREEN + f"Download Twitter sukses. File: {hasil_output}")
    except Exception as e:
        print(Fore.RED + f"Download Twitter gagal! {e}")

# Contoh penggunaan:
# unduh_video_audio_terpisah("https://www.youtube.com/watch?v=...")
# unduh_facebook("https://www.facebook.com/...", cookies_path="cookies.txt")
# unduh_twitter("https://twitter.com/...", cookies_path="cookies.txt")