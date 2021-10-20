from tkinter import *
from tkinter.ttk import *
from random import randrange as rnd, choice
import time

root = Tk()
root.geometry('800x600')

canv = Canvas(root,bg='white')
canv.pack(fill=BOTH,expand=1)

colors = ['red','orange','yellow','green','blue']
moves = [0, 10, -10]
moves = [0, 10, -10]
ovals = []

points = 0
cnt = 0

canv.create_rectangle(2, 2, 800, 600)
after_obj = None

def new_ball():
    global cnt
    global after_obj

    to_x = choice(moves)
    to_y = choice(moves)
    x = rnd(100,700)
    y = rnd(100,500)
    r = rnd(30,50)
    ov = canv.create_oval(x-r,y-r,x+r,y+r,fill = choice(colors), width=0)

    ovals.append([cnt, ov, x, y, r, to_x, to_y])
    cnt += 1

    root.after(rnd(2000, 3500), new_ball)
    if(after_obj is None):
        movement()

def movement():
    global ovals
    global after_obj

    for ind, ov, x, y, r, to_x, to_y in ovals:
        n_x = to_x
        n_y = to_y
        if x + r + to_x > 800:
            n_x = 800 - x - r
            x = 800 - r
            to_x = -to_x
        elif to_x < 0 and x - r + to_x < 2:
            n_x = 2 - x + r
            x = 2 + r
            to_x = -to_x
        else:
            x += to_x

        if y + r + to_y > 600:
            n_y = 600 - y - r
            y = 600 - r
            to_y = -to_y
        elif to_y < 0 and y  - r + to_y < 2:
            n_y = 2 - y + r
            y = 2 + r
            to_y = -to_y
        else:
            y += to_y
        
        ovals[ind][2] = x
        ovals[ind][3] = y
        ovals[ind][5] = to_x
        ovals[ind][6] = to_y
        
        canv.move(ov, n_x, n_y)
    
    after_obj = root.after(100, movement)

def rect_del():
    global rect
    canv.delete(rect)

def change_color():
    global rect
    canv.itemconfig(rect, fill=choice(colors))
    root.after(300, change_color)

def new_rectangle():
    global rect
    global r_x, r_y, a

    to_x = choice(moves)
    to_y = choice(moves)
    r_x = rnd(100,700)
    r_y = rnd(100,500)
    a = 10
    rect = canv.create_rectangle(r_x-a, r_y-a, r_x+a, r_y+a, fill = choice(colors))
    root.after(300, change_color)
    root.after(3000, rect_del)
    root.after(rnd(5000, 10000), new_rectangle)

def click(event):
    now_x, now_y = event.x, event.y
    global points
    global ovals

    if now_x <= r_x + a and now_x >= r_x - a:
        if now_y <= r_y + a and now_y >= r_y - a:
            points += 2
            print("Квадрат! Хороший результат! Количество очков: {}".format(points))
            canv.delete(rect)
            root.after(rnd(5000, 10000), new_rectangle)
            return

    for ind, ov, x, y, r, to_x, to_y in ovals:
        if abs(x - now_x) <= r and abs(y - now_y) <= r:
            points += 1
            ovals[ind][2] = -100000
            ovals[ind][3] = -100000
            print("Победа! Ты лучший! Количество очков: {}".format(points))
            canv.delete(ov)
        else:
            print("Поражение, какая досада!")

new_ball()
root.after(rnd(5000, 10000), new_rectangle)
canv.bind('<Button-1>', click)
mainloop()

print("Ваш счёт: {}".format(points))