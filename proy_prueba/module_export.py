# -*- coding: utf-8 -*-
import xlsxwriter
from datetime import date
import settings as st

def F_export_model_results(Conj_B, Conj_U, Conj_S, X, Y, week_keys):    
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
        worksheet.write(0, 1, 'Fecha Inicio')
        worksheet.write(0, 2, 'Fecha Termino')
        worksheet.write(0, 3, 'Actividad')
        worksheet.write(0, 4, 'Tipo')
        worksheet.write(0, 5, 'Especialidad')
        worksheet.write(0, 6, 'Centro')
        worksheet.write(0, 7, 'Practica')
        
        row=1
        for s in Conj_U.keys(): #en todas las semanas posibles
            for k in Conj_U[s]: #en todas las actividades de esa semana
                for act in X[docente]:#todas las atividades realizados por el profesor
                    if k == int(act): #si la actividad realizada corresponde a las actividades realizadas esa semana
                        worksheet.write(row, 0, int(s))
                        worksheet.write(row, 1, date.fromordinal((Conj_S[int(s)]['Fecha Inicio'])).strftime('%d/%m'))
                        worksheet.write(row, 2, date.fromordinal((Conj_S[int(s)]['Fecha Termino'])).strftime('%d/%m'))
                        worksheet.write(row, 3, act)
                        worksheet.write(row, 4,Conj_B[k]['Tipo'])
                        worksheet.write(row, 5,', '.join(Conj_B[k]['Especialidad']))
                        worksheet.write(row, 6,Conj_B[k]['Centro'])
                        worksheet.write(row, 7,Conj_B[k]['Practica'])
                        row += 1
                        
    worksheet = workbook.add_worksheet('Sobrecarga')
    worksheet.write(0, 0, 'Semana')
    col=1
    for p in X.keys():
        for s in range(max(week_keys)+1):
            try:
                worksheet.write(s+1, col, Y[p][s])            
            except KeyError:
                worksheet.write(s+1, col, 0)
            worksheet.write(s+1,0,s)
        worksheet.write(0, col, p)
        col+=1
    workbook.close()