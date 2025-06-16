NAMA_FOLDER = 'VidioDownload'

def buat_folder_unduhan():
    """
    Membuat folder penyimpanan hasil unduhan jika belum ada.
    """
    if not os.path.exists(NAMA_FOLDER):
        os.makedirs(NAMA_FOLDER)

def nama_berkas_hasil(judul, ekstensi):
    """
    Membuat nama file hasil unduhan agar tidak duplikat dan diberi tanggal.
    """
    = f"{judul}_{tanggal}.{ekstensi}"
    urutan = 1
    nama_berkas = nama_dasar
    while os.path.exists(os.path.join(NAMA_FOLDER, nama_berkas)):
        nama_berkas = f"{judul}_{tanggal}_{urutan}.{ekstensi}"
        urutan += 1
    return nama_berkas

def unduh_video_audio_terpisah(alamat, resolusi=None):
    """
    Mengunduh video dan audio terpisah lalu menggabungkannya dengan ffmpeg.
    """
    try:
        # Opsi unduh video
        temp_video = "temp_video.mp4"
        temp_audio = "temp_audio.m4a"

        opsi_video = {
            'format': f"bestvideo[height<={resolusi}]" if resolusi else "bestvideo",
            'outtmpl': temp_video,
            'noplaylist': True,
            'quiet': True
        }
        opsi_audio = {
            'format': "bestaudio",
            'outtmpl': temp_audio,
            'noplaylist': True,
            'quiet': True
        }

        print("Mengunduh video...")
        with YoutubeDL(opsi_video) as ydl:
            info = ydl.extract_info(alamat, download=True)
            judul = info.get('title', 'video')
        print("Mengunduh audio...")
        with YoutubeDL(opsi_audio) as ydl:
            ydl.download([alamat])

        # Dapatkan nama file hasil unduhan
        nama_berkas = nama_berkas_hasil(judul, "mp4")
        hasil_output = os.path.join(NAMA_FOLDER, nama_berkas)

        print("Menggabungkan video dan audio dengan ffmpeg...")
        perintah = [
            'ffmpeg', '-y',
            '-i', temp_video,
            '-i', temp_audio,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-strict', 'experimental',
            hasil_output
        ]
        # Jalankan ffmpeg
        proses = subprocess.run(perintah, capture_output=True, text=True)
        if proses.returncode != 0:
            print("Terjadi kesalahan saat menggabungkan video dan audio!")
            print(proses.stderr)
            return

        # Hapus file sementara
        os.remove(temp_video)
        os.remove(temp_audio)
        print(f"Video hasil gabungan disimpan di: {hasil_output}")

    except Exception as e:
        print("Gagal mengunduh atau menggabungkan video/audio!")
        print(f"Detail error: {e}")

def menu_utama():
    """
    Menu utama aplikasi unduhan.
    """
    buat_folder_unduhan()
    print("=== Menu Unduh Video + Audio (Kualitas Maksimal) ===")
    print("1. Youtube")
    print("2. Facebook")
    print("3. Twitter")
    print("0. Keluar")

    sumber = input("Pilih sumber (1/2/3): ")
    if sumber == "0":
        return
    daftar_url = []
    mode = input("Unduh 1 video atau banyak? (1/banyak): ").strip().lower()
    if mode == "banyak":
        print("Masukkan alamat video satu per satu, tekan Enter tanpa input untuk mulai unduhan otomatis.")
        while True:
            alamat = input("URL: ").strip()
            if alamat == "":
                break
            daftar_url.append(alamat)
    else:
        alamat = input("Masukkan URL video: ").strip()
        if alamat: daftar_url.append(alamat)
    resolusi = input("Pilih resolusi (misal: 720), kosongkan untuk terbaik: ").strip()
    if not resolusi: resolusi = None
    if not daftar_url:
        print("Tidak ada URL, keluar.")
        return
    for alamat in daftar_url:
        unduh_video_audio_terpisah(alamat, resolusi)

if __name__ == "__main__":
    menu_utama()