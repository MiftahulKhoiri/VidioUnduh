import os
import time  # Untuk menambah jeda waktu
from modul.logo import tampilkan_logo  # Import dari folder modul
from modul.unduh import menu_utama

def hapus_layar():
    """Membersihkan layar terminal di semua OS."""
    os.system('cls' if os.name == 'nt' else 'clear')

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

def main():
    time.sleep(2)
    hapus_layar()
    tampilkan_logo()  # Memanggil fungsi logo dari modul/logo.py
    time.sleep(2)
    menu_utama()

if __name__ == "__main__":
    main()