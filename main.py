import classes
import sys

def main():
    game = classes.GameController()
    cmdI = classes.CommandInterface()

    while True:
        game.printVals(game.gameMenu)
        prompt = 'Please select option: '
        cmd = cmdI.getCmd(prompt,'num')
        while cmd == None:
            cmd = cmdI.getCmd(prompt,'num')
        layerBegin = game.selectFromMenu(game.gameMenu, cmd)
        

        if layerBegin == 'New game':
            game.printVals(game.GameMenu_newGame)
            cmd = cmdI.getCmd(prompt, 'num')

            while cmd == None:
                cmd = cmdI.getCmd(prompt, 'num')
            layerNewGame = game.selectFromMenu(game.GameMenu_newGame, cmd)
            print(layerNewGame)

            if layerNewGame == 'Start':
                pass            

            elif layerNewGame == 'Number of players':
                prompt = 'Please enter the number of players (default is 2): '
                cmd = cmdI.getCmd(prompt, 'num')
                game.setNplayers(cmd)
                print(f'Number of players: {game.nPlayers}')

            elif layerNewGame == 'Game mode':
                prompt = "Please enter the game mode - it can only be 'classic' or 'wild': "
                cmd = input(prompt)
                game.setGameMode(cmd)
                print(f'Game mode: {game.gameMode}')

        elif layerBegin == 'Exit':
            print('Sad to see you go ;(')
            sys.exit()
        


if __name__ == '__main__':
    main()