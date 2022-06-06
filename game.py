from game_classes import *
from commands import *
from unidecode import unidecode
from Levenshtein import jaro, ratio


# Chaîne de caractères en minuscule sans accents ni espaces sur les côtés
def clean_input(text_to_display: str):
    return unidecode(input(text_to_display).lower()).strip()


# Chaîne de caractère détectée d'après la liste de commandes
def get_true_input(input_command: str, list_of_commands: list):
    # input_command doit toujours être return_clean_input() afin d'avoir une chaîne de caractères propre
    # Permet de sélectionner le mot le plus pertinent d'après la plus grande distance de Jaro-Winkler et de Levenshtein
    mixed = max([(word, max(jaro(input_command, word), ratio(input_command, word))) for word in list_of_commands], key=lambda word: word[1])

    print(mixed[1], mixed[0])

    # Renvoi une chaîne de caractère vide si le score est trop faible
    return "" if len(input_command) < 1 or mixed[1] < 0.60 else mixed[0]


# Vérifie la commande
def verify_command(command_list: list, question: str, wrong_command="", is_new_game=False):
    # asked commands += '\n> '

    while True and not is_new_game:
        command = input(question + '\n> ')

        if command in command_list:
            break

        question = wrong_command
    else:
        command = "play"

    return command


game_commands = ["menu", "kill", "inv"]
game_question = 'Write "menu" to quit the game and return to the menu or "kill" to kill a monster'
wrong_text = "Invalid command"

# Définit une liste de tous les biomes
# biome_list = [biome_village, biome_forest, biome_caves, biome_dumeors_den]
# Définit un dictionnaire avec les biomes par ordre d'apparence
# biome_dict = dict(sorted({biome.turn: biome for biome in biome_list}.items(), reverse=True))

quest_return_merchant = "Retourner voir le Marchand"
quest_return_trappist = "Retourner voir le Trappeur"


class Game:
    def __init__(self):
        self.starting_biome = Biome(**data_biomes["forest"])
        self.current_biome = self.starting_biome

        self.player = Player()
        self.killed_ennemies = dict()

        self.game_over = False
        self.game_command = ""

    def add_kill_counter(self, npc_id: str):
        if npc_id not in self.killed_ennemies:
            self.killed_ennemies[npc_id] = 1
        else:
            self.killed_ennemies[npc_id] += 1

    def display_endgame_stats(self):
        if self.killed_ennemies:
            print("Nombre de monstre tués :")
            for enemy, count in self.killed_ennemies.items():
                print(f"x{count} {enemy.name}")

        print("Killed ennemies:", self.killed_ennemies)

    def start(self):
        while not self.game_over:
            self.game_command = verify_command(game_commands, game_question, wrong_text)

            if self.game_command == "kill":
                print("You killed a monster")
                self.add_kill_counter("slime_1")

            elif self.game_command == "inv":
                self.player.display_inventory()

            elif self.game_command == "menu":
                print("Game over!")
                self.game_over = True