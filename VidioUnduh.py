import sys
import os
import time  # Untuk menambah jeda waktu

def hapus_layar():
    """Membersihkan layar terminal di semua OS."""
    os.system('cls' if os.name == 'nt' else 'clear')

# Pastikan path folder modul dikenali Python
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODUL_DIR = os.path.join(SCRIPT_DIR, 'modul')
if MODUL_DIR not in sys.path:
    sys.path.append(MODUL_DIR)

import update
from modul import modul  # Import modul Anda

def main():
    # Bersihkan layar sebelum mulai
    hapus_layar()
    # Jalankan proses update terlebih dahulu
    update.proses_update()

    # Jeda waktu setelah update
    time.sleep(2)

    # Cek dan install modul, juga buat folder VidioDownload
    modul.cek_modul_dan_folder()

    # Jeda lagi setelah proses modul
    time.sleep(2)

    # Setelah update & cek modul, jalankan main.py
    try:
        import main as main_modul
        if hasattr(main_modul, 'main') and callable(main_modul.main):
            main_modul.main()
        else:
            print("[ERROR] Modul 'main.py' tidak memiliki fungsi main().")
    except ImportError as e:
        print(f"[ERROR] Tidak dapat mengimpor modul 'main.py': {e}")

if __name__ == "__main__":
    main()