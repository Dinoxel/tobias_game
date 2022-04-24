from game_classes import *

# Chaque Biome doit avoir les propriétés de sa carte

# Implémenter système de Fog of War avec zones accessibles ou non
# Possibilité d'afficher une carte
# Possibilité d'aller vers les 4 points cardinaux

# # # # # # # # # # # #
# # # # # # # #   # # # # # # # # # #
# # # # #         #   |       # # x #
# # #             e   # #           # # #
# #                 # # # # # #         #
#               # # # # # # # # # # # _ #
#      [V]      #   x #             # D #
#                     #             # # #
# #       e         # #
# #           # # # # #
# # #       # # # # # #
# # # # # # # # # # # #

map1 = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1]
]

map_x = len(map1[0])
map_y = len(map1)
map_total = map_x * map_y
# print(map_x, map_y, map_total)

map2 = [
    [1, 3, 0, 0, 1],
]


event = {
    "wizard_question": {
        "name": "Enigma",
        "x_loc": 0,
        "y_loc": 0,
        "fix": False
    },
}
biome = {
    "village": {
        "name": "Village",
        "x_loc": 1,
        "y_loc": -2,
        "fix": True
    },
}


class Player_pos(Player):
    def __init__(
            self,
    ):
        super().__init__()
        self.x_pos = 0
        self.y_pos = 0

    def get_player_pos(self):
        print(self.x_pos, self.y_pos)
        return self.x_pos, self.y_pos

    def go_right(self):
        self.x_pos += 1

    def go_left(self):
        self.x_pos -= 1

    def go_up(self):
        self.y_pos += 1

    def go_down(self):
        self.y_pos -= 1



class Map:
    def __init__(self):
        self.area = None


class Biome(Map):
    def __init__(
            self,
            **kwargs
    ):
        super().__init__() #**kwargs)


map_test = Player_pos()

while True:
    player_input = input("Where do you want to go?\n> ")

    if player_input == "left":
        map_test.go_left()
    elif player_input == "right":
        map_test.go_right()
    elif player_input == "up":
        map_test.go_up()
    elif player_input == "down":
        map_test.go_down()
    elif player_input == "pos":
        map_test.get_player_pos()
    else:
        print("Wrong input")




