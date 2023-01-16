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

The game is developed using OOP paradigm as well as 

__Useful links:__
> [Liar's dice](https://en.wikipedia.org/wiki/Liar%27s_dice)

> [Bayes theorem](https://en.wikipedia.org/wiki/Bayes%27_theorem)

> [More on Bayes theorem](https://medium.com/swlh/bayes-theorem-probability-818deb5d1613)

> [Conditional probability](https://www.nagwa.com/en/explainers/403141497934/)

## Credits and Acknowledgements
---
Special thanks to Dimitar Gradev and Huben Keranchev regarding their creative ideas on the code style and organization. Also, absolute acknowledgements for the idea of this README file!

## Contact and feedback
---

Petar Boshnakov
#####  <img src= '/assets/github-mark.png' style = 'with: 0.2em'/> [github](https://github.com/PetarBoshnakov) | [github project page](https://github.com/PetarBoshnakov/dice-game) | [bugs and feedback](https://github.com/PetarBoshnakov/dice-game/issues)