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

        if l10n.language.lang == "english":
            name = npc.plural if pronoun in ("les", "des", "aux") else npc.name

        elif l10n.language.lang == "french":
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