import poker_gui as gui

from game import *

if __name__ == '__main__':
    while True:
        try:
            # call the gui(welcome) to get the game parameters
            datas = gui.startGame()
            # init main game with datas
            game = Game(*datas)
            # run the game
            game.run()
            break
        except startOver:
            pass
