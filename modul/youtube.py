import os
import sys
import datetime
import subprocess
from colorama import init, Fore, Style
from yt_dlp import YoutubeDL

init(autoreset=True)
NAMA_FOLDER = "VideoDownload"
os.makedirs(NAMA_FOLDER, exist_ok=True)

def tampilkan_pilihan_kualitas(info_video):
    """
    Menampilkan daftar kualitas video yang tersedia dan meminta input pengguna
    Mengembalikan format_id yang dipilih
    """
    print("\n" + Fore.CYAN + "Pilihan Kualitas Video:")
    
    # Dapatkan semua format video yang tersedia
    formats = info_video.get('formats', [])
    video_formats = []
    
    # Filter hanya format video (ada 'height' dan 'ext')
    for f in formats:
        if f.get('height') and f.get('ext'):
            video_formats.append(f)
    
    # Urutkan dari kualitas tertinggi ke terendah
    video_formats.sort(key=lambda x: (-x['height'], x['ext']))
    
    # Tampilkan pilihan
    pilihan = {}
    for idx, fmt in enumerate(video_formats, 1):
        res = fmt['height']
        ext = fmt['ext']
        fps = fmt.get('fps', '?')
        note = "(audio only)" if fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none' else ""
        print(f"{idx}. {res}p {ext.upper()} {fps}fps {note}")
        pilihan[idx] = fmt['format_id']
    
    # Minta input pengguna
    while True:
        try:
            pilih = int(input("\nPilih kualitas video (nomor): "))
            if pilih in pilihan:
                return pilihan[pilih]
            else:
                print(Fore.RED + "Pilihan tidak valid!")
        except ValueError:
            print(Fore.RED + "Masukkan angka saja!")

def unduh_video_audio_terpisah(alamat):
    """
    Fungsi utama untuk mendownload video dengan pilihan kualitas
    """
    temp_video = None
    temp_audio = None
    
    try:
        # Langkah 1: Dapatkan info video terlebih dahulu untuk pilihan kualitas
        with YoutubeDL({'quiet': True}) as ydl:
            info_video = ydl.extract_info(alamat, download=False)
            judul = info_video.get('title', 'video')
            
            # Tampilkan pilihan kualitas
            format_id = tampilkan_pilihan_kualitas(info_video)
        
        # Template nama file sementara
        temp_video_tpl = "temp_video.%(ext)s"
        temp_audio_tpl = "temp_audio.%(ext)s"

        # Konfigurasi untuk download video dengan kualitas terpilih
        opsi_video = {
            'format': format_id,
            'outtmpl': temp_video_tpl,
            'progress_hooks': [yt_progress_hook],
        }
        
        # Konfigurasi untuk download audio terbaik
        opsi_audio = {
            'format': 'bestaudio',
            'outtmpl': temp_audio_tpl,
            'progress_hooks': [yt_progress_hook],
        }

        # Langkah 2: Download video dengan kualitas terpilih
        print(Fore.YELLOW + "\nMengunduh video...")
        with YoutubeDL(opsi_video) as ydl:
            ydl.download([alamat])
            temp_video = f"temp_video.{info_video['ext']}"

        # Langkah 3: Download audio terpisah
        print(Fore.YELLOW + "\nMengunduh audio...")
        with YoutubeDL(opsi_audio) as ydl:
            ydl.download([alamat])
            temp_audio = "temp_audio.m4a"

        # Langkah 4: Konfirmasi nama file output
        tanggal = tanggal_hari_ini()
        nama_file = cek_file_dan_konfirmasi(judul, "mp4", tanggal)
        if not nama_file:
            return  # Jika user membatalkan

        # Langkah 5: Gabungkan video dan audio
        hasil_output = os.path.join(NAMA_FOLDER, nama_file)
        print(Fore.CYAN + "\nMenggabungkan video dan audio...")
        
        perintah_ffmpeg = [
            'ffmpeg', '-y',
            '-i', temp_video,
            '-i', temp_audio,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-strict', 'experimental',
            hasil_output
        ]
        
        try:
            subprocess.run(perintah_ffmpeg, check=True, 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
            print(Fore.GREEN + f"\nDownload selesai! File tersimpan di: {hasil_output}")
        except subprocess.CalledProcessError as e:
            print(Fore.RED + "\nGagal menggabungkan video dan audio!")
            print(Fore.RED + f"Error: {e.stderr.decode('utf-8')}")
            
    except Exception as e:
        print(Fore.RED + f"\nTerjadi error: {str(e)}")
    finally:
        # Bersihkan file temporary
        for temp_file in [temp_video, temp_audio]:
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)

# Fungsi-fungsi pendukung lainnya tetap sama seperti sebelumnya
# (tanggal_hari_ini, safe_filename, nama_file_unik, 
#  cek_file_dan_konfirmasi, print_progress_bar, yt_progress_hook)