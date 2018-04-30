# -*- coding: utf-8 -*-
import collections
import xlrd
#import xlwt
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
    Result = collections.namedtuple('Result',['week_L','pract_L', 'act_L', 'cent_L', 'lin_L'])
    
    #Crear una matriz con la información de las semanas...
    sheet_semanas = sheet_list['Info_Semanas']
    week_list = []
    for i in range(0, sheet_semanas.nrows-1):
        week_list.insert(i, {})
        for j in range(1,sheet_semanas.ncols):
            try:
                week_list[i][sheet_semanas.cell(0,j).value] = int(sheet_semanas.cell(i+1,j).value)
            except ValueError:
                week_list[i][sheet_semanas.cell(0,j).value] = str(sheet_semanas.cell(i+1,j).value)
    
    #Crear una matriz con la información de las prácticas...
    sheet_pract = sheet_list['Info_Practicas']
    pract_list = {}
    d = ['Semana Inicio','Semana Termino']
    for i in range(0, sheet_pract.nrows-1):
        pract_list[sheet_pract.cell(i+1,0).value] = {}
        for j in range(1, sheet_pract.ncols):
            for k in range(0,len(week_list)):
                if (week_list[k]['Fecha Inicio'] <= int(sheet_pract.cell(i+1,j).value)
                <= week_list[k]['Fecha Termino']):                    
                    pract_list[sheet_pract.cell(i+1,0).value][d[j-1]] = k
    
    #Crear matriz de los centros...
    cent_list = {}
    sheet_cent = sheet_list['Centros']
    for i in range(1, sheet_cent.nrows):
        cent_list[sheet_cent.cell(i,0).value] = []
        for j in range(1, sheet_cent.ncols):
            if sheet_cent.cell(i,j).value == 1:
                cent_list[sheet_cent.cell(i,0).value].append(sheet_cent.cell(0,j).value)
    
    #Crear una matriz transitoria para guardar la cantidad de estudiantes en
    #cada centro, para cada rotativa...
    rot_info = {'Practica - I': 3, 'Practica - II': 3, 'Internado': 7, 'Mencion': 10}
    num_est = {}
    for p in rot_info.keys():
        num_est[p] = {}
        for k in range(3, sheet_list[p].nrows):
            num_est[p][sheet_list[p].cell(k,0).value] = {}
            #num_est[p][sheet_list[p].cell(k,0).value]['Especialidad'] = str(sheet_list[p].cell(k,1).value)
            for i in range(2, sheet_list[p].ncols):
                num_est[p][sheet_list[p].cell(k,0).value][sheet_list[p].cell(2,i).value] = int(sheet_list[p].cell(k,i).value)    
    
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
    for p in rot_info.keys():
        current_rot = 1
        i = pract_list[p]['Semana Inicio']
        while i in range(pract_list[p]['Semana Inicio'], pract_list[p]['Semana Termino']+1):                
            if p == 'Practica - II' and week_list[i]['Estado'] == 'Feriado':                
                i+=1
                continue
            
            sem_sup = {'Practica - I': i+1, 'Practica - II': i+1, 'Internado': i+3, 'Mencion': i+5}
            sem_corr = {'Practica - I': i+2, 'Practica - II': i+2, 'Internado': [i+2, i+4], 'Mencion': i+6}
            sem_exam = {'Internado': i+6, 'Mencion': i+7}
                        
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
                    lin_list[Lin] = p
                    Lin+=1
            current_rot+=1
            i+=rot_info[p]
    #act_list = dict( [(k,v) for k,v in act_list.items() if len(v)>0])
    #lin_list = list(set(lin_list))
    
    for elem in act_list:
        elem['Especialidad'] = list(filter(None, elem['Especialidad']))
    
    R = Result(week_list, pract_list, act_list, cent_list, lin_list)
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


#Función para crear el parámetro e_p_k como una matriz de valores binarios con
#las coincidencias de especialidad entre cada profesor y actividad...
def F_ematch_prof_act(mat_prof, mat_act):
    e = {}
    for elem_prof in mat_prof.keys():
        e[elem_prof] = {}
        for elem_act in range(0, len(mat_act)):
            if mat_prof[elem_prof]['Especialidad'] == mat_act[elem_act]['Especialidad']:
                e[elem_prof][int(elem_act)] = 1
            else:
                e[elem_prof][int(elem_act)] = 0
    return e;
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
    
    Conj_A = {}
    for j in cent_keys:
        Conj_A[j] = []
        for k in act_keys:
            if act_list[k]['Centro'] == j:
                if (act_list[k]['Tipo'] == 'Supervision'
                    or act_list[k]['Tipo'] == 'Examen'):
                    Conj_A[j].append(k)
    
    Conj_Sup = []
    for k in act_keys:            
        if act_list[k]['Tipo'] == 'Supervision':
            Conj_Sup.append(k)
    
    Conj_Ex = []
    for k in act_keys:
        if act_list[k]['Tipo'] == 'Examen':
            Conj_Ex.append(k)
    
    Conj_Corr = []
    for k in act_keys:
        if act_list[k]['Tipo'] == 'Correccion':
            Conj_Corr.append(k)
    
    Conj_P = {'EXTERNO': [], 'INTERNO': []}
    for p in prof_keys:
        for es in Conj_P.keys():
            if prof_list[p]['Estado'] == es:
                Conj_P[es].append(p)
    
    Conj_B = act_list
    
    Conj_Lin = {}
    for l in lin_list.keys():
        if lin_list[l] == 'Practica - I':
            Conj_Lin[l] = {'Supervision': 0, 'Correccion': 0, 'Practica': 'Practica - I'}
        elif lin_list[l] == 'Internado':
            Conj_Lin[l] = {'Supervision': 0, 'Correccion': [], 'Examen': 0, 'Practica': 'Internado'}
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
    
    Conj_E = {}
    for p in prof_keys:        
        Conj_E[p] = []
        for s in Conj_U.keys():
            contador_act = {'Supervision': 0, 'Correccion': 0, 'Examen': 0}
            for k in Conj_U[s]:
                if prof_list[p]['Especialidad'] == 'TODO':
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
                elif prof_list[p]['Especialidad'] != 'TODO':
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
                                        elif act_list[k]['Practica'] == 'Practica - II':
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
                                    elif act_list[k]['Practica'] == 'Practica - II':
                                        Conj_E[p].append(k)
        
    Conj_S = week_list
    #for s in range(len(week_list)):
    #    Conj_S[s] = week_list[s]
    
    T = {}
    C_b = {}
    C_t = {}
    for k in act_keys:
        T[k] = act_list[k]['Tiempo']
        C_b[k] = act_list[k]['Costo Base']
        C_t[k] = act_list[k]['Costo Traslado']
    
    D = {}
    S = {}
    H = {}
    for p in prof_keys:
        D[p] = prof_list[p]['Disponibilidad']
        S[p] = 1
        H[p] = 1
        
    data = {'prof_keys': prof_keys, 'cent_keys': cent_keys,
            'week_keys': week_keys, 'act_keys': act_keys,
            'Conj_U': Conj_U, 'Conj_A': Conj_A,
            'Conj_Sup': Conj_Sup, 'Conj_Ex': Conj_Ex, 'Conj_Corr': Conj_Corr,
            'Conj_E': Conj_E, 'Conj_B': Conj_B,
            'Conj_P': Conj_P, 'Conj_S': Conj_S, 'Conj_Lin': Conj_Lin,
            'T': T, 'D': D, 'S': S, 'H': H, 'C_b': C_b, 'C_t': C_t}
    
    for pth in path.keys():
        with open(path[pth], 'w') as outfile:
            json.dump(data[pth], outfile)        
    
    '''
    book = xlwt.Workbook(encoding='utf-8')
    
    h1 =  book.add_sheet("T(k)")
    h1.write(0,0,"k")
    h1.write(0,1,"T")
    
    h2 =  book.add_sheet("D,S,H")
    h2.write(0,0,"p")
    h2.write(0,1,"D")
    h2.write(0,2,"S")
    h2.write(0,3,"H")
    
    h3 =  book.add_sheet("U(k,s)")
    h3.write(0,0,"k")
    h3.write(0,1,"s")
    
    h4 = book.add_sheet("C(p,k)")
    h5 = book.add_sheet("Y,M(j)")
    row = 1
    for c in cent_list.keys():
        h5.write(row,0, c)
        h5.write(row,2, 500)
        row+=1
    
    h6 =  book.add_sheet("B(k,r,l)")
    h6.write(0,0,"k")
    h6.write(0,1,"r")
    h6.write(0,2,"l")        
    
    h7 = book.add_sheet("E(p,k)")
    for k in range(0, len(act_list)):
        h7.write(k+1,0,k)
    col = 1
    for p in prof_list.keys():
            h7.write(0,col,p)
            col+=1
    col = None
    
    for k in range(0, len(act_list)):        
        col_p = 1
        for p in prof_list.keys():            
            h7.write(k+1, col_p, ematch[p][k])
            col_p+=1
    
    h8 = book.add_sheet("Especialidades")
    Esp = []
    for p in cent_list.keys():
        Esp.append(cent_list[p]['Especialidad'])
    ESP = list(set(Esp))    
    for e in range(0, len(ESP)):
        h8.write(e+1,0, ESP[e])
    
    #
    m = 0
    for k in act_list:
        h6.write(m+1,0,m+1)
        if act_list[m]['Practica'] == 'Practica - I':
            h6.write(m+1,1,'Cuarto')
        elif act_list[m]['Practica'] == 'Practica - II':
            h6.write(m+1,1,'Cuarto')
        else:
            h6.write(m+1,1,act_list[m]['Practica'])
        
        h6.write(m+1,2,act_list[m]['Tipo'])
        h1.write(m+1,0,m+1)
        h1.write(m+1,1,act_list[m]['Tiempo'])
        h3.write(m+1,0,m+1)
        h3.write(m+1,1,act_list[m]['Centro'])
        h3.write(m+1,2,act_list[m]['Semana'])
        m+=1
    
    #
    n = 0
    for p in prof_list.keys():
        h2.write(n+1,0, p)
        h2.write(n+1,1, prof_list[p]['Disponibilidad'])
        h2.write(n+1,2, prof_list[p]['Max Sobrecarga'])
        h2.write(n+1,3, prof_list[p]['Costo Sobrecarga'])
        n+=1
    
    book.save('proy_files/prm.xls')    '''
######################################################