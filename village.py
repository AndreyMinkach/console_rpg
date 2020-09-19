from actions import *


def sleep(player: Player):
    agree = input("Sleep heal you to max health\nCoast for sleep - 1 gold\n1) +\n2) -\n")
    if player.gold < 1:
        print("Not enough money")
    elif agree == "1" or "+":
        player.gold -= 1
        player.health = player.total_health
        player.short_info()
    elif agree == "2" or "-":
        return 1
    else:
        print(Style.RED + "Wrong input")


def shop(hero: Player):
    what_to_buy = int(input("What do you want to buy\n"
                            "1) Knife - 10 gold, 3 - damage\n"
                            "2) Sword - 20 gold 6 - damage\n"
                            "3) Battle Axe - 50 gold - 10 damage\n"))

    if what_to_buy == 1 and hero.gold >= 10:
        hero.add_to_inventory(Weapon(3, "Knife"))
        print("Congrat, you buy the Knife :)")
    elif what_to_buy == 2 and hero.gold >= 20:
        hero.add_to_inventory(Weapon(6, "Sword"))
        print("Congrat, you buy the Sword :)")
    elif what_to_buy == 1 and hero.gold >= 50:
        hero.add_to_inventory(Weapon(10, "Battle Axe"))
        print("Congrat, you buy the Battle Axe :)")
    else:
        print("Don not have enough money")

