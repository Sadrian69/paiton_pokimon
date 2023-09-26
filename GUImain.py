import numpy as np
import pandas as pd

import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image

# import data
poke = pd.read_csv('Pokemon.csv')

# formatting
attr = [[] for x in range(len(poke))]
prem = poke.keys().tolist() # berisi premis
del prem[0]
choices = [[] for i in range(len(prem))] # berisi pilihan jawaban untuk setiap premis

# isi pilihan jawaban
for ind in poke.index:
    for col in poke.columns.values:
        if pd.notna(poke[col][ind]) and col != 'nama':
            if not poke[col][ind] in choices[prem.index(col)]:
                choices[prem.index(col)].append(poke[col][ind])
                
# isi rule
for ind in poke.index:
    for col in poke.columns.values:
        if pd.notna(poke[col][ind]) and col != 'nama':
            attr[ind].append([prem.index(col), choices[prem.index(col)].index(poke[col][ind])])

poke['attr'] = attr
# poke['attr'][i] = list atribut pokemon ke-i
# poke['attr'][i][j] = list atribut ke-j pokemon ke-i
# poke['attr'][i][j][0] = premisnya
# poke['attr'][i][j][1] = valuenya

# print(poke['attr'][105])
# note urutan data tergantung pokemon 
# cth anggota badan urutannya 4, >4, 2, 0

# algoritma engine
# step 1
wm = [] # working memory, jawaban di x where ['answer',x] in wm
aq = [] # attribute queue table
rs = [['A', 'U'] for x in range(len(poke))] # rule status
pcs = [['FR' for y in range(len(poke['attr'][x]))] for x in range(len(poke))] # premise clause status

valInput = ""
clicked = ""
window  = tk.Tk()

def pilPil():
    global valInput
    global clicked
    global window
    valInput = clicked.get()
    window.destroy()

def updateGUI(question, choices):
    global clicked
    global window
    
    window.title("Pokemon Finder???")
    window.geometry("800x500")

    title_label = ttk.Label(
        master=window, text="Find the Pokemon", font="Calibri 24 bold")
    title_label.pack(pady=10)
    
    pertanyaan = ttk.Label(
        master=window, text=((question, "?")), font="Calibri 12")
    title_label.pack(pady=10)
    
    clicked = StringVar()
    clicked.set(choices[0])
    drop = OptionMenu(window, clicked, *choices)
    drop.pack(pady=5)
    
    # global valInput
    # valInput = clicked.get()
    
    next = Button(window, text="Next", command=pilPil).pack()
    
    window.mainloop()
    
def GUIhasil(pokName):
    window.title("Pokemon Finder???")
    window.geometry("800x500")
    
    
    title_label = ttk.Label(
        master=window, text=pokName, font="Calibri 24 bold")
    title_label.pack(pady=10)
    
    stringPok = "images/"
    stringPok += pokName
    stringPok += "_front_default.png"
    stringPok = stringPok.lower()
    
    image = Image.open(stringPok)
    image = image.resize((350,350), Image.ANTIALIAS)
    
    pok_img = ImageTk.PhotoImage(image)
    img_label = Label(image=pok_img)
    img_label.pack()
    
    next = Button(window, text="Done", command=window.destroy).pack()
    
    window.mainloop()

def updateGUI(question, choices, message):
    global clicked
    global window
    
    window.title("Pokemon Finder???")
    window.geometry("800x500")

    title_label = ttk.Label(
        master=window, text="Find the Pokemon", font="Calibri 24 bold")
    title_label.pack(pady=10)
    
    pertanyaan = ttk.Label(
        master=window, text=((question, "?")), font="Calibri 12")
    pertanyaan.pack(pady=10)
    
    clicked = StringVar()
    clicked.set(choices[0])
    drop = OptionMenu(window, clicked, *choices)
    drop.pack(pady=5)
    
    # global valInput
    # valInput = clicked.get()
    
    next = Button(window, text="Next", command=pilPil).pack()
    
    message = ttk.Label(master=window, text=message)
    message.pack(pady=10)
    
    window.mainloop()

# step 2
query = 0
print(prem[query], "?")

optPil=[]
for i in choices[query]:
    print(i)
    optPil.append(i)
# valInput = input()

updateGUI(prem[query], optPil, "")
print("dah", valInput)

while valInput not in choices[query]:
    print("Coba lagi")
    ValInput = input()
value = choices[query].index(valInput)
aq.append(query)
wm.append([query,value])

stop = False

while not stop:
    # step 3
    # cek 'Active'
    for i in rs:
        actFound = False
        if 'A' in i:
            actFound = True
            break
    if not actFound:
        print("Gagal di step 3")
        stop = True
        break
        
    # perubahan premise
    td = False
    for i in range(len(pcs)): # untuk semua pokemon
        if 'A' in rs[i]:
            for j in range(len(pcs[i])): # cari atribut
                if poke['attr'][i][j][0] == query: # kalo sama dg query
                    if poke['attr'][i][j][1] == value: # dan bener
                        pcs[i][j] = 'TU'
                        # print(poke['nama'][i])
                    else: # tapi salah
                        # step 3a
                        pcs[i][j] = 'FA'
                        rs[i].remove('A')
                        rs[i].append('D')
                    break
        # step 3b
        if pcs[i] == ['TU' for x in range(len(pcs[i]))]: # semua premis benar
            rs[i].append('TD')
            # print("harusnya ini ", poke['nama'][i])
            td = True
    # step 3c
    if td:
        # step 4
        if len(aq) > 0:
            del aq[0] # cross out topmost attr
        for i in range(len(pcs)): # change status of rule 
            if 'TD' in rs[i]:
                # print("harusnya ini ", poke['nama'][i])
                rs[i].remove('TD')
                rs[i].append('FD')
                wm.append(['conclusion', i]) # conclusion at bottom of wm
        stop = True
        continue # return to 3
    else:
        # step 5
        if len(aq) > 0:
            del aq[0] # cross out topmost attr
        # step 6
        recent = -1 # recently marked rule
        unmarked = False # sudah pernah jalanin rule 8
        for i in range(len(rs)): # scan for unmarked active
            if unmarked:
                break
            if 'U' in rs[i] and 'A' in rs[i]:
                rs[i].remove('U')
                rs[i].append('M') # mark the first one
                recent = i
                # step 7
                for j in range(len(pcs[recent])):
                    if pcs[recent][j] == 'FR': # query user for value
                        query = poke['attr'][recent][j][0]
                        # print(prem[query], "?")
                        
                        optPil = []
                        for k in choices[query]:
                            # print(k)
                            optPil.append(k)
                            
                        window = tk.Tk()
                        updateGUI(prem[query], optPil, "")
                        # valInput = input()
                        
                        # cek keberadaan itu di yang masih aktif
                        valid = False
                        if valInput in choices[query]:
                            for i in range(len(rs)):
                                if 'A' in rs[i]:
                                    # print("test1", poke['nama'][i], query, valInput)
                                    if [query, choices[query].index(valInput)] in poke['attr'][i]:
                                        valid = True
                        
                        while valInput not in choices[query] or not valid: # if no response atau gaada
                            print("Tidak menemukan data mohon coba lagi")
                            window = tk.Tk()
                            updateGUI(prem[query], optPil, "Tidak menemukan data mohon coba lagi")
                            # valInput = input()
                            # cek keberadaan itu di yang masih aktif
                            if valInput in choices[query]:
                                for i in range(len(rs)):
                                    if 'A' in rs[i]:
                                        # print("test2", poke['nama'][i], query, valInput)
                                        if [query, choices[query].index(valInput)] in poke['attr'][i]:
                                            valid = True
                            
                        unmarked = True
                        value = choices[query].index(valInput)
                        # step 8
                        aq.append(query)
                        wm.append([query,value])
                        rs[recent].remove('M')
                        rs[recent].append('U')
                        break
        # step 6 cont
        if not unmarked: # no such rules can be found
            print("Gagal di step 6")
            stop = True
            break
# sudah selesai, jawaban di wm
for i in wm:
    if i[0] == 'conclusion':
        print(poke['nama'][i[1]], "yey")
        window = tk.Tk()
        GUIhasil(poke['nama'][i[1]])
        