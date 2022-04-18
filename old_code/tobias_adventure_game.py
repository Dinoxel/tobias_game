from itertools import cycle
from threading import Thread
from time import time, sleep
from sys import stdout
from random import randrange, choice
from os import system
from unidecode import unidecode
from Levenshtein import jaro, ratio
from datetime import timedelta
system('cls')

cheat_mode = True

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

# ======================================================================================================================
# ========================== Définit l'affichage des couleurs
# DEFAULT = True
do_colors_display = True

# ============================ Définit l'affichage des lignes
# DEFAULT = False
do_lines_display = False

# ========================= Définit l'affichage du chargement
# DEFAULT = True
is_loading = False  # TESTING TESTING


# ===================================== Définit un chargement
def loading():
    global loading_points
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
        loading_points += rng_timer
        # Renvoit le nombre de secondes du chargement (Soustraie du calcul des points)
        return rng_timer
    else:
        return 0


# DÉFINIT LES VALEURS DES OPTIONS
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


# Ajoute une ligne entre certaines étapes pour une meilleure lisibilité
def default_in_bet_lines():
    print("----------------------------------------------------------------------------")


def in_between_lines():
    if do_lines_display:
        print("============================================================================")


# ================================ Définit la rng
def rng(*range_num):
    return randrange(*range_num)


# ================================ Transforme le texte en minuscule, supprime les accents et espaces sur les côtés
def input_func(input_text):
    return unidecode(input(input_text).lower()).strip()


# ================================ Choisit la commande la plus adéquat en fonction de l'input
def command_func(input_command, list_of_commands):
    # input_command doit toujours utilisé input_func() afin d'avoir une chaîne de caractères propre
    # Permet de sélectionner le mot le plus pertinent d'après la plus grande distance de Jaro-Winkler et de Levenshtein
    mixed = max([(word, max(jaro(input_command, word), ratio(input_command, word))) for word in list_of_commands], key=lambda word: word[1])

    # Renvoit une chaîne de caractère vide si le score est trop faible
    print(mixed)
    return "" if len(input_command) < 1 or mixed[1] < 0.60 else mixed[0]


# =============================== Définit la couleur du texte
# Faire en sorte que color et emphasis puisse récuperer soit des valeurs de couleur soit d'emphase
def custom_text(string, *modif_arg):
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


# =============================== Raccourci pour modifier les textes
# Toujours définir la partie à remplacer par ¤¤¤
def text_replace(text, word=''):
    # Par défaut, ne remplace par rien si le second paramètre est vide
    return text.replace("¤¤¤", word)


# ======================================================================================================================
# =========================================================== Définit les statistiques de base du héros
class Tobias:
    name = "Tobias"
    health = 80
    damage = 3
    defense = 0
    level = 0
    experience = 0
    exp_to_levelup = 30
    gold = 20
    kill_counter = dict()


tobias_hero = Tobias()

if cheat_mode:
    tobias_hero.health += 200
    tobias_hero.damage += 200
    tobias_hero.defense += 200
    tobias_hero.gold += 200

quest_return_merchant = "Retourner voir le Marchand"
quest_return_trappist = "Retourner voir le Trappeur"


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
        return npc_list[rng(len(npc_list))] if npc_list else print(custom_text(f"Error: mobs list in biome {current_biome.biome_id} is empty", "red", "bold"))

    else:  # Debug Use
        return random_npc


# ======================================================================================================================
# Permet d'ajouter ou enlever des objets de l'inventaire  # À transformer en classe
def manage_inventory(sign, quantity, item):
    global hero_inventory, total_hero_defense, total_hero_damage, item_defense, item_damage

    if sign in ("plus", "+"):
        for inventory_item in hero_inventory:
            if inventory_item[0] == item:
                inventory_item[1] += quantity
                break  # Évite de loop à travers toute la liste si beaucoup d'objets
        else:
            hero_inventory.append([item, quantity])

    elif sign in ("minus", "-"):
        for inventory_item in hero_inventory:
            if inventory_item[0] == item:
                inventory_item[1] -= quantity
                if inventory_item[1] < 1:
                    hero_inventory.remove(inventory_item)

    # Redéfinit les dégâts et points d'armure des objets de l'inventaire
    if item.item_type == "armor":
        item_defense = inventory_value("defense")
        total_hero_defense = hero_defense + item_defense
    elif item.item_type == "weapon":
        item_damage = inventory_value("damage")
        total_hero_damage = hero_damage + item_damage


# ============================================= Définit l'inventaire de base du joueur
def new_game_inventory():
    starting_items = {
        item_healing_potion: 2,
        item_putrid_perfume: 1,
        item_basic_clothes: 1,
        item_basic_pants: 1,
        item_basic_shoes: 1,
        item_basic_sword: 1
    }

    for item, qty in starting_items.items():
        manage_inventory("+", qty, item)

    if cheat_mode:
        manage_inventory("+", 1, item_dumeors_head)


# ============================================= Définit l'affichage de l'inventaire
def display_inventory(*item_args, intro=True, show_price=False):
    local_inventory = []
    inv_consumable = [item for item in hero_inventory if item[0].item_type == "consumable"]
    inv_armor = [item for item in hero_inventory if item[0].item_type == "armor"]
    inv_weapon = [item for item in hero_inventory if item[0].item_type == "weapon"]
    inv_weapon.sort(reverse=True, key=lambda x: x[0].damage)
    inv_ingredient = [item for item in hero_inventory if item[0].item_type == "ingredient"]
    inv_quest = [item for item in hero_inventory if item[0].item_type == "quest"]

    if 'all' in item_args:
        local_inventory = hero_inventory
    else:
        if "consumable" in item_args:
            local_inventory += inv_consumable

        if "armor" in item_args:
            local_inventory += inv_armor

        if "weapon" in item_args:
            local_inventory += inv_weapon

        if "ingredient" in item_args:
            local_inventory += inv_ingredient

        if "quest" in item_args:
            local_inventory += inv_quest

    # Intro
    if intro:
        print(custom_text(l10n.inventory.inventory_intro if local_inventory else l10n.inventory.no_items, "blue"))

    # DÉFINIT LES CONSOMMABLES
    if ("consumable" or "all" in item_args) and inv_consumable:
        print(custom_text(l10n.inventory.consumable_intro, "yellow"))
        for item in inv_consumable:
            print(custom_text(f'x{item[1]} {item[0].name}', "bold"), end=' ')

            if show_price:
                print(custom_text(f"[{item[0].sell_price} or par unité]", "red"), end=' ')

            if item[0].heals:  # Si objet de soin
                print(custom_text(l10n.inventory.consumable_desc_heal.format(item[0].heals), "green"))
            else:
                print(custom_text(l10n.inventory.consumable_desc_oust.format(item[0].item_effect), "green"))

    # DÉFINIT L'ARMURE
    if ("armor" or "all" in item_args) and inv_armor:
        print(custom_text(l10n.inventory.armor_intro.format(item_defense), "yellow"))
        for item in inv_armor:
            print(custom_text(f"x{item[1]} {item[0].name}", "bold"), end=' ')

            if show_price:
                print(custom_text(f"[{item[0].sell_price} or par unité]", "red"), end=' ')

            print(custom_text(l10n.inventory.armor_desc.format(item[0].defense), "green"))

    # DÉFINIT LES ARMES
    if ("weapon" or "all" in item_args) and inv_weapon:
        print(custom_text(l10n.inventory.weapon_intro.format(inv_weapon[0][0].name), "yellow", "bold"))
        for item in inv_weapon:
            print(custom_text(f"x{item[1]} {item[0].name}", "bold"), end=' ')

            if show_price:
                print(custom_text(f"[{item[0].sell_price} or par unité]", "red"), end=' ')

            print(custom_text(l10n.inventory.weapon_desc.format(item[0].damage), "green"))

    # DÉFINIT LES INGRÉDIENTS
    if ("ingredient" or "all" in item_args) and inv_ingredient:
        print(custom_text(l10n.inventory.ingredient_intro, "yellow"))
        for item in inv_ingredient:
            print(custom_text(f'x{item[1]} {item[0].name}', "bold"), end='')

            print(custom_text(f" [{item[0].sell_price} or par unité]", "red") if show_price else '')

    # DÉFINIT LES OBJETS DE QUÊTE
    if ("quest" or "all" in item_args) and inv_quest and not show_price:
        print(custom_text(l10n.inventory.quest_intro, "yellow"))
        for item in inv_quest:
            print(custom_text(f'x{item[1]} {item[0].name}', "bold"))


# Renvoit les dégâts et défense des objets de l'inventaire
def inventory_value(value):
    if value == "damage":
        return max([item[0].damage for item in hero_inventory if item[0].item_type == "weapon"], default=0)
    elif value == "defense":
        return sum([item[0].defense for item in hero_inventory if item[0].item_type == "armor"])
    elif value == "consumable":
        return [unidecode(item[0].name.lower()) for item in hero_inventory if item[0].item_type == "consumable"]
    else:
        print(custom_text("Erreur : Mauvaise valeur définie pour inventory_value(value)", "red"))


# ====================== Définit les dégâts avec crit après déduction de la défense
def get_damage(concerned):
    # Définit les valeurs dans le combat, "hero" définit que c'est le combat du joueur
    if concerned == "hero":
        base_damage = total_hero_damage
        base_defense = fighting_npc.defense
    else:
        base_damage = fighting_npc.damage
        base_defense = total_hero_defense

    # 1/5 CHANCES DE CRITIQUE
    if rng(5) == 0:
        print(custom_text("Coup critique !", 'green' if concerned == 'hero' else 'red', "bold"))
        base_damage *= 1.25
    else:
        base_damage += rng(-1, 2)

    # Calcul des dégâts finaux après déduction de la défense
    final_damage = ceil(base_damage) - base_defense

    return 1 if final_damage < 1 else final_damage


# ============================================ CODE DU JEU À PARTIR D'ICI ==============================================
was_in_options = False
is_new_game = False

# Définit la toute première commande du jeu
command = command_func(input_func(custom_text(l10n.question.ask_menu, "blue")), list_command_menu)

while True:
    ask_menu = custom_text(l10n.question.ask_menu, "blue")
    ask_menu_fail = custom_text(l10n.question.ask_menu_fail, "blue")
    ask_options_fail = custom_text(l10n.question.ask_options_fail, "blue")
    ask_options = custom_text(l10n.question.ask_options, "blue")

    while command in list_command_menu or is_new_game:
        if command in command_menu_options:
            print(custom_text('Status des options :', "yellow"))
            print(f'Couleurs - {set_options("color")} (Défaut : Activées)')
            print(f'Lignes - {set_options("line")} (Défaut : Désactivées)')
            print(f'Chargements - {set_options("loading")} (Défaut : Activés)')
            print(f'Langue - {custom_text(set_options("language").capitalize(), "yellow", "bold")} (Défaut : Français)')

            in_between_lines()
            command = command_func(input_func(ask_options), list_command_options)

            while True:
                if command in command_menu:
                    print(custom_text("Vous quittez les options, retour au menu principal.", "yellow"))
                    in_between_lines()
                    was_in_options = True
                    break
                elif command in command_help:
                    in_between_lines()
                    print(custom_text('''Menu des options - Commandes disponibles :
* lines - pour activer/désactiver les lignes
* color - pour activer/désactiver les couleurs
* lang - pour choisir la langue
* loading - pour activer/désactiver les chargements
* default - pour remettre toutes les valeurs par défaut
* menu - pour retourner au menu''', "yellow"))
                elif command in command_options_language:
                    in_between_lines()
                    print(custom_text('La langue est définie sur {}. Défaut : Français'.format(set_options("language", low=True)), "yellow"))
                    command = command_func(input_func(custom_text('Pour changer la langue, écrivez la langue souhaitée.\nLangues disponibles : Français & Anglais\n> ', "blue")), list_command_options)
                    while True:
                        if command in list_command_options:
                            if command in command_options_l10n_fr:
                                if l10n.language.lang == "french":
                                    print(text_replace(l10n.options.lang.selected, l10n.options.lang.already))
                                else:
                                    l10n = DotMap(fr_l10n)
                                    print(text_replace(l10n.options.lang.selected, l10n.options.lang.now))
                            elif command in command_options_l10n_en:
                                if l10n.language.lang == "english":
                                    print(text_replace(l10n.options.lang.selected, l10n.options.lang.already))
                                else:
                                    l10n = DotMap(en_l10n)
                                    print(text_replace(l10n.options.lang.selected, l10n.options.lang.now))
                            print(custom_text("Retour aux options.", "blue"))
                        else:
                            print(custom_text("Commande inconnue, retour aux options.", "blue"))
                        break
                elif command in command_options_color:
                    in_between_lines()
                    print(custom_text(f'Les couleurs sont {set_options("color", low=True)}. Défaut : {custom_text("Activées", "green")}', "yellow"))
                    command = command_func(input_func(custom_text("Pour changer l'affichage des couleurs, écrivez « on » pour activer ou « off » pour désactiver.\n> ", "blue")), list_command_other)

                    while command in list_command_other:
                        if command in command_yes:
                            if do_colors_display:
                                print(custom_text("Les couleurs sont déjà activées.", "yellow"))
                            else:
                                print("Les couleurs sont désormais activées.")
                                do_colors_display = True
                        elif command in command_no:
                            if not do_colors_display:
                                print("Les couleurs sont déjà désactivées.")
                            else:
                                print("Les couleurs sont désormais désactivées.")
                                do_colors_display = False
                        else:
                            print(custom_text("Commande inconnue, retour aux options.", "blue"))
                        break
                    else:
                        command = command_func(input_func(ask_options_fail), list_command_other)
                elif command in command_options_loading:
                    in_between_lines()
                    print(custom_text(f'Les chargements sont {set_options("loading", low=True)}. Défaut : {custom_text("Activés", "green")}', "yellow"))
                    command = command_func(input_func(custom_text("Pour changer l'affichage des chargements, écrivez « on » pour activer ou « off » pour désactiver.\n> ", "blue")), list_command_other)

                    while command in list_command_other:
                        if command in command_yes:
                            if is_loading:
                                print(custom_text("Les chargements sont déjà activés.", "yellow"))
                            else:
                                print(custom_text("Les chargements sont désormais activés.", "yellow"))
                                is_loading = True
                        elif command in command_no:
                            if not is_loading:
                                print(custom_text("Les chargements sont déjà désactivés.", "yellow"))
                            else:
                                print(custom_text("Les chargements sont désormais désactivés.", "yellow"))
                                is_loading = False
                        else:
                            print(custom_text("Commande inconnue, retour aux options.", "blue"))
                        break

                    else:
                        command = command_func(input_func(ask_options_fail), list_command_other)
                elif command in command_options_line:
                    in_between_lines()
                    print(custom_text(f'Les lignes sont {set_options("line", low=True)}. Défaut : {custom_text("Désactivées", "red")}', "yellow"))
                    command = command_func(input_func(custom_text("Pour changer l'affichage des lignes, écrivez « on » pour activer ou « off » pour désactiver.\n> ", "blue")), list_command_other)

                    while command in list_command_other:
                        if command in command_yes:
                            if do_lines_display:
                                print(custom_text("Les lignes sont déjà activées.", "yellow"))
                            else:
                                print(custom_text("Les lignes sont désormais activées.", "yellow"))
                                do_lines_display = True
                        elif command in command_no:
                            if not do_lines_display:
                                print(custom_text("Les lignes sont déjà désactivées.", "yellow"))
                            else:
                                print(custom_text("Les lignes sont désormais désactivées.", "yellow"))
                                do_lines_display = False
                        else:
                            print(custom_text("Commande inconnue, retour aux options.", "blue"))
                        break

                    else:
                        command = command_func(input_func(ask_options_fail), list_command_other)
                elif command in command_default:
                    if do_colors_display and not do_lines_display and is_loading and l10n.language.lang == "french":
                        print(custom_text("Les options sont déjà par défaut.", "yellow"))
                    else:
                        do_colors_display = True
                        do_lines_display = False
                        is_loading = True
                        l10n = DotMap(fr_l10n)
                        print(custom_text("Les options ont été remis par défaut.", "yellow"))

                command = command_func(input_func(ask_options), list_command_options)











        elif command in command_menu_play or is_new_game:
            # Définit les textes d'input de commande
            ask_command = custom_text(l10n.question.ask_command, "blue")
            ask_action = custom_text(l10n.question.ask_action, "blue")
            ask_command_fail = custom_text(l10n.question.ask_command_fail, "blue")
            ask_action_fail = custom_text(l10n.question.ask_action_fail, "blue")

            # Définit les paramètres de rejouabilité
            is_new_game = game_over = False

            # Définit les valeurs par défaut pour 'action = "observe"'
            observe_number_mini = 0
            observe_number_maxi = 8
            past_message = past_message_bis = False

            # Définit si c'est le premier combat pour afficher les commandes en début de jeu
            is_first_fight = True
            is_dumeors_dead = False
            coin_found_village = False

            # Définit un inventaire vierge et en créer une sauvegarde
            hero_inventory = list()
            effects = dict()
            base_village_merchant = npc_merchant
            base_village_trappist = npc_trappist

            ### Définit les points affichés à la fin de la partie
            # Nombre de combats # Temps décompté de loading()
            fight_points = loading_points = 0
            # Heure à laquelle la partie démarre
            starting_time = time()

            # Définit les stats de base du joueur
            total_hero_health = hero_health = tobias_hero.health
            hero_damage = tobias_hero.damage
            hero_defense = tobias_hero.defense
            hero_level = tobias_hero.level
            hero_exp = tobias_hero.experience
            exp_to_levelup = tobias_hero.exp_to_levelup
            hero_gold = tobias_hero.gold
            kill_counter = tobias_hero.kill_counter

            # Définit l'inventaire de base du joueur ##### Doit être défini après hero_damage et hero_defense
            new_game_inventory()

            # Définit les valeurs de base des objets dans l'inventaire
            item_damage = inventory_value("damage")
            item_defense = inventory_value("defense")

            # Définit le calcul des dégâts/défense totaux (stat du héros + objets)
            total_hero_damage = hero_damage + item_damage
            total_hero_defense = hero_defense + item_defense

            # Définit l'expérience nécessaire avant le prochain niveau
            next_level_exp = exp_to_levelup - hero_exp

            # Définit les statistiques augmentées après un niveau
            levelup_stats = {1: {"damage": 1},
                             2: {"defense": 1},
                             3: {"health": 10},
                             5: {"damage": 1},
                             6: {"defense": 1},
                             7: {"health": 10},
                             9: {"damage": 1, "defense": 1},
                             10: {"health": 20}
                             }

            # Définit le tour de base du repousse
            repeal_turn = 0

            # Définit le biome de départ
            current_biome = biome_village

            # Définit le tour auquel le joueur commence
            current_turn = current_biome.turn

            # La partie commence ici
            default_in_bet_lines()
            # Texte d'intro du jeu
            print(custom_text(l10n.quote.intro.format(biome_dumeors_den.turn), "yellow"))

            default_in_bet_lines()
            print(custom_text('''Commandes disponibles :
* avancer - Vous avancez d'une case
* reculer - Vous reculez d'une case
* observer - Vous regardez autour de vous
* soin - Vous permet d'utiliser un objet consommable
* stats - Affiche vos statistiques
* inventaire - Affiche votre inventaire
* aide - Affiche les commandes disponibles (ou aide+ pour la liste complète)
* objectif - Affiche le nombre de cases restant avant d'accomplir votre objectif''', "yellow"))

            print(custom_text("\nActions possibles dans le village :", "yellow"))
            print(custom_text('* Parler au marchand (Écrivez « marchand » pour aller le voir)', "yellow"))
            print(custom_text('* Parler au trappeur (Écrivez « trappeur » pour aller le voir)', "yellow"))

            command = command_func(input_func(ask_command), list_command_ingame)

            # Le jeu se lance ici.
            while True:
                while not game_over:
                    if command not in list_command_ingame:
                        # Si la commande ne fait pas partie de la liste de commandes, redemande d'écrire une commande valide
                        in_between_lines()
                        command = command_func(input_func(ask_command_fail), list_command_ingame)
                    else:
                        while hero_health > 0 and not game_over:
                            # Gère les dialogues des PNJs dans le village
                            if current_biome == biome_village:
                                if command in command_npc_merchant_full:
                                    print(custom_text("\nBonjour aventurier, je suis le marchand, je vends quelques objets qui pourraient vous être utiles.\n"
                                                      "Je peux également acheter tous les objets que tu possèdes mais attention, c'est définitif.", 'cyan'))
                                    print(custom_text("\nPour arrêter de parler au marchand à n'importe quel moment, écrivez « village ».", "yellow"))

                                    # Commandes raccourcies si le joueur écrit directement des commandes d'achat ou de vente
                                    if command in command_npc_merchant_buy:
                                        merchant_ask = "buy"
                                    elif command in command_npc_merchant_sell:
                                        merchant_ask = "sell"
                                    else:
                                        merchant_ask = input_func(custom_text("\nÉcrivez « achat » pour acheter et « vente » pour vendre ?\n> ", "blue"))

                                    while True:
                                        # Achat
                                        if merchant_ask in command_npc_merchant_buy:
                                            print(custom_text(f"Monnaie possédée : {hero_gold} or", "yellow"))
                                            print(custom_text("Voilà tout ce que j'ai en stock :", 'cyan'))
                                            for sold_item in base_village_merchant.sells:
                                                print(custom_text(f"* {sold_item.buy_price} or \t{sold_item.name}", 'cyan'))

                                            merchant_ask_buy = input_func(custom_text("\nQue souhaitez-vous acheter ?\n> ", 'blue'))

                                            while True:
                                                if merchant_ask_buy == 'village':
                                                    merchant_ask = merchant_ask_buy
                                                    break

                                                elif merchant_ask_buy in command_no:
                                                    merchant_ask = input_func(custom_text("Voulez-vous vendre quelque-chose alors ?\n> ", 'cyan'))
                                                    if merchant_ask in command_yes:
                                                        merchant_ask = 'sell'
                                                    break

                                                elif merchant_ask_buy in list(map(lambda m_item: unidecode(m_item.name.lower()), base_village_merchant.sells)):
                                                    selected_item = next((m_item for m_item in base_village_merchant.sells if unidecode(m_item.name.lower()) == merchant_ask_buy), None)

                                                    merchant_ask_buy_how_many = input_func(custom_text('Combien souhaitez-vous en acheter ?\n> ', 'cyan'))

                                                    # Combien d'objets à acheter
                                                    while True:
                                                        if merchant_ask_buy_how_many.isdigit() and merchant_ask_buy_how_many != '0':
                                                            total_price = int(merchant_ask_buy_how_many) * selected_item.buy_price
                                                            if hero_gold >= total_price:
                                                                merchant_ask_buy_final = input_func(custom_text(f"Confirmer l'achat de {merchant_ask_buy_how_many} {selected_item.plural if int(merchant_ask_buy_how_many) > 1 else selected_item.name} pour un total de {total_price} or ?\n> ", 'blue'))

                                                                # Validation de la commande
                                                                while True:
                                                                    if merchant_ask_buy_final in command_yes:
                                                                        hero_gold -= total_price
                                                                        manage_inventory("+", int(merchant_ask_buy_how_many), selected_item)
                                                                        print(custom_text("Merci pour votre achat !", 'cyan'))
                                                                        break
                                                                    elif merchant_ask_buy_final in command_no:
                                                                        break
                                                                    else:
                                                                        merchant_ask_buy_final = input_func(custom_text("Je n'ai pas compris, validez-vous l'achat ?\n> ", 'cyan'))
                                                            else:
                                                                print(custom_text(f"Vous n'avez pas assez d'or pour acheter ça !", 'cyan'))
                                                            break
                                                        else:
                                                            if merchant_ask_buy_how_many == '0':
                                                                print(custom_text("Pas de problème. ", 'cyan'), end="")
                                                                break
                                                            else:
                                                                merchant_ask_buy_how_many = input_func(custom_text("Je n'ai pas compris, combien ?\n> ", 'cyan'))

                                                    merchant_ask_buy = input_func(custom_text("Souhaitez-vous acheter autre chose ?\n> ", 'cyan'))

                                                    if merchant_ask_buy in command_yes:
                                                        merchant_ask_buy = input_func(custom_text("Que souhaitez-vous acheter ?\n> ", 'cyan'))

                                                else:
                                                    merchant_ask_buy = input_func(custom_text("Je n'ai pas compris, que voulez-vous acheter ?\n> ", 'cyan'))

                                        # Vente
                                        elif merchant_ask in command_npc_merchant_sell:
                                            default_in_bet_lines()
                                            print(custom_text("Objets vendables :", "blue"))
                                            display_inventory('all', show_price=True, intro=False)
                                            default_in_bet_lines()

                                            merchant_ask_sell = input_func(custom_text("\nQue souhaitez-vous vendre ?\n> ", 'blue'))
                                            while True:
                                                if merchant_ask_sell == 'village':
                                                    merchant_ask = merchant_ask_sell
                                                    break

                                                elif merchant_ask_sell in command_no:
                                                    merchant_ask = input_func(custom_text("Voulez-vous acheter quelque-chose alors ?\n> ", 'cyan'))
                                                    if merchant_ask in command_yes:
                                                        merchant_ask = 'buy'
                                                    break

                                                elif merchant_ask_sell in list(map(lambda h_item: unidecode(h_item[0].name.lower()), filter(lambda h_item: h_item[0].item_type != 'quest', hero_inventory))):
                                                    selected_item, quantity_item = next(((h_item[0], h_item[1]) for h_item in hero_inventory if unidecode(h_item[0].name.lower()) == merchant_ask_sell), None)

                                                    merchant_ask_sell_how_many = input_func(custom_text('Combien souhaitez-vous en vendre ?\n> ', 'cyan'))

                                                    # Combien d'objets à vendre
                                                    while True:
                                                        if merchant_ask_sell_how_many.isdigit() and merchant_ask_sell_how_many != '0' and int(merchant_ask_sell_how_many) <= quantity_item:
                                                            total_price = int(merchant_ask_sell_how_many) * selected_item.sell_price
                                                            merchant_ask_sell_final = input_func(custom_text(f"Confirmer la vente de {merchant_ask_sell_how_many} {selected_item.plural if int(merchant_ask_sell_how_many) > 1 else selected_item.name} pour un total de {total_price} or ?\n> ", 'blue'))

                                                            # Validation de la commande
                                                            while True:
                                                                if merchant_ask_sell_final in command_yes:
                                                                    hero_gold += total_price
                                                                    manage_inventory("-", int(merchant_ask_sell_how_many), selected_item)

                                                                    print(custom_text("Merci pour cette vente !", 'cyan'))
                                                                    break
                                                                elif merchant_ask_sell_final in command_no:
                                                                    break
                                                                else:
                                                                    merchant_ask_sell_final = input_func(custom_text("Je n'ai pas compris, validez-vous la vente ?\n> ", 'cyan'))
                                                            break
                                                        else:
                                                            if merchant_ask_sell_how_many == '0':
                                                                print(custom_text("Pas de problème.", 'cyan'), end=" ")
                                                                break
                                                            elif quantity_item < int(merchant_ask_sell_how_many):
                                                                print(custom_text(f"Vous ne possédez pas {merchant_ask_sell_how_many} {selected_item.plural if int(merchant_ask_sell_how_many) > 1 else selected_item.name}.", 'red'))
                                                                break
                                                            else:
                                                                merchant_ask_sell_how_many = input_func(custom_text("Je n'ai pas compris, combien ?\n> ", 'cyan'))

                                                    merchant_ask_sell = input_func(custom_text("Souhaitez-vous vendre autre chose ?\n> ", 'cyan'))

                                                    if merchant_ask_sell in command_yes:
                                                        merchant_ask_sell = input_func(custom_text("Que souhaitez-vous vendre ?\n> ", 'cyan'))

                                                else:
                                                    merchant_ask_sell = input_func(custom_text("Je n'ai pas compris, que voulez-vous vendre ?\n> ", 'cyan'))

                                        elif merchant_ask in ["village"] + command_no:
                                            print(custom_text("Au revoir et à bientôt !", 'cyan'))
                                            print(custom_text("Vous retournez au milieu du village", 'yellow'))
                                            break
                                        else:
                                            merchant_ask = input_func(custom_text("Je n'ai pas bien compris, tu veux acheter ou vendre ?\n> ", 'cyan'))

                                if command in command_npc_trappist:
                                    print(custom_text("Bonjour aventurier, je suis le trappeur.", 'cyan'))

                            # Gère l'arrêt de la partie
                            if command in command_gameover:
                                game_over = True
                                break

                            elif command in command_game_stat:
                                next_level_exp = exp_to_levelup - hero_exp
                                print(custom_text(f"""Santé : {hero_health}/{total_hero_health}\t\t\tNiveau : {hero_level}\t EXP actuelle : {hero_exp}
Dégâts : {total_hero_damage} ({hero_damage} +{item_damage})\t\tEXP avant prochain niveau : {next_level_exp}
Défense : {total_hero_defense} ({hero_defense} +{item_defense})\t\tBourse : {hero_gold} or""", "yellow"))

                                if effects:
                                    print('Effets en cours :')
                                    for effect, desc in effects.items():
                                        print(effect, f"- {desc.format(repeal_turn)}")

                            elif command in command_ingame_observe:
                                if current_biome == biome_village:
                                    if not rng(10) and not coin_found_village:
                                        coin_found_village = True
                                        print(custom_text("C'est votre jour de chance, vous trouvez 1 pièce d'or par terre.", "green"))
                                        hero_gold += 1

                                    else:
                                        village_observe_messages = ["Le village est composé de plusieurs maisons et commerces en briques entouré d'un épais mur le protégeant d'éventuels assaillants.",
                                                                    "Un marchand vous dévisageant joue avec une pièce d'or entre ses doigts, il semble vouloir faire affaire avec vous.",
                                                                    "Un homme se tenant à un stand avec un écritau « QUÊTES » agite des prospectus, vous devriez aller y jeter un œil."]

                                        print(village_observe_messages[rng(len(village_observe_messages))])

                                else:
                                    observe_number = rng(observe_number_mini, observe_number_maxi)

                                    # Observations s'affichant uniquement avant un combat de boss
                                    if current_turn == biome_dumeors_den.turn - 1:
                                        observe_messages = [
                                            "Une odeur putride se dégage des carcasses autour de l'entrée...",
                                            "Des griffures de loup se trouvent sur des arbres non-loin de là",
                                            "Un vent frais sortant de la grotte vous parcourt le dos..."]

                                        print(observe_messages[rng(len(observe_messages))])

                                    else:

                                        # Observations positives
                                        if observe_number == 0:
                                            # Redéfinit le nombre mini sur 1 pour empêcher de retomber sur cet évènement
                                            observe_number_mini = 1
                                            print(custom_text("Vous croisez sur votre chemin un homme élégant vétu d'un haut de forme... il semble vouloir vous poser une énigme...", "yellow"))
                                            in_between_lines()
                                            command = input_func(
                                                custom_text("« Bonjour jeune homme, auriez-vous 5 minutes à m'accorder ? »\n> ", "cyan"))
                                            while command not in list_command_other:
                                                in_between_lines()
                                                command = input_func(custom_text("« Excusez-moi, mais je n'ai pas bien compris... » (répondre oui ou non)\n> ", "cyan"))
                                            else:
                                                if command in command_yes:
                                                    question_counter = 3
                                                    q_a_list = {"Combien font 2 + 2 ?": "4",
                                                                "Combien font 23140 multiplié par 3 ?": "69420",
                                                                "À combien de mètres culmine le Sommet Blanc ?": "4809"
                                                                }
                                                    question_info, answer_info = choice(list(q_a_list.items()))

                                                    while question_counter:
                                                        # La réponse sera transformée en minuscule et tous les espaces seront suprimés
                                                        answer = input_func(custom_text(f'« {question_info} »' + '\n> ', "cyan")).replace(" ", "")
                                                        if answer == answer_info:
                                                            layton_sentence = custom_text("¤¤¤, vous avez trouvé la bonne réponse !", "green")
                                                            print(text_replace(layton_sentence, f'{"Nice" if answer == "69420" else "Bravo"}'))
                                                            print(custom_text("« Tenez, prenez cet anneau pour m'avoir fait passer un bon moment ! »", "cyan") + custom_text(" dit-il, avant de s'en aller..", "yellow"))
                                                            print(custom_text("Il semblerait qu'il augmente votre défense de 1 !", "green"))
                                                            manage_inventory("+", 1, item_enigmatic_ring)
                                                            break
                                                        else:
                                                            question_counter -= 1
                                                            if question_counter == 1:
                                                                print(custom_text(f"« Non ce n'est toujours pas ça... il ne vous reste plus qu'une chance ! »", "cyan"))
                                                            else:
                                                                print(custom_text(f"« Non ce n'est pas ça... plus que {question_counter} de chances. »", "cyan"))
                                                            in_between_lines()
                                                    else:
                                                        print(custom_text("La déception se lit sur son visage, il s'en va sans dire un mot...", "yellow"))
                                                elif command in command_no:
                                                    print(custom_text('« Ah, tant pis alors... »', "cyan") + custom_text(" dit-il, avant de s'en aller.", "yellow"))

                                                # Signifie au joueur qu'il ne pourra pas retomber sur cet évènement
                                                print(custom_text("Vous n'êtes pas prêt de le recroiser.", "yellow"))
                                                command = "default"

                                        # Observations neutres
                                        elif observe_number <= 6:

                                            observe_positive_random = rng(3)
                                            observe_messages = ["Vous tendez l'oreille et reconnaissez le bruit ¤¤¤.",
                                                                "Vous regardez autour de vous et apercevez des biches à travers les arbres.",
                                                                "Vous entendez de l'eau ruisseler non loin de là."]

                                            if not observe_positive_random and not past_message:
                                                past_message = True
                                                print(text_replace(observe_messages[0], "d'un rouge gorge"))
                                            elif not observe_positive_random and not past_message_bis:
                                                past_message_bis = True
                                                print("Vous tendez l'oreille plus attentivement et reconnaissez en fait le bruit d'une mésange.")
                                            elif not observe_positive_random:
                                                print(text_replace(observe_messages[0], "d'une mésange"))
                                            else:
                                                print(observe_messages[observe_positive_random])

                                        # Observations négatives
                                        else:
                                            if observe_number == 7:
                                                # Redéfinit le nombre max sur 1 pour empêcher de retomber sur cet évènement
                                                observe_number_maxi = 7
                                                # Inflige 20 de dégâts parce que c'est rigolo.
                                                hero_health -= 20
                                                beast_attack_sentence = custom_text("Vous entendez un grognement derrière vous, le temps de vous retourner un ours vous attaque et vous inflige 20 de dégâts !", "red")
                                                if hero_health <= 0:
                                                    game_over = True
                                                    print(custom_text("Vous êtes mort !", "red"))

                            elif command in command_ingame_quest:
                                # Implémenter le système d'affichage de quête ici
                                print("Objectif : Atteindre la tanière du monstre.")
                                print(custom_text(f"Il vous reste {biome_dumeors_den.turn - current_turn} case(s) à parcourir avant de remplir votre objectif.", "yellow"))

                            elif command in command_game_inventory:
                                default_in_bet_lines()
                                display_inventory('all')
                                default_in_bet_lines()

                            elif command in command_game_consumables:
                                inventory_consumable = [item for item in hero_inventory if item[0].item_type == "consumable"]
                                # Créer une nouvelle liste avec tous les objets consommables de l'inventaire

                                no_items_selected = True

                                # Si la liste n'est pas vide, demande quel objet utiliser
                                while len(inventory_consumable) > 0 and no_items_selected:
                                    print(custom_text(f"\nSanté de Tobias : {hero_health}/{total_hero_health}", "yellow"))
                                    print(custom_text("Liste des objets consomables :", "blue"))

                                    # Liste tous les objets consommables disponibles
                                    for item in inventory_consumable:
                                        consumable_line = custom_text(f'x{item[1]} {item[0].name}', "bold")

                                        if item[0].heals:
                                            print(consumable_line, custom_text(l10n.inventory.consumable_desc_heal.format(item[0].heals), "green"))
                                        else:
                                            print(consumable_line, custom_text(l10n.inventory.consumable_desc_oust.format(item[0].item_effect), "green"))
                                    command = input_func(custom_text('\nQuel objet consommable souhaitez-vous utiliser ? (écrivez "aucun" pour sortir du menu)\n> ', "blue"))

                                    while command not in inventory_value("consumable"):
                                        if command in ("none", "aucun"):
                                            no_items_selected = False
                                            break

                                        in_between_lines()
                                        command = input_func(custom_text('Objet consommable non reconnu. Quel objet consommable souhaitez-vous utiliser ? (écrivez "aucun" pour sortir du menu)\n> ', "blue"))
                                    else:
                                        item_selected = [consumable_item for consumable_item in inventory_consumable if command == unidecode(consumable_item[0].name.lower())][0][0]

                                        # Si potion de soin
                                        if item_selected.heals:
                                            if hero_health != total_hero_health:
                                                manage_inventory("minus", 1, item_selected)
                                                print(f"Vous utilisez : {custom_text(item_selected.name, 'bold')}")

                                                hero_health += item_selected.heals
                                                print(custom_text(f"+{item_selected.heals} de santé", "green"))

                                                if hero_health > total_hero_health:
                                                    hero_health = total_hero_health

                                                print(custom_text(f"Santé de Tobias : {hero_health}/{total_hero_health}", "yellow"))
                                            else:
                                                print("Votre santé est déjà au maximum, vous ne pouvez utiliser aucun objet de soin.")

                                        # Si potion à effet
                                        if item_selected.item_effect:
                                            manage_inventory("minus", 1, item_selected)
                                            print(f"Vous utilisez : {custom_text(item_selected.name, 'bold')}")

                                            repeal_turn = item_selected.item_effect
                                            effects[item_selected.name] = 'Cases restantes : {}'
                                            print(custom_text(f"Les ennemis s'éloignent de vous pendant {repeal_turn} cases", "green"))

                                        break

                                # Si la liste est vide, renvoit au menu des commandes
                                else:
                                    if no_items_selected:
                                        print(custom_text("Vous n'avez aucun objet consommable dans votre inventaire.", "yellow"))
                                print(custom_text("Retour au menu des commandes", "yellow"))
                                command = "default"

                            elif command in command_help:
                                if command in ("aide+", "help+"):
                                    print(custom_text(f'''Commandes disponibles :
* {" / ".join(command_ingame_go)} - Vous avancez d'une case
* {" / ".join(command_ingame_back)} - Vous reculez d'une case
* {" / ".join(command_ingame_observe)} - Vous regardez autour de vous
* {" / ".join(command_game_consumables)} - Vous permet d'utiliser un objet de soin
* {" / ".join(command_game_stat)} - Affiche vos statistiques
* {" / ".join(command_game_inventory)} - Affiche votre inventaire
* {" / ".join(command_help)} - Affiche les commandes disponibles
* {" / ".join(command_ingame_quest)} - Affiche le nombre de cases restant avant d'accomplir votre objectif''', "yellow"))
                                else:
                                    print(custom_text('''Commandes disponibles :
* avancer - Vous avancez d'une case
* reculer - Vous reculez d'une case
* observer - Vous regardez autour de vous
* soin - Vous permet d'utiliser un objet de soin
* stats - Affiche vos statistiques
* inventaire - Affiche votre inventaire
* aide - Affiche les commandes disponibles (ou aide+ pour la liste complète)
* objectif - Affiche le nombre de cases restant avant d'accomplir votre objectif''', "yellow"))

                            elif command in command_ingame_moving:
                                display_repeal_sentence = False

                                if repeal_turn:
                                    repeal_turn -= 1
                                    if not repeal_turn:
                                        display_repeal_sentence = True

                                if not is_dumeors_dead and current_turn == biome_dumeors_den.turn:
                                    fight_rng = 0
                                elif repeal_turn or (current_turn == biome_dumeors_den.turn and is_dumeors_dead):
                                    fight_rng = 99
                                else:
                                    fight_rng = rng(6)

                                # **********************************************************************************************************************
                                # 1/3 DE LANCER UN COMBAT
                                if fight_rng <= 2 and current_biome != biome_village:

                                    # DEFINIT QUEL ENNEMI SE BATTERA DANS LE COMBAT
                                    # Voir defined_npc() pour comprendre
                                    fighting_npc = defined_npc(rng(6))

                                    # Définit et stocke la santé de l'ennemi pour le combat
                                    npc_health = fighting_npc.health

                                    # Stocke des infos spécifiques au combat
                                    is_dodging = False
                                    is_running_away = False
                                    is_player_turn = True
                                    is_special_attack = False

                                    in_between_lines()
                                    print(f'Vous rencontrez {custom_text(alt_name("un", fighting_npc, is_boss=True), "bold")}...')
                                    loading()
                                    print(custom_text('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Un combat se lance ! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', "red"))
                                    if is_first_fight:
                                        print(custom_text('''Actions disponibles en combat :
* attaquer - Vous attaquer l'ennemi
* esquiver - Vous vous préparez à esquiver l'attaque de l'ennemi
* fuite - Vous permet de vous enfuire du combat (Vous n'avancez ni ne reculez d'aucune case)
* stats - Affiche vos statistiques
* aide - Affiche les actions disponibles (ou aide+ pour la liste complète)''', "yellow"))
                                        is_first_fight = False
                                        default_in_bet_lines()

                                    # Affiche la santé de Tobias et de l'ennemi au début du combat
                                    print(custom_text(f'\nSanté de Tobias : {hero_health}/{total_hero_health}', "yellow") + "   /   " + custom_text(f'Santé {alt_name("du", fighting_npc)} : {npc_health}/{fighting_npc.health}', "yellow"))
                                    print(custom_text("C'est à votre tour de jouer...", "bold"))
                                    action = input_func(ask_action)

                                    # COMBAT
                                    while npc_health > 0 and not game_over:
                                        inventory_consumable = [item for item in hero_inventory if item[0].item_type == "consumable"]
                                        consumables_list = [unidecode(item[0].name.lower()) for item in inventory_consumable]

                                        # Si le joueur souhaite quitter la partie
                                        if action in command_gameover:
                                            game_over = True
                                            break

                                        if action not in (list_command_fight + consumables_list) and is_player_turn:
                                            in_between_lines()
                                            action = input_func(ask_action_fail)
                                        else:
                                            # COMBAT - TOUR DU JOUEUR
                                            if npc_health > 0 and is_player_turn and not game_over:
                                                if action in command_fight_attack:
                                                    dealt_damage = get_damage("hero")
                                                    npc_health -= dealt_damage
                                                    is_player_turn = False

                                                    deadnpc_sentence = custom_text(f"Vous infligez {dealt_damage} de dégâts à l'ennemi ¤¤¤!", "green")
                                                    if npc_health > 0:
                                                        print(text_replace(deadnpc_sentence))
                                                        print(custom_text(f'Santé {alt_name("du", fighting_npc)} : {npc_health}/{fighting_npc.health}', "yellow"))
                                                    else:
                                                        print(text_replace(deadnpc_sentence, "qui décède suites de ces blessures "))

                                                if action in command_fight_dodge:
                                                    is_player_turn = False
                                                    print(custom_text("Vous vous préparez à esquiver...", "yellow"))
                                                    is_dodging = True

                                                if action in command_fight_escape:
                                                    is_running_away = True

                                                if action in command_game_consumables + consumables_list:
                                                    inventory_consumable = [item for item in hero_inventory if item[0].item_type == "consumable"]
                                                    no_items_selected = True

                                                    # Si la liste n'est pas vide, demande quel objet utiliser
                                                    while len(inventory_consumable) > 0 and no_items_selected:
                                                        if action in command_game_consumables:
                                                            print(custom_text("\nListe des objets consomables :", "blue"))

                                                            # Liste tous les objets consommables disponibles
                                                            for item in inventory_consumable:
                                                                consumable_line = custom_text(f'x{item[1]} {item[0].name}', "bold")

                                                                if item[0].heals:  # Si objet de soin
                                                                    print(consumable_line, custom_text(l10n.inventory.consumable_desc_heal.format(item[0].heals), "green"))
                                                                else:
                                                                    print(consumable_line, custom_text(l10n.inventory.consumable_desc_oust.format(item[0].item_effect), "green"))

                                                            action = input_func(custom_text('\nQuel objet consommable souhaitez-vous utiliser ? (écrivez "aucun" pour sortir du menu)\n> ', "blue"))

                                                        while action not in inventory_value("consumable"):
                                                            if action in ("none", "aucun"):
                                                                no_items_selected = False
                                                                break

                                                            in_between_lines()
                                                            action = input_func(custom_text('Objet consommable non reconnu. Quel objet consommable souhaitez-vous utiliser ? (écrivez "aucun" pour sortir du menu)\n> ', "blue"))
                                                        else:
                                                            item_selected = [consumable_item for consumable_item in inventory_consumable if action == unidecode(consumable_item[0].name.lower())][0][0]

                                                            # Si potion de soin
                                                            if item_selected.heals:
                                                                if hero_health != total_hero_health:
                                                                    is_player_turn = False
                                                                    manage_inventory("minus", 1, item_selected)
                                                                    print(f"Vous utilisez : {custom_text(item_selected.name, 'bold')}")

                                                                    hero_health += item_selected.heals
                                                                    print(custom_text(f"+{item_selected.heals} de santé", "green"))

                                                                    if hero_health > total_hero_health:
                                                                        hero_health = total_hero_health

                                                                    print(custom_text(f"Santé de Tobias : {hero_health}/{total_hero_health}", "yellow"))
                                                                else:
                                                                    print("Votre santé est déjà au maximum, vous ne pouvez utiliser aucun objet de soin.")

                                                            # Si potion à effet
                                                            if item_selected.item_effect:
                                                                manage_inventory("minus", 1, item_selected)
                                                                print(f"Vous utilisez : {custom_text(item_selected.name, 'bold')}")

                                                                repeal_turn = item_selected.item_effect
                                                                effects[item_selected.name] = 'Cases restantes : {}'
                                                                print(custom_text(f"Les ennemis s'éloignent de vous pendant {repeal_turn} cases", "green"))

                                                            break

                                                    # Si la liste est vide, renvoit au menu des commandes
                                                    else:
                                                        if no_items_selected:
                                                            print(custom_text("Vous n'avez aucun objet consommable dans votre inventaire.", "yellow"))

                                                if action in command_help:
                                                    if action in ("aide+", "help+"):
                                                        print(custom_text(f'''Actions disponibles en combat :
* {" / ".join(command_fight_attack)} - Vous attaquer l'ennemi
* {" / ".join(command_fight_dodge)} - Vous vous préparez à esquiver l'attaque de l'ennemi
* {" / ".join(command_fight_escape)} - Vous permet de vous enfuire du combat (Vous n'avancez ni ne reculez d'aucune case)
* {" / ".join(command_game_stat)} - Affiche vos statistiques
* {" / ".join(command_game_inventory)} - Affiche votre inventaire
* {" / ".join(command_help)} - Affiche les commandes disponibles''', "yellow"))
                                                    else:
                                                        print(custom_text('''Actions disponibles en combat :
* attaquer - Vous attaquer l'ennemi
* esquiver - Vous vous préparez à esquiver l'attaque de l'ennemi
* fuite - Vous permet de vous enfuire du combat (Vous n'avancez ni ne reculez d'aucune case)
* stats - Affiche vos statistiques
* inventaire - Affiche votre inventaire
* aide - Affiche les actions disponibles (ou aide+ pour la liste complète)''', "yellow"))

                                                if action in command_game_stat:
                                                    next_level_exp = exp_to_levelup - hero_exp
                                                    print(custom_text(f"Santé : {hero_health}/{total_hero_health}\t\t\tNiveau : {hero_level}\t EXP actuelle : {hero_exp}\n"
                                                                      f'Dégâts : {total_hero_damage} ({hero_damage} +{item_damage})\t\tEXP avant prochain niveau : {next_level_exp}\n'
                                                                      f'Défense : {total_hero_defense} ({hero_defense} +{item_defense})\t\tBourse : {hero_gold} or', "yellow"))

                                                if action in command_game_inventory:
                                                    default_in_bet_lines()
                                                    display_inventory('all')
                                                    default_in_bet_lines()

                                            # COMBAT - TOUR DU PNJ
                                            else:
                                                # SI LE HEROS N'A PLUS DE SANTÉ, ARRÊTE LE COMBAT
                                                if game_over:
                                                    break

                                                print(custom_text("\nC'est au tour de l'ennemi...", "bold"))

                                                loading()
                                                is_player_turn = True

                                                # ATTAQUE CHARGÉE
                                                if is_special_attack:
                                                    # Définit des dégâts doubles pour l'attaque lourde en fonction de la rareté d'apparition du monstre
                                                    dealt_damage = 0

                                                    if fighting_npc.rarity == 1:  # Ennemis communs
                                                        dealt_damage = ceil(get_damage("") * 1.25)
                                                    elif fighting_npc.rarity == 2:  # Ennemis communs
                                                        dealt_damage = ceil(get_damage("") * 1.5)
                                                    elif fighting_npc.rarity == 3:  # Ennemis communs
                                                        dealt_damage = ceil(get_damage("") * 1.75)
                                                    else:  # Boss
                                                        dealt_damage = ceil(get_damage("") * 2.25)

                                                    hero_health -= dealt_damage
                                                    is_special_attack = False
                                                    charge_sentence = custom_text(f'Il envoit la sauce ¤¤¤!', "red")

                                                    if hero_health <= 0:
                                                        print(text_replace(charge_sentence, f'et vous inflige {dealt_damage} de dégâts qui vous tue '))
                                                        game_over = True
                                                    else:
                                                        print(text_replace(charge_sentence, ''))
                                                        # Reset l'esquive, empêchant d'esquiver une attaque lourde
                                                        if is_dodging:
                                                            is_dodging = False
                                                            print(custom_text("Impossible d'esquiver les attaques lourdes !", "red"))
                                                        print(custom_text(f"Vous subissez -{dealt_damage} de santé !", "red"))
                                                        print(custom_text(f'Santé de Tobias : {hero_health}/{total_hero_health}', "yellow"))

                                                # 1 chance sur 4 (définit par "number") de charger un attaque
                                                elif rng(4) == 0:
                                                    is_special_attack = True
                                                    print(custom_text("L'ennemi charge une attaque lourde...", "yellow"))
                                                else:
                                                    # SI ACTION == ESQUIVE / 3 chance sur 4 de ne pas réussir à esquiver
                                                    random_dodge = rng(4)
                                                    if random_dodge > 0 and is_dodging:
                                                        print(
                                                            custom_text("L'ennemi vous attaque mais vous l'esquivez !", "green"))
                                                    else:
                                                        # FIN DE TOUR DU PNJ
                                                        dealt_damage = get_damage("")
                                                        hero_health -= dealt_damage
                                                        dmg_sentence = custom_text(f'{alt_name("le", fighting_npc, is_boss=True).capitalize()} vous attaque et vous inflige {dealt_damage} de dégâts ¤¤¤!', "red")
                                                        if hero_health <= 0:
                                                            print(text_replace(dmg_sentence, "qui vous tue "))
                                                            game_over = True

                                                        elif random_dodge == 0 and is_dodging:
                                                            # SI ESQUIVE ECHOUE
                                                            print(custom_text(f"L'ennemi passe à travers votre esquive et vous inflige {dealt_damage} de dégâts !", "red"))
                                                            print(custom_text(f'Santé de Tobias : {hero_health}/{total_hero_health}', "yellow"))
                                                        else:
                                                            # ATTAQUE NORMALE DU PNJ
                                                            print(text_replace(dmg_sentence, ""))
                                                            print(custom_text(f'Santé de Tobias : {hero_health}/{total_hero_health}', "yellow"))

                                                    # Reset l'esquive sur False après la fin du combat
                                                    is_dodging = False

                                            # SI ACTION == FUITE
                                            if is_running_away:
                                                # 1 chance sur 5 de rester en combat et de prendre des dégâts
                                                running_away_chances = rng(10)
                                                if running_away_chances <= 1:
                                                    # ANNULE LA FUITE
                                                    is_running_away = False
                                                    print(custom_text("Fuite impossible ! L'ennemi vous en a empêché !", "red"))
                                                elif running_away_chances <= 5:
                                                    # ANNULE LA FUITE ET BLESSE
                                                    is_running_away = False
                                                    inflicted_damage = get_damage("")
                                                    hero_health -= inflicted_damage
                                                    print(custom_text(f"Fuite impossible ! L'ennemi vous en a empêché et vous inflige même {inflicted_damage} de dégâts !", "red"))

                                                    if hero_health < 1:
                                                        game_over = True
                                                    else:
                                                        print(custom_text(f'Santé de Tobias : {hero_health}/{total_hero_health}', "yellow"))

                                                else:
                                                    # ARRÊTE LE COMBAT
                                                    npc_health = -1

                                            # REDEMANDE UNE COMMANDE À LA FIN DU TOUR ENNEMI OU PENDANT LE TOUR DU JOUEUR SI IL N'ATTAQUE PAS
                                            if is_player_turn and not is_running_away and not game_over:
                                                in_between_lines()
                                                if action not in (list(set(list_command_all) - set(list_command_fight))):
                                                    if action not in (command_help + command_game_stat + command_game_consumables):
                                                        default_in_bet_lines()
                                                        print(custom_text("\nC'est à votre tour de jouer...", "bold"))

                                                    action = input_func(ask_action)

                                                else:
                                                    action = input_func(ask_action_fail)

                                    # APRES COMBAT
                                    else:
                                        if game_over:
                                            break
                                        print(custom_text("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Combat terminé ! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", "red"))
                                        # SANS EXPERIENCE
                                        if is_running_away:
                                            # 3/4 de chances de réussir à fuir sans être blesser
                                            if rng(4):
                                                print("Vous prenez la fuite...")
                                            else:
                                                last_damage_dealt = get_damage("")
                                                hero_health -= last_damage_dealt
                                                print(custom_text(f'Vous prenez la fuite... mais {alt_name("le", fighting_npc)} vous enlève -{last_damage_dealt} de santé en partant...', "red"))
                                                print(custom_text(f'Santé de Tobias : {hero_health}/{total_hero_health}', "yellow"))
                                            print("Vous n'avez gagné aucun points d'experience.\nVous n'êtes avancé d'aucune case.\n")

                                        # AVEC EXPERIENCE
                                        else:
                                            if fighting_npc == npc_dumeors:
                                                is_dumeors_dead = True
                                            else:
                                                # Redéfinit le tour du joueur en fonction de si il a avancé ou non
                                                current_turn = current_turn + 1 if command in command_ingame_go else current_turn - 1

                                            # Gère le compteur de meurtres
                                            # tobias_class.kill_counter(fighting_npc)
                                            kill_counter[fighting_npc] = 1 if fighting_npc not in kill_counter else kill_counter[fighting_npc] + 1

                                            fight_points += 10

                                            fight_exp = fighting_npc.given_exp
                                            # Varie les pièces d'or gagnée de -2 à +2 de leur valeur initiale
                                            fight_gold = fighting_npc.given_gold + rng(-2, 3)

                                            hero_exp += fight_exp
                                            hero_gold += fight_gold

                                            print(custom_text(f"Vous avez gagné {fight_exp} points d'experience et {fight_gold} or !", "yellow"))

                                            # ######### SYSTÈME DE DROP
                                            loot_list = [loot for loot in fighting_npc.loot if rng(loot[2]) == 0]

                                            if loot_list:
                                                print(custom_text("L'ennemi a lâché les objets suivants que vous récupérez :", "yellow"))
                                                for loot in loot_list:
                                                    print(custom_text(f"x{loot[1]} {loot[0].name}"))
                                                    manage_inventory("+", loot[1], loot[0])

                                            # ######### SYSTÈME DE LEVEL-UP
                                            # STOCKE LE NIVEAU AVANT PASSAGE DE NIVEAU POUR COMPARER COMBIEN DE NIVEAUX ONT ÉTÉ OBTENUS
                                            old_hero_level = hero_level

                                            # ------------ Gère l'affichage du levelup
                                            # Utilisation de valeurs tampons pour afficher le texte de levelup avant ceux des stats
                                            hero_level_decoy = hero_level
                                            hero_exp_decoy = hero_exp
                                            exp_to_levelup_decoy = exp_to_levelup

                                            # Phrases de level-up stockée ici pour éviter la répétition
                                            def exp_sentences():
                                                next_level_exp_decoy = exp_to_levelup_decoy - hero_exp_decoy
                                                exp_sentence = custom_text(f"Vous êtes désormais niveau {hero_level_decoy}. Plus que {next_level_exp_decoy} ¤¤¤ d'exp pour passer au niveau supérieur.", "yellow")
                                                if next_level_exp_decoy == 1:
                                                    print(text_replace(exp_sentence, "point"))
                                                else:
                                                    print(text_replace(exp_sentence, "points"))

                                            while hero_exp_decoy >= exp_to_levelup_decoy:
                                                hero_level_decoy += 1
                                                hero_exp_decoy -= exp_to_levelup_decoy
                                                exp_to_levelup_decoy = ceil(exp_to_levelup_decoy * 1.12)

                                            # Ne se déclenche que si un seul niveau n'a été obtenu
                                            if old_hero_level + 1 == hero_level_decoy:
                                                print(custom_text(f"Niveau supérieur ! (+{hero_level_decoy - old_hero_level})", "green"))
                                                exp_sentences()

                                            # Ne se déclenche quand plusieurs niveaux ont été obtenus d'un coup
                                            elif old_hero_level + 2 <= hero_level_decoy:
                                                print(custom_text(f"Niveaux supérieurs ! (+{hero_level_decoy - old_hero_level})", "green"))
                                                exp_sentences()

                                            if hero_level_decoy != hero_level:
                                                print(custom_text("Statistique(s) augmentée(s) :", "green"))

                                            # ---------------- Gère les calculs du levelup et les augmentations de stats
                                            while hero_exp >= exp_to_levelup:
                                                hero_level += 1
                                                hero_exp -= exp_to_levelup

                                                # L'experience pour levelup augmente de 1,12 de sa valeur initiale et est arrondie au nobbre entier supérieur pour éviter d'avoir d'afficher de l'experience
                                                exp_to_levelup = ceil(exp_to_levelup * 1.12)

                                                # Augmente la bonne stat en fonction du dictionnaire levelup_stats
                                                if hero_level in levelup_stats:
                                                    for stat_type, stat_increase in levelup_stats.get(hero_level).items():
                                                        # Dégats
                                                        if "damage" in stat_type:
                                                            hero_damage += stat_increase
                                                            total_hero_damage = hero_damage + item_damage
                                                            print(custom_text(f'+{stat_increase} de dégâts'))
                                                        # Défense
                                                        elif "defense" in stat_type:
                                                            hero_defense += stat_increase
                                                            total_hero_defense = hero_defense + item_defense
                                                            print(custom_text(f'+{stat_increase} de défense'))
                                                        # Santé
                                                        elif "health" in stat_type:
                                                            hero_health += stat_increase
                                                            total_hero_health += stat_increase
                                                            print(custom_text(f'+{stat_increase} de santé et santé max'))
                                                else:
                                                    if old_hero_level + 1 == hero_level_decoy:
                                                        print("Aucune")

                                            # Redefinit next_level_exp à la fin
                                            next_level_exp = exp_to_levelup - hero_exp

                                # 2/3 QU'IL NE SE PASSE RIEN
                                else:
                                    if command in command_ingame_go:
                                        if current_biome == biome_village:
                                            print(custom_text('\nVous sortez du village, les portes se referment derrière vous...', 'yellow'))
                                            current_turn += 1

                                        elif is_dumeors_dead and current_turn == biome_dumeors_den.turn:
                                            print(custom_text("La carcasse de Dumeors git toujours sur le sol", "yellow"))
                                            print(custom_text("Vous semblez être dans une impasse...", "yellow"))
                                        else:
                                            current_turn += 1
                                            messages_go_phrase = ["Vous continuez tranquillement votre chemin tout en avançant d'un case.",
                                                                  "Vous avancez d'une case sans trop d'encombres."]
                                            print(messages_go_phrase[rng(len(messages_go_phrase))])

                                    else:
                                        if current_biome == biome_village:
                                            print(custom_text("Vous êtes déjà dans le village, vous ne pouvez sortir qu'en avançant.", "yellow"))

                                        else:
                                            current_turn -= 1
                                            messages_back_phrase = ["Vous retournez en arrière d'une case.",
                                                                    "Vous faites marche arrière d'une case sans trop d'encombres."]
                                            print(messages_back_phrase[rng(len(messages_back_phrase))])

                                if display_repeal_sentence:
                                    effects_dummy = effects.copy()
                                    for effect in effects_dummy:
                                        del effects[effect]
                                    print("L'odeur du parfum nauséabond semble s'être estompée...")

                            # UNE FOIS LE TOUR TERMINÉ, DEMANDE UNE COMMANDE
                            if hero_health > 0 and not game_over:
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
                                if current_turn == biome_dumeors_den.turn and not is_dumeors_dead:
                                    print(custom_text("\nAttention, écrire « avancer » lancera le combat. Pensez à vous soigner avant de l'affronter.", 'red'))

                                command = input_func(ask_command) if command in list_command_ingame else input_func(ask_command_fail)

                # Se déclenche une fois la partie terminée (ou l'objectif atteint en mode débug)
                else:
                    default_in_bet_lines()

                    def endgame_statistics():
                        # DÉFINIT L'AFFICHAGE DE DONNÉES À LA FIN DE LA PARTIE (POINTS, TEMPS, NOMBRES DE MEURTRES)
                        timer = ceil(time() - starting_time)
                        time_points = (timer - loading_points) / 3

                        level_points = hero_level * 10

                        if game_over:
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
                        # tobias_class.display_kill_counter()
                        if kill_counter:
                            print("Nombre de monstre tués :")
                            for enemy, count in kill_counter.items():
                                print(f"x{count} {enemy.name}")

                    if game_over:
                        # SI GAME OVER
                        print(custom_text("Game over ! Vous avez perdu !", "red"))
                        endgame_statistics()
                        command = command_func(input_func(custom_text("Voulez-vous recommencer ? (oui/non)\n> ", "red")), list_command_other)

                        while command not in list_command_other:
                            in_between_lines()
                            command = input_func(custom_text("Recommencer ? (oui/non)\n> ", "red")),
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
                    break
    else:
        # SI COMMANDE == "menu" DANS LES OPTIONS OU SI LE JOUEUR RECOMMENCE UNE PARTIE
        if was_in_options or is_new_game or command in list_command_other:
            command = command_func(input_func(ask_menu), list_command_other)
            was_in_options = False
        else:
            in_between_lines()
            command = command_func(input_func(ask_menu_fail), list_command_other)
