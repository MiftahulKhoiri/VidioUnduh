from colorama import Fore, Style

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init()
    HIJAU = Fore.GREEN
    MERAH = Fore.RED
    KUNING = Fore.YELLOW
    BIRU = Fore.BLUE
    RESET = Style.RESET_ALL
except ImportError:
    HIJAU = MERAH = KUNING = BIRU = RESET = ""


def tampilkan_logo():
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    logo = f"""
{CYAN}╔═══════════════════════╗
{BLUE}║ {GREEN}Vidio {YELLOW}Unduh{BLUE}           ║
{BLUE}║ {CYAN} Vidio Download Tools {BLUE}║
{CYAN}╚═══════════════════════╝{RESET}
    """
    print(logo)


def tampilkan_menu_utama():
    """Menampilkan menu utama dengan tampilan menarik dan warna."""
    print(Fore.CYAN + "\n" + "="*44)
    print(Fore.MAGENTA + Style.BRIGHT + "     Selamat Datang di " + Fore.YELLOW + "Vidio Unduh")
    print(Fore.CYAN + "="*44)
    print(Fore.BLUE + " 1.", Fore.WHITE + "Youtube :")
    print(Fore.BLUE + " 2.", Fore.WHITE + "Facebook :")
    print(Fore.BLUE + " 3.", Fore.WHITE + "Twitter/X :")
    print(Fore.RED + " 0. Keluar :")
    print(Fore.CYAN + "="*44)

def tampilkan_salam():
    print(f"{BIRU}{'='*40}")
    print("=        Update pembaruan script       =")
    print(f"{'='*40}{RESET}")
