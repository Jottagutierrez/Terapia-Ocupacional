# -*- coding: utf-8 -*-
import collections
import xlrd
import json


#Función para abrir el libro de Excel y guardar las hojas de cálculo en un
#diccionario...
def F_get_xl_sheets(path):
    book = xlrd.open_workbook(path)
    sheet = {}    
    for s in book.sheet_names():
        sheet[s] = book.sheet_by_name(s)
    return sheet;
######################################################


#Función para transformar la información de las hojas de Excel {Prácticas,
#Semanas, Centros} y dejarlas almacenadas en variables en Python. También
#construye la matriz de actividades...
def F_translate_into_week(sheet_list):
    Result = collections.namedtuple('Result',['week_L','pract_L', 'act_L', 'cent_L', 'lin_L', 'num_est'])
    
    #Crear una matriz con la información de las semanas...
    sheet_semanas = sheet_list['Info_Semanas']
    week_list = []
    for i in range(0, sheet_semanas.nrows-1):
        week_list.insert(i, {})
        for j in range(1,sheet_semanas.ncols):
                week_list[i][sheet_semanas.cell(0,j).value] = str(sheet_semanas.cell(i+1,j).value)
    
    #Crear una matriz con la información de las prácticas...
    pract_list = {
            'Practica - I': {'Semana Inicio': 0, 'Semana Termino': 17},
            'Practica Profesional': {'Semana Inicio': 21, 'Semana Termino': 39},
            'Internado': {'Semana Inicio': 0, 'Semana Termino': 27},
            'Mencion': {'Semana Inicio': 28, 'Semana Termino': 37},
            }
    '''sheet_pract = sheet_list['Info_Practicas']
    pract_list = {}
    d = ['Semana Inicio','Semana Termino']
    for i in range(0, sheet_pract.nrows-1):
        pract_list[sheet_pract.cell(i+1,0).value] = {}
        for j in range(1, sheet_pract.ncols):
            for k in range(0,len(week_list)):
                if (week_list[k]['Fecha Inicio'] <= int(sheet_pract.cell(i+1,j).value)
                <= week_list[k]['Fecha Termino']):                    
                    pract_list[sheet_pract.cell(i+1,0).value][d[j-1]] = k'''
    
    #Crear matriz de los centros...
    cent_list = {}
    sheet_cent = sheet_list['Centros']
    for i in range(2, sheet_cent.nrows):
        if sheet_cent.cell(i,0).value != 'N/A':
            cent_list[sheet_cent.cell(i,0).value] = []
            for j in range(1, sheet_cent.ncols):
                if 'SI' in sheet_cent.cell(i,j).value:
                    cent_list[sheet_cent.cell(i,0).value].append(sheet_cent.cell(1,j).value)
    
    #Crear una matriz transitoria para guardar la cantidad de estudiantes en
    #cada centro, para cada rotativa...
    rot_info = {'Practica - I': 3, 'Practica Profesional': 3, 'Internado': 7, 'Mencion': 10}
    num_est = {}
    for p in rot_info.keys():
        num_est[p] = {}
        for k in range(3, sheet_list[p].nrows):
            num_est[p][sheet_list[p].cell(k,0).value] = {}
            if sheet_list[p].cell(k,0).value != 'NO ACTIVO':
                for i in range(2, sheet_list[p].ncols):
                    if ((type(sheet_list[p].cell(k,i).value) == int) or
                        (type(sheet_list[p].cell(k,i).value) == float)):
                        num_est[p][sheet_list[p].cell(k,0).value][sheet_list[p].cell(2,i).value] = int(sheet_list[p].cell(k,i).value)
                    else:
                        num_est[p][sheet_list[p].cell(k,0).value][sheet_list[p].cell(2,i).value] = 0
    
    #Crear la matriz de actividades...
    sheet_act = sheet_list['Info_Actividades']
    act_info = {}
    for i in range(1, sheet_act.nrows):
        act_info[sheet_act.cell(i,0).value] = {}
        for j in range(1, sheet_act.ncols):
            act_info[sheet_act.cell(i,0).value][sheet_act.cell(0,j).value] = sheet_act.cell(i,j).value
    
    act_list = []
    Lin = 0
    lin_list = {}
    '''
    for p in rot_info.keys():
        for k in num_est[p].keys():
            print(num_est[p][k][7])
    '''
    
    
    for p in rot_info.keys():
        current_rot = 1
        i = pract_list[p]['Semana Inicio']
        while i in range(pract_list[p]['Semana Inicio'], pract_list[p]['Semana Termino']):                
            skip = 'FALSE'
            if week_list[i]['Estado'] == 'Feriado':          
                i+=1
                skip = 'TRUE'
                #continue
            
            sem_sup = {'Practica - I': i+1, 'Practica Profesional': i+1, 'Internado': i+3, 'Mencion': i+5}
            sem_corr = {'Practica - I': i+2, 'Practica Profesional': i+2, 'Internado': [i+2, i+4], 'Mencion': i+6}
            sem_exam = {'Internado': i+6, 'Mencion': i+7}
            
            if skip == 'FALSE':
                for k in num_est[p].keys():
                    for j in range(0, num_est[p][k][current_rot]):
                        act_list.append({'Practica': p,'Tipo': 'Supervision', 'Centro': k, 'Semana': sem_sup[p], 'Tiempo': act_info['Supervision']['Tiempo'], 'Costo Base': act_info['Supervision']['Costo Base'], 'Costo Traslado': act_info['Supervision']['Costo Traslado'], 'Especialidad': cent_list[k], 'Rotativa': current_rot, 'Linea': Lin})
                        try:
                            for c in sem_corr[p]:
                                act_list.append({'Practica': p,'Tipo': 'Correccion', 'Centro': k, 'Semana': c, 'Tiempo': act_info['Correccion']['Tiempo'], 'Costo Base': act_info['Correccion']['Costo Base'], 'Costo Traslado': act_info['Correccion']['Costo Traslado'], 'Especialidad': cent_list[k], 'Rotativa': current_rot, 'Linea': Lin})
                        except TypeError:
                            act_list.append({'Practica': p,'Tipo': 'Correccion', 'Centro': k, 'Semana': sem_corr[p], 'Tiempo': act_info['Correccion']['Tiempo'], 'Costo Base': act_info['Correccion']['Costo Base'], 'Costo Traslado': act_info['Correccion']['Costo Traslado'], 'Especialidad': cent_list[k], 'Rotativa': current_rot, 'Linea': Lin})
                        try:
                            act_list.append({'Practica': p,'Tipo': 'Examen', 'Centro': k, 'Semana': sem_exam[p], 'Tiempo': act_info['Examen']['Tiempo'], 'Costo Base': act_info['Examen']['Costo Base'], 'Costo Traslado': act_info['Examen']['Costo Traslado'], 'Especialidad': cent_list[k], 'Rotativa': current_rot, 'Linea': Lin})
                        except KeyError:
                            pass
                        lin_list[Lin] = {'Practica': p,'Rotativa': current_rot, 'Centro': k}
                        Lin+=1
                current_rot+=1
            i+=rot_info[p]
    
    R = Result(week_list, pract_list, act_list, cent_list, lin_list, num_est)
    return R;
######################################################


#Función para la obtención de la matriz de profesores desde la hoja de cálculo
#de Excel...
def F_get_prof_data(xls_sheet):
    mat={}
    key=[]
    for i in range(1,xls_sheet.nrows):
        key.insert(i-1, str(xls_sheet.cell(i, 0).value))
        for r in range(0,len(key)):
            mat[str(key[r])] = {}
            for i in range(1,xls_sheet.ncols):            
                mat[str(key[r])][str(xls_sheet.cell(0,i).value)] = xls_sheet.cell(r+1,i).value                
    return mat;
######################################################


#Función para la obtención de la matriz de actividades desde la hoja de cálculo
#de Excel...
def F_get_act_data(xls_sheet):    
    mat={}
    key=[]
    for i in range(1,xls_sheet.nrows):
        key.insert(i-1, float(xls_sheet.cell(i,0).value))
        for r in range(0,len(key)):
            mat[float(key[r])] = {}
            for i in range(1,xls_sheet.ncols):
                mat[float(key[r])][str(xls_sheet.cell(0,i).value)] = xls_sheet.cell(r+1,i).value                
    return mat;
######################################################


#Función para crear el archivo donde se almacenarán los parámetros
#ya procesados...
def F_create_param_file(act_list, prof_list, cent_list,
                        week_list, pract_list, lin_list, path):
        
    prof_keys = []
    for k in prof_list.keys():
        prof_keys.append(k)
    
    cent_keys = []
    for j in cent_list.keys():
        cent_keys.append(j)  
    
    week_keys = []
    for s in range(0, len(week_list)):
        week_keys.append(s)
    
    act_keys = []
    for k in range(0, len(act_list)):
        act_keys.append(k)
    
    pract_keys = ['Practica - I', 'Practica Profesional', 'Internado', 'Mencion']
    
    Conj_U = {}
    for s in week_keys:        
        Conj_U[s] = []        
        for k in act_keys:
            if act_list[k]['Semana'] == s:
                Conj_U[s].append(k)
    Conj_U = dict([(k,v) for k,v in Conj_U.items() if len(v)>0])        
    
    week_keys = []
    for s in Conj_U.keys():
        week_keys.append(s)
    
    Conj_J = {}
    for j in cent_keys:
        Conj_J[j] = []
    for k in act_keys:
        for j in cent_keys:
            if act_list[k]['Centro'] == j:
                Conj_J[j].append(k)
    
    Conj_I = {}
    for pr in pract_keys:
        Conj_I[pr] = []
    for k in act_keys:
        for pr in pract_keys:
            if act_list[k]['Practica'] == pr:
                Conj_I[pr].append(k)
    
    Conj_Sup = {}
    Conj_Sup['Total'] = []
    for j in cent_keys:
        Conj_Sup[j] = []
    for k in act_keys:
        for j in cent_keys:
            if act_list[k]['Tipo'] == 'Supervision':
                Conj_Sup['Total'].append(k)
                if act_list[k]['Centro'] == j:
                    Conj_Sup[j].append(k)
    
    Conj_Ex = {}
    Conj_Ex['Total'] = []
    for j in cent_keys:
        Conj_Ex[j] = []
    for k in act_keys:
        for j in cent_keys:
            if act_list[k]['Tipo'] == 'Examen':
                Conj_Ex['Total'].append(k)
                if act_list[k]['Centro'] == j:
                    Conj_Ex[j].append(k)
    
    Conj_Corr = {}
    Conj_Corr['Total'] = []
    for j in cent_keys:
        Conj_Corr[j] = []
    for k in act_keys:
        for j in cent_keys:
            if act_list[k]['Tipo'] == 'Correccion':
                Conj_Ex['Total'].append(k)
                if act_list[k]['Centro'] == j:
                    Conj_Corr[j].append(k)
    
    Conj_P = {'EXTERNO': [], 'INTERNO': []}
    for p in prof_keys:
        for es in Conj_P.keys():
            if prof_list[p]['Estado'] == es:
                Conj_P[es].append(p)
    
    Conj_Lin = {}
    for l in lin_list.keys():
        if lin_list[l]['Practica'] == 'Practica - I':
            Conj_Lin[l] = {'Supervision': 0, 'Correccion': 0, 'Practica': 'Practica - I', 'Rotativa': lin_list[l]['Rotativa']}
        elif lin_list[l]['Practica'] == 'Practica Profesional':
            Conj_Lin[l] = {'Supervision': 0, 'Correccion': 0, 'Practica': 'Practica Profesional', 'Rotativa': lin_list[l]['Rotativa']}
        elif lin_list[l]['Practica'] == 'Internado':
            Conj_Lin[l] = {'Supervision': 0, 'Correccion': [], 'Examen': 0, 'Practica': 'Internado', 'Rotativa': lin_list[l]['Rotativa']}
        for k in act_keys:
            if act_list[k]['Practica'] == 'Internado':
                if act_list[k]['Linea'] == l:
                    if act_list[k]['Tipo'] == 'Supervision':
                        Conj_Lin[l]['Supervision'] = k
                    elif act_list[k]['Tipo'] == 'Examen':
                        Conj_Lin[l]['Examen'] = k
                    elif act_list[k]['Tipo'] == 'Correccion':
                        Conj_Lin[l]['Correccion'].append(k)
            elif act_list[k]['Practica'] == 'Practica - I':
                if act_list[k]['Linea'] == l:
                    if act_list[k]['Tipo'] == 'Supervision':
                            Conj_Lin[l]['Supervision'] = k
                    elif act_list[k]['Tipo'] == 'Correccion':
                        Conj_Lin[l]['Correccion'] = k
            elif act_list[k]['Practica'] == 'Practica Profesional':
                if act_list[k]['Linea'] == l:
                    if act_list[k]['Tipo'] == 'Supervision':
                            Conj_Lin[l]['Supervision'] = k
                    elif act_list[k]['Tipo'] == 'Correccion':
                        Conj_Lin[l]['Correccion'] = k
    
    Conj_E = {}
    for p in prof_keys:        
        Conj_E[p] = []
        for s in Conj_U.keys():
            contador_act = {'Supervision': 0, 'Correccion': 0, 'Examen': 0}
            for k in Conj_U[s]:
                if (prof_list[p]['Especialidad'] == 'TODO' and
                    prof_list[p]['Disponibilidad'] != 0):
                    if act_list[k]['Tipo'] == 'Correccion':
                        if prof_list[p]['Max Correccion'] != 'N/A':
                            if contador_act['Correccion'] < prof_list[p]['Max Correccion']:
                                Conj_E[p].append(k)
                                contador_act['Correccion']+=1
                        elif prof_list[p]['Max Correccion'] == 'N/A':
                            Conj_E[p].append(k)
                    elif act_list[k]['Tipo'] == 'Supervision':
                        if prof_list[p]['Max Supervision'] != 'N/A':
                            if contador_act['Supervision'] < prof_list[p]['Max Supervision']:
                                Conj_E[p].append(k)
                                contador_act['Supervision']+=1
                        elif prof_list[p]['Max Supervision'] == 'N/A':
                            Conj_E[p].append(k)
                    elif act_list[k]['Tipo'] == 'Examen':
                        if prof_list[p]['Max Examen'] != 'N/A':
                            if contador_act['Examen'] < prof_list[p]['Max Examen']:
                                Conj_E[p].append(k)
                                contador_act['Examen']+=1
                        elif prof_list[p]['Max Examen'] == 'N/A':
                            Conj_E[p].append(k)
                elif (prof_list[p]['Especialidad'] != 'TODO' and
                    prof_list[p]['Disponibilidad'] != 0):
                    for es in act_list[k]['Especialidad']:
                        if es != 'COMUNITARIO':
                            if act_list[k]['Tipo'] == 'Correccion':
                                if prof_list[p]['Max Correccion'] != 'N/A':
                                    if contador_act['Correccion'] < prof_list[p]['Max Correccion']:
                                        if es == prof_list[p]['Especialidad']:
                                            Conj_E[p].append(k)
                                            contador_act['Correccion']+=1
                                elif prof_list[p]['Max Correccion'] == 'N/A':
                                    if es == prof_list[p]['Especialidad']:
                                        Conj_E[p].append(k)        
                            elif act_list[k]['Tipo'] == 'Examen':
                                if prof_list[p]['Max Examen'] != 'N/A':
                                    if contador_act['Examen'] < prof_list[p]['Max Examen']:
                                        if es == prof_list[p]['Especialidad']:
                                            Conj_E[p].append(k)
                                            contador_act['Examen']+=1
                                elif prof_list[p]['Max Examen'] == 'N/A':
                                    if es == prof_list[p]['Especialidad']:
                                        Conj_E[p].append(k)
                            elif act_list[k]['Tipo'] == 'Supervision':
                                if prof_list[p]['Max Supervision'] != 'N/A':
                                    if contador_act['Supervision'] < prof_list[p]['Max Supervision']:
                                        if act_list[k]['Practica'] == 'Mencion':
                                            if es == prof_list[p]['Especialidad']:
                                                Conj_E[p].append(k)  
                                        elif act_list[k]['Practica'] == 'Internado':
                                            Conj_E[p].append(k)
                                        elif act_list[k]['Practica'] == 'Practica - I':
                                            Conj_E[p].append(k)
                                        elif act_list[k]['Practica'] == 'Practica Profesional':
                                            Conj_E[p].append(k)
                                        contador_act['Supervision']+=1
                                elif prof_list[p]['Max Supervision'] == 'N/A':
                                    if act_list[k]['Practica'] == 'Mencion':
                                        if es == prof_list[p]['Especialidad']:
                                            Conj_E[p].append(k)                    
                                    elif act_list[k]['Practica'] == 'Internado':
                                        Conj_E[p].append(k)
                                    elif act_list[k]['Practica'] == 'Practica - I':
                                        Conj_E[p].append(k)
                                    elif act_list[k]['Practica'] == 'Practica Profesional':
                                        Conj_E[p].append(k)
    
    T = {}
    for k in act_keys:
        T[k] = act_list[k]['Tiempo']
    
    D = {}
    for p in prof_keys:
        D[p] = prof_list[p]['Disponibilidad']
        
    data = {'prof_keys': prof_keys, 'cent_keys': cent_keys, 'cent_info': cent_list,
            'week_keys': week_keys, 'act_keys': act_keys,
            'Conj_U': Conj_U, 'Conj_Sup': Conj_Sup, 'Conj_Ex': Conj_Ex, 'Conj_Corr': Conj_Corr,
            'Conj_E': Conj_E, 'Act_List': act_list,
            'Conj_P': Conj_P, 'Week_List': week_list, 'Conj_Lin': Conj_Lin,
            'Conj_J': Conj_J, 'Conj_I': Conj_I,
            'T': T, 'D': D}
    
    for pth in path.keys():
        with open(path[pth], 'w') as outfile:
            json.dump(data[pth], outfile)        

######################################################