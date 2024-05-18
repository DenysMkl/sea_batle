from random import choice
from string import ascii_lowercase as alp

from create_area import check_existence, create_empty_area
from units import SingleDeck, FourDeck, ThreeDeck, DoubleDeck


class Bot:
    def __init__(self):
        self.area = create_empty_area()
        self.hidden_area = create_empty_area()
        self.received_shoots = set()
        self.boats = self.create_boats()
        self.fill_area()

    def fill_area(self):
        for boat in self.boats:
            boat.place_boat(self.area)

    @staticmethod
    def create_boats() -> list:
        return [FourDeck(), ThreeDeck(), ThreeDeck(), DoubleDeck(),
                DoubleDeck(), DoubleDeck(), SingleDeck(), SingleDeck(),
                SingleDeck(), SingleDeck()]

    # def make_shoot(self):
    #     letter = choice(alp[:10])
    #     number = choice([str(i) for i in range(1, 11)])
    #     self.previous_shoot = letter + number

    def valid_shoot(self, x_coord, y_coord):
        return (x_coord, y_coord) in self.received_shoots or \
               self.hidden_area[x_coord][y_coord] == 'x'

    @staticmethod
    def deserialize_shoot(coord):
        letter_dict = {letter: index for index, letter in enumerate(alp[:10])}
        number_dict = {f'{i + 1}': i for i in range(10)}
        try:
            y, x = letter_dict.get(coord[0]), number_dict.get(coord[1:])
        except TypeError:
            return
        return None if x is None or y is None else (x, y)

    def check_shot(self, x, y):
        return self.area[x][y] == '1'

    def process_shot_result(self, shot):
        if self.deserialize_shoot(shot) is None:
            return
        enemy_x, enemy_y = self.deserialize_shoot(shot)

        if self.valid_shoot(enemy_x, enemy_y):
            return
        self.received_shoots.add((enemy_x, enemy_y))
        self.hidden_area[enemy_x][enemy_y] = '+' if \
            self.check_shot(enemy_x, enemy_y) else 'x'

        for boat in self.boats:
            if all(map(lambda x: x in self.received_shoots, boat.boat_coords)):
                boat.mark_fields(self.hidden_area)
                self.boats.remove(boat)
                print(self.boats)
        self.show_maps()

    def show_maps(self):
        for i, j in zip(self.area, self.hidden_area):
            print(i, j, sep='\t\t')


def check_boats(area):
    return any('1' in line for line in area)


b = Bot()
b.show_maps()
while check_boats(b.area):
    shoot = input('enter square: ').strip()
    b.process_shot_result(shoot)
