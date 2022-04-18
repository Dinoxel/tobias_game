from game import *
from os import system
system('cls')

game_commands = ["menu", "kill", "inv"]
game_question = 'Write "menu" to quit the game and return to the menu or "kill" to kill a monster'

menu_commands = ["play", "options", 'quit']
menu_question = 'Write "play" to play or "options" to access options'

wrong_text = "Invalid command"


class Menu:
    def __init__(self):
        print("Welcome into the game")
        self.menu_command = ""
        self.do_colors_display = True
        self.do_lines_display = False
        self.is_loading = False  # True

        while True:
            self.menu_command = verify_command(menu_commands, menu_question, wrong_text)

            if self.menu_command == "play":
                game = Game()
                game.start()

                game.display_endgame_stats()
                print("Back to the menu")

            elif self.menu_command == "options":
                print("triggers options")

            else:
                break

        print("You quit the game.")


if __name__ == '__main__':
    Menu()
