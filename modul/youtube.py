import os
import subprocess
import re
import sys
from yt_dlp import YoutubeDL
from colorama import init, Fore, Style
from unduh import (print_progress_bar, yt_progress_hook, nama_file_unik, safe_filename, cek_file_dan_konfirmasi, tanggal_hari_ini)

init(autoreset=True)
NAMA_FOLDER = "VidioDownload"
# os.makedirs(NAMA_FOLDER, exist_ok=True)

def hapus_file_sementara(*file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(Fore.RED + f"Gagal menghapus file sementara {file_path}: {e}")

def tampilkan_progress_ffmpeg(perintah):
    # Jalankan ffmpeg dan tampilkan progress time di terminal
    proses = subprocess.Popen(perintah, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    regex_time = re.compile(r'time=(\d+:\d+:\d+\.\d+)')
    for line in proses.stdout:
        line = line.strip()
        match = regex_time.search(line)
        if match:
            sys.stdout.write(f"\rProgress ffmpeg: {match.group(1)}")
            sys.stdout.flush()
    proses.wait()
    print()  # Untuk newline setelah selesai
    return proses.returncode

def unduh_video_audio_terpisah(alamat, resolusi=None):
    try:
        temp_video_tpl = "temp_video.%(ext)s"
        temp_audio_tpl = "temp_audio.%(ext)s"

        opsi_video = {
            'format': f"bestvideo[height<={resolusi}]" if resolusi else "bestvideo",
            'outtmpl': temp_video_tpl,
            'noplaylist': True,
            'quiet': True,
            'progress_hooks': [yt_progress_hook],
        }
        opsi_audio = {
            'format': "bestaudio",
            'outtmpl': temp_audio_tpl,
            'noplaylist': True,
            'quiet': True,
            'progress_hooks': [yt_progress_hook],
        }

        print(Fore.YELLOW + "Mengunduh video...")
        with YoutubeDL(opsi_video) as ydl:
            info_video = ydl.extract_info(alamat, download=True)
            video_ext = info_video.get('ext', 'mp4')
            judul = info_video.get('title', 'video')
            temp_video = f"temp_video.{video_ext}"

        print(Fore.YELLOW + "Mengunduh audio...")
        with YoutubeDL(opsi_audio) as ydl:
            info_audio = ydl.extract_info(alamat, download=True)
            audio_ext = info_audio.get('ext', 'm4a')
            temp_audio = f"temp_audio.{audio_ext}"

        tanggal = tanggal_hari_ini()
        nama_file = cek_file_dan_konfirmasi(judul, "mp4", tanggal)
        if not nama_file:
            hapus_file_sementara(temp_video, temp_audio)
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
        # Menggunakan progress ffmpeg secara realtime
        retcode = tampilkan_progress_ffmpeg(perintah)
        if retcode != 0:
            print(Fore.RED + "Terjadi kesalahan saat menggabungkan video dan audio!")
            hapus_file_sementara(temp_video, temp_audio)
            return

        hapus_file_sementara(temp_video, temp_audio)
        print(Fore.GREEN + f"Video hasil gabungan disimpan di: {hasil_output}")
    except Exception as e:
        print(Fore.RED + "Gagal mengunduh atau menggabungkan video/audio!")
        print(Fore.RED + f"Detail error: {e}")
        try:
            hapus_file_sementara(temp_video, temp_audio)
        except:
            pass