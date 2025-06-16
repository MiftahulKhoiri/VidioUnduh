import os
import datetime
import subprocess
from yt_dlp import YoutubeDL
from colorama import init, Fore, Style

init(autoreset=True)

NAMA_FOLDER = 'VidioDownload'

def buat_folder_unduhan():
    """Membuat folder penyimpanan hasil unduhan jika belum ada."""
    if not os.path.exists(NAMA_FOLDER):
        os.makedirs(NAMA_FOLDER)

def nama_berkas_hasil(judul, ekstensi):
    """Membuat nama file hasil unduhan agar tidak duplikat dan diberi tanggal."""
    sekarang = datetime.datetime.now()
    tanggal = sekarang.strftime("%d%m")
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

def tampilkan_menu_utama():
    """Menampilkan menu utama dengan tampilan menarik dan warna."""
    print(Fore.CYAN + "\n" + "="*44)
    print(Fore.MAGENTA + Style.BRIGHT + "     Selamat Datang di " + Fore.YELLOW + "VidioUnduh")
    print(Fore.CYAN + "="*44)
    print(Fore.BLUE + " 1.", Fore.WHITE + "Youtube :")
    print(Fore.BLUE + " 2.", Fore.WHITE + "Facebook :")
    print(Fore.BLUE + " 3.", Fore.WHITE + "Twitter/X :")
    print(Fore.RED + " 0. Keluar :")
    print(Fore.CYAN + "="*44)

def menu_utama():
    """Menu utama aplikasi unduhan video."""
    buat_folder_unduhan()
    while True:
        tampilkan_menu_utama()
        sumber = input(Fore.YELLOW + " Pilih sumber (1/2/3/0): ").strip()
        if sumber == "0":
            print(Fore.GREEN + "\nTerima kasih telah menggunakan VidioUnduh!\n")
            break
        elif sumber in ["1", "2", "3"]:
            while True:
                print(Fore.MAGENTA + "\nPilih mode unduhan:")
                print(Fore.BLUE + " 1. Unduh 1 video")
                print(Fore.BLUE + " 2. Unduh banyak video")
                print(Fore.RED + " 0. Kembali ke menu utama")
                mode = input(Fore.YELLOW + " Pilih mode (1/2/0): ").strip().lower()
                if mode == "0":
                    break
                elif mode not in ["1", "2"]:
                    print(Fore.RED + "Pilihan tidak dikenali. Silakan ulangi.")
                    continue
                daftar_url = []
                if mode == "2":
                    print(Fore.MAGENTA + "\nMasukkan alamat video satu per satu, tekan Enter tanpa input untuk mulai unduhan otomatis.")
                    while True:
                        alamat = input(Fore.YELLOW + " URL: ").strip()
                        if alamat == "":
                            break
                        daftar_url.append(alamat)
                else:
                    alamat = input(Fore.YELLOW + "\nMasukkan URL video: ").strip()
                    if alamat:
                        daftar_url.append(alamat)
                if not daftar_url:
                    print(Fore.RED + "Tidak ada URL yang dimasukkan.")
                    continue
                resolusi = input(Fore.YELLOW + "Pilih resolusi (misal: 720), kosongkan untuk terbaik: ").strip()
                if not resolusi:
                    resolusi = None
                if sumber == "1":  # Youtube
                    for alamat in daftar_url:
                        unduh_video_audio_terpisah(alamat, resolusi)
                elif sumber == "2":  # Facebook
                    cookies = input(Fore.YELLOW + "Masukkan path cookies.txt (atau kosongkan jika tidak perlu): ").strip()
                    for alamat in daftar_url:
                        unduh_facebook(alamat, cookies_path=cookies if cookies else None, resolusi=resolusi)
                elif sumber == "3":  # Twitter/X
                    cookies = input(Fore.YELLOW + "Masukkan path cookies.txt (atau kosongkan jika tidak perlu): ").strip()
                    for alamat in daftar_url:
                        unduh_twitter(alamat, cookies_path=cookies if cookies else None, resolusi=resolusi)
                print(Fore.GREEN + "\nUnduhan selesai untuk semua video yang didaftar.\n")
        else:
            print(Fore.RED + "Pilihan tidak dikenali. Silakan ulangi.")