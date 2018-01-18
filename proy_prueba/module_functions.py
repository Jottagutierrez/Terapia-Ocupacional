# -*- coding: utf-8 -*-
import collections

'''Función para la obtención de la matriz de profesores desde la hoja de cálculo
de Excel...'''
def F_get_prof_data(xls_sheet):
    mat={}
    key=[]
    for i in range(1,xls_sheet.nrows):
        key.insert(i-1, str(xls_sheet.cell(i,0).value))
        for r in range(0,len(key)):
            mat[str(key[r])] = {}
            for i in range(1,xls_sheet.ncols):            
                mat[str(key[r])][str(xls_sheet.cell(0,i).value)] = xls_sheet.cell(r+1,i).value                
    return mat;
'------------------------------'

'''Función para la obtención de la matriz de actividades desde la hoja de cálculo
de Excel...'''
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
'------------------------------'

'''Función para crear el parámetro e_p_k como una matriz de valores binarios con
as coincidencias de especialidad entre cada profesor y actividad...'''
def F_ematch_prof_act(mat_prof, mat_act):
    e = {}
    for elem_prof in mat_prof:
        e[elem_prof] = {}
        for elem_act in mat_act:
            if mat_prof[elem_prof]['Especialidad'] == mat_act[elem_act]['Especialidad']:
                e[elem_prof][float(elem_act)] = 1
            else:
                e[elem_prof][float(elem_act)] = 0
    return e;
'------------------------------'

'''Función para crear los parámetros D_p (disponibilidad de cada profesor)
y S_p (máx. horas de sobrecarga por profesor) desde la matriz de profesores...'''
def F_get_profrelated_params (mat_prof):
    D = {}
    S = {}
    
'------------------------------'