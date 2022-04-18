from itertools import cycle
from threading import Thread
from time import time, sleep
from sys import stdout
from random import randrange, choice
from os import system
from unidecode import unidecode
from Levenshtein import jaro, ratio
from datetime import timedelta
from game_data import *
from static_functions import *
system('cls')

# To Do List:
# Importants :

# Ajout du village de départ et de quêtes possibles pour gagner de l'expérience/gold
## Plusieurs quêtes disponibles (2 à la fois max)

# Village - Lieux
# Boutique pour Marchand
# 2/3 villageois avec des lignes de dialogues
# 2 gardes proches des portes du village qui informent que des monstres rodent dans les alentours


# Système de checkpoint en rentrant dans une zone (ou manuel?)

# Ajouter un marchand dans la ville
# Remplacer l'attaque lourde par des attaques spéciales liées aux ennemis (ennemis ayant plusieurs chances d'attaquer plusieurs fois pendant le même tour)

# Moins importants :

# Ajoute des options dans iteminfo pour définir si plusieurs fois le même objet dans l'inventaire offre de la défense cumulée
# Créer un système de sauvegarde
# Rendre possible le changement de langue


# Possibles futures fonctionnalités :

# Plus de monstres possibles
# Plus de variations de dégâts (feu / empoisonnement)
# Les ennemis peuvent se soigner
# Équilibrage du jeu
# Plus de mondes

cheat_mode = True


# DÉFINIT LES VALEURS DES OPTIONS
# Ajoute une ligne entre certaines étapes pour une meilleure lisibilité
def default_in_bet_lines():
    print("----------------------------------------------------------------------------")


def in_between_lines():
    if do_lines_display:
        print("============================================================================")


# ================================ Définit la rng
def rng(*range_num):
    return randrange(*range_num)


# =============================== Raccourci pour modifier les textes
# Toujours définir la partie à remplacer par ¤¤¤
def text_replace(text, word=''):
    # Par défaut, ne remplace par rien si le second paramètre est vide
    return text.replace("¤¤¤", word)


# ======================================================================================================================
# Définit les noms alternatifs
def alt_name(pronoun, npc, is_boss=False):
    name = ""
    pronoun_list = {"m": ["un", "le", "du", "au"],
                    "f": ["une", "la", "de la", "à la"],
                    "fm": ["un", "l'", "de l'", "à l'"]}

    if l10n.language.lang == "english":
        name = npc.plural if pronoun in ("les", "des", "aux") else npc.name

    elif l10n.language.lang == "french":
        if pronoun in ("les", "des", "aux"):
            name = npc.plural
        elif npc.gender in [letters for letters in pronoun_list.keys()]:
            name = pronoun_list[npc.gender][pronoun_list["m"].index(pronoun)]
            # Ajoute un espace si le dernier caractère n'est pas un appostrophe
            name += " " + npc.name if name[-1] != "'" else npc.name
        else:
            name = npc.name if is_boss else npc.gender + ' ' + npc.name

    return name


# Définit quel PNJ sera invoqué en fonction de la liste de current_biome.mobs
def defined_npc(random_npc):
    if isinstance(random_npc, int):  # Normal Use
        npc_list_rarity = [npcs.rarity for npcs in current_biome.mobs]

        # Gère le spawn des boss
        if 4 in npc_list_rarity:
            local_npc_rarity = 4

        # Monstre commun
        # 3/6 de chances
        elif random_npc < 3:
            if 1 in npc_list_rarity:
                local_npc_rarity = 1
            else:
                if 2 in npc_list_rarity and 3 in npc_list_rarity:
                    # 1/3 de faire apparaître le monstre rare et 2/3 le peu commun  # Équilibrage
                    local_npc_rarity = 2 if rng(3) else 3
                else:
                    local_npc_rarity = 2 if 2 in npc_list_rarity else 3

        # Monstre peu commun
        # 2/6 de chances
        elif random_npc < 5:
            if 2 in npc_list_rarity:
                local_npc_rarity = 2
            else:
                if 1 in npc_list_rarity and 3 in npc_list_rarity:
                    # 1/4 de faire apparaître le monstre rare et 3/4 le commun  # Équilibrage
                    local_npc_rarity = 1 if rng(4) else 3
                else:
                    local_npc_rarity = 1 if 1 in npc_list_rarity else 3

        # Monstre rare
        # 1/6 de chances
        else:  # random_npc == 5:
            if 3 in npc_list_rarity:
                local_npc_rarity = 3
            else:
                local_npc_rarity = 1 if 1 in npc_list_rarity else 2

        npc_list = [npcs for npcs in current_biome.mobs if npcs.rarity == local_npc_rarity]

        # Si npc_list vide, renvoit un message d'erreur
        return npc_list[rng(len(npc_list))] if npc_list else print(custom_text(f"Error: mobs list in biome_id : {current_biome.biome_id} is empty", "red", "bold"))

    else:  # Debug Use
        return random_npc


# class Localization:

class Menu:
    self.was_in_options = False
    self.do_colors_display = True
    self.do_lines_display = False
    self.is_loading = False  # True

    @staticmethod
    def set_options(option, low=False):
        def lower_func(text):
            return text.lower() if low else text

        options_on = lower_func(custom_text("Activées", "green", "bold"))
        options_off = lower_func(custom_text("Désactivées", "red", "bold"))

        if option in command_options_color:
            return options_on if do_colors_display else options_off

        elif option in command_options_line:
            return options_on if do_lines_display else options_off

        elif option in command_options_loading:
            return options_on if is_loading else options_off

        elif option in command_options_language:
            return l10n.language.name[l10n.language.lang]

    # =============================== Définit la couleur du texte
    # Faire en sorte que color et emphasis puisse récupérer soit des valeurs de couleur soit d'emphase
    def custom_text(self, string: str, *modif_arg: str):
        color, emphasis = 39, 1

        # Charge uniquement les dictionnaires si les couleurs sont activées
        if self.do_colors_display:
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

    def start_game(self):
        return Game().start()


class Player:
    def __init__(self):
        # Statistiques du joueur
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

        # Tour où se trouve le joueur
        self.current_turn = 0

        # Effets (buffs & débuffs)
        self.effects = dict()
        self.repeal_turn = 0

        # Compteur de meurtres
        self.kill_counter = dict()

    # =============================================== Commandes de gestion =============================================
    # Ajoute un monstre au compteur de monstre
    def add_npc_to_kill_counter(self, npc: object):
        if npc not in self.kill_counter:
            self.kill_counter[npc] = 1
        else:
            self.kill_counter[npc] += 1

    # =============================================== Affichage d'informations =========================================
    # Nombre de monstres tués
    def display_kill_counter(self):
        if self.kill_counter:
            print("Nombre de monstre tués :")
            for enemy, count in self.kill_counter.items():
                print(f"x{count} {enemy.name}")

    # =============================================== Renvoi de valeurs ================================================
    # Noms des objets dans l'inventaire par type d'objet
    def get_item_names(self, item_type="consumable"):
        item_names = list()

        if item_type in self.inventory:
            item_names = list(map(lambda x: unidecode(x.name.lower()), self.inventory[item_type]))

        return item_names


class Game(Menu):
    def __init__(self):
        self.game_over = False
        self.is_new_game = False

        self.dumeors_alive = True

        # Statistiques de fin de jeu
        self.total_points = 0
        self.loading_points = 0

        self.starting_time = time()

        self.command = ''
        self.menu = Menu()

    # ===================================== Définit un chargement
    def loading(self):
        rng_timer = rng(2, 4)
        if is_loading:
            done = False

            def animate():
                for c in cycle(['.', '..', '...', '']):
                    if done:
                        break
                    stdout.write('\r' + c)
                    stdout.flush()
                    sleep(0.25)

            Thread(target=animate).start()
            sleep(rng_timer)
            done = True

            # Ajoute le nombre de secondes du temps de chargements au compteur de points de chargement
            self.loading_points += rng_timer
            # Renvoit le nombre de secondes du chargement (Soustraie du calcul des points)
            return rng_timer
        else:
            return 0

    # ===================================== Check les commandes
    def command_checker(self, command, commands_list):
        if command in commands_list:
            in_between_lines()
            self.command = get_true_input(clean_input(ask_command), commands_list)
        else:
            self.command = get_true_input(clean_input(ask_command_fail), commands_list)

        return self.command

    # ===================================== Lance le jeu
    def start(self):
        # Définit les textes d'input de commande
        ask_command = menu.custom_text(l10n.question.ask_command, "blue")
        ask_action = custom_text(l10n.question.ask_action, "blue")
        ask_command_fail = custom_text(l10n.question.ask_command_fail, "blue")
        ask_action_fail = custom_text(l10n.question.ask_action_fail, "blue")

        # Définit les valeurs par défaut pour 'action = "observe"'
        observe_number_mini = 0
        observe_number_maxi = 8
        past_message = past_message_bis = False

        # Définit si c'est le premier combat pour afficher les commandes en début de jeu
        is_first_fight = True
        coin_found_village = False

        # Définit un inventaire vierge et en créer une sauvegarde
        effects = dict()
        base_village_merchant = npc_merchant
        base_village_trappist = npc_trappist

        # Définit les stats de base du joueur
        player = Player()
        player.add_new_game_items()

        # Définit le biome de départ
        current_biome = biome_village

        # Définit le tours auquel le joueur commence
        current_turn = current_biome.turn

        # La partie commence ici
        default_in_bet_lines()
        # Texte d'intro du jeu
        print(custom_text(l10n.quote.intro.format(biome_dumeors_den.turn), "yellow"))

        default_in_bet_lines()
        display_command_help()

        print(custom_text("\nActions possibles dans le village :", "yellow"))
        print(custom_text('* Parler au marchand (Écrivez « marchand » pour aller le voir)', "yellow"))
        print(custom_text('* Parler au trappeur (Écrivez « trappeur » pour aller le voir)', "yellow"))

        command = get_true_input(clean_input(ask_command), list_command_ingame)

        while not self.game_over:
            if command not in list_command_ingame:
                # Si la commande ne fait pas partie de la liste de commandes, redemande d'écrire une commande valide
                in_between_lines()
                command = get_true_input(clean_input(ask_command_fail), list_command_ingame)
            else:
                while player.health > 0 and not self.game_over:

                    # Gère l'arrêt de la partie
                    if command in command_gameover:
                        self.game_over = True

                    elif command in command_game_stat:
                        player.display_stats()

                    elif command in command_help:
                        display_command_help()

                    elif command in command_game_inventory:
                        default_in_bet_lines()
                        player.display_inventory()
                        default_in_bet_lines()

                    # UNE FOIS LE TOUR TERMINÉ, DEMANDE UNE COMMANDE
                    if player.health > 0 and not self.game_over:
                        current_biome_checker = current_biome

                        # Redéfinit le biome du joueur à la fin du tour
                        current_biome = next((biome_dict[turn] for turn, biome in biome_dict.items() if current_turn >= turn), None)

                        if current_biome_checker != current_biome:

                            if current_biome == biome_village:
                                print(custom_text(f"Vous rentrez au {current_biome.name}", "yellow"))

                                print(custom_text("\nActions possibles dans le village :", "yellow"))
                                print(custom_text('* Parler au marchand (Écrivez « marchand » pour aller le voir)', "yellow"))
                                print(custom_text('* Parler au trappeur (Écrivez « trappeur » pour aller le voir)', "yellow"))
                            else:
                                print(custom_text(f"\nVous pénétrez dans le biome {current_biome.name}", "yellow"))

                        # Gère le texte d'avant boss
                        if current_turn == biome_dumeors_den.turn and self.dumeors_alive:
                            print(custom_text("\nAttention, écrire « avancer » lancera le combat. Pensez à vous soigner avant de l'affronter.", 'red'))

                        command = get_true_input(clean_input(ask_command if command in list_command_ingame else ask_command_fail), list_command_ingame)

        # Se déclenche une fois la partie terminée (ou l'objectif atteint en mode débug)
        else:
            default_in_bet_lines()

            def endgame_statistics():
                # DÉFINIT L'AFFICHAGE DE DONNÉES À LA FIN DE LA PARTIE (POINTS, TEMPS, NOMBRES DE MEURTRES)
                timer = ceil(time() - self.starting_time)

                time_points = (timer - self.loading_points) / 3
                level_points = hero_level * 10
                fight_points = sum(player.kill_counter.values())

                if self.game_over:
                    time_points = 5
                elif time_points < 200:
                    time_points = 500
                elif time_points < 400:
                    time_points = 250
                else:
                    time_points = 100

                # Affiche la durée de la partie
                total_time = timedelta(seconds=timer)
                print(f"Durée de la partie : {total_time}.")

                # Affiche le total des points
                total_points = time_points + level_points + fight_points
                print(f"Votre score est de {total_points} points.")

                # Affiche le nombre de monstres tués
                player.display_kill_counter()

            if self.game_over:
                # SI GAME OVER
                print(custom_text("Game over ! Vous avez perdu !", "red"))
                endgame_statistics()
                command = get_true_input(clean_func(custom_text("Voulez-vous recommencer ? (oui/non)\n> ", "red")), list_command_other)

                while command not in list_command_other:
                    in_between_lines()
                    command = clean_func(custom_text("Recommencer ? (oui/non)\n> ", "red")),
                else:
                    # game_over = False
                    if command in command_no:
                        print("Merci d'avoir joué !")
                        default_in_bet_lines()
                    elif command in command_yes:
                        print("Et c'est reparti !")
                        is_new_game = True
            else:
                endgame_statistics()
                print("Merci d'avoir joué !")
                command = "default"


Game().start_game()
