def pushMenu(stak: list, menu: list):
    
    if len(stak) == 0 or stak[-1] != menu:
        stak.append(menu)