import os
import time  # Untuk menambah jeda waktu
from modul.logo import tampilkan_logo  # Import dari folder modul
from modul.unduh import menu_utama

def hapus_layar():
    """Membersihkan layar terminal di semua OS."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    time.sleep(2)
    hapus_layar()
    tampilkan_logo()  # Memanggil fungsi logo dari modul/logo.py
    time.sleep(2)
    menu_utama()

if __name__ == "__main__":
    main()