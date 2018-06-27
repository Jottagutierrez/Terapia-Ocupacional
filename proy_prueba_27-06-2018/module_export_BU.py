# -*- coding: utf-8 -*-
import xlsxwriter
#from datetime import date
#import settings as st

######################################################
#   Función donde se crea la planilla excel con los resultados del modelo
#   incorporando las funciones de creación de hojas...
######################################################
def F_student_rotative(X, Conj_B, tb_pract, tb_act, prof, cent, rot):
    pract_info = {
            'Practica - I': ['Supervision', 'Correccion'],
            'Practica Profesional': ['Supervision', 'Correccion'],
            'Internado': ['Supervision', 'Correccion', 'Examen'],
            'Mencion': ['Supervision', 'Correccion', 'Examen']
            }
    est_count = []
    for act in X[prof]:
        if ((Conj_B[act]['Centro'] == cent) and (Conj_B[act]['Rotativa'] == rot)):
            for pr in pract_info.keys():
                if (pr == tb_pract):
                    for act_type in pract_info[pr]:
                        if (act_type == tb_act):
                            if ((Conj_B[act]['Practica'] == pr) and
                                (Conj_B[act]['Tipo'] == act_type)):
                                est_count.append((Conj_B[act]['Linea']))
    est_count = len(list(set(est_count)))
    return est_count

def F_cent_student_row(X, Conj_B, tb_pract, tb_act, prof, cent_asigned):
    cent_row = {}
    for cent in cent_asigned:
        cent_row[cent] = {}
        est_sum = 0
        for rot in range(1, 7):
            cent_row[cent][rot] = F_student_rotative(X, Conj_B, tb_pract, tb_act,
                    prof, cent, rot)
            est_sum = est_sum + cent_row[cent][rot]
        cent_row[cent]['Total'] = est_sum
    return cent_row

def F_export_model_results(G, Conj_B, Conj_U, Conj_S, Conj_Lin, X, Y, W,
                           week_keys, cent_keys, cent_info, fileName):    
    
    workbook = xlsxwriter.Workbook(str(fileName))
    
    cell_format = {'Normal': workbook.add_format(),
                   'Normal_Centered': workbook.add_format(),
                   'Title_Centered': workbook.add_format(),
                   'Title_BG_Centered_Yellow': workbook.add_format(),
                   'Title_BG_Centered_LightBlue': workbook.add_format(),
                   'Title_BG_Centered_LightLilac': workbook.add_format(),
                   'Title_BG_Centered_LightRed': workbook.add_format()}
    for f in cell_format.keys():
        cell_format[f].set_align('vcenter')
        cell_format[f].set_text_wrap()
        cell_format[f].set_border(1)
        if 'Title' in f:
            cell_format[f].set_bold()
        if 'Centered' in f:
            cell_format[f].set_align('center')
    cell_format['Title_BG_Centered_Yellow'].set_bg_color('#FFFF00')
    cell_format['Title_BG_Centered_LightBlue'].set_bg_color('#A9D0F5')
    cell_format['Title_BG_Centered_LightLilac'].set_bg_color('#D6BBE6')
    cell_format['Title_BG_Centered_LightRed'].set_bg_color('#E6BBBB')
    
    #   Crear la hoja con el resumen de los profesores que realizarán cada tipo
    #   de actividad por cada centro...
    worksheet = workbook.add_worksheet('Resumen Centros')
    worksheet.set_column(0, 1, 30)
    worksheet.set_column(2, 2, 15)
    worksheet.set_column(3, 5, 20)
    worksheet.merge_range(0, 0, 1, 0, 'Nombre CDP', cell_format['Title_BG_Centered_Yellow'])
    worksheet.merge_range(0, 1, 1, 1, 'Especialidad', cell_format['Title_BG_Centered_Yellow'])
    worksheet.merge_range(0, 2, 1, 2, 'Docente Supervisor', cell_format['Title_BG_Centered_Yellow'])
    worksheet.merge_range(0, 3, 0, 5, 'Docente Corrector', cell_format['Title_BG_Centered_Yellow'])
    worksheet.write(1, 3, '4to', cell_format['Title_BG_Centered_Yellow'])
    worksheet.write(1, 4, '5to', cell_format['Title_BG_Centered_Yellow'])
    worksheet.write(1, 5, 'Examen', cell_format['Title_BG_Centered_Yellow'])
    
    row = 2
    for c in cent_keys:
        worksheet.write(row, 0, c, cell_format['Normal'])
        c_esp = ''
        p_sup = []
        p_corr = {'4to': [], '5to': []}
        p_ex = []
        
        for esp in cent_info[c]:
            if 'COMUNITARIO' in esp:
                c_esp = 'COMUNITARIO'
            else:
                c_esp = esp
        for p in G.keys():
            if c in G[p].keys():
                p_sup.append(p)
        for p in X.keys():
            for act in X[p]:
                if Conj_B[act]['Centro'] == c:
                    if Conj_B[act]['Tipo'] == 'Correccion':
                        if (Conj_B[act]['Practica'] == 'Practica - I' or
                            Conj_B[act]['Practica'] == 'Practica Profesional'):
                            p_corr['4to'].append(p)
                        elif (Conj_B[act]['Practica'] == 'Internado' or
                            Conj_B[act]['Practica'] == 'Mencion'):
                            p_corr['5to'].append(p)
                    elif Conj_B[act]['Tipo'] == 'Examen':
                        p_ex.append(p)
                    p_corr['4to'] = list(set(p_corr['4to']))
                    p_corr['5to'] = list(set(p_corr['5to']))
                    p_ex = list(set(p_ex))
        worksheet.write(row, 1, c_esp, cell_format['Normal'])
        worksheet.write(row, 2, ', '.join(p_sup), cell_format['Normal'])
        worksheet.write(row, 3, ', '.join(p_corr['4to']), cell_format['Normal'])
        worksheet.write(row, 4, ', '.join(p_corr['5to']), cell_format['Normal'])
        worksheet.write(row, 5, ', '.join(p_ex), cell_format['Normal'])
        
        row+=1
    ######################################################
    
    #   Crear la hoja con la tabla resumen con las horas de excedente para cada
    #   profesor en cada semana...
    worksheet = workbook.add_worksheet('Excedente (hrs)')
    worksheet.write(0, 0, 'Semana')
    col=1
    for p in X.keys():
        if p != 'Externalizaciones':
            for s in range(0, max(week_keys)+1):
                try:
                    worksheet.write(s+1, col, Y[p][s])
                    '''
                    if (Y[p][s] > 0):
                        worksheet.write(s+1, col, Y[p][s])
                    elif (W[p][s] > 0):
                        worksheet.write(s+1, col, (-1 * W[p][s]))
                        '''
                except KeyError:
                    #worksheet.write(s+1, col, (-1 * W[p][s]))
                    pass
                worksheet.write(s+1,0, s+1)
            worksheet.write(0, col, p)
            col+=1
    '''        
    worksheet = workbook.add_worksheet('Subcarga (hrs)')
    worksheet.write(0, 0, 'Semana')
    col=1
    for p in X.keys():
        if p != 'Externalizaciones':
            for s in range(0, max(week_keys)+1):
                try:
                    worksheet.write(s+1, col, W[p][s])
                except KeyError:
                    pass
                worksheet.write(s+1,0, s+1)
            worksheet.write(0, col, p)
            col+=1'''
    ######################################################
    
    #   Crear las hojas con la asignación de actividades para cada profesor...
    for p in X.keys():
        worksheet = workbook.add_worksheet(p)
        
        worksheet.write(0, 0, 'Semana')
        worksheet.write(0, 1, 'Actividad')
        worksheet.write(0, 2, 'Tipo')
        worksheet.write(0, 3, 'Especialidad')
        worksheet.write(0, 4, 'Centro')
        worksheet.write(0, 5, 'Practica')
        worksheet.write(0, 6, 'Rotativa')
        
        row=1
        for s in Conj_U.keys(): #en todas las semanas posibles
            for k in Conj_U[s]: #en todas las actividades de esa semana
                for act in X[p]:#todas las atividades realizados por el profesor
                    if k == int(act): #si la actividad realizada corresponde a las actividades realizadas esa semana
                        worksheet.write(row, 0, (int(s)+1))
                        worksheet.write(row, 1, act)
                        worksheet.write(row, 2,Conj_B[k]['Tipo'])
                        worksheet.write(row, 3,', '.join(Conj_B[k]['Especialidad']))
                        worksheet.write(row, 4,Conj_B[k]['Centro'])
                        worksheet.write(row, 5,Conj_B[k]['Practica'])
                        worksheet.write(row, 6,Conj_B[k]['Rotativa'])
                        row += 1
        
        
        row = 0
        col = 9
        worksheet.set_column(col, col, 11)
        worksheet.write(row+2, col, 'Semana', cell_format['Normal_Centered'])
        
        worksheet.merge_range(row+2, col, row+4, col, '4to Año', cell_format['Title_BG_Centered_LightBlue'])
        worksheet.merge_range(row+5, col, row+6, col, 'Actividades', cell_format['Title_BG_Centered_LightLilac'])
        worksheet.write(row+4, col+1, '1er Aux + Induccion', cell_format['Title_BG_Centered_LightLilac'])
        worksheet.write(row+4, col+22, 'Inducc.', cell_format['Title_BG_Centered_LightLilac'])
        worksheet.write(row+5, col+1, 'Supervision', cell_format['Title_Centered'])
        worksheet.write(row+6, col+1, 'Correccion', cell_format['Title_Centered'])
        
        worksheet.merge_range(row+10, col, row+12, col, '5to Año', cell_format['Title_BG_Centered_LightRed'])
        worksheet.merge_range(row+13, col, row+15, col, 'Actividades', cell_format['Title_BG_Centered_LightLilac'])
        worksheet.write(row+12, col+1, 'Induccion', cell_format['Title_BG_Centered_LightLilac'])
        worksheet.write(row+13, col+1, 'Supervision', cell_format['Title_Centered'])
        worksheet.write(row+14, col+1, 'Correccion', cell_format['Title_Centered'])
        worksheet.write(row+15, col+1, 'Examen', cell_format['Title_Centered'])
        
        worksheet.merge_range(row+2, col+1, row+2, col+19, 'Practica - I', cell_format['Title_BG_Centered_LightBlue'])
        worksheet.merge_range(row+2, col+22, row+2, col+40, 'Practica Profesional', cell_format['Title_BG_Centered_LightBlue'])
        worksheet.merge_range(row+10, col+1, row+10, col+29, 'Internado', cell_format['Title_BG_Centered_LightRed'])
        worksheet.merge_range(row+10, col+30, row+11, col+39, 'Mencion', cell_format['Title_BG_Centered_LightLilac'])
        worksheet.merge_range(row+2, col+20, row+6, col+21, 'VACACIONES', cell_format['Title_BG_Centered_LightLilac'])
        
        col = 11
        current_col = col
        rot = ['Rotativa I - PI', 'Rotativa II - PI', 'Rotativa III - PI', 'Rotativa IV - PI',
               'Rotativa V - PI', 'Rotativa VI - PI']
        for r in rot:
            worksheet.merge_range(row+3, current_col, row+3, current_col+2, r, cell_format['Title_BG_Centered_LightLilac'])
            worksheet.write(row+4, current_col, 1, cell_format['Title_Centered'])
            worksheet.write(row+4, current_col+1, 2, cell_format['Title_Centered'])
            worksheet.write(row+4, current_col+2, 3, cell_format['Title_Centered'])
            current_col = current_col + 3
        
        col = 11
        current_col = col
        rot = ['Internado I', 'Internado II', 'Internado III', 'Internado IV']
        for r in rot:
            worksheet.merge_range(row+11, current_col, row+11, current_col+6, r, cell_format['Title_BG_Centered_LightLilac'])
            worksheet.write(row+12, current_col, 1, cell_format['Title_Centered'])
            worksheet.write(row+12, current_col+1, 2, cell_format['Title_Centered'])
            worksheet.write(row+12, current_col+2, 3, cell_format['Title_Centered'])
            worksheet.write(row+12, current_col+3, 4, cell_format['Title_Centered'])
            worksheet.write(row+12, current_col+4, 5, cell_format['Title_Centered'])
            worksheet.write(row+12, current_col+5, 6, cell_format['Title_Centered'])
            worksheet.write(row+12, current_col+6, 7, cell_format['Title_Centered'])
            current_col = current_col + 7
        
        col = 32
        current_col = col
        rot = ['Rotativa I - PP', 'Rotativa II - PP', 'Rotativa III - PP', 'Rotativa IV - PP',
               'Rotativa V - PP', 'Rotativa VI - PP']
        for r in rot:
            worksheet.merge_range(row+3, current_col, row+3, current_col+2, r, cell_format['Title_BG_Centered_LightLilac'])
            worksheet.write(row+4, current_col, 1, cell_format['Title_Centered'])
            worksheet.write(row+4, current_col+1, 2, cell_format['Title_Centered'])
            worksheet.write(row+4, current_col+2, 3, cell_format['Title_Centered'])
            current_col = current_col + 3
        
        col = 39
        for i in range(10):
            worksheet.write(row+12, col+i, i+1, cell_format['Title_Centered'])
        
        
        row = 21
        
        rot_info = {'Practica - I': 6, 'Practica Profesional': 6, 'Internado': 4, 'Mencion': 1}
        
        table_list = {'Practica - I (Supervision)': {'Practica': 'Practica - I', 'Actividad': 'Supervision'},
                      'Practica - I (Correccion)': {'Practica': 'Practica - I', 'Actividad': 'Correccion'},
                      'Practica Profesional (Supervision)': {'Practica': 'Practica Profesional', 'Actividad': 'Supervision'},
                      'Practica Profesional (Correccion)': {'Practica': 'Practica Profesional', 'Actividad': 'Correccion'},
                      'Internado (Supervision)': {'Practica': 'Internado', 'Actividad': 'Supervision'},
                      'Internado (Correccion)': {'Practica': 'Internado', 'Actividad': 'Correccion'},
                      'Internado (Examen)': {'Practica': 'Internado', 'Actividad': 'Examen'},
                      'Mencion (Supervision)': {'Practica': 'Mencion', 'Actividad': 'Supervision'},
                      'Mencion (Correccion)': {'Practica': 'Mencion', 'Actividad': 'Correccion'},
                      'Mencion (Examen)': {'Practica': 'Mencion', 'Actividad': 'Examen'}}
        
        cent_asigned = []
        for act in X[p]:
            cent_asigned.append(Conj_B[act]['Centro'])
        cent_asigned = list(set(cent_asigned))
        
        worksheet.set_column(10, 10, 40)
        for tb in table_list.keys():
            col = 10
            
            cent_row = F_cent_student_row(X, Conj_B, table_list[tb]['Practica'],
                                          table_list[tb]['Actividad'], p, cent_asigned)
            total_tb = 0
            for cent in cent_row.keys():
                total_tb = total_tb + cent_row[cent]['Total']
            
            for pr in rot_info.keys():
                if ((total_tb > 0) and (pr in tb)):
                    worksheet.write(row, col, tb, cell_format['Title_BG_Centered_LightBlue'])
                    worksheet.write(row+1, col, 'Centros/Rotativa', cell_format['Title_BG_Centered_LightBlue'])
                    worksheet.merge_range(row, col+1, row, col+rot_info[pr], 'Alumnos por Rotativa', cell_format['Title_BG_Centered_LightBlue'])
                    for i in range(1, rot_info[pr]+1):
                        worksheet.write(row+1, col+i, i, cell_format['Title_BG_Centered_LightBlue'])
                    worksheet.merge_range(row, col+rot_info[pr]+1, row+1, col+rot_info[pr]+1, 'Total por Centro', cell_format['Title_BG_Centered_LightBlue'])
                    worksheet.merge_range(row, col+rot_info[pr]+2, row+1, col+rot_info[pr]+2, 'Total', cell_format['Title_BG_Centered_LightBlue'])
                    row+=2
                    
                    row_i = row
                    
                    cent_count = 0
                    for cent in cent_row.keys():
                        if (cent_row[cent]['Total'] > 0):
                            cent_count+=1
                            worksheet.write(row, col, cent, cell_format['Normal_Centered'])
                            for rot in range(1, rot_info[pr]+1):
                                worksheet.write(row, col+rot, cent_row[cent][rot], cell_format['Normal_Centered'])
                            worksheet.write(row, col+rot_info[pr]+1, cent_row[cent]['Total'], cell_format['Normal_Centered'])
                            row+=1
                    if (cent_count > 1):
                        worksheet.merge_range(row_i, col+rot_info[pr]+2, row-1, col+rot_info[pr]+2, total_tb, cell_format['Normal_Centered'])
                    else:
                        worksheet.write(row_i, col+rot_info[pr]+2, total_tb, cell_format['Normal_Centered'])
                    row+=1
    ######################################################
    
    workbook.close()