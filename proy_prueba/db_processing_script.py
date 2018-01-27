# -*- coding: utf-8 -*-

#Importar librerías y paquetes...
import module_dbreader as dbr
import settings as st
import json
######################################################


#Abrir libro Excel y obtener las hojas de cálculo...            
xl_sheet = dbr.F_get_xl_sheets(st.DB_path)
######################################################


#Rescatar las matrices con la información de las Semanas, las Prácticas y de las
#Actividades desde Excel...
DATA_matrix_Weeks = dbr.F_translate_into_week(xl_sheet).week_L
DATA_matrix_Pract = dbr.F_translate_into_week(xl_sheet).pract_L
DATA_matrix_Act = dbr.F_translate_into_week(xl_sheet).act_L
DATA_matrix_Cent = dbr.F_translate_into_week(xl_sheet).cent_L
######################################################


#Rescatar matriz de profesores...
DATA_matrix_Prof = dbr.F_get_prof_data(xl_sheet['Profesores'])
######################################################

#Crear parámetro e_p_k (match entre especialidades profesor-actividad)...
#PARAM_ematch_PA = ini.F_ematch_prof_act(DATA_matrix_Prof, DATA_matrix_Act)
######################################################

#Escribir los parámetros en un archivo JSON...
dbr.F_create_param_file(DATA_matrix_Act, DATA_matrix_Prof, DATA_matrix_Cent,
                        DATA_matrix_Weeks, DATA_matrix_Pract,
                        st.param_path_list)
######################################################


Conj_E = json.load(open(st.param_path_list['Conj_E']))

'''
Tipo = []
for k in Conj_E['CB']:
    Tipo.append(DATA_matrix_Act[k]['Tipo'])
Tipo = list(set(Tipo))
print (Tipo)

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


B = {}
cont = 0
for j in N_est['Practica - I'].keys():
    suma = 0    
    if N_est['Practica - I'][j]['Especialidad'] == 'PEDIATRIA':
        cont = cont + 1
        for i in range (1,7):
            suma = suma + N_est['Practica - I'][j][i]
            B[j] = suma
B['AAA - Conteo'] = cont    
print(B)



Conj_E = json.load(open(param_path_list['Conj_E']))
prof_keys = json.load(open(param_path_list['prof_keys']))
conteo = []
for p in prof_keys:
    for k in Conj_E[p]:
        conteo.append(k)
conteo = list(set(conteo))
print(len(conteo))
'''