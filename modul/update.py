import subprocess

def tampilkan_salam():
    """Menampilkan salam pembuka saat script dijalankan."""
    print("="*40)
    print("Mendapatkan pembaruan script")
    print("="*40)

def tampilkan_pembaruan():
    """
    Menampilkan daftar pembaruan (commit) terbaru dari repository.
    Akan menampilkan commit dari remote jika ada.
    """
    print("\n[INFO] Daftar pembaruan terbaru di repository:")
    try:
        # Mengambil pembaruan dari remote repository
        subprocess.run(
            ["git", "fetch"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        # Menampilkan commit terbaru dari remote (origin/main)
        hasil = subprocess.run(
            ["git", "log", "HEAD..origin/main", "--oneline"],
            check=False,  # Tidak error jika sudah up-to-date
            capture_output=True,
            text=True
        )
        if hasil.stdout.strip():
            print(hasil.stdout)
        else:
            print("Sudah menggunakan versi terbaru! Tidak ada pembaruan di remote.")
    except Exception as error:
        print(f"[ERROR] Gagal mengambil log pembaruan: {error}")

def konfirmasi_pembaruan():
    """
    Meminta konfirmasi user untuk melanjutkan proses git pull.
    Akan mengulang input jika tidak valid.
    """
    while True:
        try:
            jawaban = input("\nLanjutkan pembaruan dengan git pull? (y/n): ").strip().lower()
            if jawaban == "y":
                return True
            elif jawaban == "n":
                print("Pembaruan dibatalkan oleh pengguna.")
                return False
            else:
                print("Input tidak valid. Masukkan 'y' untuk setuju, atau 'n' untuk membatalkan.")
        except Exception as error:
            print(f"[ERROR] Terjadi kesalahan saat input: {error}")

def lakukan_git_pull():
    """
    Menjalankan perintah git pull untuk memperbarui repository.
    Menampilkan notifikasi jika berhasil atau gagal.
    """
    print("\n[PROSES] Menjalankan git pull...")
    try:
        subprocess.run(["git", "pull"], check=True)
        print("[SUKSES] Pembaruan selesai.")
    except subprocess.CalledProcessError:
        print("[ERROR] Gagal melakukan git pull. Pastikan folder ini adalah repository git dan tidak ada konflik.")
    except Exception as error:
        print(f"[ERROR] Terjadi kesalahan saat menjalankan git pull: {error}")

def proses_update():
    """
    Fungsi utama untuk proses update.
    Bisa dipanggil dari script lain sebagai modul.
    """
    try:
        tampilkan_salam()
        tampilkan_pembaruan()
        if konfirmasi_pembaruan():
            lakukan_git_pull()
    except KeyboardInterrupt:
        print("\n[INFO] Proses dibatalkan oleh pengguna (Ctrl+C).")
    except Exception as error:
        print(f"[ERROR] Terjadi kesalahan fatal: {error}")

if __name__ == "__main__":
    # Jika file dijalankan langsung, lakukan proses update
    proses_update()