import math
from items import *
from const import *


class Creature:
    def __init__(self, hp_coef=1, name="No name", gold=0, experience=0, creature_level_difficulty=1):
        self.experience = experience
        self.lvl = 1
        self.power = lvl_pwr[self.lvl]
        hp_average = round(math.sqrt(self.power) * math.sqrt(6))
        self.health = round(hp_average * hp_coef * creature_level_difficulty)
        dmg_average = hp_average / 6
        dmg_coef = 1 / hp_coef
        self.strength = round(dmg_average * dmg_coef * creature_level_difficulty)
        self.gold = gold
        self.total_health = self.health
        self.name = name
        self.total_damage = self.strength + Weapon().damage
        self.Weapon = Weapon()
        self.Armor = Armor()

    def check_lvl(self):
        if self.experience >= arr_exp_for_next_lvl[self.lvl]:
            self.experience = 0
            self.lvl += 1

    def get_power(self):
        return self.lvl * 10 * ((self.strength + self.Weapon.damage) * (self.health + self.Armor.durability))

    def get_health(self):
        return self.health

    def set_health(self, health):
        self.health = health

    def attack(self):
        print(f"{self.name} give damage {self.total_damage}")

    def check_health(self):
        if self.health <= 0:
            print(f"{self.name} dead! ☠")
            return False
        else:
            print(f"{self.name} health {self.health}")

    def short_info(self):
        print(f"{Style.YELLOW + self.name}:  "
              f"{Style.GREEN + ('health ' + str(self.health))}, "
              f"{Style.RED + ('damage ' + str(self.total_damage))}" +
              Style.RESET)

    def information(self):
        print(Style.YELLOW + "Name:", self.name, Style.GREEN +
              "\nHealth:", self.health, f"(max hp: {self.total_health})" + Style.RED +
              "\nDamage:", self.total_damage, f"(weapon damage: {self.Weapon.damage})", Style.CYAN +
              "\nWeapon:", self.Weapon.name, ", damage ", self.Weapon.damage,
              "\nArmor:", self.Armor.name, ", durability ", self.Armor.durability, Style.YELLOW + Style.UNDERLINE +
              "\nGold:", self.gold,
              "\nLevel:", self.lvl,
              f"(exp: {round(self.experience/arr_exp_for_next_lvl[self.lvl] * 100)}%)" + Style.RESET)


class Hero(Creature):
    hero_weapon_inventory = []
    hero_armor_inventory = []

    def add_to_inventory(self, item):
        if type(item) == Weapon:
            self.hero_weapon_inventory.append(item)
        elif type(item) == Armor:
            self.hero_armor_inventory.append(item)

    def skill_heal(self):
        self.health += self.strength * 0.75
        print(f"Heroes health encrease {self.health}")


class Zombie(Creature):
    def skill_increase_damage(self):
        self.strength += 1
        print(f"Zombies damage encrease {self.strength}")
