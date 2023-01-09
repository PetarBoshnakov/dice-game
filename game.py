import classes
import sys
import misc


def pushMenu(stak: list, menu: list):
    '''
    Summary:
    ---
    Keeps track of the menu navigation. It essentially creates a breadcrumb for the menu navigation

    Parameters:
    ---

    stak: the current stack that holds the menus

    menu: a menu (list of items) to be pushed to the stack
    '''
    
    if len(stak) == 0 or stak[-1] != menu:
        stak.append(menu)

def gameMenu():
    '''
    Summary:
    ---
    Iterates the game menus and starts the game
    '''
    game = classes.GameController()
    cmdI = classes.CommandInterface()

    currMenu = game.gameMenu_startScreen
    pathStack = []
    pushMenu(pathStack,currMenu)
    while True:
        
        misc.printSep()
        currMenu = pathStack[-1]
        game.printVals(currMenu)

        prompt = 'Please select option: '
        cmd = cmdI.getCmd(prompt,'num')
        
        while cmd == None:
            cmd = cmdI.getCmd(prompt,'num')
        selection = game.selectFromMenu(currMenu, cmd)
        

        if selection == 'New game':
            pushMenu(pathStack, game.gameMenu_newGame)
            game.printVals(currMenu)

        elif selection == 'Start':
            print('start game')
            playGame(game) 

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
        

def playGame(game: classes.GameController):
    '''
    Summary:
    ---
    Runs the actual game
    '''
    cmdI = classes.CommandInterface()
    currentGameStats = classes.GameStats(game.nPlayers)
    game.setCurrentPlayer()

    print("Bid in the form of 'int int' or 'liar'. Press 'q' to quit the current game.")
    
    # game loop
    while True:

        misc.printSep()
        # print game state
        game.printGameState(currentGameStats.getGameState(), game.currentPlayer)
        
        # get current player input
        cmd = cmdI.getCmd('Your bid: ', 'bid')
        playerBid = cmd

        # if invalid input - again
        if not game.isValidBid(cmd, currentGameStats.getnDice()):
            continue
        

        # continue to next player
        game.setNextPlayer()
        





