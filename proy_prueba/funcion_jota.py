# -*- coding: utf-8 -*-
import json
import xlsxwriter
leer = json.loads(open('resultado1.txt').read())

#Detallar todas las direcciones de los archivos...
files_folder_path = 'proy_files'
param_folder_path = files_folder_path + '/parameters'
param_path_list = {'prof_keys': param_folder_path + '/prof_keys.json',
                   'cent_keys': param_folder_path + '/cent_keys.json',
                   'week_keys': param_folder_path + '/week_keys.json',
                   'act_keys': param_folder_path + '/act_keys.json',
                   'Conj_U': param_folder_path + '/Conj_U.json',
                   'Conj_A': param_folder_path + '/Conj_A.json',
                   'Conj_E': param_folder_path + '/Conj_E.json',
                   'T': param_folder_path + '/T.json',
                   'D': param_folder_path + '/D.json',
                   'S': param_folder_path + '/S.json',
                   'H': param_folder_path + '/H.json',
                   'C': param_folder_path + '/C.json'}

Conj_U = json.load(open(param_path_list['Conj_U']))
    #Conjunto de actividades 'k' que se realizan en cada semana 's'...



lista = list(leer.keys())

'''lista=[]
for i in lectura:
    key = str(i)
    lista.append(key)'''
    
diccionario={}    
lista_2=[]
name=[]
activity=[]
for k in range(len(lista)):
    if str(lista[k])[0]== 'x':
        key_1=str(lista[k]).replace('x[','')
        key_2=key_1.replace(']','')
        Nombre, Actividad= key_2.split(',')
        name.append(Nombre)
        activity.append(Actividad)
        

Profes=list(set(name))
for j in range(len(Profes)):
    diccionario[Profes[j]]=[]
    for e in range(len(name)): 
        if Profes[j] == name[e]:
            diccionario[Profes[j]].append(activity[e])


workbook = xlsxwriter.Workbook('Calendario.xlsx')

for docente in diccionario.keys():
    worksheet = workbook.add_worksheet('%s'%docente)

    row=0
    for s in Conj_U.keys(): #en todas las semanas posibles
        for k in Conj_U[s]: #en todas las actividades de esa semana
            for act in diccionario[docente]:#todas las atividades realizados por el profesor
                if k == int(act): #si la actividad realizada corresponde a las actividades realizadas esa semana
                    worksheet.write(row, 0, s)
                    worksheet.write(row, 1, act)
                    row += 1
workbook.close()