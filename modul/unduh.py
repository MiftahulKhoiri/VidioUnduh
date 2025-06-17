import os
import datetime
import subprocess
from yt_dlp import YoutubeDL
from colorama import init, Fore, Style

init(autoreset=True)


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
            'quiet': True
        }
        opsi_audio = {
            'format': "bestaudio",
            'outtmpl': temp_audio,
            'noplaylist': True,
            'quiet': True
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
            'quiet': False
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
            'quiet': False
        }
        if cookies_path:
            opsi['cookiefile'] = cookies_path
        with YoutubeDL(opsi) as ydl:
            ydl.download([alamat])
        print(Fore.GREEN + "Download Twitter sukses.")
    except Exception as e:
        print(Fore.RED + f"Download Twitter gagal! {e}")
