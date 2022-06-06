from game import *
from os import system
system('cls')


menu_commands = ["play", "options", "lang", 'quit']
menu_question = 'Write "play" to play or "options" to access options'


l10n.set_main_key('questions')
ask_menu = custom_text(l10n.get("ask_menu"), "blue")
ask_menu_fail = custom_text(l10n.get("ask_menu_fail"), "blue")
ask_options_fail = custom_text(l10n.get("ask_options_fail"), "blue")
ask_options = custom_text(l10n.get("ask_options"), "blue")
l10n.reset_main_key()


class Menu:
    def __init__(self):
        self.menu_command = ""

        self.do_colors_display = True
        self.do_lines_display = False
        self.is_loading = False  # True

        self.was_in_options = False
        self.is_new_game = False

    def start(self):
        while True:
            self.menu_command = verify_command(
                menu_commands,
                ask_menu,
                ask_menu_fail,
                is_new_game=self.is_new_game
            )

            if self.menu_command == "options":
                print("triggers options")

            elif self.menu_command == "play":
                print("Game has started!")
                game = Game()
                game.start()

                game.display_endgame_stats()
                print("Back to the menu")

            elif self.menu_command == "lang":
                if l10n.lang == "french":
                    l10n.set_language_to("english")
                else:
                    l10n.set_language_to("french")

            elif self.menu_command == "quit":
                break

        print("You quit the game.")


if __name__ == '__main__':
    Menu().start()
