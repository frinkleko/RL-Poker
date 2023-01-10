# A project for 1v1 texas poker with stupid AI

## file structure
```
│  .gitignore
│  classes.py
│  dealerCheck.py
│  drawCard.py
│  files.py
│  playGame.py
│  poker_gui.py
│  README.md
│  requirements.txt
│  stupid.py
│
├─sounds
│      check.mp3
│      chips.mp3
│      flip.mp3
│      lose.mp3
│      win.mp3
```

## classes
contain classes of Player,Table,Card,Deck

## dealChecker
contains functions to check points and winner

## drawCard
contain function to draw a image for Card object

## file
store base64 image infos

## poker_gui
draw the gui parts and bind parts with function

## stupid
contain a math-based stupid AI

## playGame
contains logic function for one game, and repeat it in a while Loop

## OOP todo List
- [ ] add game record and review function from record file
    + store players card per turn
    + read record file and play the game in visible card mode auto
- [ ] add inherit and multi poly.. in this project
    + create player and computer class inherit participant class 
    + computer class have more details math ai content
    + create checker class to sort `dealerCheck` function
    + create card class inherit card and a draw class so that a card object contain card infos and draw function
    + create img class inherit from file class. create record class inherit from file class.
