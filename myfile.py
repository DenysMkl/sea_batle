import time
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
        self.previous_shoot = None
        self.fill_area()

    def fill_area(self):
        for boat in self.boats:
            boat.place_boat(self.area)

    @staticmethod
    def create_boats() -> list:
        return [FourDeck(), ThreeDeck(), ThreeDeck(), DoubleDeck(),
                DoubleDeck(), DoubleDeck(), SingleDeck(), SingleDeck(),
                SingleDeck(), SingleDeck()]

    def make_shoot(self, player):
        letter = choice(alp[:10])
        number = choice([str(i) for i in range(1, 11)])
        self.previous_shoot = letter + number
        player.process_shot_result(self.previous_shoot)

    def generate_next_shoots(self, player):
        previous_x, previous_y = self.deserialize_shoot(self.previous_shoot)
        sides = [(1, 0), (0, -1), (0, 1), (-1, 0)]
        for x, y in sides:
            print(check_existence(previous_x+x, previous_y+y))

    def valid_shoot(self, x_coord, y_coord):
        return (x_coord, y_coord) in self.received_shoots or \
               self.hidden_area[x_coord][y_coord] == 'x'

    @staticmethod
    def get_letter_dict():
        return {letter: index for index, letter in enumerate(alp[:10])}

    @staticmethod
    def get_number_dict():
        return {f'{i + 1}': i for i in range(10)}

    def deserialize_shoot(self, coord):
        letter_dict = self.get_letter_dict()
        number_dict = self.get_number_dict()
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


b1 = Bot()
b2 = Bot()
b2.show_maps()
b1.make_shoot(b2)
print(b1.previous_shoot)
b1.generate_next_shoots(b2)
# b2.show_maps()
# while len(b1.boats):
    # shoot = input('enter square: ').strip()
    # b1.process_shot_result(shoot)

    # time.sleep(5)
