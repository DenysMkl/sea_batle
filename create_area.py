from random import randint
from units import *

def create_empty_area():
    return [['0' for j in range(10)] for i in range(10)]


def choose_square(row, col):
    return randint(0, row - 1), randint(0, col - 1)


def check_existence(curr_x, curr_y, max_x, max_y):
    return 0 <= curr_x < max_x and 0 <= curr_y < max_y


def check_reservation(area, x, y):
    return area[x][y] == 'x' or area[x][y] == '1'


def add_boat(boat_size, area):
    sides = [(1, 0), (0, -1), (0, 1), (-1, 0)]
    x, y = choose_square(10, 10)

    for side in sides:
        add_square = set()
        new_x, new_y = x, y
        for i in range(boat_size):
            step_x, step_y = side
            if not check_existence(new_x, new_y, len(area), len(area[0])) or \
                    check_reservation(area, new_x, new_y):
                break
            add_square.add((new_x, new_y))
            new_x, new_y = step_x + new_x, step_y + new_y
            if len(add_square) == boat_size:
                return add_square


def reserve_squares(boat):
    sides = [(1, 0), (0, -1), (0, 1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for point in boat:
        x, y = point
        reservation_list = [(x + add_x, y + add_y) for add_x, add_y in sides]

        arr = list(filter(lambda coords: check_existence(*coords, 10, 10)
                                    and coords not in boat, reservation_list))

        yield arr


def implement_changes(area, boat, value='1'):
    for square in boat:
        x, y = square
        area[x][y] = value


def show_area(area):
    for line in area:
        print(line)
    print()


def constructor(squares, area):
    while True:
        boat = add_boat(squares, area)
        if boat:
            break
    implement_changes(area, boat)
    reserve_squares(boat)
    for i in reserve_squares(boat):
        implement_changes(area, i, 'x')


def generate_filled_area():
    area = create_empty_area()
    boats = [FourDeck(), ThreeDeck(), DoubleDeck(), SingleDeck()]
    for boat in boats:
        for count in range(boat.count):
            constructor(boat.length, area)
    return area


if __name__ == '__main__':
    for i in generate_filled_area():
        print(i)
