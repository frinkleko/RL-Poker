import funPIL as df
import io
import base64
import files
from PIL import Image, ImageDraw


class Card:
    def __init__(self, number, suit, image=None):
        self.number = number
        self.suit = suit
        self.image = image


class Drawcard(Card):
    def __init__(
        self,
        number,
        suit,
        image=None,
        size=100,
        FONTPATH='C:\\Windows\\Fonts\\Arial.ttf',
    ):
        super().__init__(number, suit, image)
        self.CARDB, CARDD = df.backgroundPNG(int(self.size * 1),
                                             int(self.size * 1.3), 'white')
        self.CARDB = df.roundCorners(self.CARDB, int(self.size * 0.05))
        self.Fontpath = FONTPATH

    def main(self):

        # Start with blank card
        cardB = self.CARDB.copy()
        cardD = ImageDraw.Draw(cardB)

        # Choose color for font
        if self.suit in ["♣", "♠"]:
            cardColor = 'black'
        elif self.suit in ["♥", "♦"]:
            cardColor = 'red'

        # Replace high cards with symbols
        number = self.number
        if number in [i for i in range(11, 15)]:
            number = ["J", "Q", "K", "A"][number - 11]

        # Links to which base64 image it should be used
        pasteSuit = ["♣", "♠", "♥", "♦"].index(self.suit)
        pasteSuit = [files.club, files.spade, files.heart,
                     files.diamond][pasteSuit]

        # Open the base64 image and adapts it
        pasteSuit = Image.open(io.BytesIO(
            base64.b64decode(pasteSuit))).convert('RGBA')
        pasteSuit, _ = df.resize(pasteSuit, *[int(self.size * 0.25)] * 2)

        # Define font
        font = df.fontDefiner(self.FONTPATH, int(self.size * 0.175))
        # Define coordinates
        x, y = int(self.size * 0.125), int(self.size * 0.075)
        # Define coordinates for pasting suit image
        center = df.getSize(str(number), font)
        w, h = x + center[0] // 2 - pasteSuit.width // 2, y + center[1] + int(
            self.size * 0.025)

        # Draw number / symbol, rotate, redo, exit
        for i in range(2):
            cardD = df.drawText(x, y, cardD, str(number), cardColor, font)
            cardB = df.pasteItem(cardB, pasteSuit, w, h)
            if i != 1:
                cardB, cardD = df.rotate(cardB, 180)
                # cardD = ImageDraw.Draw(cardB)

        # Define font but bigger
        font = df.fontDefiner(self.Fontpath, int(self.size * 0.5))

        # Draw big symbol at center
        center = [each // 2 for each in cardB.size]
        cardD = df.drawText(*center,
                            cardD,
                            str(number),
                            cardColor,
                            font,
                            anchor='mm')

        # Deleting for possible memory leak
        del pasteSuit
        del cardD

        # Return image in data
        return df.image_to_data(cardB)