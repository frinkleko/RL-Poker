import classes
import poker_gui as gui
import dealerCheck
import stupid

from game import *

while True:
    try:

        datas = gui.startGame()
        game(*datas)
        break
    except startOver:
        pass
