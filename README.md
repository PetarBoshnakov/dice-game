# Readme

1. [About](#about)
1. [System requirements](#system-requirements)
1. [How to run](#how-to-run)
1. [Rules of the game](#rules-of-the-game)
1. [How to play the game](#how-to-play-the-game)
1. [Design and architechture](#design-and-architecture)
1. [Credits and Acknowledgements](#credits-and-acknowledgements)
1. [Contact and feedback](#contact)

## About
---
This game is developed as a project invitation that I found on the Strypes portal. I tried to provide a solution to a very hard problem where players are forced to use deception. More on the game can be found in the section [Rules of the game](#rules-of-the-game)

## System Requirements
---
Operating system: [^1]Windows 

Python: 3.9 or higher

Dependencies: no dependencies, packages or wheels needed 

System requirements: as long as the machine can run a console it should be just fine

[^1]: The game is developed in Python so it should be platform agnostic. However, there might be some glitches when used on other operating systems when system calls are concerned.

## How to run
To play the game you will need to run it directly from a console. To quickly start the game you can type:

> main.py -start

If you want to explore the available options you can use a __-help__ argument instead. At the moment the other main option is __-debug__. This option reveals all player hands as well as some of the percentages used by the bot in the decision making process.

## Rules of the game
---
The game is played by two or more players. Five dice are used per player with dice cups used for concealment. The game is round-based. Each round, each player rolls a "hand" of dice under their cup and looks at their hand while keeping it concealed from other players. The first player begins his turn by bidding. A bid consists of announcing any face value and a number of dice. This bid is the player's claim as to how many dice with that particular value there are on the whole table. Turns rotate among the players in a clockwise order. Each player has two choices during their turn: 

> __to make a higher bid__

> __to challenge the previous bid, by calling the last bidder liar__

Raising the bid means that the player may bid a higher quantity of the same face, or any particular quantity of a higher face. If the current player challenges the previous bid, all dice are revealed. If the bid is valid (there are at least as many of the face value as were bid), the bidder wins. Otherwise, the challenger wins. The player who loses a round loses one of their dice. The last player to still retain a die is the winner. The loser of the last round starts the bidding for the next round. If the loser of the last round was eliminated, the next player starts the new round.

The game has a 'wild' mode option. The rules for the wild mode are that the 1s are counted toward the players bid. Essentially every time the player is playing with twice as many options.

## How to play the game
---
You are provided with a settings menu in the form of:
1. New game
2. Exit

In order for you to navigate the menu you need to input the number of the menu item. For example, if you want to navigate the New Game menu, you need to press 1 and then enter. There are several setup settings that can be done in the game. You can:

> __Choose the number of players that you want to go against__

> __Choose the game mode - wild or classic__

Once you are set you can hit on start game and enjoy the challenge.

## Design and Architecture
---

### __Design__


The game is developed using OOP paradigm as well as the functional programming concept. No object mutations are allowed. 

Overview by files:

#### - main.py
#### - game.py
#### - classes.py
#### - misc.py
#### - stats.py

> main.py: 
- is used for starting the game
- sets major game stats at startup
- provides help on how to use the program

> game.py:
- contains the menu logic
- contains the game loop
- objects change their states through the game.py as the game is played

> classes.py:
- contains all user defined objects used for the game
- classes: Player, Bot, GameMenu, CommandInterface, GameController

> misc.py
- contains helper functions

> stats.py
- contains the statistical functions used for the game

### __Architecture__


![Process Diagram](/assets/process_diag.png)

The process diagram above showcaes how flow of information in the game. 

1. Player and Bot feed information to the Command Line Interface class. 
2. Purpose of the Command Line Interface is to check raw data input and make sure that this data is in correct raw data format
3. After the data is processed it can be sent to the Game Menu or Game Controller - depending on who requested it.
4. Game Menu - sets all necessary properties of the Game Controller. This can be the number of players or the game mode
5. Game Controller
    1. Receives data from Command Line Interface and checks the already processed raw data for logical consistency regarding the game logic
    2. Receives data from Game Menu as described above
6. Game Loop - runs the game. It makes sure that the higher level game logic is applied as well as outputs the information in a formatted way to the console



### __Useful links:__
> [Liar's dice](https://en.wikipedia.org/wiki/Liar%27s_dice)

> [Bayes theorem](https://en.wikipedia.org/wiki/Bayes%27_theorem)

> [More on Bayes theorem](https://medium.com/swlh/bayes-theorem-probability-818deb5d1613)

> [Conditional probability](https://www.nagwa.com/en/explainers/403141497934/)

## Credits and Acknowledgements
---
Special thanks to Dimitar Gradev and Huben Keranchev regarding their creative ideas on the code style, organization and testing. Also, absolute acknowledgements for the idea of this README file!

## Contact and feedback
---

Petar Boshnakov
##### [github](https://github.com/PetarBoshnakov) | [github project page](https://github.com/PetarBoshnakov/dice-game) | [bugs and feedback](https://github.com/PetarBoshnakov/dice-game/issues)