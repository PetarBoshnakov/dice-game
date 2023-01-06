import classes

def main():
    gameControl = classes.Game_Controller()
    cmdI = classes.CommandInterface()

    gameControl.setNplayers('df')
    print(gameControl.nPlayers)
    print(isinstance(2, int))
if __name__ == '__main__':
    main()