# just helper functions

import os
import time
import sys

def print_sep():
    '''
    Prints the default screen separator
    '''
    os.system('cls')
    print('\n')
    print('#'*15)

def print_sent(val: str, time_step: float = 0.0005):
    '''
    Summary:
    ---
    Defines the default printing way for the text

    Parameters:
    ---
    val: the value to be printed
    time_step: the delay between each print

    '''
    wds = val.split(' ')
    for wd in wds:
        print(f'{wd} ', end='', flush=True)
        time.sleep(time_step)
    print()

def action_to_continue():
    '''
    Summary:
    ---
    Initiates a wait state so the player can see what happened
    '''
    print
    print_sent("Press enter  to continue..")
    val = input('')
    if val == 'q':
        sys.exit()