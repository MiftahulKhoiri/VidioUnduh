import subprocess
import sys

def greeting():
    print("="*40)
    print("Mendapatkan pembaruan script")
    print("="*40)

def show_updates():
    print("\n[INFO] Daftar pembaruan terbaru di repo:")
    try:
        # Menampilkan 5 commit terakhir dari remote
        subprocess.run(
            ["git", "fetch"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        result = subprocess.run(
            ["git", "log", "HEAD..origin/main", "--oneline"],
            check=False,  # Tidak error jika sudah up-to-date
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            print(result.stdout)
        else:
            print("Sudah versi terbaru! Tidak ada pembaruan di remote.")
    except Exception as e:
        print(f"Gagal mengambil log pembaruan: {e}")

def confirm_update():
    while True:
        jawab = input("\nLanjutkan pembaruan dengan git pull? (y/n): ").strip().lower()
        if jawab == "y":
            return True
        elif jawab == "n":
            print("Pembaruan dibatalkan.")
            return False
        else:
            print("Masukkan 'y' untuk setuju, atau 'n' untuk membatalkan.")

def do_git_pull():
    print("\n[PROSES] Menjalankan git pull...")
    try:
        subprocess.run(["git", "pull"], check=True)
        print("Pembaruan selesai.")
    except subprocess.CalledProcessError:
        print("Gagal melakukan git pull. Pastikan folder ini adalah repository git dan tidak ada konflik.")

if __name__ == "__main__":
    greeting()
    show_updates()
    if confirm_update():
        do_git_pull()