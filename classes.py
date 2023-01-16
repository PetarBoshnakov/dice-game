# game objects

import sys
import random
import misc
import math
import stats
import time 

DEBUG_MODE = 'off'

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
        curr_player_higher_count =  bid_in_limit and curr_player_ge_face or current_player_count > prev_player_count

        if not bid_in_limit:
            misc.print_sent('the dice must have a valid side and adequate face count')
        
        if not curr_player_ge_face:
            misc.print_sent('current player incorrect face')
            
        if not curr_player_higher_count:
            misc.print_sent('current player incorrect count')



        return bid_in_limit and curr_player_higher_count and curr_player_ge_face

    def ini_players(self) -> None:    
        '''
        Summary:
        ---
        Ini the number of players for the game

        '''
        
        for i in range(1,self.nplayers + 1):
            player_x_name = Player(f'Player {i}')
            dice_n_count = 5
            hand = self.game_generate_hand(dice_n_count)
            self.player_stats[i-1] = {
                'Name': player_x_name.Name,
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

    def get_prev_player(self, curr_player) -> int:
        '''
        Summery:
        ---
        Returns the index of the previous player

        '''

        if curr_player == 0:
            prev_player = self.nplayers - 1
        else:
            prev_player =  curr_player - 1
        
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

    def print_game_state(self, DEBUG_MODE: str = 'off') -> None:
        '''
        Summary:
        ---
        Prints the game state

        Parameters:
        ---
        gameStats: the stats to be printed

        currentPlayer: the current Player index - decides whose turn it is

        debug: debug mode - showing all player stats. Can take two values 'debug' or 'off'.

        It is off by default

        '''

        player_vals = self.player_stats.keys()
        curr_player = self.get_current_player()
        prev_player = self.get_prev_player(curr_player)
        

        if DEBUG_MODE == 'off':
            for cntr, playerVal in enumerate(player_vals):
                to_print = f"{self.player_stats[playerVal]['Name']} ::: Face: {self.player_stats[playerVal]['Face']} ::: Count: {self.player_stats[playerVal]['Count']} ::: Number of Dice: {self.player_stats[playerVal]['DiceN']}"

                if curr_player == cntr and curr_player == 0:
                    to_print = f"{to_print} ::: Your dice: {self.player_stats[playerVal]['Hand']}"
                    misc.print_sent(f'==>{to_print}')
                elif curr_player == cntr:
                    misc.print_sent(f'==>{to_print}')
                elif prev_player == cntr:
                    misc.print_sent(f'   {to_print} <== Previous Player')    
                else:
                    misc.print_sent(f'   {to_print}')

        elif DEBUG_MODE == 'debug':
            for cntr, playerVal in enumerate(player_vals):
                to_print = f'{playerVal}: {self.player_stats[playerVal]}'

                if self.current_player == cntr:
                    misc.print_sent(f'==>{to_print}')
                else:
                    misc.print_sent(f'   {to_print}')

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
            misc.print_sent(f"Invalid game mode - {mode}! Mode can be only 'classic' or 'wild' Game mode set to default: 'classic'")

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
            misc.print_sent(f'{nplayers} is not valid input. The number of players must be an integer. The player count is set to the default: 2')
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
            misc.print_sent(f"Invalid number of players: {num}. The number of players must be an integer greater than 1. Number of players set to default: 2")
            
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
            misc.print_sent('players cannot be less than 1')
            self.players_left = 1
        else:
            self.players_left -= 1
    
    def set_prev_player(self) -> None:
        '''
        Summary:
        ---
        It's the previous player turn now

        '''

        if self.current_player == 0:
            self.current_player = self.nplayers - 1
        else:
            self.current_player =  self.current_player - 1
        
        if self.player_stats[self.current_player]['Status'] == 'out':
            self.set_prev_player()

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

    def get_bot_cmd(self, cmd: str):
        '''
        Summary:
        ---
        Gets a cmd from a bot in the format 'int int' or 'liar' and processes it. 

        Returns:
        a bot command in the format: [int, int] or 'liar'
        '''

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
            misc.print_sent('Please provide correct number format')
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
                misc.print_sent(f"Wrong bid format: {cmd}. Format must be 'int int' or 'liar' !")
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
            misc.print_sent(f'{order}. {val}')

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

        self.false_score = {'score': 0.3, 'true': 2, 'false': 1} # holds a arbitratry value deciding how hones a player is
    

    def is_wild_mode(self, game: GameController):
        '''
        Summary:
        ---
        Returns true if wild mode else false

        '''

        if game.get_game_mode() == 'wild':
            return True
        return False    

    def action(self, game: GameController) -> str:
        
        WILD_MODE_MULTIPL = 2
        DEFAULT_LIER_SCORE = 0.7
        RISK_RAISE_PROB = 0.4

        # game globals
        wild_mode = self.is_wild_mode(game)
        dice_in_game = game.get_n_dice()
        
        # player state
        curr_player_pos = game.get_current_player()
        prev_player_pos = game.get_prev_player(curr_player_pos)
        prev_player_stats = game.get_player_stats(prev_player_pos)
        curr_player_stats = game.get_player_stats(curr_player_pos)
        curr_player_hand_limits = self.generate_hand_limits(curr_player_stats)

        prev_player_face = prev_player_stats['Face']
        prev_player_count = prev_player_stats['Count']

        curr_player_same_face_count = curr_player_stats['Hand'].count(prev_player_face)


        e = math.floor((1/6) * dice_in_game)

        # wild mode setup
        if wild_mode and prev_player_face > 1:
            prev_player_count *= WILD_MODE_MULTIPL
            curr_player_same_face_count *= WILD_MODE_MULTIPL
            e *= WILD_MODE_MULTIPL

        # update player truth score        
        if prev_player_pos == 0 and game.get_turn_counter() > 0:
            cmd = [prev_player_face, prev_player_count]
            self.eval_truth_bet(cmd, prev_player_stats, e)

        # calculating dice probabilities
        if curr_player_same_face_count > 0 and curr_player_same_face_count <= prev_player_count:
            prob_prev_player_higher = stats.bayes_prob(dice_in_game, curr_player_same_face_count, prev_player_count) * 100
        else:
            prob_prev_player_higher = stats.mass_prob(dice_in_game, prev_player_count) * 100


        # percentage sum must be 100
        lier_score = 0.7 # actually this is the bmot's lier score
        if prev_player_pos == 0:
           lier_score = self.false_score['score'] # here the player lier score is set
        liar_perc = (100 - prob_prev_player_higher) * lier_score
        risk_raise_perc = RISK_RAISE_PROB * liar_perc

        if DEBUG_MODE == 'debug':
            misc.print_sent(f'player liar score: {lier_score}')
            misc.print_sent(f'liar perc: {liar_perc}')
            misc.print_sent(f'player false score: {self.false_score}')

        choice_val = random.randint(0,100)

        call_raise = choice_val > liar_perc
        call_bluff_raise = choice_val < risk_raise_perc

        bid_face = 0
        bid_count = 0
        # bid logic here
        target_count = prev_player_count + 1
        

        # opening raise
        if prev_player_face == 0:
            opening_hand = self.get_opening_hand(curr_player_stats)
            bid_face = opening_hand[0]
            bid_count = 1
        elif call_bluff_raise and prev_player_count <= e:
            bid_face = prev_player_face            
            if target_count < dice_in_game:
                bid_count = target_count
        # the raise logic is here
        elif call_raise:
            curr_player_hand_limits_count = curr_player_hand_limits[prev_player_face] 
            if curr_player_same_face_count > 0 and curr_player_hand_limits_count > 0 and curr_player_same_face_count < dice_in_game:
                bid_face = prev_player_face
                bid_count = prev_player_count + curr_player_hand_limits[prev_player_face]
            elif curr_player_same_face_count < dice_in_game:
                for i in range(1,7):
                    if curr_player_hand_limits[i] > 0 and i > prev_player_face:
                        bid_face = i
                        bid_count = 1
                        return f'{bid_face} {bid_count}'
                if prev_player_count + 1 < e:
                    return f'{prev_player_face} {prev_player_count + 1}'
                return 'liar'
            else:
                return 'liar'
        else:
            return 'liar'

        return f'{bid_face} {bid_count}'
        
    def generate_hand_limits(self, player_stats: dict) -> dict:
        '''
        Summary:
        ---
        Generates a summary of all faces and their counts in the current hand

        Parameters:
        ---
        player_stats: a dictionary holding the player stats

        Returns:
        ---
        a dictionary with the hand distirbtuion {1:2, 2:3.. etc}
        '''

        hand = player_stats['Hand']

        hand_glob = {
            1:0,
            2:0,
            3:0,
            4:0,
            5:0,
            6:0
        }

        for i in range(1,7):
            hand_glob[i] += hand.count(i)

        return hand_glob
    
    def eval_truth_bet(self, bet: list, player_stats: dict, e: int) -> None:
        '''
        Summarty:
        ---
        Evaluates whether the hooman lied in their bet or not.

        Parameters:

        bet: the bet to be evaluated

        hand: the hand to eval the bet against

        e: expected value for the current game run

        Returns:
        None. Updates the false_score of the bot
        '''

        
        stated_face = int(bet[0])
        stated_count = int(bet[1])

        hand_lim = self.generate_hand_limits(player_stats)

        if hand_lim[stated_face] >= stated_count or (hand_lim[stated_face] > 0 and stated_count <= e):
            self.set_update_truth_score(1)
        else:
            self.set_update_truth_score(0)
        
    
    def set_update_truth_score(self, direction: int) -> None:
        '''
        Summary:
        ---
        Increments or decrements the truth score. The truth score for the player starts
        as 1 or 100% and it is continuously updated based on the showdowns. If the 
        player didnt lie the truth score is updated accordingly

        Parameters:
        ---
        direction: 1 or 0. the number indicates pos or negative reinforcement
        '''

        if direction == 1:
            self.false_score['true'] += 1
        elif direction == 0:
            self.false_score['false'] += 1
        else:
            misc.print_sent('Please provide a valid truth score')
            return
        
        true_cases = self.false_score['true']
        false_cases = self.false_score['false']
        self.false_score['score'] = false_cases / (true_cases + false_cases) 

    def get_opening_hand(self, curr_player_stats: dict) -> str:
        '''
        Summary:
        ---
        Returns the weakest hand
        '''
        hand = self.generate_hand_limits(curr_player_stats)

        for face in range(1,7):
            hand_cnt = hand[face] 
            if hand_cnt > 0:
                return [face,hand_cnt]
    
    def print_bot_thinkig(self):
        '''
        Summary:
        ---
        Wastes some time to create the illusion of thought. Prints a funny phrase 
        in the process
        '''


        funny_phrases = [
            "Calculating the age of the universe",
            "Multiplication of variation",
            "Reversing the effect of the Big Bang",
            "Waiting at the coffee que",
            "Hold my beer",
            "Ah, that's easy just need a quick permutation calculation",
            "You gotta me kidding me",
            "Got you there, bruh?",
            "You need to up your game... Calculating your chances...",
            "A plane crashd on the border of Canada and USA. Where should the survivors be buried?",
            "You think I'm lying?",
            "Not, AI but close.."
        ]

        chosen_phrase = random.choice(funny_phrases)
        to_print = f'Bot: {chosen_phrase}'
        time_step = 0.025
        for i in range(len(to_print)):
           print(to_print[i], end='', flush=True)
           time.sleep(time_step)

        wait_multpl = random.randint(2,5)
        wait_fraction = random.randint(60,86) / 100

        to_print = '.'*wait_multpl
        for i in range(len(to_print)):
           print(to_print[i], end='', flush=True)
           time.sleep(wait_fraction)
        print()

    

