from colorama import Fore, Style

colors = [
    "BLACK", "RED", "GREEN", "YELLOW",
    "BLUE", "MAGENTA", "CYAN", "WHITE",
    "LIGHTBLACK_EX", "LIGHTRED_EX", "LIGHTGREEN_EX",
    "LIGHTYELLOW_EX", "LIGHTBLUE_EX", "LIGHTMAGENTA_EX",
    "LIGHTCYAN_EX", "LIGHTWHITE_EX"
]

styles = {
    "DIM": Style.DIM,
    "NORMAL": Style.NORMAL,
    "BRIGHT": Style.BRIGHT
}

for style_name, style in styles.items():
    print(f"\n{style_name}")
    for color in colors:
        print(f"{style}{getattr(Fore, color)}{color}{Style.RESET_ALL}")