import Env
import poker_gui as gui
from exceptions import *
import Participant
import logging
import os
import Checker
import record


class Game():
    def __init__(self, playerName, computerName, startingMoney, minBet,
                 mode) -> None:
        self.playerName = playerName
        self.computerName = computerName
        self.startingMoney = startingMoney
        self.minBet = minBet
        self.mode = mode

        # init players and self.table
        self.player = Participant.Player(self.playerName, self.startingMoney,
                                         None, 0, None)
        self.computer = Participant.Computer(self.computerName,
                                             self.startingMoney, None, 0, None)
        self.table = Env.Table(self.minBet, self.startingMoney)

        self.window = gui.gameWindow(self.minBet, self.player, self.computer)

        self.winnerIndex = None

        # the turn can be reverse, used for indicates current turn and run the turn function
        self.turn = [lambda: self.comTurn(), lambda: self.playerTurn()]

        self.smallBlind = [
            lambda y,: y.betting(self.minBet),
            lambda y: y.betting(self.minBet * 2)
        ]
        self.smallFirst = [self.player, self.computer]

    def giveCards(self):
        # init deck for this game
        deck = Env.Deck()

        # 4 cards are drawn from deck by twice
        player_cards = self.player.giveCards(deck)
        computer_cards = self.computer.giveCards(deck)

        logging.info("Player cards: " + str(player_cards))
        logging.info("Computer cards: " + str(computer_cards))

        return deck

    def playerTurn(self):
        logging.info("Player turn")

        self.table.checkMinMaxBet(self.player, [self.computer])
        self.updateSliderAndText()

        # lock or unlock check button
        if ((self.player.bet == None and self.computer.bet == None)
                or (self.computer.bet == 0 and self.player.bet == None)):
            gui.unlockCheck(self.window)
        else:
            gui.lockCheck(self.window)

        # if begin a new game
        event, value = gui.readInput(self.window)
        logging.info("Player action: " + str(event) + " " + str(value))

        if event == 'New Game':
            raise startOver
        gui.lockButtons(self.window)
        gui.lockCheck(self.window)

        # if self.player fold
        if event == 'Fold':
            raise playerFold

        # get init betting value and print
        self.player.betting(value)
        self.updateText()

        gui.updateOut(self.window, self.actionDone(self.player, self.computer))

        # check action taken
        if event == 'Bet':
            gui.playBet()
        elif event == 'Check':
            gui.playCheck()

        # if one self.player allin, self.table is allin
        self.table.isALLIN([self.player, self.computer])
        gui.pause()

    def comTurn(self):
        logging.info("Computer turn")

        self.table.checkMinMaxBet(self.computer, [self.player])

        # stupid action
        action, bet = self.computer.main(self.table, self.player)
        logging.info("Computer action: " + str(action) + " " + str(bet))

        if action in ['Bet', 'Check']:
            self.computer.betting(bet)
        elif action == 'Fold':
            raise comFold

        self.updateText()
        if self.computer.bet == 0:
            gui.playCheck()
        else:
            gui.playBet()

        gui.updateOut(self.window, self.actionDone(self.computer, self.player))
        gui.pause()

    def bettingTime(self):
        # loop util betting end
        while True:
            for i in range(len(self.turn)):
                logging.info("Turn: " + str(i))
                self.turn[i]()
                if (self.player.bet == self.computer.bet
                        and self.player.bet != None
                        and self.computer.bet != None):
                    raise endTurn

    def foldFunction(self):
        # cal the reward and reward
        self.table.addToPot([self.player, self.computer])
        self.rewardWinner()
        self.updateText()

    def declareWinner(self):
        return Checker.checkWinner([self.player, self.computer], self.table)

    def rewardWinner(self):
        self.table.payPlayer([self.player, self.computer][self.winnerIndex])

    def updateSliderAndText(self):
        gui.updateBet(self.window, self.player)
        gui.updateText(self.window, self.player, self.computer, self.table)

    def updateText(self):
        gui.updateText(self.window, self.player, self.computer, self.table)

    def actionDone(self, p1, p2):
        if p1.getMoney() == 0 and p2.getMoney() != 0:
            return p1.name + " goes ALLIN with $" + str(p1.bet) + "!!!!"
        elif p1.getMoney() == 0 and p2.getMoney() == 0:
            return p1.name + " follows ALLIN with $" + str(p1.bet) + "!!!!"
        elif p1.bet == 0:
            return p1.name + " checks."
        elif p2.bet == None:
            return p1.name + " bets $" + str(p1.bet)
        elif p1.bet > p2.bet:
            return p1.name + " raises $" + str(p1.bet)
        elif p1.bet == p2.bet:
            return p1.name + " calls " + p2.name + " with $" + str(p1.bet)

    def clear(self):
        self.table.clear()
        self.player.clear()
        self.computer.clear()
        gui.clear(self.window)

    #############################################################################

    def run(self):
        record_dict = record.load_dict()
        if os.path.exists('log') == False:
            os.mkdir('log')
        logging.basicConfig(
            handlers=[
                logging.FileHandler(filename='log/{}_{}.txt'.format(
                    self.player.name, self.computer.name),
                    encoding='utf-8',
                    mode='a+')
            ],
            format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
            datefmt="%F %A %T",
            level=logging.INFO)
        while self.player.getMoney() != 0 and self.computer.getMoney() != 0:
            logging.info('New Game')
            try:
                # Reset all the self.table
                self.clear()
                logging.info('Clear')

                # Shuffle deck and give cards
                logging.info('Give cards')
                deck = self.giveCards()
                gui.giveCards(self.window, self.player)

                # Update GUI points
                self.player.points = Checker.Check(
                    [self.player], self.table).check(self.player)
                gui.updatePoints(self.window, self.player.points)

                self.smallBlind[0](self.smallFirst[0])
                self.updateText()
                gui.playBet()
                gui.pause()
                self.smallBlind[1](self.smallFirst[1])
                self.updateText()
                gui.playBet()
                gui.pause()

                self.turn.reverse()
                # self.smallBlind.reverse()
                self.smallFirst.reverse()

                # check if allin in self.table
                self.table.isALLIN([self.player, self.computer])
                logging.info('Table allin:{}'.format(self.table.allin))
                self.updateText()

                phase = ["Flop", "Turn", "River"]
                for i in range(3):
                    if self.table.allin == False:
                        try:
                            self.bettingTime()
                        except endTurn:
                            self.updateText()
                            self.table.addToPot([self.player, self.computer])
                            self.updateText()
                            gui.updateOut(self.window, phase[i] + "!")

                    self.table.flop(deck)
                    gui.updateFlop(self.window, self.table)
                    self.player.points = Checker.Check(
                        [self.player], self.table).check(self.player)
                    gui.updatePoints(self.window, self.player.points)
                    self.updateText()

                try:
                    if self.table.allin == False:
                        self.bettingTime()
                except endTurn:
                    self.updateText()

                self.table.addToPot([self.player, self.computer])

                # Flip COM cards
                gui.flipCOM(self.window, self.computer)

                # Checking winner
                self.winnerIndex = self.declareWinner()

                if self.winnerIndex == 1:
                    result = "Computer Win"
                else:
                    result = "Player Win"

                # Winning or losing interactive response
                self.player.points = Checker.Check(
                    [self.player], self.table).check(self.player)
                self.computer.points = Checker.Check(
                    [self.computer], self.table).check(self.computer)

                ai_card = self.computer.points
                player_card = self.player.points
                label = ai_card + '\t' + player_card + '\t' + result
                record_dict.setdefault(label, 0)
                record_dict[label] += 1

                logging.info('Player points:{}'.format(self.player.points))
                logging.info('Computer points:{}'.format(self.computer.points))

                gui.updateOut(
                    self.window,
                    [self.player, self.computer][self.winnerIndex].name +
                    " wins $" + str(self.table.pot) + " with " +
                    [self.player, self.computer][self.winnerIndex].points +
                    "!!")

                logging.info('Winner:{}'.format([self.player, self.computer
                                                 ][self.winnerIndex].name))

                gui.playHand(self.winnerIndex)
                self.rewardWinner()
                self.updateText()

                # Waiting for continue or new game, analyze the self.table
                if gui.readInput(self.window, True)[0] == 'New Game':
                    raise startOver

            except playerFold:
                logging.info('Player fold')
                self.winnerIndex = 1
                self.foldFunction()
                gui.playHand(self.winnerIndex)

            except comFold:
                logging.info('Computer fold')
                self.winnerIndex = 0
                self.foldFunction()
                gui.playHand(self.winnerIndex)

        record.write_file(record_dict)
        record.print_info()
        self.window.close()
        return None

    def debug(self):
        self.player.money = 1000
        self.computer.money = 1000
        self.player.bet = 0
        self.computer.bet = 0
        self.player.points = None
        self.computer.points = None
        self.table.pot = 0
        self.table.allin = False
        self.table.cards = []
        self.player.cards = []
        self.computer.cards = []

        if os.path.exists('log') == False:
            os.mkdir('log')
        logging.basicConfig(
            handlers=[
                logging.FileHandler(filename='log/debug_{}_{}.txt'.format(
                    self.player.name, self.computer.name),
                    encoding='utf-8',
                    mode='a+')
            ],
            format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
            datefmt="%F %A %T",
            level=logging.INFO)
        self.run()
