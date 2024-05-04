from random import choice
from string import ascii_lowercase as alp

from create_area import generate_filled_area, create_empty_area

bot_area = generate_filled_area()
user_view_area = create_empty_area()


class Bot:
    def __init__(self):
        self.area = generate_filled_area()
        self.previous_shoot = None

    def make_shoot(self):
        letter = choice(alp[:10])
        number = choice([str(i) for i in range(1, 11)])
        self.previous_shoot = letter + number

    @staticmethod
    def deserialize_shoot(coord):
        letter_dict = {letter: index for index, letter in enumerate(alp[:10])}
        number_dict = {f'{i + 1}': i for i in range(10)}
        y, x = letter_dict.get(coord[0]), number_dict.get(coord[1])
        return x, y

    def check_shoot(self): pass


    # def continue_shooting(self):
    #     sides = [(1, 0), (0, -1), (0, 1), (-1, 0)]
    #     for


def check_boats(area):
    return any('1' in line for line in area)





# def fight(user, bot):
    # while check_boats(bot):
    #     coords = make_shoot()
    #     y, x = letter_dict.get(coords[0]), number_dict.get(coords[1])
    #
    #     if bot[x][y] == '1':
    #         bot[x][y] = 's'
    #         user[x][y] = 's'
    #     else:
    #         bot[x][y] = 'm'
    #         user[x][y] = 'm'
    #
    #     for i in user:
    #         print(i)


# fight(user_view_area, bot_area)
