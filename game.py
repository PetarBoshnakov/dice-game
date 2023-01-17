# the actual game happens here

import classes
import sys
import misc

def push_menu(stak: list, menu: list):
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

def game_menu():
    '''
    Summary:
    ---
    Iterates the game menus and starts the game
    '''
    game_menu = classes.GameMenu()
    cmd_i = classes.CommandInterface()
    game_new = classes.GameController(2)

    curr_menu = game_menu.game_menu_start_screen
    path_stack = []
    push_menu(path_stack,curr_menu)
    while True:
        
        misc.print_sep()
        curr_menu = path_stack[-1]
        game_menu.print_vals(curr_menu)

        prompt = 'Please select option: '
        cmd = cmd_i.get_cmd(prompt,'num')
        
        while cmd == None:
            cmd = cmd_i.get_cmd(prompt,'num')
        selection = game_menu.select_from_menu(curr_menu, cmd)
        

        if selection == 'New game':
            push_menu(path_stack, game_menu.game_menu_new_game)

        elif selection == 'Start':

            misc.print_sent('starting game....')
            play_game(game_new) 

        elif selection == 'Number of players':
            prompt = 'Please enter the number of players (default is 2): '
            cmd = cmd_i.get_cmd(prompt, 'num')
            game_new.set_nplayers_game(cmd)
            misc.print_sent(f'Number of players: {game_new.nplayers}')
            misc.action_to_continue()

        elif selection == 'Game mode':
            prompt = "Please enter the game mode - it can only be 'classic' or 'wild': "
            cmd = input(prompt)
            game_new.set_game_mode(cmd)
            misc.print_sent(f'Game mode: {game_new.game_mode}')
            misc.action_to_continue()


        elif selection == 'Exit':
            misc.print_sent('Sad to see you go ;(')
            sys.exit()

        elif selection == 'Back':
            path_stack.pop()
        
        else:
            misc.print_sent('Please select a valid menu item by inputing a menu number. For example 1 unless advised otherwise.')
            misc.action_to_continue

def play_game(game: classes.GameController):
    '''
    Summary:
    ---
    Runs the actual game
    '''

    cmdI = classes.CommandInterface()
    game = classes.GameController(game.nplayers)
    game.set_start_current_player()
    bot = classes.Bot('KilaPlaya')

    misc.print_sent("Bid in the form of 'int int' or 'liar'. Press 'q' to quit the current game.")
    misc.action_to_continue()
    
    # game loop
    while True:
        
        # curr_player = game.get_current_player()
        # turn_counter = game.get_turn_counter()
        # if curr_player != 0 and turn_counter == 0:
        #     misc.action_to_continue()
        misc.print_sep()

        # check if we have a winner
        if game.get_players_left() == 1:
            misc.print_sep()
            curr_player = game.get_current_player()
            curr_player_stats = game.get_player_stats(curr_player)
            game.print_game_state()
            misc.print_sent(f"{curr_player_stats['Name']} is the winner!")
            break
        
        # print game state
        game.print_game_state()

        # get current player input
        curr_player = game.get_current_player()
        if curr_player > 0:
            bot_cmd = bot.action(game)
            cmd = cmdI.get_bot_cmd(bot_cmd)
            bot.print_bot_thinkig()
            if cmd == 'liar':
                misc.print_sent('Bot bid ==> liar')
            else:
                misc.print_sent(f'Bot bid ==> Face:{cmd[0]} :: Count:{cmd[1]}')
        else:
            curr_turn = game.get_turn_counter()
            cmd = cmdI.get_cmd('Your bid (face, count): ', 'bid', curr_turn)

        # check if the prev player is a liar and adjust dice count accordingly
        curr_turn = game.get_turn_counter()
        
        if cmd == 'liar' and curr_turn > 0:
            curr_player = game.get_current_player()
            prev_player = game.get_prev_player(curr_player)
            dice_counts = game.get_dice_stats()
            curr_player_stats = game.get_player_stats(curr_player)
            prev_player_stats = game.get_player_stats(prev_player)
            prev_player_face = game.get_player_stats(prev_player)['Face']
            prev_player_count = game.get_player_stats(prev_player)['Count']
         
            # wild mode setting
            game_mode = game.get_game_mode()
            if game_mode == 'wild' and prev_player_face > 1:
                prev_player_count += dice_counts[1]

            # checks if the prev player has correct face count
            # if they do, the curr players loses a die

            # sets the turn counter to zero since we are dealing new hands
            if dice_counts[prev_player_face] >= prev_player_count:
                
                # reveal player hands
                print()
                misc.print_sent(f"{curr_player_stats['Name']} loses 1 die")
                print()
                print('Player hands:')
                game.print_game_state(showdown=True)
                
                # prepare game for next round
                game.set_dice_decr(curr_player)
                if curr_player_stats['DiceN'] == 0:
                    game.set_next_player()

                # update hooman_player_truth score
                game.set_next_round()
                game.set_turn_counter_zero()
                misc.action_to_continue()
                continue
            
            else:
                # reveal player hands
                print()
                misc.print_sent(f"{prev_player_stats['Name']} loses 1 die")
                print()
                print('Player hands:')
                game.print_game_state(showdown=True)

                game.set_dice_decr(prev_player)
                if prev_player_stats['DiceN'] > 0:
                    game.set_prev_player()
                game.set_next_round()
                game.set_turn_counter_zero()
                misc.action_to_continue()
                continue
        
        # check for input on first round
        # if invalid input - again
        valid_bid = game.is_valid_bid(cmd, game.get_n_dice())
        if curr_turn == 0 and valid_bid:
            game.set_player_bid(game.current_player,cmd)
            game.set_next_player()
            game.set_turn_counter_incr()
            misc.action_to_continue()
            continue
        elif curr_turn == 0 and not valid_bid:
            misc.action_to_continue()
            continue
        
        # checks the input after first round
        curr_player = game.get_current_player()
        prev_player = game.get_prev_player(curr_player)
        curr_player_stats = game.get_player_stats(curr_player)
        prev_player_stats = game.get_player_stats(prev_player)
        if not game.is_valid_bid(cmd, game.get_n_dice(), prev_player_stats):
            misc.action_to_continue()
            continue
        
        # continue to next player
        game.set_player_bid(game.get_current_player(),cmd)
        game.set_next_player()
        game.set_turn_counter_incr()
        misc.action_to_continue()
        