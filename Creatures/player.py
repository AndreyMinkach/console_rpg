from Creatures.creature import Creature
from Items.Outfits.outfit import Outfit
from Items.Weapons.weapon import Weapon


class Player(Creature):
    hero_weapon_inventory = []
    hero_armor_inventory = []

    def add_to_inventory(self, item):
        if type(item) == Weapon:
            self.hero_weapon_inventory.append(item)
        elif type(item) == Outfit:
            self.hero_armor_inventory.append(item)

    def skill_heal(self):
        self.health += self.strength * 0.75
        print(f"Heroes health increase {self.health}")
