# -*- coding: utf-8 -*-
import xlsxwriter
import settings as st

def F_export_model_results(Conj_B, Conj_U, X):    
    '''
    lista = list(X.keys())
        
    diccionario={}        
    name=[]
    activity=[]
    for k in range(len(lista)):        
        key_1=str(lista[k]).replace('X[','')
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
    '''
    
    workbook = xlsxwriter.Workbook(str(st.result_folder_path + '/Calendario.xlsx'))
    
    
    for docente in X.keys():
        worksheet = workbook.add_worksheet(docente)
        
        worksheet.write(0, 0, 'Semana')
        worksheet.write(0, 1, 'Actividad')
        worksheet.write(0, 2, 'Centro')
        worksheet.write(0, 3, 'Especialidad')
        worksheet.write(0, 4, 'Tipo')
        worksheet.write(0, 5, 'Practica')
        
        row=1
        for s in Conj_U.keys(): #en todas las semanas posibles
            for k in Conj_U[s]: #en todas las actividades de esa semana
                for act in X[docente]:#todas las atividades realizados por el profesor
                    if k == int(act): #si la actividad realizada corresponde a las actividades realizadas esa semana
                        worksheet.write(row, 0, s)
                        worksheet.write(row, 1, act)
                        worksheet.write(row, 2,Conj_B[k]['Centro'])
                        worksheet.write(row, 3,', '.join(Conj_B[k]['Especialidad']))
                        worksheet.write(row, 4,Conj_B[k]['Tipo'])
                        worksheet.write(row, 5,Conj_B[k]['Practica'])
                        row += 1
    workbook.close()