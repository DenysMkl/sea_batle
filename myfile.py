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
        self.all_shots = []
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
        self.previous_shoot = self.generate_new_shot()
        player.process_shot_result(self.previous_shoot)

    def generate_new_shot(self):
        while True:
            letter = choice(alp[:10])
            number = choice([str(i) for i in range(1, 11)])
            new_shot = f'{letter}{number}'
            if new_shot not in self.all_shots:
                self.all_shots.append(new_shot)
                return new_shot

    def generate_next_shoots(self, player):
        sides = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        curr_letter, curr_numb = self.previous_shoot[0], self.previous_shoot[1:]
        serialized_x, serialized_y = self.deserialize_shoot(self.previous_shoot)
        filter_sides = [(x, y) for x, y in sides if check_existence(serialized_x + x, serialized_y + y)]

        if not player.check_shot(self.previous_shoot):
            return
        for x_side, y_side in filter_sides:
            counter = 1
            while True:
                next_letter = alp[self.get_letter_dict().get(curr_letter) + y_side * counter]
                next_numb = int(curr_numb) + x_side * counter
                next_coord = f'{next_letter}{next_numb}'
                if not check_existence(self.get_letter_dict().get(next_letter, 11),
                                       int(next_numb)-1):
                    break
                player.process_shot_result(next_coord)
                if not player.check_shot(next_coord):
                    break
                self.all_shots.append(next_coord)
                counter += 1

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

    def check_shot(self, coords):
        x, y = self.deserialize_shoot(coords)
        return self.area[x][y] == '1'

    def process_shot_result(self, shot):

        if self.deserialize_shoot(shot) is None:
            return
        enemy_x, enemy_y = self.deserialize_shoot(shot)

        if self.valid_shoot(enemy_x, enemy_y):
            return
        self.received_shoots.add((enemy_x, enemy_y))
        self.hidden_area[enemy_x][enemy_y] = '+' if \
            self.check_shot(shot) else 'x'
        for boat in self.boats:
            if all(map(lambda x: x in self.received_shoots, boat.boat_coords)):
                boat.mark_fields(self.hidden_area)
                self.boats.remove(boat)

    def show_maps(self):
        for i, j in zip(self.area, self.hidden_area):
            print(i, j, sep='\t\t')
        print(end='\n\n\n\n')


b1 = Bot()
b2 = Bot()

while len(b2.boats):
    b1.make_shoot(b2)
    b1.generate_next_shoots(b2)
    b2.show_maps()
