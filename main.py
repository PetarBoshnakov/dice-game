import classes

def main():
    gameControl = classes.Game_Controller()
    cmdI = classes.CommandInterface()
    
    while True:
        menu = gameControl.GameMenu_newGame
        gameControl.printVals(menu)
        val = cmdI.getCmd("please select menu item or 'q' to quit the app: ",'num')
        print(gameControl.selectFromMenu(menu,val))


if __name__ == '__main__':
    main()