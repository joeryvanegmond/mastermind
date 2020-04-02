import random


class GameController:
    def __init__(self, username, size, maxvalue, doubles):
        self.username = username
        self.size = size
        self.code = self.generatecode(maxvalue, doubles)
        self.roundcounter = 0
        self.blackpins = 0
        self.whitepins = 0
        self.processanwser(input())

    def generatecode(self, maxvalue, doubles):
        possibleValues = []
        i = 0
        while i < maxvalue:
            possibleValues.append(i + 1)
            i += 1
        x = 0
        code = []
        if doubles:
            while x < self.size:
                code.append(random.choice(possibleValues))
                x += 1
        else:
            while x < self.size:
                rndint = random.randint(0, len(possibleValues) - 1)
                code.append(possibleValues.pop(rndint))
                x += 1
        return code

    def processanwser(self, anwserlong):
        anwser = [int(a) for a in str(anwserlong)]
        self.roundcounter += 1
        self.whitepins = 0
        self.blackpins = 0
        codecopy = self.code.copy()
        x = 0
        while x < self.size:
            if anwser[x] == codecopy[x]:
                self.whitepins += 1
                codecopy[x] = 0
                anwser[x] = 0
            x += 1
        if self.whitepins != self.size:

            y = 0
            while y < self.size:
                if anwser[y] != 0:
                    z = 0
                    while z < self.size:
                        if anwser[y] == codecopy[z]:
                            self.blackpins += 1
                            anwser[y] = 0
                            codecopy[z] = 0
                            break
                        z += 1
                y += 1
            self.nextround()
        else:
            self.victory()

    def victory(self):
        print("You win")

    def nextround(self):
        print("Not good")
        print("W:")
        print(self.whitepins)
        print("B:")
        print(self.blackpins)
        self.processanwser(input())