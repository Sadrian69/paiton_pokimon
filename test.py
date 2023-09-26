import tkinter as tk
from tkinter import ttk
from tkinter import *


def showSel():
    attr = Label(window, text = clicked.get()).pack()


window = tk.Tk()
window.title("Pokemon Finder???")
window.geometry("800x500")

title_label = ttk.Label(
    master=window, text="Find the Pokemon", font="Calibri 24 bold")
title_label.pack(pady=10)

options = ["Monday", "Tuesday", "Wed"]

clicked = StringVar()
clicked.set(options[0])

drop = OptionMenu(window, clicked, *options)
drop.pack(pady=5)

next = Button(window, text="Next", command=showSel).pack()

# input_frame = ttk.Frame(master=window)
# entry = ttk.Entry(master=input_frame)
# button = ttk.Button(master=input_frame, text="Convert", command=convert)
# entry.pack()
# button.pack()
# input_frame.pack(pady=10)


window.mainloop()
