import os
import sys
import subprocess

def pasang_dan_cek_modul(nama_file_requirements='requirements.txt'):
    """
    Memasang dan mengecek modul-modul yang diperlukan sesuai daftar pada requirements.txt.
    Jika modul belum terpasang, maka akan diinstall otomatis.
    """
    try:
        if not os.path.exists(nama_file_requirements):
            print(f"File {nama_file_requirements} tidak ditemukan.")
            return

        with open(nama_file_requirements, 'r') as f:
            modul_modul = [baris.strip() for baris in f if baris.strip() and not baris.startswith('#')]

        for modul in modul_modul:
            try:
                # Mengambil nama modul tanpa versi
                nama_modul = modul.split('==')[0].split('>=')[0].split('<=')[0]
                __import__(nama_modul)
                print(f"Modul [{modul}] sudah terpasang.")
            except ImportError:
                print(f"Modul [{modul}] belum terpasang. Memasang...")
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', modul])
                except Exception as e:
                    print(f"Gagal memasang modul [{modul}]: {e}")
    except Exception as e:
        print(f"Terjadi kesalahan saat memproses file requirements: {e}")

def buat_folder_vidio_download(nama_folder='VidioDownload'):
    """
    Membuat folder dengan nama yang diberikan jika belum ada.
    """
    try:
        if not os.path.exists(nama_folder):
            os.makedirs(nama_folder)
            print(f"Folder [{nama_folder}] berhasil dibuat.")
        else:
            print(f"Folder [{nama_folder}] sudah ada.")
    except Exception as e:
        print(f"Terjadi kesalahan saat membuat folder: {e}")

def cek_modul_dan_folder():
    """
    Mengecek dan memasang modul yang diperlukan serta membuat folder VidioDownload.
    Fungsi ini dapat diimpor oleh script lain.
    """
    pasang_dan_cek_modul()
    buat_folder_vidio_download()