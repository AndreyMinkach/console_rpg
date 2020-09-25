from Creatures.creature import Creature
from Items.Outfits.outfit import Outfit
from Items.Weapons.weapon import Weapon


class Player(Creature):
    def __init__(self):
        super().__init__()

    def skill_heal(self):
        self.health += self.strength * 0.75
        print(f"Heroes health increase {self.health}")
