from dotmap import DotMap
from math import ceil

# French
fr_l10n = {
    # --------------------------------- Interface
    'inventory': {
        'inventory_intro': "Inventaire : ",
        'no_items': "Aucun objet dans l'inventaire.",
        'consumable_intro': "Consommables",
        'consumable_desc_heal': "(Soigne {} de santé)",                     # Santé soignée
        'consumable_desc_oust': "(Éloigne les ennemis sur {} cases)",       # Cases éloignées
        'armor_intro': "Armure (totale : {} de défense)",                # Défense d'armure totale
        'armor_desc': "({} de défense)",                                    # Défense d'armure
        'weapon_intro': "Armes (équipée : {})",                          # Dégâts de l'arme la plus puissante
        'weapon_desc': "({} de dégâts)",                                    # Dégâts d'arme
        'ingredient_intro': "Ingrédients",
        'quest_intro': "Objets de Quête"
    },

    # --------------------------------- Options
    'options': {
        "lang":
            {"selected": "La langue est ¤¤¤ définie sur Français.",
             "already": "déjà",
             "now": "désormais"
             }
    },

    # --------------------------------- Inputs de commande
    'question': {
        # Menu
        'ask_menu': 'Menu principal - Commandes disponibles :\n* « jouer » - Lancer une partie\n* « options » - Menu des options\n> ',
        'ask_menu_fail': "Commande inconnue, écrivez une commande valide.\n> ",
        # Options
        'ask_options': 'Quelle option souhaitez-vous modifier ? Écrivez « aide » pour afficher les commandes disponibles.\n> ',
        'ask_options_fail': "Commande inconnue, retour aux options. Quelle option souhaitez-vous modifier ?\n> ",
        # Hors combat
        'ask_command': "\nQue souhaitez vous faire ?\n> ",
        'ask_command_fail': 'Commande non reconnue ou indisponible - Écrivez « aide » pour afficher la liste des commandes disponibles.\n> ',
        # Combat
        'ask_action': "Quelle action souhaitez vous faire ?\n> ",
        'ask_action_fail': 'Action non reconnue ou indisponible - Écrivez « aide » pour afficher la liste des actions disponibles.\n> '
    },

    # --------------------------------- Dialogues
    'quote': {
        "intro": """Année 359, contrée de Blère Ouitch
  Vous incarnez Tobias, un jeune explorateur en quête d'aventures ayant récemment accepté une chasse aux monstres.
  Les portes du village d'où vous venez de faire escale viennent de se refermer derrière vous afin de protéger le village des monstres environnants, vous ne pouvez plus faire marche arrière.
  L'entrée de la tanière du monstre se trouve à {} cases devant vous.""",              # Nombre de cases pour atteindre la tanière du monstre

        "intro2": """Année 359, contrée de Blère Ouitch
Vous incarnez Tobias, un jeune explorateur en quête d'aventures.
Vous commencez dans le village de départ.
Les portes du village d'où vous venez de faire escale viennent de se refermer derrière vous afin de protéger le village des monstres environnants, vous ne pouvez plus faire marche arrière."""
    },

    # --------------------------------- Langues
    'language': {
        'name': {
            "french": 'Français',
            "english": 'Anglais (English)',
            "german": 'Allemand (Deutsch)'
        },
        'lang': 'french'
    },

    # --------------------------------- Objets
    'item': {
        'healing_potion': {
            'name': {
                'one': 'Potion de soin',
                'many': 'Potions de soin'
                },
            'desc': "Une petite potion qui régénère 15 de santé"
            },
        'goblin_axe': {
            'name': {
                'one': 'Hache de gobelin',
                'many': 'Haches de gobelin'
            },
            'desc': "Une hache couverte de sang composée de divers morceaux de ferailles"
        },
        'enigmatic_ring': {
            'name': {
                'one': 'Anneau énigmatique',
                'many': 'Anneaux énigmatiques'
            },
            'desc': "Un anneau élégant serti d'un haut de forme"
        },
        'basic_sword': {
            'name': {
                'one': 'Épée basique',
                'many': 'Épées basiques'
            },
            'desc': "Une épée tout à fait sommaire"
        },
        'basic_clothes': {
            'name': {
                'one': 'Vêtement rudimentaire',
                'many': 'Vêtements rudimentaires'
            },
            'desc': "Des fripes appartenant à votre oncle"
        },
        'basic_pants': {
            'name': {
                'one': "Pantalon rudimentaire",
                'many': 'Pantalons rudimentaires'
            },
            'desc': "Un vieux pantalon délavé"
        },
        'basic_shoes': {
            'name': {
                'one': "Chaussures rudimentaires",
                'many': "Chaussures rudimentaires"
            },
            'desc': "Cette vieille paire semble avoir déteint avec les années"
        },
        'greater_healing_potion': {
            'name': {
                'one': 'Forte potion de soin',
                'many': 'Fortes potions de soin'
            },
            'desc': "Une grande potion qui régénère 35 de santé"
        },
        'dumeors_head': {
            'name': {
                'one': 'Tête de Dumeors',
                'many': 'Têtes de Dumeors'
            },
            'desc': "La tête coupée de la bête"
        },
        'goblin_belt': {
            'name': {
                'one': 'Ceinture de gobelin',
                'many': 'Ceintures de gobelin'
            },
            'desc': "Une ceinture rustique composée de vieux morceaux de cuir"
        },
        'venom_vial': {
            'name': {
                'one': "Fiole de venin",
                'many': "Fioles de venin",
            },
            'desc': ""
        },
        'putrid_perfume': {
            'name': {
                'one': "Parfum nauséabond",
                'many': "Parfums nauséabonds",
            },
            'desc': "Un parfum aux odeurs putrides qui éloigne les ennemis pour 5 cases"
        },
        'goblin_boots': {
            'name': {
                'one': "Bottes gobelines",
                'many': "Bottes gobelines",
            },
            'desc': ""
        },
        'goblin_stick': {
            'name': {
                'one': "Bâton gobelin",
                'many': "Bâtons gobelins",
            },
            'desc': ""
        },
        'goblin_beanie': {
            'name': {
                'one': "Bonnet gobelin",
                'many': "Bonnets gobelins",
            },
            'desc': ""
        },
    },

    # --------------------------------- PNJs
    'npc': {
        'slime': {
            'name': {
                'one': 'Gelée',
                'many': 'Gelées',
            },
            'desc': ""
        },
        'bat': {
            'name': {
                'one': 'Chauve-souris',
                'many': 'Chauves-souris',
            },
            'desc': ""
        },
        'goblin': {
            'name': {
                'one': 'Gobelin',
                'many': 'Gobelins',
            },
            'desc': ""
        },
        'rat': {
            'name': {
                'one': 'Rat',
                'many': 'Rats',
            },
            'desc': ""
        },
        'hobgoblin': {
            'name': {
                'one': 'Hobgobelin',
                'many': 'Hobgobelins',
            },
            'desc': ""
        },
        'dumeors': {
            'name': {
                'one': "Dumeors l'Acéré",
                'many': "Dumeors l'Acéré",
            },
            'desc': ""
        },
        'merchant': {
            'name': {
                'one': 'Marchand',
                'many': 'Marchands',
            },
            'desc': ""
        },
        'trappist': {
            'name': {
                'one': 'Trappeur',
                'many': 'Trappeurs',
            },
            'desc': ""
        },
        'smol_goblin': {
            'name': {
                'one': "P'tit gobelin",
                'many': "P'tits gobelins",
            },
            'desc': ""
        },
    },

    # --------------------------------- Biomes
    'biome': {
        'forest': {
            'name': "Forêt",
            'desc': ""
        },
        'caves': {
            'name': "Grottes",
            'desc': ""
        },
        'base_village': {
            'name': "Village",
            'desc': ""
        },
        'dumeors_den': {
            'name': "Tanière de Dumeors",
            'desc': ""
        }
    }
}

# English
en_l10n = {
    # --------------------------------- Interface
    'inventory': {
        'inventory_intro': "Inventory : ",
        'no_items': "No items in inventory.",
        'consumable_intro': "Consumables",
        'consumable_desc_heal': "(Heal {} health)",
        'consumable_desc_oust': "(Keep enemies away for {} squares)",
        'armor_intro': "Armor (total: {} defense)",
        'armor_desc': "({} defense)",
        'weapon_intro': "Weapons (equipped: {})",
        'weapon_desc': "({} damage)",
        'ingredient_intro': "Ingredients",
        'quest_intro': "Quest Items"
    },

    # --------------------------------- Options
    'options': {
        "lang":
            {"selected": "The language is ¤¤¤ set to English.",
             "already": "already",
             "now": "now"
             }
    },

    # --------------------------------- Command Inputs
    'question': {
        # Menu
        'ask_menu': 'Main menu - Available commands :\n* "play" - Start a game\n* "options" - Options menu\n> ',
        'ask_menu_fail': "Unknown command, write a valid command.\n> ",
        # Options
        'ask_options': 'What option would you like to change? Write "help" to display the list of available commands.\n> ',
        'ask_options_fail': "Unknown command, back to options. What option do you want to change?\n> ",
        # Hors combat
        'ask_command': "\nWhat do you want to do?\n> ",
        'ask_command_fail': 'Unknown or unavailable command - Write "help" to display the list of available commands.\n> ',
        # Combat
        'ask_action': "What action do you want to execute?\n> ",
        'ask_action_fail': 'Unknown or unavailable action - Write "help" to display the list of available actions.\n> '
    },

    # --------------------------------- Quotes
    'quote': {
        "intro": """Year 359, Blère Ouitch county
  You play Tobias, a young explorer looking for adventures who have recently accepted a monster hunt.
  The doors from the village you took a stepover just closed behind you in order to protect the village from surrounding monsters, you cannot go back.
  The entrance to the monster's lair is {} squares in front of you."""
    },

    # --------------------------------- Languages
    'language': {
        'name': {
            "french": 'French (Français)',
            "english": 'English',
            "german": 'German (Deutsch)'
        },
        'lang': 'english'
    },

    # --------------------------------- Items
    'item': {
        'healing_potion': {
            'name': {
                'one': 'Healing Potion',
                'many': 'Healing Potion',
            },
            'desc': "A small potion that restores 15 health"
        },
        'goblin_axe': {
            'name': {
                'one': 'Goblin Axe',
                'many': 'Goblin Axes',
            },
            'desc': "A blood covered axe composed of various metal scraps"
        },
        'enigmatic_ring': {
            'name': {
                'one': 'Enigmatic Ring',
                'many': 'Enigmatic Rings'
            },
            'desc': "A fancy ring set with a top hat"
        },
        'basic_sword': {
            'name': {
                'one': 'Simple Sword',
                'many': 'Simple Swords'
            },
            'desc': "A quite sketchy sword"
        },
        'basic_clothes': {
            'name': {
                'one': "Basic Clothes",
                'many': "Basic Clothes"
            },
            'desc': "Some rags belonging to your uncle"
        },
        'basic_pants': {
            'name': {
                'one': "Basic Pants",
                'many': "Basic Pants"
            },
            'desc': "A pants likely worn for manual labor"
        },
        'basic_shoes': {
            'name': {
                'one': "Basic Shoes",
                'many': "Basic Shoes"
            },
            'desc': "This old pair seems to have faded over the years"
        },
        'greater_healing_potion': {
            'name': {
                'one': "Greater Healing Potion",
                'many': "Greater Healing Potions"
            },
            'desc': "A great potion that restores 35 health"
        },
        'dumeors_head': {
            'name': {
                'one': "Dumeors Head",
                'many': "Dumeors Heads"
            },
            'desc': "The severed head of the beast"
        },
        'goblin_belt': {
            'name': {
                'one': "Goblin Belt",
                'many': 'Goblin Belts'
            },
            'desc': "A rustic belt made of old pieces of leather"
        },
        'venom_vial': {
            'name': {
                'one': "Venom Vial",
                'many': "Venom Vials",
            },
            'desc': ""
        },
        'putrid_perfume': {
            'name': {
                'one': "Putrid Perfume",
                'many': "Putrid Perfumes",
            },
            'desc': "A putrid-smelling perfume that repels enemies for 5 squares"
        },
        'goblin_boots': {
            'name': {
                'one': "Goblin Boots",
                'many': "Goblin Boots",
            },
            'desc': ""
        },
        'goblin_stick': {
            'name': {
                'one': "Goblin Stick",
                'many': "Goblin Sticks",
            },
            'desc': ""
        },
        'goblin_beanie': {
            'name': {
                'one': "Goblin Beanie",
                'many': "Goblin Beanies",
            },
            'desc': ""
        },
    },

    # --------------------------------- NPCs
    'npc': {
        'slime': {
            'name': {
                'one': 'Slime',
                'many': 'Slimes',
            },
            'desc': ""
        },
        'bat': {
            'name': {
                'one': 'Bat',
                'many': 'Bats',
            },
            'desc': ""
        },
        'goblin': {
            'name': {
                'one': 'Goblin',
                'many': 'Goblins',
            },
            'desc': ""
        },
        'rat': {
            'name': {
                'one': 'Rat',
                'many': 'Rats',
            },
            'desc': ""
        },
        'hobgoblin': {
            'name': {
                'one': 'Hobgoblins',
                'many': 'Hobgoblins',
            },
            'desc': ""
        },
        'dumeors': {
            'name': {
                'one': "Dumeors the Sharp",
                'many': "Dumeors the Sharp",
            },
            'desc': ""
        },
        'merchant': {
            'name': {
                'one': 'Merchant',
                'many': 'Merchants',
            },
            'desc': ""
        },
        'smol_goblin': {
            'name': {
                'one': "Smol Goblin",
                'many': "Smol Goblins",
            },
            'desc': ""
        },

    },

    # --------------------------------- Biomes
    'biome': {
        'forest': {
            'name': "Forest",
            'desc': ""
        },
        'caves': {
            'name': "Caves",
            'desc': ""
        },
        'base_village': {
            'name': "Village",
            'desc': ""
        },
        'dumeors_den': {
            'name': "Dumeors' Den",
            'desc': ""
        }
    }
}

# Définit la langue par défaut sur français
l10n = DotMap(fr_l10n)

# =========================== Concerne les commandes utilisables en jeu
# Toutes les commandes doivent être écrites en minuscule et sans accents
command_default = ["defaut"]  # Redéfinit la commande sur défaut
command_help = ["help", "aide", "help+", "aide+"]  # Affiche le menu des commandes

command_menu = ["menu"]  # Fait retourner au menu principal
command_menu_play = ["jouer", "play", "demarrer", "start", "commencer"]  # Lance la partie
command_menu_options = ["option", "setting", "parametre"]  # Ouvre le menu des options

command_options_color = ["color", "couleur"]  # Affiche le menu des couleurs
command_options_line = ["line", "ligne"]  # Affiche le menu des lignes
command_options_loading = ["loading", "chargement"]  # Affiche le menu des chargements
command_options_language = ["langue", "language"]  # Affiche le menu des langues

command_options_l10n_fr = ['fre']
command_options_l10n_en = ['eng']
command_options_l10n = command_options_l10n_fr + command_options_l10n_en  # Définit les valeurs des langues

command_game_stat = ["information", "statistic", "statistique"]  # Affiche les statistiques du héros
command_game_consumables = ["soin", "heal", "item", "objet", "consumable", "potion", "antidote"]  # Permet d'utiliser des objets
command_game_inventory = ["inventaire", "inventory"]  # Affiche l'inventaire


command_npc_merchant = ["marchand", "merchant", "seller", "vendor", "vendeur", "acheteur", "shopkeeper", "trader"]  # Commandes du marchand
command_npc_merchant_buy = ["achat", "buy", "acheter", "purchase"]  # Commandes d'achat du marchand
command_npc_merchant_sell = ["vente", "vendre", "sell", "vend"]  # Commandes de vente du marchand
command_npc_merchant_full = command_npc_merchant + command_npc_merchant_buy + command_npc_merchant_sell + ['trade', 'trading', "echanger"]

command_npc_trappist = ["trappeur", "trappist"]  # Commandes du trappeur
command_npc_names = command_npc_merchant_full + command_npc_trappist  # Commandes custom des PNJs


command_ingame_go = ["avancer", "go", "marcher", "walk"]  # Permet d'avancer
command_ingame_back = ["reculer", "back"]  # Permet de reculer
command_ingame_moving = command_ingame_go + command_ingame_back
command_ingame_quest = ["rappel", "objectif", "turn", "objective", "tour", "quest", 'quete']  # Affiche les quêtes en cours
command_ingame_observe = ["observe", "observer"]  # Provoque des actions aléatoires

command_fight_attack = ["atque", "atck", "fight", "combatre"]  # Permet d'attaquer
command_fight_dodge = ["dodge", "evade", "esquive"]  # Permet d'esquiver
command_fight_escape = ["fuite", "partir", "run"]  # Permet de s'échapper du combat

command_yes = ["oui", "yes", "oe", "ok", "vasy", "go", "on", "active", "activate", "true", "vrai"]  # Oui
command_no = ["non", "off", "rien", "none", "aucun", "nothing", "desactivate", "desactive", "false", "faux"]  # Non

command_gameover = ["gameover", "quit"]

# Commandes disponibles dans le menu
list_command_menu = command_menu_play + command_menu_options

# Commandes disponibles dans les options
list_command_options = command_options_color + command_options_line + command_options_loading + command_options_language + command_options_l10n + command_menu + command_help + command_default

# Commandes disponibles hors combat
list_command_ingame = command_ingame_moving + command_ingame_quest + command_ingame_observe + command_game_inventory + command_game_stat + command_game_consumables + command_help + command_default + command_gameover + command_npc_names

# Commandes disponibles en combat
list_command_fight = command_help + command_game_stat + command_fight_attack + command_fight_dodge + command_fight_escape + command_game_consumables + command_gameover

# Autres commandes
list_command_other = command_yes + command_no + command_default

# Toutes les commandes
list_command_all = list(set(list_command_menu + list_command_options + list_command_ingame + list_command_fight + list_command_other))


# ======================================================================================================================
# =========================================================== Définit et stocke les informations des objets
class Items:
    def __init__(
            self,
            item_id: int,
            name: str,
            plural: str,
            item_type: str,
            body_slot: str,
            damage: int,
            defense: int,
            heals: int,
            item_effect: int,
            buy_price: int,
            item_desc: str
    ):
        self.item_id = item_id
        self.name = name
        self.plural = plural
        self.item_type = item_type  # armor, weapon, consumable, quest, ingredient
        self.body_slot = body_slot  # hat, breastplate, ring, belt, pants, shoes
        self.damage = damage
        self.defense = defense
        self.heals = heals
        self.item_effect = item_effect
        self.buy_price = buy_price
        self.sell_price = ceil(self.buy_price / 5) if self.buy_price else 0
        self.item_desc = item_desc


item_healing_potion = Items(
    item_id=0,
    name=l10n.item.healing_potion.name.one,
    plural=l10n.item.healing_potion.name.many,
    item_type="consumable",
    body_slot="",
    damage=0,
    defense=0,
    heals=15,
    item_effect=0,
    buy_price=20,
    item_desc=l10n.item.healing_potion.desc
    )
item_goblin_axe = Items(
    item_id=1,
    name=l10n.item.goblin_axe.name.one,
    plural=l10n.item.goblin_axe.name.many,
    item_type="weapon",
    body_slot="",
    damage=7,
    defense=0,
    heals=0,
    item_effect=0,
    buy_price=100,
    item_desc=l10n.item.goblin_axe.desc
    )
item_enigmatic_ring = Items(
    item_id=2,
    name=l10n.item.enigmatic_ring.name.one,
    plural=l10n.item.enigmatic_ring.name.many,
    item_type="armor",
    body_slot="ring",
    damage=0,
    defense=1,
    heals=0,
    item_effect=0,
    buy_price=80,
    item_desc=l10n.item.enigmatic_ring.desc
    )
item_basic_sword = Items(
    item_id=3,
    name=l10n.item.basic_sword.name.one,
    plural=l10n.item.basic_sword.name.many,
    item_type="weapon",
    body_slot="",
    damage=4,
    defense=0,
    heals=0,
    item_effect=0,
    buy_price=50,
    item_desc=l10n.item.basic_sword.desc
    )
item_basic_clothes = Items(
    item_id=4,
    name=l10n.item.basic_clothes.name.one,
    plural=l10n.item.basic_clothes.name.many,
    item_type="armor",
    body_slot="breastplate",
    damage=0,
    defense=1,
    heals=0,
    item_effect=0,
    buy_price=45,
    item_desc=l10n.item.basic_clothes.desc
    )
item_basic_pants = Items(
    item_id=5,
    name=l10n.item.basic_pants.name.one,
    plural=l10n.item.basic_pants.name.many,
    item_type="armor",
    body_slot="pants",
    damage=0,
    defense=1,
    heals=0,
    item_effect=0,
    buy_price=30,
    item_desc=l10n.item.basic_pants.desc
    )
item_basic_shoes = Items(
    item_id=6,
    name=l10n.item.basic_shoes.name.one,
    plural=l10n.item.basic_shoes.name.many,
    item_type="armor",
    body_slot="shoes",
    damage=0,
    defense=0,
    heals=0,
    item_effect=0,
    buy_price=10,
    item_desc=l10n.item.basic_shoes.desc
    )
item_greater_healing_potion = Items(
    item_id=7,
    name=l10n.item.greater_healing_potion.name.one,
    plural=l10n.item.greater_healing_potion.name.many,
    item_type="consumable",
    body_slot="",
    damage=0,
    defense=0,
    heals=35,
    item_effect=0,
    buy_price=55,
    item_desc=l10n.item.greater_healing_potion.desc
    )
item_dumeors_head = Items(
    item_id=8,
    name=l10n.item.dumeors_head.name.one,
    plural=l10n.item.dumeors_head.name.many,
    item_type="quest",
    body_slot="",
    damage=0,
    defense=0,
    heals=0,
    item_effect=0,
    buy_price=0,
    item_desc=l10n.item.dumeors_head.desc
    )
item_goblin_belt = Items(
    item_id=9,
    name=l10n.item.goblin_belt.name.one,
    plural=l10n.item.goblin_belt.name.many,
    item_type="armor",
    body_slot="belt",
    damage=0,
    defense=2,
    heals=0,
    item_effect=0,
    buy_price=120,
    item_desc=l10n.item.goblin_belt.desc
    )
item_venom_vial = Items(
    item_id=10,
    name=l10n.item.venom_vial.name.one,
    plural=l10n.item.venom_vial.name.many,
    item_type="ingredient",
    body_slot="",
    damage=0,
    defense=0,
    heals=0,
    item_effect=0,
    buy_price=50,
    item_desc=l10n.item.venom_vial.desc
    )
item_putrid_perfume = Items(
    item_id=11,
    name=l10n.item.putrid_perfume.name.one,
    plural=l10n.item.putrid_perfume.name.many,
    item_type="consumable",
    body_slot="",
    damage=0,
    defense=0,
    heals=0,
    item_effect=5,
    buy_price=40,
    item_desc=l10n.item.putrid_perfume.desc
    )
item_goblin_boots = Items(
    item_id=12,
    name=l10n.item.goblin_boots.name.one,
    plural=l10n.item.goblin_boots.name.many,
    item_type="armor",
    body_slot="shoes",
    damage=0,
    defense=1,
    heals=0,
    item_effect=0,
    buy_price=80,
    item_desc=l10n.item.goblin_boots.desc
    )
item_goblin_stick = Items(
    item_id=13,
    name=l10n.item.goblin_stick.name.one,
    plural=l10n.item.goblin_stick.name.many,
    item_type="weapon",
    body_slot="",
    damage=3,
    defense=0,
    heals=0,
    item_effect=0,
    buy_price=60,
    item_desc=l10n.item.goblin_stick.desc
    )
item_goblin_beanie = Items(
    item_id=14,
    name=l10n.item.goblin_beanie.name.one,
    plural=l10n.item.goblin_beanie.name.many,
    item_type="armor",
    body_slot="hat",
    damage=3,
    defense=0,
    heals=0,
    item_effect=0,
    buy_price=150,
    item_desc=l10n.item.goblin_beanie.desc
    )
item_test = Items(
    item_id=999,
    name="test",
    plural="",
    item_type="misc",
    body_slot="",
    damage=0,
    defense=0,
    heals=0,
    item_effect=0,
    buy_price=120,
    item_desc="Vive les tests"
    )


# ======================================================================================================================
# =========================== Définit et stocke les informations des attaques spéciales
class SpecialAttack:
    def __init__(
            self,
            sa_id: int,
            name: str,
            attack_type: str,
            percent: float,
            attempt_min: int,
            attempt_max: int
    ):
        self.sa_id = sa_id
        self.name = name
        self.attack_type = attack_type
        self.percent = percent  # Pourcentage de dégâts infligés en plus
        self.attempt_min = attempt_min
        self.attempt_max = attempt_max
        self.attempt = (attempt_min, attempt_max)  # (X, Y) --> X chances min sur Y chances max


attack_claw_strike = SpecialAttack(
    sa_id=0,
    name="Coup de griffe",
    attack_type='ground',
    percent=1.0,
    attempt_min=2,
    attempt_max=5
    )
attack_heavy_strike = SpecialAttack(
    sa_id=1,
    name="Frappe lourde",
    attack_type='ground',
    percent=1.25,
    attempt_min=1,
    attempt_max=1
    )


# ======================================================================================================================
# =========================================================== Définit et stocke les informations des PNJs
class Npcs:
    def __init__(
            self,
            npc_id: int,
            name: str,
            plural: str,
            gender: str,
            npc_type: str,
            rarity: int,
            health: int,
            damage: int,
            defense: int,
            level: int,
            given_exp: int,
            given_gold: int,
            loot: list,
            special_attack: list,
            sells: list
    ):
        self.npc_id = npc_id
        self.name = name
        self.plural = plural
        self.gender = gender  # Masculin = m, Féminin = f, mixte = fm ou custom
        self.npc_type = npc_type
        self.rarity = rarity  # 0 = friendly npc, 1 = common, 2 = uncommon, 3 = rare, 4 = boss
        self.health = health
        self.damage = damage
        self.defense = defense
        self.level = level
        self.given_exp = given_exp
        self.given_gold = given_gold
        self.loot = loot   # [item, quantity, rate] - rate est la valeur maxi de rng()
        self.special_attack = special_attack
        self.sells = sells


npc_slime = Npcs(
    npc_id=0,
    name=l10n.npc.slime.name.one,
    plural=l10n.npc.slime.name.many,
    gender="f",
    npc_type="ground",
    rarity=1,
    health=20,
    damage=7,
    defense=0,
    level=0,
    given_exp=10,
    given_gold=4,
    loot=[[item_healing_potion, 1, 4]],
    special_attack=[],
    sells=[]
    )
npc_bat = Npcs(
    npc_id=1,
    name=l10n.npc.bat.name.one,
    plural=l10n.npc.bat.name.many,
    gender="f",
    npc_type="flying",
    rarity=2,
    health=16,
    damage=9,
    defense=2,
    level=1,
    given_exp=14,
    given_gold=7,
    loot=[[item_healing_potion, 1, 4], [item_venom_vial, 1, 3]],
    special_attack=[],
    sells=[]
    )
npc_goblin = Npcs(
    npc_id=1,
    name=l10n.npc.goblin.name.one,
    plural=l10n.npc.goblin.name.many,
    gender="m",
    npc_type="ground",
    rarity=3,
    health=28,
    damage=12,
    defense=0,
    level=2,
    given_exp=18,
    given_gold=10,
    loot=[[item_healing_potion, 1, 3], [item_goblin_axe, 1, 3], [item_goblin_belt, 1, 4]],
    special_attack=[attack_claw_strike],
    sells=[]
    )
npc_rat = Npcs(
    npc_id=2,
    name=l10n.npc.rat.name.one,
    plural=l10n.npc.rat.name.many,
    gender="m",
    npc_type="ground",
    rarity=1,
    health=14,
    damage=6,
    defense=2,
    level=1,
    given_exp=14,
    given_gold=3,
    loot=[[item_healing_potion, 1, 4]],
    special_attack=[],
    sells=[]
    )
npc_smol_goblin = Npcs(
    npc_id=3,
    name=l10n.npc.smol_goblin.name.one,
    plural=l10n.npc.smol_goblin.name.many,
    gender="m",
    npc_type="ground",
    rarity=1,
    health=12,
    damage=8,
    defense=2,
    level=1,
    given_exp=12,
    given_gold=5,
    loot=[[item_goblin_boots, 1, 4], [item_goblin_stick, 1, 3]],
    special_attack=[],
    sells=[]
    )
npc_hobgoblin = Npcs(
    npc_id=4,
    name=l10n.npc.hobgoblin.name.one,
    plural=l10n.npc.hobgoblin.name.many,
    gender="m",
    npc_type="ground",
    rarity=3,
    health=36,
    damage=12,
    defense=2,
    level=5,
    given_exp=28,
    given_gold=15,
    loot=[[item_greater_healing_potion, 1, 2], [item_goblin_axe, 1, 2], [item_goblin_beanie, 1, 4]],
    special_attack=[],
    sells=[]
    )
npc_dumeors = Npcs(
    npc_id=5,
    name=l10n.npc.dumeors.name.one,
    plural=l10n.npc.dumeors.name.many,
    gender="de",
    npc_type="ground",
    rarity=4,
    health=100,
    damage=16,
    defense=2,
    level=5,
    given_exp=100,
    given_gold=40,
    loot=[[item_greater_healing_potion, 2, 1], [item_dumeors_head, 1, 1]],
    special_attack=[],
    sells=[]
    )
npc_merchant = Npcs(
    npc_id=6,
    name=l10n.npc.merchant.name.one,
    plural=l10n.npc.merchant.name.many,
    gender="m",
    npc_type="ground",
    rarity=0,
    health=120,
    damage=0,
    defense=0,
    level=5,
    given_exp=0,
    given_gold=0,
    loot=[],
    special_attack=[],
    sells=[item_healing_potion, item_putrid_perfume]
    )
npc_trappist = Npcs(
    npc_id=7,
    name=l10n.npc.trappist.name.one,
    plural=l10n.npc.trappist.name.many,
    gender="m",
    npc_type="ground",
    rarity=0,
    health=150,
    damage=0,
    defense=0,
    level=5,
    given_exp=0,
    given_gold=0,
    loot=[],
    special_attack=[],
    sells=[]
    )
npc_test = Npcs(
    npc_id=8,
    name="TEST",
    plural="",
    gender="m",
    npc_type="ground",
    rarity=1,
    health=1,
    damage=1,
    defense=0,
    level=0,
    given_exp=3,
    given_gold=1,
    loot=[[item_greater_healing_potion, 1, 3], [item_healing_potion, 1, 4], [item_goblin_axe, 1, 2], [item_goblin_belt, 1, 2], [item_dumeors_head, 1, 1]],
    special_attack=[],
    sells=[]
    )


# ======================================================================================================================
# =========================== Définit et stocke les informations des quêtes
class Event:
    def __init__(
            self,
            event_id: int,
            event_desc: str,
            event_type: int,
            damaging: int
    ):
        self.event_id = event_id
        self.event_desc = event_desc
        self.event_type = event_type  # Positif = 1, Neutral = 0, Negative = -1
        self.damaging = damaging  # Dégâts infligés par l'event


# Positives
event_enigmatic_guy = Event(
    event_id=0,
    event_desc="Quizz du magicien pour anneau",
    event_type=1,
    damaging=0
    )

# Neutres
event_biome_neutral = Event(
    event_id=1,
    event_desc="Phrases neutres d'observation",
    event_type=0,
    damaging=0
    )

# Négatives
event_bear_attack = Event(
    event_id=2,
    event_desc="Attaque d'ours",
    event_type=-1,
    damaging=20
    )


# ======================================================================================================================
# =========================== Définit et stocke les informations des environnements
class Biome:
    def __init__(
            self,
            biome_id: int,
            name: str,
            mobs: list,
            turn: int,
            events: list
    ):
        self.biome_id = biome_id
        self.name = name
        self.mobs = mobs
        self.turn = turn
        self.events = events


biome_village = Biome(
    biome_id=0,
    name=l10n.biome.base_village.name,
    mobs=[],
    turn=-1,
    events=[event_biome_neutral]
    )
biome_forest = Biome(
    biome_id=1,
    name=l10n.biome.forest.name,
    mobs=[npc_slime, npc_bat, npc_goblin],
    turn=0,
    events=[event_enigmatic_guy, event_biome_neutral, event_bear_attack]
    )
biome_caves = Biome(
    biome_id=2,
    name=l10n.biome.caves.name,
    mobs=[npc_rat, npc_smol_goblin, npc_bat, npc_hobgoblin],
    turn=10,
    events=[event_biome_neutral]
    )
biome_dumeors_den = Biome(
    biome_id=3,
    name=l10n.biome.dumeors_den.name,
    mobs=[npc_dumeors],
    turn=20,
    events=[event_biome_neutral]
    )

# Définit une liste de tous les biomes
biome_list = [biome_village, biome_forest, biome_caves, biome_dumeors_den]

# Définit un dictionnaire avec les biomes par ordre d'apparence
biome_dict = dict(sorted({biome.turn: biome for biome in biome_list}.items(), reverse=True))


# ======================================================================================================================
# =========================== Définit et stocke les informations des quêtes
class Quest:
    def __init__(
            self,
            quest_id: int,
            name: str,
            quest_type: str,
            quest_desc: str,
            progress: str,
            prog_counter: int,
            lvl_mini: int,
            exp: int,
            gold: int
    ):
        self.quest_id = quest_id
        self.name = name
        self.quest_type = quest_type
        self.quest_desc = quest_desc
        self.progress = progress  # Équivalent au nombre restant à accomplir pour terminer la quête
        self.prog_counter = prog_counter  # Équivalent au nombre total à accomplir (nbr de monstres à tuer, d'objets à récup...)
        self.lvl_mini = lvl_mini  # Niveau conseillé pour la quête
        self.exp = exp
        self.gold = gold


quest_return_merchant = "Retourner voir le Marchand"
quest_return_trappist = "Retourner voir le Trappeur"

''' Type de quête
Chasse aux monstres - Tuer X ennemis
Trancheur de tête - Tuer tel boss
Récolte d'objets - Ramener X objets
'''

quest_slime_overcrowding_1 = Quest(
        quest_id=0,
        name="Surpopulation de gelées",
        quest_type="Chasse aux monstres",
        quest_desc="Tuer 5 gelées et faire son rapport au donneur de quêtes",
        progress="Plus que {} monstre(s) à tuer",
        prog_counter=5,
        lvl_mini=0,
        exp=65,
        gold=15
        )

quest_bat_venom = Quest(
    quest_id=1,
    name="Du poison pour les poissons",
    quest_type="Récolte d'objets",
    quest_desc='Ramener 4 fioles de venin de chauve-souris au donneur de quêtes',
    progress="Plus que {} objet(s) à récupérer",
    prog_counter=4,
    lvl_mini=1,
    exp=65,
    gold=item_venom_vial.sell_price * 4
    )

quest_dumeors_head = Quest(
    quest_id=2,
    name="Dumeors l'Acéré",
    quest_type="Trancheur de tête",
    quest_desc='Ramener la tête de la bête au marchand',
    progress="Tuer {}",
    prog_counter=1,
    lvl_mini=3,
    exp=240,
    gold=item_dumeors_head.sell_price
    )
