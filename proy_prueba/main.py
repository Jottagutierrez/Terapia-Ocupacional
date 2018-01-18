# -*- coding: utf-8 -*-

'Importar librerías y paquetes...'
from gurobipy import *
import module_functions as fn
import module_initiate as ini
'------------------------------'

'Abrir libro Excel y obtener las hojas de cálculo...'
xl_path = 'C:/Users/Gerardo/Python_Proyectos/Terapia-Ocupacional-master/Test_Nacho.xlsx'
xl_sheet = ini.F_get_xl_sheets(xl_path)

week = ini.F_translate_into_week(xl_sheet).week_L
pract = ini.F_translate_into_week(xl_sheet).pract_L
num_est = ini.F_translate_into_week(xl_sheet).num_est
act_list = ini.F_translate_into_week(xl_sheet).act_list


a = {'hola': 3, 'chao': 5, 'hello': 1}
b  = ['hola', 'chao', 'hello', 'bye']
for i in b:        
    try:
        print(a[i])
    except KeyError:        
        print('no')

print (num_est['ARETE'][1])
'------------------------------'

'Rescatar matriz de profesores...'
DATA_matrix_P = fn.F_get_prof_data(xl_sheet['Profesores'])
'------------------------------'

'Rescatar matriz de actividades...'
DATA_matrix_A = fn.F_get_act_data(xl_sheet['Actividad'])
'------------------------------'

'Crear parámetro e_p_k (match entre especialidades profesor-actividad)...'
PARAM_ematch_PA = fn.F_ematch_prof_act(DATA_matrix_P, DATA_matrix_A)
'------------------------------'