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
    def add_to_inv(self, quantity: int, item: object):
        if item.item_type not in self.inventory.keys():
            self.inventory[item.item_type] = dict()

        sub_inventory = self.inventory[item.item_type]

        if item not in sub_inventory.keys():
            sub_inventory[item] = quantity
        else:
            sub_inventory[item] += quantity

        # Redéfinit les dégâts d'objet sur l'arme la plus puissante
        self.items_damage = 0 if self.get_best_weapon() is None else self.get_best_weapon().damage
        self.items_defense = 0

        # Redéfinit les dégâts et défense totaux
        self.total_damage = self.damage + self.items_damage
        self.total_defense = self.defense + self.items_defense

    # Supprime un objet de l'inventaire
    def del_from_inv(self, quantity: int, item: object):
        if item.item_type in self.inventory.keys():
            sub_inventory = self.inventory[item.item_type]
            sub_inventory[item] -= quantity

            if sub_inventory[item] < 1:
                sub_inventory.pop(item)

                if not sub_inventory:
                    self.inventory.pop(item.item_type)

    # Ajoute un mosntre au compteur de monstre
    def add_npc_to_kill_counter(self, npc: object):
        if npc not in self.kill_counter:
            self.kill_counter[npc] = 1
        else:
            self.kill_counter[npc] += 1

    # Ajoute les objets de nouvelle partie à l'inventaire
    def add_new_game_items(self):
        starting_items = {
            item_healing_potion: 2,
            item_putrid_perfume: 1,
            item_basic_clothes: 1,
            item_basic_pants: 1,
            item_basic_shoes: 1,
            item_basic_sword: 1
        }

        for item, qty in starting_items.items():
            self.add_to_inv(qty, item)

    # =============================================== Commandes d'action ===============================================
    def heals_himself(self, healing_value):
        if self.health + healing_value > self.max_health:
            self.health = self.max_health
        else:
            self.health += healing_value

    # =============================================== Affichage d'informations =========================================
    # Inventaire
    def display_inventory(self, *item_args: str, intro=True, show_price=False):
        show_all = True if not item_args and self.inventory else False

        if intro:
            print(custom_text(l10n.inventory.inventory_intro if self.inventory else l10n.inventory.no_items, "blue"))

        # DÉFINIT LES CONSOMMABLES
        if "consumable" in self.inventory.keys() and ("consumable" in item_args or show_all):
            print(custom_text(l10n.inventory.consumable_intro, "yellow"))

            for item, qty in self.inventory["consumable"].items():
                print(custom_text(f'x{qty} {item.name}', "bold"), end=' ')

                if show_price:
                    print(custom_text(f"[{item.sell_price} or par unité]", "red"), end=' ')

                if item.heals:  # Si objet de soin
                    print(custom_text(l10n.inventory.consumable_desc_heal.format(item.heals), "green"))
                else:
                    print(custom_text(l10n.inventory.consumable_desc_oust.format(item.item_effect), "green"))

        # DÉFINIT L'ARMURE
        if "armor" in self.inventory.keys() and ("armor" in item_args or show_all):
            print(custom_text(l10n.inventory.armor_intro.format(self.get_total_defense()), "yellow"))

            for item, qty in self.inventory["armor"].items():
                print(custom_text(f"x{qty} {item.name}", "bold"), end=' ')

                if show_price:
                    print(custom_text(f"[{item.sell_price} or par unité]", "red"), end=' ')

                print(custom_text(l10n.inventory.armor_desc.format(item.defense), "green"))

        # DÉFINIT LES ARMES
        if "weapon" in self.inventory.keys() and ("weapon" in item_args or show_all):
            print(custom_text(l10n.inventory.weapon_intro.format(self.get_best_weapon().name), "yellow", "bold"))

            for item, qty in self.inventory["weapon"].items():
                print(custom_text(f"x{qty} {item.name}", "bold"), end=' ')

                if show_price:
                    print(custom_text(f"[{item.sell_price} or par unité]", "red"), end=' ')

                print(custom_text(l10n.inventory.weapon_desc.format(item.damage), "green"))

        # DÉFINIT LES INGRÉDIENTS
        if "ingredient" in self.inventory.keys() and ("ingredient" in item_args or show_all):
            print(custom_text(l10n.inventory.ingredient_intro, "yellow"))

            for item, qty in self.inventory["ingredient"].items():
                print(custom_text(f'x{qty} {item.name}', "bold"), end='')

                print(custom_text(f" [{item.sell_price} or par unité]", "red") if show_price else '')

        # DÉFINIT LES OBJETS DE QUÊTE
        if "quest" in self.inventory.keys() and ("quest" in item_args or show_all):
            print(custom_text(l10n.inventory.quest_intro, "yellow"))

            for item, qty in self.inventory["quest"].items():
                print(custom_text(f'x{qty} {item.name}', "bold"))

    # Nombre de monstres tués
    def display_kill_counter(self):
        if self.kill_counter:
            print("Nombre de monstre tués :")
            for enemy, count in self.kill_counter.items():
                print(f"x{count} {enemy.name}")

    # Statistiques du joueur
    def display_player_stats(self):
        print(custom_text(
            f"""Santé : {self.health}/{self.max_health}\t\t\tNiveau : {self.level}\t EXP actuelle : {self.experience}
Dégâts : {self.total_damage} ({self.damage} +{self.items_damage})\t\tEXP avant prochain niveau : {self.get_next_level_exp()}
Défense : {self.total_defense} ({self.defense} +{self.items_defense})\t\tBourse : {self.gold} or""", "yellow"))

    # =============================================== Renvoi de valeurs ================================================
    # Arme ayant les dégâts maximum
    def get_best_weapon(self):
        best_weapon = None

        if 'weapon' in self.inventory:
            for weapon in self.inventory["weapon"].keys():
                if best_weapon is None or weapon.damage > best_weapon.damage:
                    best_weapon = weapon

        return best_weapon

    # Défense totale
    def get_total_defense(self):
        total_defense = 0

        if 'armor' in self.inventory:
            for armor in self.inventory["armor"].keys():
                print(armor.defense)

        return total_defense

    # Expérience restante pour monter d'un niveau
    def get_next_level_exp(self):
        return self.exp_to_levelup - self.experience

    # Noms des objets dans l'inventaire par type d'objet sélectionné
    def get_item_names(self, item_type="consumable"):
        item_names = list()

        if item_type in self.inventory:
            item_names = list(map(lambda x: unidecode(x.name.lower()), self.inventory[item_type]))

        return item_names

    # =============================================== LEVEL-UP =========================================================
    # Gère l'ajout d'exp, le système de monter de niveau et l'ajout de statistiques en montant d'un niveau
    def manage_levelup(self, won_exp=0):
        # Permet d'ajouter des statistiques
        def add_stat(amount: int, stat: str):
            if stat == "damage":
                self.damage += amount
                self.total_damage = self.damage + self.items_damage
                print(f'+{amount} de dégâts')

            elif stat == "defense":
                self.defense += amount
                self.total_defense = self.defense + self.items_defense
                print(f'+{amount} de défense')

            elif stat == "health":
                self.health += amount
                self.max_health += amount
                print(f'+{amount} de santé et santé max')

            elif stat == "level":
                self.level += amount
                print(custom_text(f"+{amount} niveau !", "green"))

            elif stat == "experience":
                if amount:
                    self.experience += amount
                    print(f"Vous avez gagné {amount} points d'expérience !")
                else:
                    print("Vous n'avez gagné aucun points d'expérience.")

            elif stat == "gold":
                if amount:
                    self.gold += amount
                    print(f"Vous avez gagné {amount} or !")

        add_stat(won_exp, "experience")

        while self.experience >= self.exp_to_levelup:
            previous_level = self.level
            add_stat(1, "level")
            self.experience -= self.exp_to_levelup

            self.exp_to_levelup = ceil(self.exp_to_levelup * 1.12)

            if previous_level != self.level:
                if self.level in levelup_stats:
                    print(custom_text("Statistique(s) augmentée(s) :", "green"))

                    for stat_name, stat_increase in levelup_stats.get(self.level).items():
                        add_stat(stat_increase, stat_name)

        print(custom_text(f"Vous êtes désormais niveau {self.level}. Plus que {self.get_next_level_exp()} point(s) d'exp pour passer au niveau supérieur.", "yellow"))


player = Player()

player.add_new_game_items()
