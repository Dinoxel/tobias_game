from static_functions import *
from math import ceil

data_biomes = open_json("biomes")
data_events = open_json("events")
data_items = open_json("items")
data_monsters = open_json("monsters")
data_npcs = open_json("npcs")
data_quests = open_json("quests")
data_special_attacks = open_json("special_attacks")

l10n = Localization()


# Character
class Character:
    def __init__(
        self,
        name="dummy",
        health=20,
        damage=1,
        defense=0,
        level=0,
        gold=0,
        experience=0,
        starting_items=tuple()
    ):
        self.name = name
        self.health = health
        self.damage = damage
        self.defense = defense
        self.level = level
        self.gold = gold
        self.experience = experience
        self.starting_items = starting_items

        # Valeurs par défaut
        self.inventory = dict()
        self.items_damage = 0
        self.items_defense = 0

        self.max_health = self.health
        self.total_damage = self.damage + self.items_damage
        self.total_defense = self.defense + self.items_defense


    # =============================================== Affichage d'informations =========================================
    # Inventaire
    def display_inventory(self, *item_args: str, intro=True, show_price=False):
        l10n.set_main_key("inventory")

        show_all = True if not item_args and self.inventory else False

        if intro:
            print(custom_text(l10n.get("intro") if self.inventory else l10n.get("no_items"), "blue"))

        # DÉFINIT LES CONSOMMABLES
        if "consumable" in self.inventory.keys() and ("consumable" in item_args or show_all):
            print(custom_text(l10n.get("consumable_intro"), "yellow"))

            for item, qty in self.inventory["consumable"].items():
                print(custom_text(f'x{qty} {item.name}', "bold"), end=' ')

                if show_price:
                    print(custom_text(f"[{item.sell_price} or par unité]", "red"), end=' ')

                if item.heals:  # Si objet de soin
                    print(custom_text(l10n.get("consumable_desc_heal").format(item.heals), "green"))
                else:
                    print(custom_text(l10n.get("consumable_desc_oust").format(item.item_effect), "green"))

        # DÉFINIT L'ARMURE
        if "armor" in self.inventory.keys() and ("armor" in item_args or show_all):
            print(custom_text(l10n.get("armor_intro").format(self.get_total_defense()), "yellow"))

            for item, qty in self.inventory["armor"].items():
                print(custom_text(f"x{qty} {item.name}", "bold"), end=' ')

                if show_price:
                    print(custom_text(f"[{item.sell_price} or par unité]", "red"), end=' ')

                print(custom_text(l10n.get("armor_desc").format(item.defense), "green"))

        # DÉFINIT LES ARMES
        if "weapon" in self.inventory.keys() and ("weapon" in item_args or show_all):
            print(custom_text(l10n.get("weapon_intro").format(self.get_best_weapon().name), "yellow", "bold"))

            for item, qty in self.inventory["weapon"].items():
                print(custom_text(f"x{qty} {item.name}", "bold"), end=' ')

                if show_price:
                    print(custom_text(f"[{item.sell_price} or par unité]", "red"), end=' ')

                print(custom_text(l10n.get("weapon_desc").format(item.damage), "green"))

        # DÉFINIT LES INGRÉDIENTS
        if "ingredient" in self.inventory.keys() and ("ingredient" in item_args or show_all):
            print(custom_text(l10n.get("ingredient_intro"), "yellow"))

            for item, qty in self.inventory["ingredient"].items():
                print(custom_text(f'x{qty} {item.name}', "bold"), end='')

                print(custom_text(f" [{item.sell_price} or par unité]", "red") if show_price else '')

        # DÉFINIT LES OBJETS DE QUÊTE
        if "quest" in self.inventory.keys() and ("quest" in item_args or show_all):
            print(custom_text(l10n.get("quest_intro"), "yellow"))

            for item, qty in self.inventory["quest"].items():
                print(custom_text(f'x{qty} {item.name}', "bold"))

        l10n.reset_main_key()

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
        defense_item_types = list()
        # Si deux objets d'armure ont le même type, ne prendre en compte que le plus haut et les deux anneaux les plus hautes

        if 'armor' in self.inventory:
            total_defense = sum(armor_item.defense for armor_item in self.inventory["armor"].keys())

        return total_defense

    # =============================================== Commandes de gestion =============================================
    # Ajoute un objet à l'inventaire
    def add_to_inv(self, quantity: int, item_id: object):
        item = Item(**data_items[item_id])

        if item.item_type not in self.inventory.keys():
            self.inventory[item.item_type] = dict()

        type_inventory = self.inventory[item.item_type]

        if item not in type_inventory.keys():
            type_inventory[item] = quantity
        else:
            type_inventory[item] += quantity

        # Redéfinit les dégâts d'objet sur l'arme la plus puissante et les dégâts totaux
        self.items_damage = 0 if self.get_best_weapon() is None else self.get_best_weapon().damage
        self.total_damage = self.damage + self.items_damage

        # Redéfinit la défense des objets et la défense totale
        self.items_defense = self.get_total_defense()
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


class Player(Character):
    def __init__(self):
        super().__init__(
            name="Tobias",
            health=80,
            damage=3,
            defense=0,
            gold=20,
            starting_items=(
                (2, "healingPotion"),
                (1, "putridPerfume"),
                (1, "simpleSword"),
                (1, "basicClothes"),
                (1, "basicPants"),
                (1, "basicShoes")
            )
        )
        self.exp_to_levelup = 30

        # Tour où se trouve le joueur
        self.current_turn = 0

        # Effets (buffs & débuffs)
        self.effects = dict()
        self.repeal_turn = 0

        # Compteur de meurtres
        self.kill_counter = dict()

        for qty, item in self.starting_items:
            self.add_to_inv(qty, item)

    # =============================================== Affichage d'informations =========================================
    # Statistiques
    def display_stats(self):
        print(custom_text(
            f"""Santé : {self.health}/{self.max_health}\t\t\tNiveau : {self.level}\t EXP actuelle : {self.experience}
Dégâts : {self.total_damage} ({self.damage} +{self.items_damage})\t\tEXP avant prochain niveau : {self.get_next_level_exp()}
Défense : {self.total_defense} ({self.defense} +{self.items_defense})\t\tBourse : {self.gold} or""", "yellow"))

        if self.effects:
            print('Effets en cours :')
            for effect, desc in self.effects.items():
                print(effect, f"- {desc.format(self.repeal_turn)}")

    # =============================================== Renvoi de valeurs ================================================
    # Expérience restante pour monter d'un niveau
    def get_next_level_exp(self):
        return self.exp_to_levelup - self.experience

    # =============================================== Commandes d'action ===============================================
    # Utilise un objet
    def use_item(self, item):
        if item.heals and self.health != self.max_health:
            self.del_from_inv(item, 1)

            if self.health + item.heals > self.max_health:
                self.health = self.max_health
            else:
                self.health += item.heals
        else:
            print("Nothing happened, no item was consumed.")

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


class Monster(Character):
    def __init__(
            self,
            plural: str,
            gender: str,
            monster_type: str,
            experience: int,
            rarity=1,
            is_boss=False,
            loot=tuple(),
            special_attack=tuple(),
            **kwargs
    ):
        super().__init__(**kwargs)
        self.plural = plural
        self.gender = gender
        self.monster_type = monster_type
        self.rarity = rarity
        self.experience = experience
        self.is_boss = is_boss
        self.loot = loot
        self.special_attack = special_attack


class FriendlyNpc(Character):
    def __init__(
            self,
            npc_type: str,
            plural: str,
            gender: str,
            sells=tuple(),
            **kwargs
    ):
        super().__init__(**kwargs)
        self.npc_type = npc_type
        self.plural = plural
        self.gender = gender
        self.sells = sells


# Quest
class Quest:
    def __init__(
            self,
            name: str,
            quest_type: str,
            quest_desc: str,
            progress: str,
            prog_counter: int,
            lvl_mini: int,
            experience: int,
            gold: tuple
    ):
        self.name = name
        self.quest_type = quest_type
        self.quest_desc = quest_desc
        self.progress = progress  # Équivalent au nombre restant à accomplir pour terminer la quête
        self.prog_counter = prog_counter  # Équivalent au nombre total à accomplir (nbr de monstres à tuer, d'objets à récup...)
        self.lvl_mini = lvl_mini  # Niveau conseillé pour la quête
        self.experience = experience
        self.gold = gold


# Biome
class Biome:
    def __init__(
            self,
            name: str,
            turn: int,
            events: tuple,
            mobs=tuple()
    ):
        self.name = name
        self.mobs = mobs
        self.turn = turn
        self.events = events


# Event
class Event:
    def __init__(
            self,
            desc="dummy",
            event_type="neutral",
            damaging=0
    ):
        self.desc = desc
        self.event_type = event_type  # positive, neutral, negative
        self.damaging = damaging  # Dégâts infligés par l'évent


# Item
class Item:
    def __init__(
            self,
            name="dummy",
            plural="dummies",
            item_type="",
            body_slot="",
            damage=0,
            defense=0,
            health=0,
            heals=0,
            item_effect=0,
            buy_price=0,
            item_desc="dummy"
    ):

        self.name = name
        self.plural = plural

        self.item_type = item_type

        self.body_slot = body_slot

        self.health = health
        self.damage = damage
        self.defense = defense

        self.heals = heals
        self.item_effect = item_effect

        self.buy_price = buy_price
        self.sell_price = ceil(self.buy_price / 5) if self.buy_price else 0

        self.item_desc = item_desc


# Special Attacks
class SpecialAttack:
    def __init__(
            self,
            name: str,
            attack_type: str,
            percent: float,
            attempt_min: int,
            attempt_max: int
    ):
        self.name = name
        self.attack_type = attack_type
        self.percent = percent  # Pourcentage de dégâts infligés en plus
        self.attempt_min = attempt_min
        self.attempt_max = attempt_max
        self.attempt = (attempt_min, attempt_max)  # (X, Y) --> X chances min sur Y chances max
