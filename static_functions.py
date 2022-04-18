from itertools import cycle
from threading import Thread
from time import time, sleep
from sys import stdout
from random import randrange, choice
from os import path
from datetime import timedelta
import json


debug = False


def debugging(text):
    if debug:
        print(text)


# =============================================== LOCALIZATION =========================================================
def open_json(file_name, is_l10n=False):
    if is_l10n:
        file_name = "l10n_" + file_name

    return json.load(open(f"json_data/{file_name}.json", encoding='utf-8'))


class Localization:
    def __init__(
            self,
            l10n_pack=open_json("french", is_l10n=True)  # Langue par défaut
    ):
        self.default_pack = l10n_pack
        self.selected_pack = self.default_pack
        self.lang = self.selected_pack["lang"]
        self.main_key = ""
        self.saved_main_key = list()

    # Défini la langue sur la langue souhaitée
    def set_language_to(self, lang: str):
        # Si langue disponible et si fichier existe
        if lang in self.selected_pack["languages"].keys() and path.isfile(f'json_data/l10n_{lang}.json'):
            self.selected_pack = open_json(lang, is_l10n=True)
            self.lang = self.selected_pack["lang"]

            print("\nLanguage now set to:", self.lang)
        else:
            print(f'Error: typo in "{lang}" or "l10n_{lang}" doesn\'t exist in ./json_data/')

    def set_main_key(self, main_key):
        if self.main_key:
            self.saved_main_key.append(self.main_key)

        self.main_key = main_key
        debugging(f"Main key selected : {self.main_key}")

    def reset_main_key(self):
        debugging(f"Main key reset : {self.main_key}")
        if self.saved_main_key:
            self.main_key = self.saved_main_key[0]
            self.main_key = self.saved_main_key.pop(0)
        else:
            self.main_key = ""

    # Récupère la chaîne de caractère si elle existe sinon renvoi la chaîne par défaut
    def get(self, *l10n_keys):
        """
        Returns wanted l10n string

            Parameters:
                *l10n_keys (str): Path to wanted string

            Returns:
                string (str): L10n string or default string if not found
        """
        default_string = self.default_pack
        string = self.selected_pack

        if self.main_key:
            default_string = self.default_pack[self.main_key]
            string = self.selected_pack[self.main_key]

        if len(l10n_keys) == 1:
            l10n_keys = l10n_keys[0].split()

        try:
            for key in l10n_keys:
                default_string = default_string[key]

                if key in string.keys():
                    string = string[key]
                else:
                    string = default_string
                    print(f'\nError: "{key}" key cannot be found in ./json_data/l10n_{self.lang}, using default value instead')

            return string
        except KeyError:
            print(f'"{key}" key is missing from ./json_data/l10n_{self.default_pack["lang"]}')


# =============================================== Affichage d'information ==============================================
# Interlignes par défaut
def default_in_bet_lines():
    print("----------------------------------------------------------------------------")


# Interlignes
def in_between_lines():
    if do_lines_display:
        print("============================================================================")
# À intégrer dans Menu() avec check de self.do_lines_display


# Commandes disponibles
def display_command_help():
    print(custom_text(
        '''Commandes disponibles :
* avancer - Vous avancez d'une case
* reculer - Vous reculez d'une case
* observer - Vous regardez autour de vous
* soin - Vous permet d'utiliser un objet de soin
* stats - Affiche vos statistiques
* inventaire - Affiche votre inventaire
* aide - Affiche les commandes disponibles (ou aide+ pour la liste complète)
* objectif - Affiche le nombre de cases restant avant d'accomplir votre objectif''',
        "yellow"))


# =============================================== Renvoi de valeurs ====================================================
# =============================== Définit la couleur du texte
# Faire en sorte que color et emphasis puisse récupérer soit des valeurs de couleur soit d'emphase
def custom_text(string: str, *modif_arg: str, do_colors_display=True):
    color, emphasis = 39, 1

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


# Définit les noms alternatifs
def alt_name(pronoun, npc, is_boss=False):
    name = npc.name

    if not is_boss:
        pronoun_list = {"m": ("un", "le", "du", "au"),
                        "f": ("une", "la", "de la", "à la"),
                        "fm": ("un", "l'", "de l'", "à l'")}

        if l10n.lang == "english":
            name = npc.plural if pronoun in ("les", "des", "aux") else npc.name

        elif l10n.lang == "french":
            if pronoun in ("les", "des", "aux"):
                name = npc.plural
            elif npc.gender in [letters for letters in pronoun_list.keys()]:
                name = pronoun_list[npc.gender][pronoun_list["m"].index(pronoun)]
                # Ajoute un espace si le dernier caractère n'est pas une apostrophe
                name += " " + npc.name if name[-1] != "'" else npc.name
            else:
                name = npc.gender + ' ' + npc.name

    return name
# À supprimer et corriger les strings correspondants


# Définit quel PNJ sera invoqué en fonction de la liste de current_biome.mobs
def defined_npc(random_npc, current_biome):
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

        # Si npc_list vide, renvoi un message d'erreur
        return npc_list[rng(len(npc_list))] if npc_list else print(custom_text(f"Error: mobs list in biome_id : {current_biome.biome_id} is empty", "red", "bold"))

    else:  # Debug Use
        return random_npc
# À intégrer dans class Fight()


# Nombre aléatoire
def rng(*range_num):
    return randrange(*range_num)


# Remplace ¤¤¤ par le texte voulu
def replace_text(text: str, word=''):
    return text.replace("¤¤¤", word)







levelup_stats = {
    1: {"damage": 1},
    2: {"defense": 1},
    3: {"health": 10},
    5: {"damage": 1},
    6: {"defense": 1},
    7: {"health": 10},
    9: {"damage": 1, "defense": 1},
    10: {"health": 20}
    }