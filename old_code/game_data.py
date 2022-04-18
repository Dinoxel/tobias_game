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


