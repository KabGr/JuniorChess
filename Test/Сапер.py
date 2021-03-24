from random import randint as rd
from time import sleep as sl
from tkinter import *

def setting():
    global h, w, b
    window.geometry('200x200')
    Label(window, bg='white').place(x=0, y=0, width=200, height=200)
    Label(window, text='Сапёр', bg='white', font=10).place(x=70, y=20, width=60, height=20)
    Label(window, text='Высота:', bg='white').place(x=6, y=55, width=60, height=20)
    Label(window, text='Ширина:', bg='white').place(x=3, y=80, width=60, height=20)
    Label(window, text=' Бомбы:', bg='white').place(x=5, y=105, width=60, height=20)
    h = Entry(bd=2)
    h.place(x=60, y=55, width=80, height=20)
    w = Entry(bd=2)
    w.place(x=60, y=80, width=80, height=20)
    b = Entry(bd=2)
    b.place(x=60, y=105, width=80, height=20)
    Button(text='Confirm', bd=2, command=st).place(x=60, y=140, width=80, height=20)

def win_check():
    if disabled == h * w - b:
        Label(window, text='YOU WIN!').place(x=0, y=-30, width=w * 20, height=h * 20 + 30)
        Label(window, text='Congratulation').place(x=w * 10 - 40, y=h * 10-10, width=80, height=20)
        Button(text='Restart', bg='light gray', command=lambda: setting()).place(x=w * 10 - 40, y=h * 10 + 10, width=80, height=20)
    return disabled < h * w - b

def zero_click(x, y):
    global disabled
    if not field[x][y]:
        Label(window).place(x=x * 20, y=y * 20, width=20, height=20)
        field[x][y] = 'hl'
        disabled += 1
        zero_click_check(x, y)
    elif field[x][y] != 'hl':
        Label(window, text=field[x][y]).place(x=x * 20, y=y * 20, width=20, height=20)
        disabled += 1
        field[x][y] = 'hl'
    win_check()

def zero_click_check(x, y):
    if x > 0 and y > 0 and field[x - 1][y - 1] != 'hl':
        zero_click(x - 1, y - 1)
    if x > 0 and field[x - 1][y] != 'hl':
        zero_click(x - 1, y)
    if x > 0 and y < h - 1 and field[x - 1][y + 1] != 'hl':
        zero_click(x - 1, y + 1)
    if y > 0 and field[x][y - 1] != 'hl':
        zero_click(x, y - 1)
    if y < h - 1 and field[x][y + 1] != 'hl':
        zero_click(x, y + 1)
    if x < w - 1 and y > 0 and field[x + 1][y - 1] != 'hl':
        zero_click(x + 1, y - 1)
    if x < w - 1 and field[x + 1][y] != 'hl':
        zero_click(x + 1, y)
    if x < w - 1 and y < h - 1 and field[x + 1][y + 1] != 'hl':
        zero_click(x + 1, y + 1)

def click(x, y):
    global field_b, f, disabled
    if f:
        field_b, f = b, 0
        while field_b:
            x1, y1 = rd(0, w - 1), rd(0, h - 1)
            if (x1, y1) != (x - 1, y - 1) and (x1, y1) != (x - 1, y) and (x1, y1) != (x - 1, y + 1) and \
                    (x1, y1) != (x, y - 1) and (x1, y1) != (x, y) and (x1, y1) != (x, y + 1) and \
                    (x1, y1) != (x + 1, y - 1) and (x1, y1) != (x + 1, y) and (x1, y1) != (x + 1, y + 1):
                set_bomb(x1, y1)
    if field[x][y] != 'b':
        disabled += 1
        Label(window, text=field[x][y] if field[x][y] else '').place(x=x * 20, y=y * 20, width=20, height=20)
        if not field[x][y]: zero_click_check(x, y)
    else:
        Label(window, text='GAME OVER').place(x=0, y=-10, width=w * 20, height=h * 20 + 10)
        Button(text='Restart', bg='light gray', command=lambda: setting()).place(x=w * 10 - 40, y=h * 10, width=80, height=20)
    win_check()

def set_bomb(x, y):
    global field_b
    if field[x][y] != 'b':
        field_b -= 1
        field[x][y] = 'b'
        if x > 0 and y > 0 and field[x - 1][y - 1] != 'b':
            field[x - 1][y - 1] += 1
        if x > 0 and field[x - 1][y] != 'b':
            field[x - 1][y] += 1
        if x > 0 and y < h - 1 and field[x - 1][y + 1] != 'b':
            field[x - 1][y + 1] += 1
        if y > 0 and field[x][y - 1] != 'b':
            field[x][y - 1] += 1
        if y < h - 1 and field[x][y + 1] != 'b':
            field[x][y + 1] += 1
        if x < w - 1 and y > 0 and field[x + 1][y - 1] != 'b':
            field[x + 1][y - 1] += 1
        if x < w - 1 and field[x + 1][y] != 'b':
            field[x + 1][y] += 1
        if x < w - 1 and y < h - 1 and field[x + 1][y + 1] != 'b':
            field[x + 1][y + 1] += 1

def st():
    global h, w, b, field, f, disabled
    h, w, b = int(h.get()), int(w.get()), int(b.get())
    window.geometry('%dx%d' % (w * 20, h * 20))
    field, f, disabled = [[0] * h for i in range(w)], 1, 0
    for i in range(w):
        for j in range(h):
            Button(bg='light gray', command=lambda i=i, j=j: click(i, j)).place(x=i * 20, y=j * 20, width=20, height=20)

h, w, b, f, field_b, disabled, deb, field = 10, 10, 0, 1, 0, 0, 0,[]

window = Tk()
window.title('Сапёр')
window.geometry('%dx%d' % (w * 20, h * 20))

setting()
window.mainloop()
