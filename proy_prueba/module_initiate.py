# -*- coding: utf-8 -*-
import collections
import xlrd

'''Función para abrir el libro de Excel y guardar las hojas de cálculo en un
diccionario...'''
def F_get_xl_sheets(path):
    book = xlrd.open_workbook(path)
    sheet = {}
    'sheet_arr = xl_book.sheet_names()'
    for s in book.sheet_names():
        sheet[s] = book.sheet_by_name(s)
    return sheet;
'------------------------------'

def F_translate_into_week(sheet_list):
    Result = collections.namedtuple('Result',['week_L','pract_L', 'num_est', 'act_list'])
    
    sheet_semanas = sheet_list['Info_Semanas']
    week_list = []
    for i in range(0, sheet_semanas.nrows-1):
        week_list.insert(i, {})
        for j in range(1,sheet_semanas.ncols):
            try:
                week_list[i][sheet_semanas.cell(0,j).value] = int(sheet_semanas.cell(i+1,j).value)
            except ValueError:
                week_list[i][sheet_semanas.cell(0,j).value] = str(sheet_semanas.cell(i+1,j).value)
    
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
        
    rot_info = {'Practica - I': 3, 'Practica - II': 3, 'Internado': 7, 'Mencion': 10}
    num_est = {}
    for p in rot_info.keys():
        num_est[p] = {}
        for k in range(3, sheet_list[p].nrows):
            num_est[p][sheet_list[p].cell(k,0).value] = {}
            num_est[p][sheet_list[p].cell(k,0).value]['Especialidad'] = str(sheet_list[p].cell(k,1).value)
            for i in range(2, sheet_list[p].ncols):
                num_est[p][sheet_list[p].cell(k,0).value][sheet_list[p].cell(2,i).value] = int(sheet_list[p].cell(k,i).value)
         
    act_list = []    
    T = {'Supervision': 1, 'Correccion': 1.5, 'Examen': 2}
    for p in rot_info.keys():
        current_rot = 0
        for i in range(pract_list[p]['Semana Inicio'], pract_list[p]['Semana Termino']+1, rot_info[p]):                
            if week_list[i]['Estado'] == 'Feriado':
                continue
            if p == 'Internado':
                sem_sup = i+1
                sem_corr = i+2
            elif p == 'Mencion':
                sem_sup = i+1
                sem_corr = i+2
            else:
                sem_sup = i+1
                sem_corr = i+2
            
            sem_sup = {'Practica - I': i+1, 'Practica - II': i+1, 'Internado': i+3, 'Mencion': i+5}
            sem_corr = {'Practica - I': i+2, 'Practica - II': i+2, 'Internado': [i+2, i+4], 'Mencion': i+6}
            sem_exam = {'Internado': i+6, 'Mencion': i+7}
            
            current_rot = current_rot + 1            
            for k in num_est[p].keys():
                for j in range(0, num_est[p][k][current_rot]):
                    act_list.append({'Practica': p,'Tipo': 'Supervision', 'Centro': k, 'Semana': sem_sup[p], 'Tiempo': T['Supervision']})
                    try:
                        for c in sem_corr[p]:
                            act_list.append({'Practica': p,'Tipo': 'Correccion', 'Centro': k, 'Semana': c, 'Tiempo': T['Correccion']})
                    except TypeError:
                        pass
                    try:
                        act_list.append({'Practica': p,'Tipo': 'Examen', 'Centro': k, 'Semana': sem_exam[p], 'Tiempo': T['Examen']})
                    except KeyError:
                        pass
    
    R = Result(week_list, pract_list, num_est, act_list)
                
    return R;

