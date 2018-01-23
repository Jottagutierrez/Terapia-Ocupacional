# -*- coding: utf-8 -*-

#Importar librerías y paquetes...
import module_initiate as ini
import json
######################################################


#Detallar todas las direcciones de los archivos...
files_folder_path = 'proy_files'
BD_path = files_folder_path + '/BD.xlsx'
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
######################################################


#Abrir libro Excel y obtener las hojas de cálculo...            
xl_sheet = ini.F_get_xl_sheets(BD_path)
######################################################


#Rescatar las matrices con la información de las Semanas, las Prácticas y de las
#Actividades desde Excel...
DATA_matrix_Weeks = ini.F_translate_into_week(xl_sheet).week_L
DATA_matrix_Pract = ini.F_translate_into_week(xl_sheet).pract_L
DATA_matrix_Act = ini.F_translate_into_week(xl_sheet).act_L
DATA_matrix_Cent = ini.F_translate_into_week(xl_sheet).cent_L
N_est = ini.F_translate_into_week(xl_sheet).est_L
######################################################


#Rescatar matriz de profesores...
DATA_matrix_Prof = ini.F_get_prof_data(xl_sheet['Profesores'])
######################################################


#Crear parámetro e_p_k (match entre especialidades profesor-actividad)...
#PARAM_ematch_PA = ini.F_ematch_prof_act(DATA_matrix_Prof, DATA_matrix_Act)
######################################################

#Escribir los parámetros en un archivo JSON...
ini.F_create_param_file(DATA_matrix_Act, DATA_matrix_Prof, DATA_matrix_Cent,
                        DATA_matrix_Weeks, DATA_matrix_Pract,
                        param_path_list)
######################################################

A = []
pi = 0
inter = 0
for k in range(0, len(DATA_matrix_Act)):    
    A.append(DATA_matrix_Act[k]['Practica'])
    if DATA_matrix_Act[k]['Practica'] == 'Practica - I':
        pi+=1
    elif DATA_matrix_Act[k]['Practica'] == 'Internado':
        inter+=1
A = list(set(A))
print(A)
print(pi)
print(inter)
print(pi + inter)

#
#A = json.load(open(param_path_list['S']))
