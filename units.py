from create_area import add_boat, implement_changes, reserve_squares, create_empty_area


class Boat:
    def __init__(self, length):
        self.boat_coords = set()
        self.reserve_coords = set()
        self.length = length

    def mark_fields(self, area):
        for square in reserve_squares(self.boat_coords):
            self.reserve_coords.update(square)
        implement_changes(area, self.reserve_coords, 'x')

    def place_boat(self, area):
        while True:
            self.boat_coords = add_boat(self.length, area)
            if self.boat_coords:
                break
        implement_changes(area, self.boat_coords)
        self.mark_fields(area)


class FourDeck(Boat):
    def __init__(self, lenght=4):
        super().__init__(lenght)


class ThreeDeck(Boat):
    def __init__(self, lenght=3):
        super().__init__(lenght)


class DoubleDeck(Boat):
    def __init__(self, lenght=2):
        super().__init__(lenght)


class SingleDeck(Boat):
    def __init__(self, lenght=1):
        super().__init__(lenght)


if __name__ == '__main__':
    b = FourDeck()
    u_area = create_empty_area()
    for i in u_area:
        print(i)