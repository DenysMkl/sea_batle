class Boat:
    def __init__(self, count, length):
        self.count = count
        self.length = length


class FourDeck(Boat):
    def __init__(self, count=1, lenght=4):
        super().__init__(count, lenght)


class ThreeDeck(Boat):
    def __init__(self, count=2, lenght=3):
        super().__init__(count, lenght)


class DoubleDeck(Boat):
    def __init__(self, count=3, lenght=2):
        super().__init__(count, lenght)


class SingleDeck(Boat):
    def __init__(self, count=4, lenght=1):
        super().__init__(count, lenght)
