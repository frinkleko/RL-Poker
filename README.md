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

## hints for OOP in python
+ write private/protected function by add "__" before function name, like "__add", teh same for variable ("__name")

+ For python is a dynamic weak type language, polymorphism for derived class use same name function is just define the same name function 

+ if you want to use base class function, use `super` in init function

+ to define a abstract class and function use 

  ```python
  class File(metaclass=abc.ABCMeta):  # 同一类事物:文件
      @abc.abstractmethod
      def click(self):
          pass
  ```

+ define a interface to use polymorphism like 

  ```python
  peo=People()
  dog=Dog()
  pig=Pig()
  
  peo.talk()
  dog.talk()
  pig.talk()
  
  def func(obj):
      obj.talk()
  ```

  