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


stop = False

while not stop:
    
    print()
    print("Working Memory")
    for i in wm.index:
        print(wm['attribute'][i],': ',wm['value'][i])
    print()
        
    # step 3
    # cek 'Active'
    actFound = False
    for i in rules.index:
        if rules['A'][i] == '1':
            actFound = True
            break
        
    if not actFound:
        print("Pokemon tidak ditemukan")
        stop = True
        break
        
    # perubahan premise
    for i in rules.index: # untuk semua rule
        # print('rule', rules['id'][i])
        if rules['A'][i] == '1':
            for j in ruleDetails.index: # cari premis
                if ruleDetails['rule_id'][j] == rules['id'][i]:
                    preID = int(ruleDetails['premise_id'][j])-1
                    
                    # print(premiseTable['attribute'][int(preID)], premiseTable['value'][int(preID)])
                    if premiseTable['attribute'][preID] == wm['attribute'][len(wm)-1]: # kalo sama dg query
                        if premiseTable['value'][preID] == wm['value'][len(wm)-1]: # dan bener
                            premiseTable['premise clause status'][int(preID)] = 'TU'
                            # print(premiseTable['value'][int(preID)],'TU')
                        else: # tapi salah
                            # step 3a
                            premiseTable['premise clause status'][int(preID)] = 'FA'
                            # print(premiseTable['value'][int(preID)],'FA')
                            rules['A'][i] = 0
                            rules['D'][i] = 1
                        break

    # step 3b
    for i in rules.index: 
        if rules['TD'][i] == '1' or rules['FD'][i] == '1':
            continue
        td = True
        for j in ruleDetails.index:
            if ruleDetails['rule_id'][j] == rules['id'][i]:
                preID = int(ruleDetails['premise_id'][j])-1
                if premiseTable['premise clause status'][preID] != 'TU':
                    # ada premis yang salah
                    td = False
                    
        if td:
            rules['TD'][i] = '1'
            break
    
    # step 3c
    if td:
        # step 4
        for i in rules.index: # change status of rule 
            if rules['TD'][i] == '1':
                # print('TD', i+1)
                rules['TD'][i] = '0'
                rules['FD'][i] = '1'
                wm.loc[len(wm)] = pd.Series({'attribute' : rules['attribute_conclude'][i] , 'value' : rules['conclusion'][i]}) # conclusion at bottom of wm
                if rules['attribute_conclude'][i] == 'support':
                    stop = True
        continue # return to 3
    else:
        # step 6
        unmarked = False # sudah pernah jalanin rule 8
        
        for i in rules.index: # scan for unmarked active
            if unmarked:
                break
            if rules['A'][i] == '1' and rules['U'][i] == '1':
                rules['U'][i] = '0'
                rules['M'][i] = '1' # mark the first one
                
                # print('UA', rules['id'][i], rules['U'][i], rules['M'][i])
                
                # step 7
                for j in ruleDetails.index:
                    preID = int(ruleDetails['premise_id'][j])-1
                    if ruleDetails['rule_id'][j] == rules['id'][i] and premiseTable['premise clause status'][int(preID)] == 'FR':
                        # query user 
                        curQuestionAttr = premiseTable['attribute'][int(preID)]
                        idQuestion = ''
                        for k in questions.index:
                            if questions['attribute'][k] == curQuestionAttr:
                                idQuestion = k
                                break
                        query = idQuestion
                            
                        if questions['type'][idQuestion] == 'question':
                            print(questions['question'][query])
                            for k in choices.index:
                                if choices['id_question'][k] == questions['id'][query]:
                                    print(choices['choice'][k])
                            valInput = input()
                           
                            # step 8
                            wm.loc[len(wm)] = pd.Series({'attribute' : questions['attribute'][query], 'value' : valInput})
                    
                        unmarked = True
                        break
                    
                rules['U'][i] = '1'
                rules['M'][i] = '0'
                        
        # step 6 cont
        if not unmarked: # no such rules can be found
            print("Pokemon tidak ditemukan")
            stop = True
            break

# sudah selesai, jawaban di wm
for i in wm.index:
    if wm['attribute'][i] == ans:
        print('Pokemon yang anda cari adalah', wm['value'][i])