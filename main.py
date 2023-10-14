import tkinter as tk
import pandas as pd
import numpy as np
pd.set_option('display.expand_frame_repr', False)

# jawaban
ans = 'support'

# algoritma engine
# step 1
# import data
premiseTable = pd.read_excel('C:/School/Semester_5/ASP/paiton_pokimon/pokemon.xlsx', 'Premise').astype(str)
rules = pd.read_excel('C:/School/Semester_5/ASP/paiton_pokimon/pokemon.xlsx', 'Rules').astype(str)
ruleDetails = pd.read_excel('C:/School/Semester_5/ASP/paiton_pokimon/pokemon.xlsx', 'Rule Detail').astype(str)
questions = pd.read_excel('C:/School/Semester_5/ASP/paiton_pokimon/pokemon.xlsx', 'Questions').astype(str)
choices = pd.read_excel('C:/School/Semester_5/ASP/paiton_pokimon/pokemon.xlsx', 'Choices').astype(str)
wm = pd.read_excel('C:/School/Semester_5/ASP/paiton_pokimon/pokemon.xlsx', 'WM Table').astype(str).reset_index(drop=True)

# step 2
query = 0
print(questions['question'][query])
for i in choices.index:
    if choices['id_question'][i] == questions['id'][query]:
        print(choices['choice'][i])
valInput = input()
wm.loc[len(wm)] = pd.Series({'attribute' : questions['attribute'][query], 'value' : valInput})

for i in wm.index:
    print(wm['attribute'][i],': ',wm['value'][i])

stop = False

while not stop:
    # step 3
    # cek 'Active'
    for i in rules['A']:
        actFound = False
        if i == 1:
            actFound = True
            break
    if not actFound:
        print("Gagal di step 3")
        stop = True
        break
        
    # perubahan premise
    td = False
    for i in rules.index: # untuk semua rule
        if rules['A'][i] == 1:
            for j in ruleDetails.index: # cari premis
                if ruleDetails['rule_id'][j] == i:
                    preID = ruleDetails['premise_id'][j]
                    if premiseTable['attribute'][preID+1] == questions['attribute'][query]: # kalo sama dg query
                        if premiseTable['value'][preID+1] == valInput: # dan bener
                            premiseTable['premise clause status'][preID+1] = 'TU'
                        else: # tapi salah
                            # step 3a
                            premiseTable['premise clause status'][preID+1] = 'FA'
                            rules['A'][i] = 0
                            rules['D'][i] = 1
                        break
                    
# note to self
# nanti waktu question if the question type is i-conclude langsung auto masuk
# tapi masuknya kalo udah TD
# trus kalo support yang TD langsung crot (dipikir nanti)

#         # step 3b
#         if pcs[i] == ['TU' for x in range(len(pcs[i]))]: # semua premis benar
#             rs[i].append('TD')
#             # print("harusnya ini ", poke['nama'][i])
#             td = True
#     # step 3c
#     if td:
#         # step 4
#         if len(aq) > 0:
#             del aq[0] # cross out topmost attr
#         for i in range(len(pcs)): # change status of rule 
#             if 'TD' in rs[i]:
#                 # print("harusnya ini ", poke['nama'][i])
#                 rs[i].remove('TD')
#                 rs[i].append('FD')
#                 wm.append(['conclusion', i]) # conclusion at bottom of wm
#         stop = True
#         continue # return to 3
#     else:
#         # step 5
#         if len(aq) > 0:
#             del aq[0] # cross out topmost attr
#         # step 6
#         recent = -1 # recently marked rule
#         unmarked = False # sudah pernah jalanin rule 8
#         for i in range(len(rs)): # scan for unmarked active
#             if unmarked:
#                 break
#             if 'U' in rs[i] and 'A' in rs[i]:
#                 rs[i].remove('U')
#                 rs[i].append('M') # mark the first one
#                 recent = i
#                 # step 7
#                 for j in range(len(pcs[recent])):
#                     if pcs[recent][j] == 'FR': # query user for value
#                         query = poke['attr'][recent][j][0]
#                         print(prem[query], "?")
#                         for k in choices[query]:
#                             print(k)
#                         valInput = input()
#                         # cek keberadaan itu di yang masih aktif
#                         valid = False
#                         if valInput in choices[query]:
#                             for i in range(len(rs)):
#                                 if 'A' in rs[i]:
#                                     # print("test1", poke['nama'][i], query, valInput)
#                                     if [query, choices[query].index(valInput)] in poke['attr'][i]:
#                                         valid = True
                        
#                         while valInput not in choices[query] or not valid: # if no response atau gaada
#                             print("Tidak menemukan data mohon coba lagi")
#                             valInput = input()
#                             # cek keberadaan itu di yang masih aktif
#                             if valInput in choices[query]:
#                                 for i in range(len(rs)):
#                                     if 'A' in rs[i]:
#                                         # print("test2", poke['nama'][i], query, valInput)
#                                         if [query, choices[query].index(valInput)] in poke['attr'][i]:
#                                             valid = True
                            
#                         unmarked = True
#                         value = choices[query].index(valInput)
#                         # step 8
#                         aq.append(query)
#                         wm.append([query,value])
#                         rs[recent].remove('M')
#                         rs[recent].append('U')
#                         break
#         # step 6 cont
#         if not unmarked: # no such rules can be found
#             print("Gagal di step 6")
#             stop = True
#             break
# # sudah selesai, jawaban di wm
# for i in wm:
#     if i[0] == 'conclusion':
#         print(poke['nama'][i[1]])