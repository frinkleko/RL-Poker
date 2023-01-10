import poker_gui as gui

from game import *

if __name__ == '__main__':
    while True:
        try:
            datas = gui.startGame()
            game = Game(*datas)
            game.run()
            break
        except startOver:
            pass
