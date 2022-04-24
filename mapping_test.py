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
        self.pos = self.x_pos, self.y_pos

        self.min_x_pos = -2
        self.max_x_pos = 3
        self.min_y_pos = -2
        self.max_y_pos = 3

    def redefine_pos(self):
        self.pos = self.x_pos, self.y_pos

    def display_pos(self):
        print(self.pos)

    def go(self, where):
        if where == "right":
            if self.x_pos != self.max_x_pos:
                self.x_pos += 1
                print(f"Moved {where}")
            else:
                print(f"Cannot go {where} anymore")

        elif where == "left":
            if self.x_pos != self.min_x_pos:
                self.x_pos -= 1
                print(f"Moved {where}")
            else:
                print(f"Cannot go {where} anymore")

        elif where == "up":
            if self.y_pos != self.max_y_pos:
                self.y_pos += 1
                print(f"Moved {where}")
            else:
                print(f"Cannot go {where} anymore")

        elif where == "down":
            if self.y_pos != self.min_y_pos:
                self.y_pos -= 1
                print(f"Moved {where}")
            else:
                print(f"Cannot go {where} anymore")

        self.redefine_pos()

forest_biome = Biome(**(data_biomes["forest"]))


print(vars(forest_biome))


class Biome_map(Biome):
    def __init__(
            self,
    ):
        super().__init__("Jungle", 1, ())
        self.area = [
            [1, 3, 0, 0, 1],
        ]
        self.start_x_pos = 0
        self.start_y_pos = 1


map_test = Biome_map()


player = Player_pos()

while True:
    player_input = input("Where do you want to go?\n> ")

    if player_input == "left":
        player.go("left")
    elif player_input == "right":
        player.go("right")
    elif player_input == "up":
        player.go("up")
    elif player_input == "down":
        player.go("down")
    elif player_input == "pos":
        player.display_pos()
    else:
        print("Wrong input")




