from game_classes import *

# Implémenter système de Fog of War avec zones accessibles ou non


event = {
    "wizard_question": {
        "name": "Enigma",
        "x_loc": 0,
        "y_loc": 0,
        "fix": False
    },
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
        event_dict = {
            (5, 6): "You found a chest!"}

        for k, v in event_dict.items():
            if k == (self.y_pos, self.x_pos):
                print(v)

    def go(self, where):
        previous_pos = self.x_pos, self.y_pos

        pos_dict = {
            "right": {"row": 0, "col": 1},
            "left": {"row": 0, "col": -1},
            "up": {"row": -1, "col": 0},
            "down": {"row": 1, "col": 0}
        }

        for direction, travel in pos_dict.items():
            if direction == where and self.biome_area[self.y_pos + travel["row"]][self.x_pos + travel["col"]] != 1:
                if travel["row"] == 0:
                    self.x_pos = self.x_pos + travel["col"]
                else:
                    self.y_pos = self.y_pos + travel["row"]

        if previous_pos != (self.x_pos, self.y_pos):
            print(f"Moved {where}")
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
        player.go("up")
    elif player_input in ["down", "bot", "b", "d"]:
        player.go("down")
    elif player_input == "pos":
        player.display_pos()
    else:
        print("Wrong input")




