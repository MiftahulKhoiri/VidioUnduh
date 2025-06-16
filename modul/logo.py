# logo.py
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
