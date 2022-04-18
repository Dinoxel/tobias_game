from unidecode import unidecode

do_colors_display = True

levelup_stats = {
    1: {"damage": 1, "defense": 1},
    2: {"defense": 1},
    3: {"health": 10},
    5: {"damage": 1},
    6: {"defense": 1},
    7: {"health": 10},
    9: {"damage": 1, "defense": 1},
    10: {"health": 20}
}


def custom_text(string: str, *modif_arg: str):
    color, emphasis = 39, 1

    # Charge uniquement les dictionnaires si les couleurs sont activées
    if do_colors_display:
        color_list = {"white": 29,
                      "red": 31,
                      "green": 32,
                      "yellow": 33,
                      "blue": 34,
                      "magenta": 35,
                      "cyan": 36
                      }
        emphasis_list = {"bold": 1,
                         "italic": 3,
                         "underline": 4
                         }

        for modif in modif_arg:
            if modif in color_list:
                color = color_list[modif]

            if modif in emphasis_list:
                emphasis = emphasis_list[modif]

    return f"\033[{emphasis};{color};48m{string}\u001b[0m"


class Player:
    def __init__(self):
        self.name = "Tobias"

        self.health = 80
        self.max_health = self.health

        self.damage = 3
        self.items_damage = 0
        self.total_damage = self.damage + self.items_damage

        self.defense = 0
        self.items_defense = 0
        self.total_defense = self.defense + self.items_defense

        self.level = 0
        self.experience = 0
        self.exp_to_levelup = 30

        self.gold = 20
        self.inventory = dict()

        self.kill_counter = dict()
        self.effects = dict()

    # =============================================== Commandes de gestion =============================================
    # Ajoute un objet à l'inventaire


    # Ajoute un mosntre au compteur de monstre
    def add_npc_to_kill_counter(self, npc: object):
        if npc not in self.kill_counter:
            self.kill_counter[npc] = 1
        else:
            self.kill_counter[npc] += 1



    # =============================================== Commandes d'action ===============================================
    def heals_himself(self, healing_value):
        if self.health + healing_value > self.max_health:
            self.health = self.max_health
        else:
            self.health += healing_value

    # =============================================== Affichage d'informations =========================================
    # Nombre de monstres tués
    def display_kill_counter(self):
        if self.kill_counter:
            print("Nombre de monstre tués :")
            for enemy, count in self.kill_counter.items():
                print(f"x{count} {enemy.name}")


    # Noms des objets dans l'inventaire par type d'objet sélectionné
    def get_item_names(self, item_type="consumable"):
        item_names = list()

        if item_type in self.inventory:
            item_names = list(map(lambda x: unidecode(x.name.lower()), self.inventory[item_type]))

        return item_names


player = Player()
player.display_kill_counter()
