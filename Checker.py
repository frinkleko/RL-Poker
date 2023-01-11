class Check:
    def __init__(self, players, table):
        self.POINTS = [
            "ROYALFLUSH", "STRAIGHTFLUSH", "FOUROFAKIND", "FULL", "FLUSH", "STRAIGHT",
            "TRIPLE", "TWOPAIRS", "ONEPAIR", "HIGHCARD"
        ]
        self.SUITS = ["♥", "♦", "♣", "♠"]
        self.players = players
        self.table = table
        self.player = None
        self.playersScore = [self.check() for self.player in self.players]
        self.playersScore = [POINTS.index(each) for each in self.playersScore]
        self.bestHand = min(playersScore)
        self.isItDraw = True if self.playersScore.count(self.bestHand) > 1 else False
        self.indices = None

    def check(self):

        a = self.player.cards.copy()
        if self.table is not None and self.table.cards is not None:
            a += self.table.cards.copy()
        numbers, suits = list(zip(*[[each.number, each.suit] for each in a]))
        numbers, suits = list(numbers), list(suits)
        numbers.sort()

        if 14 in numbers:
            numbers.insert(0, 1)
        coppie = {i: numbers.count(i) for i in numbers}

        HIGHCARD = True
        ONEPAIR = True if 2 in coppie.values() else False

        if self.table.cards is None:
            for value, name in list(
                    zip(*[[ONEPAIR, HIGHCARD], ['ONEPAIR', 'HIGHCARD']])):
                if value == True:
                    return name

        TWOPAIRS = True if list(coppie.values()).count(2) >= 2 else False

        TRIPLE = True if 3 in coppie.values() else False

        count = 0
        duplicates = 0
        index = 0
        a.sort(key=lambda x: x.number, reverse=True)
        rSortedTable = a

        for i in range(0, len(rSortedTable) - 1):
            if rSortedTable[i].number - 1 == rSortedTable[i + 1].number:
                count += 1
            elif rSortedTable[i].number == rSortedTable[i + 1].number:
                duplicates += 1
                continue

            else:
                if count >= 4:
                    break
                count = 0
                index = i + 1

        STRAIGHT = True if count >= 4 else False

        # colorCount = max(*[suits.count(s) for s in ["♠", "♥", "♦", "♣"]])
        suitsDict = {i: suits.count(i) for i in suits}
        FLUSH = True if sum([each in suitsDict.values()
                             for each in [5, 6, 7]]) else False

        FULL = True if list(coppie.values()).count(3) >= 2 else False
        FULL = True if 3 in coppie.values() and 2 in coppie.values() else False

        FOUROFAKIND = True if 4 in coppie.values() else False

        ROYALFLUSH = False
        STRAIGHTFLUSH = False

        if STRAIGHT and FLUSH:
            straight = rSortedTable[index:index + count + duplicates + 1]
            flushSuit = list(suitsDict.keys())[list(suitsDict.values()).index(
                max(list(suitsDict.values())))]
            straight = [card for card in straight if card.suit == flushSuit]
            if len(straight) >= 5:
                if straight[0].number == 14 and straight[-1].number == 10:
                    ROYALFLUSH = True
                else:
                    STRAIGHTFLUSH = True

        value = [[
            ROYALFLUSH, STRAIGHTFLUSH, FOUROFAKIND, FULL, FLUSH, STRAIGHT, TRIPLE,
            TWOPAIRS, ONEPAIR, HIGHCARD
        ]]
        name = [POINTS]
        for value, name in list(zip(*value + name)):
            if value == True:
                return name

    def return_type(self):

        if self.isItDraw:
            self.indices = [i for i, x in enumerate(self.playersScore) if x == self.bestHand]

            if bestHand in ['FLUSH', 'STRAIGHTFLUSH']:
                result = "FlushDraw"

            elif bestHand == 'STRAIGHT':
                result = "StraightDraw"

            elif bestHand == 'FULL':
                result = "FullDraw"

            else:
                result = self.indices

            if type(result) == list:
                result = "HighestCard"
        else:
            result = self.playersScore.index(self.bestHand)

        return result


class FlushDrawchecker(Check):
    def __init__(self, players, table):
        super().__init__(players, table)

    def check(self):

        suits = [card.suit for card in self.table.cards]
        suits = {i: suits.count(i) for i in suits}

        # Get the suit of flush
        flushSuit = max(list(suits.values()))
        flushSuit = list(suits.keys())[flushSuit]

        # Create a new list of cards only of suits
        playersSuit = []
        for i in range(len(self.players)):
            if i == self.indices:
                playersSuit.append([
                    card.number if card.suit == flushSuit else 0
                    for card in self.players[i].cards
                ])

        # Get max card
        for i in range(len(playersSuit)):
            playersSuit[i] = max(playersSuit[i])

        if all(each == 0 for each in playersSuit):
            return self.indices
        else:
            return playersSuit.index(max(playersSuit))


class StraightDrawchecker(Check):
    def __init__(self, players, table):
        super().__init__(players, table)

    def check(self):

        totalPlayers = [
            self.players[i].cards + self.table.cards if i in self.indices else 0
            for i in range(len(self.players))
        ]

        for i in range(len(totalPlayers)):
            if totalPlayers[i] != 0:
                numbers = [card.number for card in totalPlayers[i]]
                numbers = list(dict.fromkeys(numbers))
                numbers.sort(reverse=True)

                count = 0
                for i in range(len(numbers) - 1):
                    if numbers[i] - 1 == numbers[i + 1]:
                        count += 1
                    else:
                        count = 0

                    if count == 4:
                        totalPlayers[i] = max(numbers[i - 4])
                        break

        highest = max(totalPlayers)
        if totalPlayers.count(highest) > 1:
            return [i for i, x in enumerate(totalPlayers) if x == highest]
        elif totalPlayers.count(highest) == 0:
            return self.indices
        else:
            return totalPlayers.index(max(totalPlayers))


class FullDrawchecker(Check):
    def __init__(self, players, table):
        super().__init__(players, table)

    def checkFullDraw(self):
        triple = []
        double = []
        for i in range(len(self.players)):
            if i in self.indices:
                total = self.players[i].cards + self.table[i].cards
                total = [card.number for card in total]
                total = {i: total.count(i) for i in total}

                tempTriple = [key for key, value in total.items() if value == 3]
                try:
                    triple.append(max(tempTriple))
                except:
                    triple.append(0)
                    double.append(0)
                    continue

                tempDouble = [
                    key for key, value in total.items()
                    if value >= 2 and key != tempTriple
                ]
                try:
                    double.append(max(tempDouble))
                except:
                    double.append(0)

            else:
                total.append([0, 0])

        indices = [i for i, x in enumerate(triple) if x == max(triple)]
        if len(indices) > 1:
            indices = [
                i for i, x in enumerate(triple)
                if x == max(double) and i in indices
            ]
            if len(indices) > 1:
                return indices
            else:
                return indices[0]

        else:
            return indices[0]

"""
res = Check(players, table)
typ = res.return_type()
if type(typ) is str:
    if typ == "FlushDraw":
        checker = FlushDrawchecker(players, table)
        res = checker.check()
    elif typ == "...":
        pass
        "..."
"""

