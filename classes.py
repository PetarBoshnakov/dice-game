# game objects

import sys
import random
import uuid
import misc

class Player:
    '''
    Defines the player class
    '''

    def __init__(self, name: str):
        '''
        Summary:
        ---
        Ini a player with a name
        
        Parameters:
        ---
        name: player name
        '''
        self.Name = name

class Bot(Player):
    '''
    Summary:
    ---
    Defines the actions that a bot can take
    '''
    def isWildMode(self):
        if GameController.gameMode == 'wild':
            return True
        return False
    

    def bid(self, bid):
        #TODO
        '''
        Summary:
        ---
        Submits a bid to the Game Stats

        Parameters:
        ---
        bid: 
        '''
        #TODO
        pass
        
    def liar(self):
        '''
        Summary:
        ---
        showdown. winner is decided between current and previous player. loser 
        loses one die
        '''
        #TODO
        pass

    def generateBid(self):
        #TODO
        pass
    
class GameStats():
    '''
    Summary:
    ---
    Keeps the current game log - active players, who's turn is, what are the bids so far

    Attributes:
    ---
    
    nPlayers: number of players in the game

    nDice: number of dices

    playerStats: dictionary to hold the player stats: 
        current bid
            face 
            count 
        status call - 'bid' or 'liar'

    '''

    def __init__(self, nplayers):
        '''
        Symmary: 
        ---
        Holds the current game stats and creates a game log.
        playerStats:
            -Face - the dice face
            -Count - number of dice faces in the game
            -DiceN - current player dice
            -Hand - current player hand
            -Status - Bid, Liar, Out, Won


        Parameters:
        ---
        nplayers: the number of players to be set for the class intialization
        
        '''

        self.nPlayers = self.setNPlayers(nplayers)
        self.nDice = nplayers * 5
        self.playerStats = {}

        # initializes the players DB
        self.ini_players()
    
    def setNPlayers(self, nplayers):
        '''
        Summary:
        ---
        Sets the number of players for the class

        Parameters:
        ---
        nplayers: the number of players to be set for the game.

        Returns:
        ---
        nplayers or 2 if the conditions are not met
        '''
        if isinstance(nplayers,int):
            return nplayers    
        else:
            misc.printSep()
            print(f'{nplayers} is not valid input. The number of players must be an integer. The player count is set to the default: 2')
            return 2

    def ini_players(self):    
        '''
        Summary:
        ---
        Ini the number of players for the game
        '''
        
        for i in range(1,self.nPlayers + 1):
            playerX = Player(f'Player {i}')
            hand = GameController.gameGenerateHand(self)
            self.playerStats[i-1] = {'Name': playerX.Name,'Face': 0, 'Count': 0, 'DiceN': 5, 'Hand': hand, 'Status': 'Not set'}

    def getDiceStats(self) -> dict:
        '''
        Summary:
        ---
        Calculates the dice summary for the current game.

        Returns:
        ---
        A dictionary containing the values and their counts in the game        
        '''
        players = self.nPlayers - 1
        
        dicevals = []
        for player in range(players):
            dicevals.append(self.getPlayerStats(player)['Hand'])

                
        diceGlob = {
            1:0,
            2:0,
            3:0,
            4:0,
            5:0,
            6:0
        }

        for val in dicevals:
            for i in range(1,7):
                diceGlob[i] += val.count(i)

        return diceGlob


    def getnDice(self):
        '''
        Summary:
        ---
        Returns the global number of dice
        '''

        diceN = 0
        keys = self.playerStats.keys()
        for key in keys:
            diceN += self.playerStats[key]['DiceN']

        return diceN

    def getPlayerStats(self, player):
        #TODO
        '''
        Summary:
        ---
        Get the player's stats

        Parameters:
        ---
        player: 

        Returns:
        All game moves of the player by game id
        '''
        return self.playerStats[player]  

    def getGameState(self):
        '''
        Returns:
        ---
        Dictionary with the current players information
        '''
        return self.playerStats

    def setDiceDecr(self, player):
        pass
    
    def updatePlayerBid(self, player, stats):
        '''
        Summary:
        ---
        Update the player stats

        Parameters:
        ---

        player: the player name to be updated in the stats dictionary

        bid: holds the bid value in a list 

        '''
        if stats == 'liar':
            self.playerStats[player]['Status'] = 'liar'
        else:    
            face = stats[0]
            count = stats[1]
            self.playerStats[player]['Face'] = face
            self.playerStats[player]['Count'] = count
            self.playerStats[player]['Status'] = 'bid'

    def generateUUID(self):
      
        return uuid.uuid4()


class CommandInterface:
    '''
    Summary:
    ---
    reads and translates comamnds from the console
    '''

    def getCmd(self, cmdPrompt: str, type: str):
        '''
        Summary:
        ---        
        Reads a command from the command line. Checks if the command passed 
        has the correct type of arguments format and type - for bids and commandline interface.

        'q' is an escape that quits the program at any point
        
        Parameters:
        ---
        cmdPrompt: the prompt text to display for the particular command
       
        type: the type of command as string a 'bid' or 'num'

        Returns:
        ---
        the input from the interface

        '''

        # type = ['num', 'bid']

        cmd = input(f'{cmdPrompt}')
        
        if cmd == 'q':
            sys.exit()
        
        if type == 'num':
            return self.processNum(cmd)

        if type == 'bid':
           return self.processBid(cmd)

    def processNum(self, cmd: str) -> int:
        '''
        Summary:
        ---
        Usually used for the menu navigation. Takes the numeric input and checks it
        and returns the command number for the command menu 

        Parameters:
        ---

        cmd: the text command to be processed 

        Returns:
        ---
        returns the number for the command after checking
        format was given
        '''

        num = cmd.split(' ')[0]
        
        try:
            val = int(num)
            return val
        except:
            misc.printSep()
            print('Please provide correct number format')
            return None

    def processBid(self, cmd: str) -> list:
        '''
        Summary:
        ---
        Takes a bid and processed it by checking if it is in correct format and 
        turns it into array

        Parameters:
        ---
        
        cmd: the text input to be processed

        Returns:
        ---
        list of values
        '''
        if cmd == 'liar':
            return cmd
        
        vals = cmd.split(' ')
        
        valsInt = []
        for val in vals:
            try:
                int(val)
                valsInt.append(int(val))
            except:
                misc.printSep()
                print(f"Wrong bid format: {cmd}. Format must be 'int int' or 'liar' !")
                return [0,0]
        return valsInt
            


class GameController:
    
    '''
    Summary:
    ---
    Runs the game - receives cmds from the console and controls the game objects
    '''

    def __init__(self) -> None:
        '''
        Summary:
        ---
        Ini the GameController
        '''
        self.nPlayers = 2
        self.gameMode = 'classic' # classic (default) or wild
        self.gameLog = []

        self.gameMenu_startScreen = ['New game', 'Exit']
        self.gameMenu_newGame = ['Start', 'Number of players', 'Game mode', 'Back']
        self.currentPlayer = 0

    def selectFromMenu(self, menu: list, selectionN: int) -> str:
        '''
        Summary:
        ---
        Selects a value from the menu

        Parameters:
        ---
        menu: an array item to be selected from

        selectionN: a manu number (start index 1) that indicates which menu item should be returned

        Returns:
        a menu item or None if selection is invalid
        '''
        if self.checkValidSelection(menu,selectionN):
            retVal = selectionN - 1
            return menu[retVal]
        else:
            return None
    
    def checkValidSelection(self, menu: list, selectionN: int) -> bool:
        '''
        Summary:
        ---
        Checks if the requested list item is within the list boundaries

        Parameters:
        ---
        menu: a valid list of items 

        selectionN: a selectin number item (starting index 1) that indicates 
        which menu item should be returned
        '''

        lenMenu = len(menu)
        nArr = int(selectionN) - 1
        if not isinstance(selectionN, int) or nArr < 0 or nArr > lenMenu - 1:
            return False
        return True
  
    def isValidBid(self, bid: list, ndice: int, prevPlayerStats = None) -> bool:
        '''
        Summary:
        ---
        Checks for bid validy. The bid count cannot be higher than what's on the
        table and the die must have a valid face. Previous player must have a higher face
        or higher count of the same face.


        Parameters:
        ---

        bid: a list containing the opening bid parameters

        ndice: the number of dice in the game
        
        prevPlayerStats: a dictionary containing the stats of the previous player

        Returns:
        ---
        True if valid. False if invalid
        '''

        if prevPlayerStats == None:
            bidInLimit = bid[0] > 0 and bid[0] <= 6 and bid[1] > 0 and bid[1] < ndice 

            if bidInLimit:
                return True
            else:
                print('the dice must have a valid side and adequate face count')
                return False

        if bid == 'liar':
            return True

        currentPlayerFace = bid[0]
        currentPlayerCount = bid[1]
        prevPlayerFace = prevPlayerStats['Face']
        prevPlayerCount = prevPlayerStats['Count']

        bidInLimit = bid[0] > 0 and bid[0] <= 6 and bid[1] > 0 and bid[1] < ndice
        
        # higher face
        currPlayerFaceHigher = bidInLimit and currentPlayerFace > prevPlayerFace
        currPlayerGeFace = bidInLimit and currentPlayerFace >= prevPlayerFace
        # equal faces but higher count 
        currPlayerHigherCount =  bidInLimit and currPlayerGeFace and currentPlayerCount > prevPlayerCount

        if not bidInLimit:
            print('the dice must have a valid side and adequate face count')
        
        if not currPlayerGeFace:
            print('current player incorrect face')
            
        if not currPlayerHigherCount:
            print('current player incorrect count')



        return bidInLimit and (currPlayerHigherCount or currPlayerFaceHigher)

        
        

    def printVals(self, vals: list) -> None:
        '''
        Summary:
        ---
        Outputs the vals array to the screen 
        '''

        for order,val in enumerate(vals, start=1):
            print(f'{order}. {val}')
    
    def printGameState(self, gameStats: dict, currentPlayer: int):
        '''
        Summary:
        ---
        Prints the game state

        Parameters:
        ---
        gameStats: the stats to be printed

        currentPlayer: the current Player index - decides whose turn it is
        '''

        playerVals = gameStats.keys()
        for cntr, playerVal in enumerate(playerVals):
            if currentPlayer == cntr:
                print(f'==>{playerVal}: {gameStats[playerVal]}')
            else:
                print(f'   {playerVal}: {gameStats[playerVal]}')

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getPrevPlayer(self):
        if self.currentPlayer == 0:
            return self.nPlayers - 1
        else:
            return self.currentPlayer - 1

    def setNplayers(self, num: int) -> None:
        '''
        Summary:
        ---
        Sets the number of players for the game

        Parameters:
        ---

        num: the number of players 
        '''

        if not isinstance(num, int) or num < 2:
            misc.printSep()
            print(f"Invalid number of players: {num}. The number of players must be an integer greater than 1. Number of players set to default: 2")
            
            self.nPlayers = 2
        else:
            self.nPlayers = num    

    def setNextPlayer(self):
        '''
        Summary:
        ---
        Increments the current player so it is now next player's turn.
        '''
        if self.currentPlayer + 1 == self.nPlayers:
            self.currentPlayer = 0
        else: self.currentPlayer += 1
        
    def setCurrentPlayer(self: int):
        '''
        Summary:
        Sets a random player for game start
        ---
        '''

        self.currentPlayer = random.randrange(start= 0,stop= self.nPlayers,step= 1)

    def setGameMode(self, mode) -> None:
        '''
        Summary:
        ---
        Sets the game mode. Defaults to classic if invalid game mode is set

        Parameters:
        ---

        mode: the mode to be set - 'classic' or 'wild'
        '''

        vars = ['classic', 'wild']
        if mode in vars:
            self.gameMode = mode
        else:
            misc.printSep()
            print(f"Invalid game mode - {mode}! Mode can be only 'classic' or 'wild' Game mode set to default: 'classic'")

    def gameGenerateHand(self):
        '''
        Summary:
        ---
        Generates a hand based on dice values
        '''
        vals = [1,2,3,4,5,6]
        return  [random.choice(vals) for i in range(len(vals))]

    