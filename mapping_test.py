from static_functions import *

l10n = Localization()
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



class Map:
    def __init__(self, area):
        self.area = area


class Biome(Map):
    def __init__(
            self,
            **kwargs
    ):
        super().__init__(**kwargs)
