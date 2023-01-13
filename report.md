# A project for 1v1 Texas poker with stupid AI

[TOC]

## Project description 

In this project, we use OOP way design a 1v1 Texas poker game. Meanwhile, we design a simple math-based AI as the competitor for user.

### Usage

```bash
pip install -r requirements.txt
python playGame.py
```

## Analysis and design

For the Texas game, we need to have classes of environment like table, deck, card. We also need to have classes of player and computer. After all, a checker class/function to decide who is winner is also needed. For GUI recourses, it is also a great idea to manage with class. So the project can be divided and designed as the following parts.

![image-20230113132947250](https://raw.githubusercontent.com/frinkleko/PicgoPabloBED/main/images_for_wechatimage-20230113132947250.png)

```
│  Card&draw.py
│  Checker.py
│  drawCard.py
│  Env.py
│  exceptions.py
│  files.py
│  files_content.py
│  game.py
│  Participant.py
│  playGame.py
│  poker_gui.py
│  README.md
│  report.md
│  requirements.txt
```

## Technical requirements

### Classes (more than 5) & Objects

As we mentioned in analysis part, our project have many class and objects.

In `Env.py`, we have three classes: Table,Card,Deck.

In `Partipants.py`, we have three class: Participants,Player,Computer.

In `Checker.py`, we have a base and some derived class for checking the final results.

The game class, which contain all content for the game running, include all the instance of bellowing class .

### Encapsulation

For class Participants and its derived classes Player and Computer, we set the member variable `cards` and `money` private for security consideration.

```python
class Participant:
    def __init__(self, name,money=0,cards=None,bet=None,points=None):
        self.name = name
        self.__cards = cards
        self.__money  = money
        self.bet = bet
        self.points = points
        self.allin = False
        self.minBet = None
        self.maxBet = None

    def getMoney(self):
        return self.__money

    def setMoney(self, money):
        self.__money  = money
    
    def getCards(self):
        return self.__cards
    
    def setCards(self, cards):
        self.__cards = cards

    def giveCards(self, deck):
        self.__cards = deck.draw(2)
        return [str(each) for each in self.__cards]
    ...
```

### Inheritance

As we just mentioned, the Computer and Player are inherit from the Participants class.

```python
class Player(Participant):
	...
class Computer(Participant):
	...
```

Another example for inheritance in our project is File class. As you can see, the base File class is an abstract class.

```python
import abc
import base64
import funPIL as df
import io
import base64
from PIL import Image, ImageDraw

class File(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, name, mode):
        pass
    @abc.abstractmethod
    def read(self):
        pass
    @abc.abstractmethod
    def write(self):
        pass

class Record(file):
    def __init__(self, name, mode):
        self.name = name
        self.mode = mode
        self.file = open(self.name, self.mode)
    def read(self):
        return self.file.read()
    def write(self, content):
        self.file.write(content)

class Img(file):
    def __init__(self, name, mode = 'r'):
        self.name = name
        self.mode = mode
        self.file = open(self.name, mode=mode)
        self.image = Image.open(io.BytesIO(base64.b64decode(self.data.read()))).convert('RGBA')
    def read(self, name, mode='r'):
        self.file = open(name,mode=mode)
        self.image = Image.open(io.BytesIO(base64.b64decode(self.file.read()))).convert('RGBA')
    def write(self, content, mode='w'):
        self.file = open(self.name, mode=mode)
        self.file.write(base64.b64encode(content))
    def resize(self, size):
        self.image, _ = df.resize(self.image, *size)
        return self.image
```

### polymorphism
`Checker.py` contains some methods to detect the different results of game matches. The base Check class and derived various check class have show the polymorphism. All of them have the same name method called check. For that, we can use a function which parameter is any of these  class and call their check function. Same interface, different results.

```python
class Check:
    def __init__(self, players, table):
        self.players = players
        self.table = table
        self.player = None
        self.playersScore = [self.check(self.player) for self.player in self.players]
        self.playersScore = [POINTS.index(each) for each in self.playersScore]
        self.bestHand = min(self.playersScore)
        self.isItDraw = True if self.playersScore.count(self.bestHand) > 1 else False
    
    def check(self,player):
        ...
```

```python
class FullDrawchecker(Check):
    def __init__(self, players, table):
        super().__init__(players, table)
    
    def check(self,player):
        ...
    
class StraightDrawchecker(Check):
    def __init__(self, players, table):
        super().__init__(players, table)
    
    def check(self,player):
        ...
    
class FlushDrawchecker(Check):
    def __init__(self, players, table):
        super().__init__(players, table)
    
    def check(self,player):
        ...
```

```python
checker = Check()
checkpoints_result = checker.check()
result1 = FullDrawchecker(players, table).check()
result2 = StraightDrawchecker(players, table).check()
result3 = FlushDrawchecker(players, table).check()
```
```python
def checkWinner(players, table):
    first_check = Check(players, table)
    typ = first_check.return_type()
    if typ:

        indices = [i for i, x in enumerate(first_check.playersScore) if x == first_check.bestHand]

        if first_check.bestHand in ['FLUSH', 'STRAIGHTFLUSH']:
            checker = FlushDrawchecker(players, table)
            res = checker.check(indices)

        elif first_check.bestHand == 'STRAIGHT':
            checker = StraightDrawchecker(players, table)
            res = checker.check(indices)

        elif first_check.bestHand == 'FULL':
            checker = FullDrawchecker(players, table)
            res = checker.check(indices)
        else:
            res = indices

        if type(res) == list:
            res= checkHighestCard(players, res)

    else:
        res = first_check.playersScore.index(first_check.bestHand)

    return res
```
### UI

This project use `PySimpleGUI` as the GUI module.  All the UI codes is stored in `poker_gui.py`

We design two GUI windows. One is the Welcome UI for inputting basic info.

![image-20230111231855780](https://raw.githubusercontent.com/frinkleko/PicgoPabloBED/main/images_for_wechatimage-20230111231855780.png)

The other is the game UI for playing.

![image-20230111233320007](https://raw.githubusercontent.com/frinkleko/PicgoPabloBED/main/images_for_wechatimage-20230111233320007.png)

![image-20230111233344952](https://raw.githubusercontent.com/frinkleko/PicgoPabloBED/main/images_for_wechatimage-20230111233344952.png)

### file read and write

In file read and write part, 

All the Game information is  written in log file. Logging info are format like:

```bash
2023-01-11 Wednesday 21:43:38 root:INFO:New Game
2023-01-11 Wednesday 21:43:38 root:INFO:Clear
2023-01-11 Wednesday 21:43:38 root:INFO:Give cards
2023-01-11 Wednesday 21:43:38 root:INFO:Player cards: ['11♣', '7♠']
2023-01-11 Wednesday 21:43:38 root:INFO:Computer cards: ['3♥', '13♥']
2023-01-11 Wednesday 21:43:39 root:INFO:Nobody bet 500
2023-01-11 Wednesday 21:43:41 root:INFO:StupidAI bet 1000
2023-01-11 Wednesday 21:43:42 root:INFO:Table allin:False
2023-01-11 Wednesday 21:43:42 root:INFO:Turn: 0
2023-01-11 Wednesday 21:43:42 root:INFO:Player turn
2023-01-11 Wednesday 21:43:44 root:INFO:Player action: Bet 500
2023-01-11 Wednesday 21:43:44 root:INFO:Nobody bet 500
2023-01-11 Wednesday 21:43:46 root:INFO:Flop
2023-01-11 Wednesday 21:43:46 root:INFO:Cards on table: [14♥, 6♦, 5♥]
...
2023-01-11 Wednesday 21:52:12 root:INFO:Player points:TRIPLE
2023-01-11 Wednesday 21:52:12 root:INFO:Computer points:TRIPLE
2023-01-11 Wednesday 21:52:12 root:INFO:Winner:StupidAI
```

We read file from logging file and image file. Image files are stored as base64, it’s easy and also save for both writing and reading. In Image Class:

```python
import base64
import funPIL as df
import io
import base64
from PIL import Image, ImageDraw

class Img(file):
    def __init__(self, name, mode = 'r'):
        self.name = name
        self.mode = mode
        self.file = open(self.name, mode=mode)
        self.image = Image.open(io.BytesIO(base64.b64decode(self.data.read()))).convert('RGBA')
    def read(self, name, mode='r'):
        self.file = open(name,mode=mode)
        self.image = Image.open(io.BytesIO(base64.b64decode(self.file.read()))).convert('RGBA')
    def write(self, content, mode='w'):
        self.file = open(self.name, mode=mode)
        self.file.write(base64.b64encode(content))
    def resize(self, size):
        self.image, _ = df.resize(self.image, *size)
        return self.image
```

In the report.dat file, the results of each round are stored, including: the computer's hand, the player's hand, the win/loss result and the number of times this result occurred.
In record.dat file, data are stored in this form:
```python
ONEPAIR	STRAIGHT	Player Win	1
```
load_dict() : Loads the dictionary generated by the current game result and is used to update it during the game.

write_file() : Write the dict that store the results into the record file.

print_info() : Visualize the results of all games
```python
def load_dict():
    with open('record.dat', 'r') as f:
        dict = {}
        for i in f.readlines():
            info = i.replace('\n', '').split('\t')
            label = '\t'.join(info[:3])
            dict[label] = int(info[-1])
        return dict


def write_file(dict):
    with open('record.dat', 'w') as f:
        for k in dict.keys():
            f.write(k)
            f.write('\t')
            f.write(str(dict[k]))
            f.write('\n')


def print_info():
    with open('record.dat', 'r') as f:
        print("Matchups:")
        print("----------------------")
        for i, info in enumerate(f.readlines()):
            info = info.replace('\n', '').split('\t')
            print("Round" + str(i) + ":", "Computer: " + info[0], "Player: " + info[1], "Game result: " + info[2],
                  "times: " + info[3])
```
### Code lines number



## Test and Use

### normal test

In normal test, program finish one game normally. All the cards and money are granted to be greater or equal to 0. 

![image-20230112001047424](https://raw.githubusercontent.com/frinkleko/PicgoPabloBED/main/images_for_wechatimage-20230112001047424.png)

### bound test

For the bet amount will be limited by the slider, while the slider is limited by plater’s balance, the bet per turn will be normal. Firstly, accomplish the bound test by bet the min or max bet. Secondly, test the basic info’s bound.

In the second test, for python have been designed for huge number, the input number have no limit commonly. Meanwhile, in the basic input GUI, startingMoney and minBet are checked to granted normal running.

```python
if event == "START":
    playerName, computerName, startingMoney, minBet, mode = (
    values["PLAYERNAME"].strip("\n").strip(" "),
    values["COMPUTERNAME"].strip("\n").strip(" "),
    values["STARTINGMONEY"].strip("\n").strip(" "),
    values["MINBET"].strip("\n").strip(" "),
    values["GAMEMODE"].strip("\n").strip(" "),
    )
    if startingMoney.isdigit() and minBet.isdigit():
        startingMoney, minBet = int(startingMoney), int(minBet)
        if startingMoney > minBet:
            window.close()
            return playerName, computerName, startingMoney, minBet, mode

```

Thus, for the second bound test, startingMoney is 1 and minBet is 1. The program passes this

## Summary

In this project, we design 1v1 Texas game with GUI and a simple AI in OOP way. OOP is a great concept, which helps the project to organize all the parts and help to write codes more effectively.

### Further discussion

We design this game for fun. Meanwhile, we also want to have further practice of this game. We mainly have two goal to achieve in future.

+ make this game online and more players can join in one game

+ apply reinforce learning to this game