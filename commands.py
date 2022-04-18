# ==================================================== Générique
# Défaut
cmd_default = command_default = ["defaut"]
# Aide
cmd_help = command_help = ["help", "aide", "help+", "aide+"]
# Quitte la partie/jeu
cmd_gameover = command_gameover = ["gameover", "quit"]

# ==================================================== Menu
# Retour au menu
cmd_menu_menu = command_menu = ["menu"]
# Lance une partie
cmd_menu_play = command_menu_play = ["jouer", "play", "demarrer", "start", "commencer"]
# Ouvre les options
cmd_menu_option = command_menu_options = ["option", "setting", "parametre"]

# ==================================================== Options
# Couleurs
cmd_option_color = command_options_color = ["color", "couleur"]
# Lignes
cmd_option_line = command_options_line = ["line", "ligne"]
# Chargements
cmd_option_loading = command_options_loading = ["loading", "chargement"]
# Langues
cmd_option_lang = command_options_language = ["langue", "language"]

# ==================================================== Langues
cmd_option_l10n_fr = command_options_l10n_fr = ['fre']
cmd_option_l10n_en = command_options_l10n_en = ['eng']
cmd_option_l10n = command_options_l10n = cmd_option_l10n_fr + cmd_option_l10n_en

cmd_option_full = cmd_option_color + cmd_option_line + cmd_option_loading + cmd_option_lang + cmd_option_l10n

# ==================================================== Tout le temps en jeu
# Statistiques
cmd_game_stat = command_game_stat = ["information", "statistic", "statistique"]
# Utilisation d'objets
cmd_game_consumable = command_game_consumables = ["soin", "heal", "item", "objet", "consumable", "potion", "antidote"]
# Inventaire
cmd_game_inv = command_game_inventory = ["inventaire", "inventory"]

# ==================================================== Village
# Parler au marchand
cmd_npc_merchant = command_npc_merchant = ["marchand", "merchant", "seller", "vendor", "vendeur", "acheteur", "shopkeeper", "trader"]
# Acheter au marchand
cmd_npc_merchant_buy = command_npc_merchant_buy = ["achat", "buy", "acheter", "purchase"]
# Vendre au marchand
cmd_npc_merchant_sell = command_npc_merchant_sell = ["vente", "vendre", "sell", "vend"]
cmd_npc_merchant_full = command_npc_merchant_full = cmd_npc_merchant + cmd_npc_merchant_buy + cmd_npc_merchant_sell + ['trade', 'trading', "echanger"]

# Parler au trappeur
cmd_npc_trappist = command_npc_trappist = ["trappeur", "trappist"]

# Commandes dans village
cmd_npc_names = command_npc_names = cmd_npc_merchant_full + cmd_npc_trappist

# ==================================================== Uniquement hors combat
# Avancer
cmd_ingame_go = command_ingame_go = ["avancer", "go", "marcher", "walk"]
# Reculer
cmd_ingame_back = command_ingame_back = ["reculer", "back"]
# Déplacement
cmd_ingame_moving = command_ingame_moving = cmd_ingame_go + cmd_ingame_back

# Quête
cmd_ingame_quest = command_ingame_quest = ["rappel", "objectif", "turn", "objective", "tour", "quest", 'quete']
# Observer
cmd_ingame_observe = command_ingame_observe = ["observe", "observer"]

cmd_ingame_full = cmd_ingame_moving + cmd_ingame_quest + cmd_ingame_observe

# ==================================================== Uniquement en combat
# Attaquer
cmd_fight_attack = command_fight_attack = ["atque", "atck", "fight", "combatre"]
# Esquiver
cmd_fight_dodge = command_fight_dodge = ["dodge", "evade", "esquive"]
# Fuire
cmd_fight_escape = command_fight_escape = ["fuite", "partir", "run"]

cmd_fight_full = cmd_fight_attack + cmd_fight_dodge + cmd_fight_escape

# ==================================================== Booléens
# True
cmd_yes = command_yes = ["oui", "yes", "oe", "ok", "vasy", "go", "on", "active", "activate", "true", "vrai"]
# False
cmd_no = command_no = ["non", "off", "rien", "none", "aucun", "nothing", "desactivate", "desactive", "false", "faux"]

# Commandes disponibles dans le menu
cmd_list_menu = list_command_menu = cmd_menu_play + cmd_menu_option

# Commandes disponibles dans les options
cmd_list_option = list_command_options = cmd_option_full + cmd_menu_menu + cmd_help + cmd_default

# Commandes disponibles hors combat
cmd_list_ingame = list_command_ingame = cmd_ingame_full + cmd_game_inv + cmd_game_stat + cmd_game_consumable + cmd_help + cmd_default + cmd_gameover + cmd_npc_names

# Commandes disponibles en combat
cmd_list_fight = list_command_fight = cmd_help + cmd_game_stat + cmd_fight_full + cmd_game_consumable + cmd_gameover

# Autres commandes
cmd_list_other = list_command_other = cmd_yes + cmd_no + cmd_default

# Toutes les commandes
cmd_list_all = list_command_all = list(set(cmd_list_menu + cmd_list_option + cmd_list_ingame + cmd_list_fight + cmd_list_other))