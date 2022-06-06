from game_classes import *

# Implémenter système de Fog of War avec zones accessibles ou non


event_test = {
    "wizard_question": {
        "name": "Enigma",
        "loc": (1, 8),
        "fix": False,
        "desc": "Enigma",
        "damaging": 20
    }
}

current_biome = Biome(**data_biomes["forest"])


class Player_pos(Player):
    def __init__(self):
        super().__init__()

        self.biome_area = current_biome.area
        self.starting_pos = (5, 5)
        self.y_pos, self.x_pos = self.starting_pos

    def get_player_pos(self):
        return self.y_pos, self.x_pos

    def get_map_pos(self, plus_y=0, plus_x=0):
        return self.biome_area[self.y_pos + plus_y][self.x_pos + plus_x]

    def display_map(self, display_full_map=True):
        replacing_dict = {
            0: ".",  # Case
            1: "▒",  # Mur
            8: "C",  # Passage
            7: "V",  # Village
        }

        if display_full_map:
            area_to_display = self.biome_area
        else:
            def set_pos(map_area, pos):
                return map_area[pos - 2:pos + 3]

            area_to_display = [set_pos(row, self.x_pos) for row in set_pos(self.biome_area, self.y_pos)]

        zone_list = list()

        for row_num, row in enumerate(area_to_display):
            col_list = list()
            for col_num, col in enumerate(row):
                if self.get_player_pos() == (row_num, col_num):
                    col_list.append("P")
                else:
                    col_list.append(replacing_dict.get(col, "!"))
            zone_list.append(' '.join(col_list))

        if not display_full_map:
            zone_list[2] = zone_list[2][:4] + 'P' + zone_list[2][5:]

        print("╔" + "═" * (len(zone_list[0])) + '╗')
        for line in zone_list:
            print("║" + line + "║")
        print("╚" + "═" * (len(zone_list[0])) + '╝')

    def display_pos(self):
        self.display_map()
        print(self.get_player_pos())

    def event_checker(self):
        for event_name, event_info in event_test.items():
            if event_info["loc"] == self.get_player_pos():
                print(event_name)

    def go(self, where):
        directions_dict = {
            "right": {"row": 0, "col": 1},
            "left": {"row": 0, "col": -1},
            "top": {"row": -1, "col": 0},
            "bottom": {"row": 1, "col": 0}
        }

        direction = directions_dict[where]

        if self.get_map_pos(direction["row"], direction["col"]) != 1:
            print(f"Moved {where}")
            self.x_pos = self.x_pos + direction["col"]
            self.y_pos = self.y_pos + direction["row"]

            self.display_map()
            self.event_checker()

        else:
            print(f"Cannot go to the {where}")




# forest_biome = Biome(**data_biomes["forest"])
# print(vars(forest_biome))





player = Player_pos()

while True:
    player_input = input("Where do you want to go?\n> ")

    if player_input in ["left", "l"]:
        player.go("left")
    elif player_input in ["right", "r"]:
        player.go("right")
    elif player_input in ["up", "u", "top", "t"]:
        player.go("top")
    elif player_input in ["down", "bot", "b", "d", "bottom"]:
        player.go("bottom")
    elif player_input == "pos":
        player.display_pos()
    else:
        print("Wrong input")




