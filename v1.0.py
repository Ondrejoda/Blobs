from turtle import *
from random import randint as random
from random import random as rfloat
from matplotlib import pyplot as plt
from time import sleep

global colors

colors = ["purple", "blue", "green", "yellow", "orange", "red"]

gens = int(input("generations: ")) + 3
food_amount = int(input("food amount: "))
blob_amount = int(input("blob amount: "))
global speed
speed = float(input("blob speed: "))
global b_energy
b_energy = int(input("blob energy: "))
global f_energy
f_energy = int(input("food energy: "))


def rf():
    return rfloat() - rfloat()


s = Screen()

delay(0)

txt = Turtle()
txt.ht()


def show_text(toShow):
    txt.clear()
    txt.penup()
    x = w - 20
    y = h - 20
    txt.setpos(x, y)
    txt.write(str(toShow), align="right", font=("Airal", 10))


sleep(3)

w = window_width() / 2
h = window_height() / 2

w = int(w)
h = int(h)


class Blob:
    def __init__(self, dna):
        self.dna = dna
        self.blob = Turtle()
        self.speed = speed + dna[0]
        self.size = 1 + dna[1]
        self.blob.shape("circle")
        self.blob.up()
        self.blob.speed("fastest")
        self.energy = 0
        self.eaten_food = int()

    def reset(self, w, h):
        self.eaten_food = 0
        self.energy = b_energy
        self.blob.turtlesize(self.dna[1])
        self.color()
        x = random(-w + 20, w - 20)
        y = random(-h + 20, h - 20)
        randint = random(1, 4)
        if randint == 1:
            self.blob.goto(x, -h)
        elif randint == 2:
            self.blob.goto(-w, y)
        elif randint == 3:
            self.blob.goto(w, y)
        elif randint == 4:
            self.blob.goto(x, h)

    def delete(self):
        self.blob.ht()

    def color(self):
        val = b_energy / len(colors)
        if val > 0:
            colval = self.energy / val
            if colval > 5:
                self.blob.color(colors[5])
            if colval < 5 and colval > 4:
                self.blob.color(colors[4])
            if colval < 4 and colval > 3:
                self.blob.color(colors[3])
            if colval < 3 and colval > 2:
                self.blob.color(colors[2])
            if colval < 2 and colval > 1:
                self.blob.color(colors[1])
            if colval < 1 and colval > 0:
                self.blob.color(colors[1])
            if colval < 1:
                self.blob.color(colors[0])

    def go_to_closest_food(self, f_list):
        tmp = 100000
        food = None
        for i in range(len(f_list)):
            if self.blob.distance(f_list[i]) < tmp:
                tmp = self.blob.distance(f_list[i])
                food = f_list[i]
        self.blob.setheading(self.blob.towards(food))
        if self.energy > 0:
            self.blob.forward(self.speed)
            self.energy -= 1 + self.dna[0]
            eng = False
        else:
            eng = True
        self.color()
        if self.blob.distance(food) < 15 * self.dna[1]:
            food.ht()
            self.eaten_food += 1
            self.energy += f_energy * self.dna[1]
            f_list.remove(food)
        return f_list, eng

    def next(self):
        return self.eaten_food


def make_food(w, h):
    food = Turtle()
    food.up()
    food.turtlesize(0.5)
    food.shape("circle")
    food.color("green")
    food.speed("fastest")
    x = random(-w + 20, w - 20)
    y = random(-h + 20, h - 20)
    food.goto(x, y)
    return food


def clean_f_list(f_list):
    for i in f_list:
        i.ht()
        f_list.remove(i)
    return f_list


f_list = []
b_list = []

dna_data = []
dna_tmp = []

b_data_list = []
f_data_list = []

for i in range(blob_amount):
    b_list.append(Blob([0, 1]))
    dna_data.append([0, 1])

for i in range(gens):
    # generation printout

    if i > 3:
        show_text("Generation {}: {}".format(i - 3, len(b_list)))
    else:
        show_text("Preperation Generation {}: {}".format(i, len(b_list)))

    for i in b_list:
        i.reset(w, h)
    for i in range(food_amount):
        f_list.append(make_food(w, h))

    # while there is food
    while len(f_list) > 0:
        for i in b_list:
            if len(f_list) == 0:
                break
            f_list, eng = i.go_to_closest_food(f_list)
        if eng:
            f_list = clean_f_list(f_list)
            break

    # next gen setup
    for i in b_list:
        res = i.next()
        if res == 0:
            i.delete()
            dna_data.remove(i.dna)
            b_list.remove(i)
        elif res > 1:
            for _ in range(res - 1):
                randna = [i.dna[0] + rf(), i.dna[1] + rf()]
                b_list.append(Blob(randna))
                dna_data.append(randna)
    dna_tmp = []
    eng = False
    # b data managment
    b_data_list.append(len(b_list))

    # if all py_algs are dead, break
    if len(b_list) == 0:
        break

print(len(dna_data))

plt.plot(dna_data)

plt.title("Blob Simulation Results:")

plt.legend(["speed", "size"])

plt.show()
