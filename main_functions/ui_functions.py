from datetime import datetime

def paint(rgb: tuple[int, int, int], text: str):
    r = int(rgb[0])
    g = int(rgb[1])
    b = int(rgb[2])
    return str(f'\033[40;38;2;{r};{g};{b}m{text}\033[0m')

def hour():
    return datetime.now().strftime('%H:%M:%S')