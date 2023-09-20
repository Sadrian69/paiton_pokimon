import numpy as np
import pandas as pd

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

# step 2
query = 0
print(prem[query], "?")
for i in choices[query]:
    print(i)
valInput = input()
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
        for j in range(len(pcs[i])): # cari atribut
            if poke['attr'][i][j][0] == query: # kalo sama dg query
                if poke['attr'][i][j][1] == value: # dan bener
                    pcs[i][j] = 'TU'
                else: # tapi salah
                    # step 3a
                    pcs[i][j] = 'FA'
                    rs[i].remove('A')
                    rs[i].append('D')
                break
        # step 3b
        if pcs[i] == ['TU' for x in range(len(pcs[i]))]: # semua premis benar
            rs[i].append('TD')
            td = True
    # step 3c
    if td:
        # step 4
        del aq[0] # cross out topmost attr
        for i in range(len(pcs)): # change status of rule 
            if 'TD' in rs[i]:
                rs[i].remove('TD')
                rs[i].append('FD')
        wm.append['conclusion', i] # conclusion at bottom of wm
        continue # return to 3
    else:
        # step 5
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
                        print(prem[query], "?")
                        for k in choices[query]:
                            print(k)
                        if valInput not in choices[query]: # if no response
                            continue # continue
                        unmarked = True
                        value = choices[query].index(valInput)
                        aq.append(query)
                        wm.append([query,value])
                        rs[recent].remove('M')
                        rs[recent].remove('U')
        # step 6 cont
        if not unmarked: # no such rules can be found
            print("Gagal di step 6")
            stop = True
            break