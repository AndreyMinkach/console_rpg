from willage import *
from const import *

h = Hero(1, "Hero", 0, 0, 1)
welcome(h)
while 1:
    choose = input(Style.BLACK + "What do you want?\n"
                                "1) Find adventures ⚔\n"
                                "2) Willage 🏠\n"
                                "3) Hero stat 🦾\n"
                                "4) Inventory 💼\n")
    if choose == "1":
        adventure(h)
    elif choose == "2":
        willage_choose = input("What do you want?\n1) Shop\n2) Sleap\n")
        if willage_choose == "1":
            shop(h)
        elif willage_choose == "2":
            sleap(h)
    elif choose == "3":
        h.information()
    elif choose == "4":
        inventory(h)
    else:
        print(Style.RED + "Wrong input")
        choose
