import os
import subprocess
import re
import sys
from yt_dlp import YoutubeDL
from colorama import init, Fore, Style
from unduh import *

init(autoreset=True)
NAMA_FOLDER = "VidioDownload"
os.makedirs(NAMA_FOLDER, exist_ok=True)

def hapus_file_sementara(*file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(Fore.RED + f"Gagal menghapus file sementara {file_path}: {e}")

def get_video_duration(file_path):
    # Ambil durasi video (detik) dengan ffprobe
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return float(result.stdout.strip())
    except Exception:
        return None

def parse_ffmpeg_time(time_str):
    # Ubah string time ffmpeg ke detik
    if not time_str:
        return 0.0
    try:
        h, m, s = time_str.split(':')
        return float(h) * 3600 + float(m) * 60 + float(s)
    except Exception:
        return 0.0

def tampilkan_progress_ffmpeg(perintah, sumber_video):
    total_duration = get_video_duration(sumber_video)
    proses = subprocess.Popen(perintah, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    regex_time = re.compile(r'time=(\d+:\d+:\d+\.\d+)')
    last_percent = -1
    for line in proses.stdout:
        line = line.strip()
        match = regex_time.search(line)
        if match and total_duration:
            now_sec = parse_ffmpeg_time(match.group(1))
            percent = int((now_sec / total_duration) * 100)
            if percent != last_percent:
                sys.stdout.write(f"\rProgress ffmpeg: {percent}%")
                sys.stdout.flush()
                last_percent = percent
    proses.wait()
    print()
    return proses.returncode

def get_video_resolutions(alamat):
    """
    Mengambil daftar resolusi video yang tersedia dari link YouTube.
    """
    with YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(alamat, download=False)
        formats = info.get('formats', [])
        resolutions = []
        for fmt in formats:
            if fmt.get('vcodec', 'none') != 'none' and fmt.get('acodec', 'none') == 'none':
                height = fmt.get('height')
                ext = fmt.get('ext')
                if height:
                    resolutions.append((height, ext))
        # Hilangkan duplikat dan urutkan dari tinggi ke rendah
        resolutions = sorted(list(set(resolutions)), reverse=True)
    return resolutions

def unduh_video_audio_terpisah(alamat, resolusi=None):
    try:
        # Pilih resolusi
        if not resolusi:
            daftar_resolusi = get_video_resolutions(alamat)
            if not daftar_resolusi:
                print(Fore.RED + "Tidak ada opsi resolusi yang ditemukan!")
                return
            print(Fore.CYAN + "Pilihan resolusi video yang tersedia:")
            for i, (height, ext) in enumerate(daftar_resolusi):
                print(f"{i+1}. {height}p ({ext})")
            # Minta input user
            while True:
                pilihan = input("Pilih nomor resolusi yang diinginkan: ")
                if pilihan.isdigit() and 1 <= int(pilihan) <= len(daftar_resolusi):
                    resolusi = daftar_resolusi[int(pilihan)-1][0]
                    break
                else:
                    print("Pilihan tidak valid. Silakan coba lagi.")

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
            return

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
        # Menggunakan progress ffmpeg secara persentase
        retcode = tampilkan_progress_ffmpeg(perintah, temp_video)
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