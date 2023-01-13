# the actual game happens here

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
    gameMenu = classes.GameMenu()
    cmdI = classes.CommandInterface()
    gameN = classes.GameController(2)

    currMenu = gameMenu.gameMenu_startScreen
    pathStack = []
    pushMenu(pathStack,currMenu)
    while True:
        
        misc.printSep()
        currMenu = pathStack[-1]
        gameMenu.printVals(currMenu)

        prompt = 'Please select option: '
        cmd = cmdI.getCmd(prompt,'num')
        
        while cmd == None:
            cmd = cmdI.getCmd(prompt,'num')
        selection = gameMenu.selectFromMenu(currMenu, cmd)
        

        if selection == 'New game':
            pushMenu(pathStack, gameMenu.gameMenu_newGame)
            gameMenu.printVals(currMenu)

        elif selection == 'Start':
            print('start game')
            playGame(gameN) 

        elif selection == 'Number of players':
            prompt = 'Please enter the number of players (default is 2): '
            cmd = cmdI.getCmd(prompt, 'num')
            gameN.setNplayers(cmd)
            print(f'Number of players: {gameN.nPlayers}')

        elif selection == 'Game mode':
            prompt = "Please enter the game mode - it can only be 'classic' or 'wild': "
            cmd = input(prompt)
            gameN.setGameMode(cmd)
            print(f'Game mode: {gameN.gameMode}')

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
    game = classes.GameController(game.nPlayers)
    game.setStartCurrentPlayer()

    print("Bid in the form of 'int int' or 'liar'. Press 'q' to quit the current game.")
    
    # game loop
    while True:

        misc.printSep()

        # print game state
        game.printGameState()

        # check if we have a winner
        if game.getPlayersLeft() == 1:
            misc.printSep()
            print(f"Playr {currPlayerStats['Name']} is the winner!")
            break
        
        # get current player input
        cmd = cmdI.getCmd('Your bid: ', 'bid')
        playerBid = cmd

        # check if the prev player is a liar and adjust dice count accordingly
        turnCounter = game.getTurnCounter()
        
        if cmd == 'liar' and turnCounter > 0:
            currPlayer = game.getCurrentPlayer()
            prevPlayer = game.getPrevPlayer(currPlayer)
            diceCounts = game.getDiceStats()
            currPlayerStats = game.getPlayerStats(currPlayer)
            prevPlayerStats = game.getPlayerStats(prevPlayer)
            prevPlayerFace = game.getPlayerStats(prevPlayer)['Face']
            prevPlayerCount = game.getPlayerStats(prevPlayer)['Count']
            
            # wild mode setting
            gameMode = game.getGameMode()
            if gameMode == 'wild' and prevPlayerFace > 1:
                prevPlayerCount += diceCounts[1]

            # checks if the prev player has correct face count
            # if they do, the curr players loses a die

            # sets the turn counter to zero since we are dealing new hands
            if diceCounts[prevPlayerFace] >= prevPlayerCount:
                print(f"{currPlayerStats['Name']} loses 1 die")
                game.setDiceDecr(currPlayer)
                game.setNextRound()
                game.setTurnCounterZero()
                continue
            
            else:
                print(f"{prevPlayerStats['Name']} loses 1 die")
                game.setDiceDecr(prevPlayer)
                game.setNextRound()
                game.setTurnCounterZero()
                continue
        
        # check for input on first round
        # if invalid input - again
        validBid = game.isValidBid(cmd, game.getnDice())
        if turnCounter == 0 and validBid:
            game.setPlayerBid(game.currentPlayer,playerBid)
            game.setNextPlayer()
            game.setTurnCounterIncr()
            continue
        elif turnCounter == 0 and not validBid:
            continue
        
        # checks the input after first round
        currPlayer = game.getCurrentPlayer()
        prevPlayer = game.getPrevPlayer(currPlayer)
        currPlayerStats = game.getPlayerStats(currPlayer)
        prevPlayerStats = game.getPlayerStats(prevPlayer)
        if not game.isValidBid(cmd, game.getnDice(), prevPlayerStats):
            continue
        

        # continue to next player
        game.setPlayerBid(game.getCurrentPlayer(),cmd)
        game.setNextPlayer()
        game.setTurnCounterIncr()
        





