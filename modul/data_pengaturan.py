import os
from modul import *

def cek_data_buat():
    """Cek keberadaan file pengaturan.txt, buat jika belum ada"""
    if not os.path.exists('pengaturan.txt'):
        with open('pengaturan.txt', 'w') as f:
            pass  # File kosong dibuat
        print("File pengaturan.txt dibuat karena belum ada.")
    else:
        print("File pengaturan.txt sudah ada.")

def cek_isi():
    """Cek isi file terhadap requirements.txt dan jalankan update() jika berbeda"""
    # Fungsi update (asumsi dibuat terpisah)1
    
    try:
        with open('requirements.txt', 'r') as req_file:
            required_content = req_file.read()
        
        with open('pengaturan.txt', 'r') as setting_file:
            current_content = setting_file.read()
        
        if current_content != required_content:
            print("Isi file tidak sesuai, melakukan update...")
            buat_folder_vidio_download()
            pasang_dan_cek_modul()
        else:
            print("Isi file sudah sesuai, tidak perlu update.")
    
    except FileNotFoundError:
        print("Error: requirements.txt tidak ditemukan.")

def pengaturan_data():
    print ("data")
    cek_data_buat()
    cek_isi() 
