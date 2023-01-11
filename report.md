# A project for 1v1 Texas poker with stupid AI

[TOC]

## Project description 

In this project, we use OOP way design a 1v1 Texas poker game. Meanwhile, we design a simple math-based AI as the competitor for user.

## Analysis and design

For the Texas game, we need to have classes of environment like table, deck, card. We also need to have classes of player and computer. After all, a checker class/function to decide who is winner is also needed. For GUI recourses, it is also a great idea to manage with class. So the project can be divided and designed as the following parts.

【IMG】 

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



### UI



### file read and write



### Code lines number



## Test and Use



## Summary



### Further discussion