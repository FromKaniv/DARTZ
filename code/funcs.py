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

move_count_forms = ("хід", "ходи", "ходів")

def sort_move(move):
    all_b = move.count('b')
    all_a = move.count('a')

    move = move.replace('a', '').replace('b', '')

    move = list(move)
    move = list(map(int, move))
    move = list(sorted(move))
    move = list(map(str, move))
    move = ''.join(move)

    return 'b'*all_b + ''.join(move) + 'a'*all_a

def avg(arr):
    return sum(arr) / len(arr)

def convert_to_percents(n):
    return '%s%%' % round(n*100)

def add_arrow(n):
    if round(n, 2) == 0:
        return YELLOW + '~0' + RESET
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
    
def correct_word_form(number: int, word_forms: tuple) -> str:
    if 11 <= number % 100 <= 19:
        return f"{number} {word_forms[2]}"
    last_digit = number % 10
    if last_digit == 1:
        return f"{number} {word_forms[0]}"
    if 2 <= last_digit <= 4:
        return f"{number} {word_forms[1]}"
    return f"{number} {word_forms[2]}"

