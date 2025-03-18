from colorama import init, Fore, Style
init()

def loadbar(prev_val, new_val, maxval, w):
    if prev_val < 0: prev_val = 0
    if new_val < 0: new_val = 0

    new_val = min(maxval, new_val)
        
    percents = prev_val / maxval * 100
    percents2 = new_val / maxval * 100
    if percents > 100:
        percents = 100
        
    cells = round(percents / 100 * w)
    cells2 = round(percents2 / 100 * w) - cells
    all_cells = cells + cells2

    if all_cells > cells:
        loaded_symbols = '█' * cells + Fore.GREEN + '█' * cells2 + Fore.WHITE
        unloaded_symbols = '░' * (w - (cells + cells2))
    else:
        loaded_symbols = '█' * (cells + cells2) + Fore.RED + '█' * abs(cells2) + Fore.WHITE
        unloaded_symbols = '░' * (w - cells)

    bar = Style.BRIGHT + '|' + loaded_symbols + unloaded_symbols + '|'
        
    return bar
