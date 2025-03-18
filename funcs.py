from colorama import init, Fore, Style
from os import system

init(autoreset=True)
clear = lambda: system('cls||clear')

RESET = Style.RESET_ALL
GREEN = Style.BRIGHT + Fore.GREEN
YELLOW = Style.BRIGHT + Fore.YELLOW
RED = Style.BRIGHT + Fore.RED
BLUE = Style.BRIGHT + Fore.BLUE
WHITE = Style.BRIGHT + Fore.WHITE

def avg(arr):
    return sum(arr) / len(arr)

def convert_to_percents(n):
    return '%s%%' % round(n*100)

def add_arrow(n):
    if round(n, 2) == 0:
        return YELLOW + '±0' + RESET
    if n > 0:
        return GREEN + '+%s▲' % round(n, 2) + RESET
    else:
        return RED + '%s▼' % round(n, 2) + RESET

def format_time(seconds):
    seconds = round(seconds)

    m, s = divmod(seconds, 60)

    return '%sхв %sсек' % (m, s)

def color_the_rank(accuracy, rank):
    if accuracy < 1/4:
        color = RED
    elif accuracy < 1/2:
        color = YELLOW
    elif accuracy < 3/4:
        color = GREEN
    else:
        color = BLUE

    return color + rank
