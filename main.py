import game
import sys
import classes

def main():
    
    help_info = '''
It's nice to see you here! This is my lovely implementation of Liar's Dice game.
More information can be found on the repository page in GitHub here: 
https://github.com/PetarBoshnakov/dice-game

    -help, -help, h, -h: to get the help menu 
    -start: to start the game 
    -debug: to enter debug mode revealing system information on the player and the bot'''

    try:
        main_arg = sys.argv[1]
    except:
        main_arg = None

    if main_arg == '-start':
        game.game_menu()
    elif main_arg == '-debug':
        classes.DEBUG_MODE = 'on'
        game.game_menu()
    elif main_arg in ['help', '-help', 'h', '-h']:
        print(help_info)
    else:
        print(help_info)

if __name__ == '__main__':
    main()