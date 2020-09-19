from Creatures.creature import Creature


class Zombie(Creature):
    def skill_increase_damage(self):
        self.strength += 1
        print(f"Zombies damage increase {self.strength}")