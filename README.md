# Move-tac-toe
Extended version of tic-tac-toe game.

<img src="https://raw.githubusercontent.com/BarnaSir/move-tac-toe/master/images/demo/game_0.png" width="420"><img src="https://raw.githubusercontent.com/BarnaSir/move-tac-toe/master/images/demo/game_1.png" width="420"> 

## Short Description:
Move-tac-toe, self-coined name for this game, is a modified form of tic-tac-toe game where the number of pieces for each player is limited to 3, and the players should move 
their pieces after finishing up their 3 pieces. The objective of this game is to arrange the like pieces linearly and the game is won by whoever does that first with his/her pieces. User can play against AI.

## Requirements:
- Python 3
- Tkinter (Python GUI library)
- Playsound (Python audio library)

## Dependencies
 Install tkinter and playsound by executing the following commands in the terminal.
```
$ sudo apt-get update
$ sudo apt-get install python3-tk
$ sudo pip install playsound
```

## Instructions:
* Run main.py with python3 as the interpreter(shebang would take care in our file) and the game will be started with a pop-up containing some instructions.
```
./main.py
```
* Single click will allow the filling of the pieces in the empty locations.
* When all the pieces (3 per player) of a player are filled, then each player can move his/her piece by dragging.
