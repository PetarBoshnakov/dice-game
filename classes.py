# game objects

import sys
import random
import misc
import math
import stats

  
class GameController():
    '''
    Summary:
    ---
    Tha game controller runs the game

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

        self.game_mode = 'classic' # classic (default) or wild
        self.game_log = []
        self.nplayers = self.set_nplayers_default(nplayers)
        self.ndice = nplayers * 5
        self.current_player = 0
        self.player_stats = {}
        self.players_left = self.nplayers
        self.turn_counter = 0

        # initializes the players DB
        self.ini_players()
    
    def is_valid_bid(self, bid: list, ndice: int, prev_player_stats = None) -> bool:
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

        if prev_player_stats == None:
            try:
                face = bid[0]
                count = bid[1]
                bid_in_limit = face > 0 and face <= 6 and count > 0 and count <= ndice 
                
                if bid_in_limit:
                    return True
                else:
                    print('the dice must have a valid side and adequate face count')
                    return False
            except:
                print('the dice must have a valid side and adequate face count')
                return False

        if bid == 'liar':
            return True

        try:
            current_player_face = bid[0]
            current_player_count = bid[1]
        except:
            return False
        prev_player_face = prev_player_stats['Face']
        prev_player_count = prev_player_stats['Count']

        bid_in_limit = bid[0] > 0 and bid[0] <= 6 and bid[1] > 0 and bid[1] <= ndice
        
        # higher face
        curr_player_face_higher = bid_in_limit and current_player_face > prev_player_face
        curr_player_ge_face = bid_in_limit and current_player_face >= prev_player_face
        # equal faces but higher count 
        curr_player_higher_count =  bid_in_limit and curr_player_ge_face and current_player_count > prev_player_count

        if not bid_in_limit:
            print('the dice must have a valid side and adequate face count')
        
        if not curr_player_ge_face:
            print('current player incorrect face')
            
        if not curr_player_higher_count:
            print('current player incorrect count')



        return bid_in_limit and (curr_player_higher_count or curr_player_face_higher)

    def ini_players(self) -> None:    
        '''
        Summary:
        ---
        Ini the number of players for the game

        '''
        
        for i in range(1,self.nplayers + 1):
            playerX = Player(f'Player {i}')
            dice_n_count = 5
            hand = self.game_generate_hand(dice_n_count)
            self.player_stats[i-1] = {
                'Name': playerX.Name,
                'Face': 0, 
                'Count': 0, 
                'DiceN': dice_n_count, 
                'Hand': hand, 
                'Status': 'Not set'}

    def get_current_player(self):
        return self.current_player

    def get_dice_stats(self) -> dict:
        '''
        Summary:
        ---
        Calculates the dice summary for the current game.

        Returns:
        ---
        A dictionary containing the values and their counts in the game       

        '''

        players = self.nplayers
        
        dicevals = []
        for player in range(players):
            dicevals.append(self.get_player_stats(player)['Hand'])

                
        dice_glob = {
            1:0,
            2:0,
            3:0,
            4:0,
            5:0,
            6:0
        }

        for val in dicevals:
            for i in range(1,7):
                dice_glob[i] += val.count(i)

        return dice_glob


    def get_n_dice(self) -> int:
        '''
        Summary:
        ---
        Returns the current global number of dice

        '''

        dicen = 0
        keys = self.player_stats.keys()
        for key in keys:
            dicen += self.player_stats[key]['DiceN']

        return dicen
    
    def get_players_left(self) -> int:
        '''
        Summary:
        ---
        Returns the players left

        '''


        return self.players_left

    def get_player_stats(self, player: int) -> dict:
        '''
        Summary:
        ---
        Get the player's stats

        Parameters:
        ---
        player: int pointing at the player in the player dict

        Returns:
        Dict of the player current stats

        '''

        return self.player_stats[player]

    def get_prev_player(self, currPlayer) -> int:
        '''
        Summery:
        ---
        Returns the index of the previous player

        '''

        if currPlayer == 0:
            prev_player = self.nplayers - 1
        else:
            prev_player =  currPlayer - 1
        
        if self.player_stats[prev_player]['Status'] == 'out':
            prev_player = self.get_prev_player(prev_player)
        
        return prev_player

    def get_game_mode(self) -> str:
        '''
        Summary:
        ---
        Returns the current game mode

        '''

        return self.game_mode

    def get_game_state(self) -> dict:
        '''
        Returns:
        ---
        Dictionary with the current players information

        '''

        return self.player_stats
    
    def get_turn_counter(self) -> int:
        '''
        Summary:
        ---
        Returns the turncounter

        '''

        return self.turn_counter

    def print_game_state(self) -> None:
        '''
        Summary:
        ---
        Prints the game state

        Parameters:
        ---
        gameStats: the stats to be printed

        currentPlayer: the current Player index - decides whose turn it is

        '''

        player_vals = self.player_stats.keys()
        for cntr, playerVal in enumerate(player_vals):
            if self.current_player == cntr:
                print(f'==>{playerVal}: {self.player_stats[playerVal]}')
            else:
                print(f'   {playerVal}: {self.player_stats[playerVal]}')

    def set_dice_decr(self, player) -> None:
        '''
        Summery:
        ---
        Descreases if possible the number of dice available to a player

        '''
        
        current_n = self.player_stats[player]['DiceN'] 

        if current_n > 1:
            self.player_stats[player]['DiceN'] -= 1
        else:
            self.player_stats[player]['DiceN'] = 0

    def set_game_mode(self, mode) -> None:
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
            self.game_mode = mode
        else:
            misc.print_sep()
            print(f"Invalid game mode - {mode}! Mode can be only 'classic' or 'wild' Game mode set to default: 'classic'")

    def set_next_player(self) -> None:
        '''
        Summary:
        ---
        Increments the current player so it is now next player's turn.

        '''

        if self.current_player + 1 == self.nplayers:
            self.current_player = 0
        else: 
            self.current_player += 1 

        if self.player_stats[self.current_player]['Status'] == 'out':
            self.set_next_player()

    def set_next_round(self) -> None:
        '''
        Summary:
        ---
        Adjusts the player statuses and zeroes their bets. Generates new hands forthe players
        taking into account their available dice

        '''

        players = self.get_game_state()


        for player in players:
            if players[player]['DiceN'] == 0 and players[player]['Status'] != 'out':
                players[player]['Status'] = 'out'
                self.set_players_left_decr()
        
        for player in players:
            players[player]['Face'] = 0
            players[player]['Count'] = 0
            player_dice_n = players[player]['DiceN']
            players[player]['Hand'] = self.game_generate_hand(player_dice_n)
    
    def set_nplayers_default(self, nplayers) -> int:
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
            misc.print_sep()
            print(f'{nplayers} is not valid input. The number of players must be an integer. The player count is set to the default: 2')
            return 2
            
    def set_nplayers_game(self, num: int) -> None:
        '''
        Summary:
        ---
        Sets the number of players for the game

        Parameters:
        ---

        num: the number of players 

        '''

        if not isinstance(num, int) or num < 2:
            misc.print_sep()
            print(f"Invalid number of players: {num}. The number of players must be an integer greater than 1. Number of players set to default: 2")
            
            self.nplayers = 2
        else:
            self.nplayers = num    

    def set_player_bid(self, player, stats) -> None:
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
            self.player_stats[player]['Status'] = 'liar'
        else:    
            face = stats[0]
            count = stats[1]
            self.player_stats[player]['Face'] = face
            self.player_stats[player]['Count'] = count
            self.player_stats[player]['Status'] = 'bid'
    
    def set_players_left_decr(self) -> None:
        '''
        Summary:
        ---
        Decrements the current players in the game

        '''

        temp_val =  self.players_left - 1

        if temp_val == 0:
            print('players cannot be less than 1')
            self.players_left = 1
        else:
            self.players_left -= 1

    def set_start_current_player(self) -> None:
        '''
        Summary:
        ---
        Sets a random player for game start

        '''

        self.current_player = random.randrange(start= 0,stop= self.nplayers,step= 1)

    def set_turn_counter_zero(self) -> None:
        '''
        Summary:
        ---
        Zeroes the turncounter
        
        '''

        self.turn_counter = 0

    def set_turn_counter_incr(self) -> None:
        '''
        Summary:
        ---
        Increments the turn counter by 1.
        
        '''

        self.turn_counter += 1

    def game_generate_hand(self, nDice) -> list:
        '''
        Summary:
        ---
        Generates a hand based on dice values for specific die number

        Parameters:
        ---

        nDice: the number of dice to generate number for

        Returs:
        ---
        The dice hand in list format

        '''

        vals = [1,2,3,4,5,6]
        return  [random.choice(vals) for i in range(nDice)] 


class CommandInterface:
    '''
    Summary:
    ---
    reads and translates comamnds from the console
    '''

    def get_cmd(self, cmd_prompt: str, type: str):
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

        cmd = input(f'{cmd_prompt}')
        
        if cmd == 'q':
            sys.exit()
        
        if type == 'num':
            return self.process_num(cmd)

        if type == 'bid':
           return self.process_bid(cmd)

    def process_num(self, cmd: str) -> int:
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
            misc.print_sep()
            print('Please provide correct number format')
            return None

    def process_bid(self, cmd: str) -> list:
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
                misc.print_sep()
                print(f"Wrong bid format: {cmd}. Format must be 'int int' or 'liar' !")
                return [0,0]
        return valsInt
            


class GameMenu:
    
    '''
    Summary:
    ---
    Class to operate the game menu
    '''

    def __init__(self) -> None:
        '''
        Summary:
        ---
        Ini the game menu
        '''

        self.game_menu_start_screen = ['New game', 'Exit']
        self.game_menu_new_game = ['Start', 'Number of players', 'Game mode', 'Back']
        self.current_player = 0

    def select_from_menu(self, menu: list, selection_n: int) -> str:
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
        if self.check_valid_selection(menu,selection_n):
            ret_val = selection_n - 1
            return menu[ret_val]
        else:
            return
    
    def check_valid_selection(self, menu: list, selection_n: int) -> bool:
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

        len_menu = len(menu)
        n_arr = int(selection_n) - 1
        if not isinstance(selection_n, int) or n_arr < 0 or n_arr > len_menu - 1:
            return False
        return True

    def print_vals(self, vals: list) -> None:
        '''
        Summary:
        ---
        Outputs the vals array to the screen 
        '''

        for order,val in enumerate(vals, start=1):
            print(f'{order}. {val}')

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

    def __init__(self, name: str):
        super().__init__(name)

        self.truthScore = {} # holds a arbitratry value deciding how hones a player is

    def is_wild_mode(self, game: GameController):
        if game.get_game_mode() == 'wild':
            return True
        return False    

    def bid(self, game: GameController):
        '''
        Summary:
        ---
        Returns a bid

        Parameters:
        ---
        game: a game controller class instance to act upon

        '''
        
        # game globals
        wild_mode = self.is_wild_mode(game)
        dice_in_game = game.get_n_dice()
        

        # player state
        curr_player = game.get_current_player()
        prev_player = game.get_prev_player(curr_player)
        prev_player = game.get_player_stats(prev_player)
        prev_player_face = prev_player['Face']
        prev_player_count = prev_player['Count']

        e = math.floor((1/6) * dice_in_game)
        
        if wild_mode and prev_player_face > 1:
            prev_player_count
            e *= 2

        if prev_player_count > e:
            self.liar()
        
        prob_after_raise = stats.mass_prob(dice_in_game,prev_player_count + 1)

        # percentage sum must be 100
        raise_norm_per = prob_after_raise

        choice_val = random.randint(0,100)
        call_raise = choice_val <= raise_norm_per
        call_risk_raise = choice_val <= (0.3 * raise_norm_per)

        bid_face = 0
        bid_count = 0
        # bid logic here
        target_count = prev_player_count + 1

        # a risk raise is a raise that is done outside e
        if call_risk_raise and prev_player >= e:
            bid_face = prev_player_face            
            if dice_in_game > target_count:
                bid_count = target_count
            else:
                self.liar()

        # normal raise - raising within the e bounds
        elif call_raise:
            if prev_player_count < e:
                bid_face = prev_player_face
                bid_count = target_count
                if dice_in_game > target_count:
                    bid_count = target_count
                else:
                    self.liar()
            else:
                if prev_player_face < 6:
                    bid_face = prev_player_face + 1
                    bid_count = 1
                elif prev_player_face == 6 and bid_count < e:
                    bid_count = target_count
                elif prev_player_face == 6 and bid_count > e:
                    self.liar()
        else:
            self.liar()

        return [bid_face, bid_count]

                
    def liar(self) -> str:
        '''
        Summary:
        ---
        Showdown. winner is decided between current and previous player. loser 
        loses one die

        '''
        return 'liar'