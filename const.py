import colorama
import matplotlib.pyplot as plt


def my_prog(first_el, power, count):
    ele_before = first_el
    arr = list()
    arr.append(ele_before)
    for i in range(count + 1):
        arr.append(round(ele_before * power, 2))
        ele_before = ele_before * power
    return arr


class Style:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    CVIOLETBG2 = '\33[105m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    CVIOLET = '\33[35m'


lvl_pwr = {1: 105, 2: 169, 3: 252, 4: 350, 5: 461}
colorama.init()

# temp = Zombie(lvl_pwr[1], 1.5)

# t = Creature(lvl_pwr[1], 1.5)
# print(temp.health, temp.damage)
#print(t.health, t.damage)

# out_red("Вывод красным цветом")
# out_yellow("Текст жёлтого цвета")
# out_blue("Синий текст")

d, f, n = 10, 1, 5  # degree, first element, number
a = [i for i in range(12)]
arr_exp_for_next_lvl = (my_prog(1000, 1.4, 10))

# print(my_prog(10, 1.7, 1))
# print(my_prog(10, 3.4, 0.02))
