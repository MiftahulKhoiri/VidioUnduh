import os
from modul.modul import buat_folder_vidio_download, pasang_dan_cek_modul
from modul.Logo import *

def cek_data_buat():
    """Cek keberadaan file pengaturan.txt, buat jika belum ada"""
    if not os.path.exists('pengaturan.txt'):
        with open('pengaturan.txt', 'w') as f:
            pass  # File kosong dibuat
        print("File pengaturan.txt dibuat karena belum ada.")
    else:
        print("File pengaturan.txt sudah ada.")

def cek_isi():
    """Cek isi file pengaturan.txt terhadap modul pada requirements.txt dan update jika perlu"""
    try:
        # Dapatkan nama modul dari requirements.txt (tanpa versi)
        with open('requirements.txt', 'r') as req_file:
            required_moduls = set([
                baris.strip().split('==')[0].split('>=')[0].split('<=')[0]
                for baris in req_file if baris.strip() and not baris.startswith('#')
            ])

        # Dapatkan nama modul dari pengaturan.txt
        with open('pengaturan.txt', 'r') as setting_file:
            current_moduls = set([
                baris.strip() for baris in setting_file if baris.strip()
            ])

        if required_moduls != current_moduls:
            print("Isi file tidak sesuai, melakukan update...")
            modul_belum_lengkap()
            buat_folder_vidio_download(nama_folder='VidioDownload')
            pasang_dan_cek_modul(
                nama_file_requirements='requirements.txt',
                file_pengaturan='pengaturan.txt'
            )
        else:
            print("Isi file sudah sesuai, tidak perlu update.")

    except FileNotFoundError:
        print("Error: requirements.txt tidak ditemukan.")

def pengaturan_data():
    print("data")
    cek_data_buat()
    cek_isi()