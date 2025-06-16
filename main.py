import os
import time  # Untuk menambah jeda waktu
from modul.logo import tampilkan_logo  # Import dari folder modul

def hapus_layar():
    """Membersihkan layar terminal di semua OS."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    hapus_layar()
    tampilkan_logo()  # Memanggil fungsi logo dari modul/logo.py
    print("main.py")

if __name__ == "__main__":
    main()