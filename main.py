import os
import time  # Untuk menambah jeda waktu

def hapus_layar():
    """Membersihkan layar terminal di semua OS."""
    os.system('cls' if os.name == 'nt' else 'clear')



def main():
 print ("main.py")

if __name__ == "__main__":
    main()