from village import *
from const import *

h = Player(1, "Hero", 0, 0, 1)
show_greeting(h)
while 1:
    choose = input(Style.BLACK + "What do you want?\n"
                                "1) Find adventures ⚔\n"
                                "2) Village 🏠\n"
                                "3) Hero stat 🦾\n"
                                "4) Inventory 💼\n")
    if choose == "1":
        adventure(h)
    elif choose == "2":
        village_choose = input("What do you want?\n1) Shop\n2) Sleep\n")
        if village_choose == "1":
            shop(h)
        elif village_choose == "2":
            sleep(h)
    elif choose == "3":
        h.information()
    elif choose == "4":
        show_inventory(h)
    else:
        print(Style.RED + "Wrong input")
        choose
