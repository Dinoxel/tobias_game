from game_classes import *
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
def verify_command(command_list: list, question: str, wrong_command=""):
    while True:
        command = input(question + '\n> ')

        if command in command_list:
            break

        if wrong_command:
            print(wrong_command)

    return command


class Game:
    def __init__(self):
        self.game_over = False
        self.game_command = ""
        self.killed_ennemies = 0
        self.player = Player()
        print("Game has started!")

    def add_kill_counter(self):
        self.killed_ennemies += 1

    def display_endgame_stats(self):
        print("Killed ennemies:", self.killed_ennemies)

    def start(self):
        while not self.game_over:
            self.game_command = verify_command(game_commands, game_question, wrong_text)

            if self.game_command == "kill":
                print("You killed a monster")
                self.add_kill_counter()

            elif self.game_command == "inv":
                self.player.display_inventory()

            elif self.game_command == "lang":
                if l10n.lang == "french":
                    l10n.set_language_to("english")
                else:
                    l10n.set_language_to("french")

            elif self.game_command == "menu":
                print("Game over!")
                self.game_over = True


game_commands = ["menu", "kill", "inv", "lang"]
game_question = 'Write "menu" to quit the game and return to the menu or "kill" to kill a monster'

menu_commands = ["play", "options", 'quit']
menu_question = 'Write "play" to play or "options" to access options'

wrong_text = "Invalid command"
