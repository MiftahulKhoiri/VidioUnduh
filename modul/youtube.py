import os
from yt_dlp import YoutubeDL
from colorama import init, Fore, Style
from unduh import (print_progress_bar,yt_progress_hook,nama_file_unik,safe_filename,cek_file_dan_konfirmasi,tanggal_hari_ini)

init(autoreset=True)
NAMA_FOLDER = "VidioDownload"
os.makedirs(NAMA_FOLDER, exist_ok=True)

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