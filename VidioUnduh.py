import sys
import os

# Pastikan path folder modul dikenali Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'modul'))

import update

def main():
    # Jalankan proses update terlebih dahulu
    update.proses_update()
    
    # Setelah update selesai, jalankan main.py
    # Import main.py sebagai modul
    import main
    main.main()  # Pastikan di main.py ada fungsi main()

if __name__ == "__main__":
    main()