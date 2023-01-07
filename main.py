import classes
import misc
import sys


def main():
    game = classes.GameController()
    cmdI = classes.CommandInterface()

    currMenu = game.gameMenu_startScreen
    pathStack = []
    misc.pushMenu(pathStack,currMenu)
    while True:
        
        print('\n')
        print('#'*15)
        currMenu = pathStack[-1]
        game.printVals(currMenu)

        prompt = 'Please select option: '
        cmd = cmdI.getCmd(prompt,'num')
        
        while cmd == None:
            cmd = cmdI.getCmd(prompt,'num')
        selection = game.selectFromMenu(currMenu, cmd)
        

        if selection == 'New game':
            misc.pushMenu(pathStack, game.gameMenu_newGame)
            game.printVals(currMenu)

        elif selection == 'Start':
            print('start game')
            pass            

        elif selection == 'Number of players':
            prompt = 'Please enter the number of players (default is 2): '
            cmd = cmdI.getCmd(prompt, 'num')
            game.setNplayers(cmd)
            print(f'Number of players: {game.nPlayers}')

        elif selection == 'Game mode':
            prompt = "Please enter the game mode - it can only be 'classic' or 'wild': "
            cmd = input(prompt)
            game.setGameMode(cmd)
            print(f'Game mode: {game.gameMode}')

        elif selection == 'Exit':
            print('Sad to see you go ;(')
            sys.exit()

        elif selection == 'Back':
            pathStack.pop()
        
        else:
            print('Please select a valid menu item by inputing a menu number. For example 1 unless advised otherwise.')
        

if __name__ == '__main__':
    main()