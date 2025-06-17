import os
import sys
import datetime
import subprocess
from colorama import init, Fore, Style

init(autoreset=True)
NAMA_FOLDER = "VidioDownload"
os.makedirs(NAMA_FOLDER, exist_ok=True)

def tanggal_hari_ini():
    return datetime.datetime.now().strftime("%d-%m-%Y")

def safe_filename(name):
    return "".join(c for c in name if c.isalnum() or c in " ._-").rstrip()

def nama_file_unik(judul, ekstensi, tanggal):
    judul = safe_filename(judul)
    nama_dasar = f"{judul}_{tanggal}.{ekstensi}"
    nama_file = nama_dasar
    idx = 1
    while os.path.exists(os.path.join(NAMA_FOLDER, nama_file)):
        if idx == 1:
            nama_file = f"{judul}_{tanggal} (copy).{ekstensi}"
        else:
            nama_file = f"{judul}_{tanggal} (copy {idx}).{ekstensi}"
        idx += 1
    return nama_file

def cek_file_dan_konfirmasi(judul, ekstensi, tanggal):
    nama_file = f"{safe_filename(judul)}_{tanggal}.{ekstensi}"
    path_file = os.path.join(NAMA_FOLDER, nama_file)
    if os.path.exists(path_file):
        jawab = input(
            f"{Fore.YELLOW}File sudah ada: {nama_file}. Lanjutkan download dan simpan dengan nama baru? (y/n): "
        ).lower().strip()
        if jawab == "y":
            return nama_file_unik(judul, ekstensi, tanggal)
        else:
            print(Fore.CYAN + "Download dibatalkan.")
            return None
    else:
        return nama_file

def print_progress_bar(percent, width=32, color=Fore.GREEN, msg=""):
    fill_len = int(width * percent // 100)
    empty_len = width - fill_len
    bar = color + '█' * fill_len + Style.RESET_ALL + '░' * empty_len
    progress = f"{percent:6.2f}%"
    sys.stdout.write(f"\r{bar} {progress} {msg}")
    sys.stdout.flush()
    if percent >= 100:
        print()

def yt_progress_hook(status):
    if status['status'] == 'downloading':
        percent = float(status.get('percent', 0.0))
        speed = status.get('speed', 0)
        eta = status.get('eta', 0)
        color = (
            Fore.RED if percent < 33 else
            Fore.YELLOW if percent < 66 else
            Fore.GREEN if percent < 99.99 else
            Fore.CYAN
        )
        msg = f"Speed: {speed/1024:.1f} KB/s ETA: {eta}s"
        print_progress_bar(percent, width=32, color=color, msg=msg)
    elif status['status'] == 'finished':
        print_progress_bar(100, width=32, color=Fore.CYAN, msg="Done!")
