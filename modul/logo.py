# logo.py
def tampilkan_logo():
    # ANSI escape codes untuk warna
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    logo = f"""
{CYAN}██    ██ ██   ██ ██████  ██ ██████   ██████  ██    ██ █    ██ ██████  ██   ██
{BLUE} ██  ██  ██   ██ ██   ██ ██ ██   ██ ██    ██ ██    ██ ██  ██  ██   ██  ██ ██ 
{GREEN}  ████   ███████ ██████  ██ ██████  ██    ██ ██    ██ ██ ██   ██████    ███  
{YELLOW}   ██    ██   ██ ██      ██ ██      ██    ██ ██    ██ ██  ██  ██         ██  
{CYAN}   ██    ██   ██ ██      ██ ██       ██████   ██████  ██   ██ ██         ██   

           {YELLOW}VidioUnduh - Download Video Tools{RESET}
    """
    print(logo)
