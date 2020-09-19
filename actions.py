from Creatures.creature import *
from Creatures.player import Player
from Creatures.zombie import Zombie


def adventure(h: Player):
    choose = input("Choose difficulty\n"
                   "1) Easy\n"
                   "2) Medium\n"
                   "3) Hard\n")
    if choose == '1':
        battle(Zombie(1, "Zombie", 11, 100, 0.9), h)
    if choose == '2':
        battle(Zombie(1, "Creeper", 1, 150, 0.9), h)
    if choose == '3':
        battle(Zombie(1, "Enderman", 1, 200, 0.9), h)


def battle(enemy: Zombie, hero: Player):
    print(f"Your opponent is {Style.MAGENTA + Style.UNDERLINE + enemy.name}" + Style.RESET +
          f" with {Style.GREEN + str(enemy.health)} hp, "
          f"{Style.RED + str(enemy.total_damage)} dmg" + Style.RESET)
    while enemy.health > 0 and hero.health > 0:
        choose = input(Style.BLACK + "What to do?\n"
                                     "1) Attach\n"
                                     "2) Run\n"
                                     "3) Use skill\n"
                                     "4) Watch info\n")
        if choose == "1":
            hero.health -= round(enemy.total_damage * (1 - (hero.Armor.durability * 0.1)))
            enemy.health -= round(hero.total_damage * (1 - (enemy.Armor.durability * 0.1)))
            if hero.health <= 0:
                print("Game Over")
                break
            elif enemy.health <= 0:
                hero.gold += enemy.gold
                hero.experience += 100 * (10 + (enemy.lvl - hero.lvl)) / (10 + hero.lvl)
                hero.check_lvl()

        elif choose == "2":
            print("You run away, chicken :D")
            break

        elif choose == "3":
            enemy.skill_increase_damage()
            hero.skill_heal()

        elif choose == "4":
            hero.information()

        else:
            print(Style.RED + "Wrong input")
            choose
        enemy.short_info()
        hero.short_info()
    print(f"End of the battle")


def show_inventory(hero: Player):
    c = input("What to do?\n1) Use weapon\n2) Weapon list\n3) Use armor\n4) Armor list \n")
    if c == '1':
        for i in range(len(hero.hero_weapon_inventory)):
            print(f"{i + 1}) ", hero.hero_weapon_inventory[i].name, hero.hero_weapon_inventory[i].damage)
        weapon_number = int(input("Choose number of weapon\n"))
        hero.Weapon = hero.hero_weapon_inventory[weapon_number-1]
        hero.total_damage = hero.strength + hero.Weapon.damage
    elif c == '2':
        for i in range(len(hero.hero_weapon_inventory)):
            print(f"{i + 1}) ", hero.hero_weapon_inventory[i].name, hero.hero_weapon_inventory[i].damage)
    elif c == '3':
        for i in range(len(hero.hero_armor_inventory)):
            print(f"{i + 1}) ", hero.hero_armor_inventory[i].name, hero.hero_armor_inventory[i].durability)
        armor_number = int(input("Choose number of armor\n"))
        hero.Armor = hero.hero_armor_inventory[armor_number-1]
        hero.total_hp = hero.health
    elif c == '4':
        for i in range(len(hero.hero_armor_inventory)):
            print(f"{i + 1}) ", hero.hero_armor_inventory[i].name, hero.hero_armor_inventory[i].durability)


def show_greeting(hero: Player):
    print(Style.BLACK + f"Hello Hero, welcome in our RPG world\nHere is your stick and Shkura\nGood luck ☘")
    hero.name = input("Enter your name\n")
    hero.add_to_inventory(Weapon(1.5, "Stick"))
    hero.add_to_inventory(Outfit(1.5, "Shkura"))
