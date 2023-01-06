import sys

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
        if Game_Controller.gameMode == 'wild':
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
    
class Game_Stats():
    '''
    Summary:
    ---
    Keeps the current game log - active players, who's turn is, what are the bids so far
    '''

    def __init__(self, nplayers):
        #TODO
        '''
        Symmary: 
        ---

        Parameters:
        ---
        nPlayers:
        '''
        self.nPlayers = nplayers
        self.nDice = nplayers * 5
        self.playerStats = {}
        self.ini_players()
    
    def ini_players(self):    
        '''
        Summary:
        ---
        Ini the number of players for the game
        '''
        
        for i in range(1,self.nPlayers + 1):
            self.playerStats[f'Player {i}'] = []

    def updatePlayerStats(self, player, stats):
        #TODO
        '''
        Summary:
        ---
        Update the player stats

        Parameters:
        ---
        player:

        stats: 
        '''
        if self.isValidStatsFormat(stats):
            self.playerStats[player].append(stats)

    def isValidStatsFormat(self, stats) -> bool:
        #TODO
        '''
        Summary:
        ---
        Check if provided stats are valid. 

        Parameters:
        ---
        stats: holds the last bid of a player 
        and the number of dice they have in the format: [face, nFaces, nDice]
        '''
        pass

    def getPlayerStats(self, player):
        #TODO
        '''
        Summary:
        ---
        Get the player's stats

        Parameters:
        ---
        player: 
        '''
        return self.playerStats[player]

    def isPlayerOut(self, player):
        #TODO
        '''
        Summary:
        ---
        flags a player as lost the game

        Parameters:
        ---
        player:
        '''
        #TODO
        pass
    

    def isPlayerWinner(self, player):
        #TODO
        '''
        Summary:
        ---
        flags a player as game winner

        Parameters:
        ---
        player: 
        '''
        #TODO
        pass

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
        returns the number for the command after checking or ValueError if wrong
        format was given
        '''

        num = cmd.split(' ')[0]
        
        if self.checkInt(num):
            return int(num)
        else:
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
        vals = cmd.split(' ')
        
        valsInt = []
        for val in vals:
            self.checkInt(val)
            valsInt.append(int(val))
        return valsInt
        

    def checkInt(self, val: str):
        '''
        Summary:
        ---
        checks whether a value is of type int

        Parameters:
        ---
        
        val: a text value to be checked

        Returns:
        ---
        return True if the value is int or False if the value is not

        '''

        try:
            int(val)
            return True
        except ValueError: 
            return False


class Game_Controller:
    
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
        self.nPlayers = 0
        self.gameMode = 'classic' # classic (default) or wild
        self.gameLog = []

        self.gameMenu = ['New game', 'Exit']
        self.gameMode = ['classic', 'wild']
        self.GameMenu_newGame = ['Start', 'Number of players', 'Game mode']
        self.numPlayers = ['Set number of players']


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
        if nArr < 0 or nArr > lenMenu - 1:
            return False
        return True  

    def printVals(self, vals: list) -> None:
        '''
        Summary:
        ---
        Outputs the vals array to the screen 
        '''

        for order,val in enumerate(vals, start=1):
            print(f'{order}. {val}')

    def updateLog(self, player, bid):
        #TODO
        '''
        Summary:
        ---
        updates game stats after game end

        Parameters:
        ---
        stats:

        lots:
        '''
        #TODO
        pass
    
    def updateGameStats(self, stats):
        #TODO
        '''
        Summary:
        ---
        updates game stats after game end

        Parameters:
        ---
        stats:

        lots:
        '''
        #TODO
        pass

    def checkValidBid(self, bid):
        #TODO
        '''
        Summary:
        ---
        Checks if the bid is valid


        Parameters:
        ---

        bid: The bid cannot consists of more faces than the available dice number
        '''
        #TODO
        pass


