import os
import sys
import subprocess

def pasang_dan_cek_modul(nama_file_requirements='requirements.txt'):
    """
    Memasang dan mengecek modul-modul yang diperlukan sesuai daftar pada requirements.txt.
    Jika modul belum terpasang, maka akan diinstall otomatis.
    """
    print("\n\033[1;36m=== Pengecekan Modul yang Dibutuhkan ===\033[0m")
    print("\033[1;34mSedang memeriksa dan memasang modul-modul sesuai requirements...\033[0m")
    try:
        if not os.path.exists(nama_file_requirements):
            print(f"\033[1;31mFile {nama_file_requirements} tidak ditemukan.\033[0m")
            return

        with open(nama_file_requirements, 'r') as f:
            modul_modul = [baris.strip() for baris in f if baris.strip() and not baris.startswith('#')]

        for modul in modul_modul:
            try:
                nama_modul = modul.split('==')[0].split('>=')[0].split('<=')[0]
                __import__(nama_modul)
                print(f"\033[1;32m✔ Modul [{modul}] sudah terpasang.\033[0m")
            except ImportError:
                print(f"\033[1;33m✖ Modul [{modul}] belum terpasang. Memasang...\033[0m")
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', modul])
                    print(f"\033[1;32m✔ Modul [{modul}] berhasil dipasang.\033[0m")
                except Exception as e:
                    print(f"\033[1;31mGagal memasang modul [{modul}]: {e}\033[0m")
    except Exception as e:
        print(f"\033[1;31mTerjadi kesalahan saat memproses file requirements: {e}\033[0m")

def buat_folder_vidio_download(nama_folder='VidioDownload'):
    """
    Membuat folder dengan nama yang diberikan jika belum ada.
    """
    print("\n\033[1;36m=== Pengecekan Folder Download ===\033[0m")
    try:
        if not os.path.exists(nama_folder):
            os.makedirs(nama_folder)
            print(f"\033[1;32m✔ Folder [{nama_folder}] berhasil dibuat.\033[0m")
        else:
            print(f"\033[1;34mℹ Folder [{nama_folder}] sudah ada.\033[0m")
    except Exception as e:
        print(f"\033[1;31mTerjadi kesalahan saat membuat folder: {e}\033[0m")

def cek_modul_dan_folder():
    """
    Mengecek dan memasang modul yang diperlukan serta membuat folder VidioDownload.
    Fungsi ini dapat diimpor oleh script lain.
    """
    pasang_dan_cek_modul()
    buat_folder_vidio_download()