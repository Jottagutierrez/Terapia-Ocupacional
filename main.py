# -*- coding: utf-8 -*-

'Importar librerías y paquetes...'
from gurobipy import *
import module_functions as fn
import module_initiate as ini
#import pandas as pd
#import numpy as np
import xlwt as wt
'------------------------------'

'Abrir libro Excel y obtener las hojas de cálculo...'
xl_path = 'C:/Users/aleva/Test_Nacho.xlsx'
xl_sheet = ini.F_get_xl_sheets(xl_path)

week = ini.F_translate_into_week(xl_sheet).week_L
pract = ini.F_translate_into_week(xl_sheet).pract_L
num_est = ini.F_translate_into_week(xl_sheet).num_est
act_list = ini.F_translate_into_week(xl_sheet).act_list
'------------------------------'

'Rescatar matriz de profesores...'
Profesores = fn.F_get_prof_data(xl_sheet['Profesores'])
'------------------------------'
'Obtener llaves de la matriz de profesores y crear una lista con ellas...'
Profe = list()
for i in Profesores.keys():
    Profe.append(i)
'------------------------------'
'Crear un excel con distintas hojas...'
book = wt.Workbook(encoding="utf-8")

h1 =  book.add_sheet("B(k,r,l)")
h1.write(0,0,"k")
h1.write(0,1,"r")
h1.write(0,2,"l")

h2 =  book.add_sheet("T(k)")
h2.write(0,0,"k")
h2.write(0,1,"T")

h3 =  book.add_sheet("U(k,s)")
h3.write(0,0,"k")
h3.write(0,1,"s")

h4 =  book.add_sheet("D,S,H(p)")
h4.write(0,0,"p")
h4.write(0,1,"D")
h4.write(0,2,"S")
h4.write(0,3,"H")
'------------------------------'
'Rellenar hojas que dependen de la actividad como indice..'
m=0

for k in act_list:
    h1.write(m+1,0,m+1)
    h1.write(m+1,1,act_list[m]['Practica'])
    h1.write(m+1,2,act_list[m]['Tipo'])
    h2.write(m+1,0,m+1)
    h2.write(m+1,1,act_list[m]['Tiempo'])
    h3.write(m+1,0,m+1)
    h3.write(m+1,1,act_list[m]['Semana'])
    m+=1
'------------------------------'

'Rellenar hojas que dependen del profesor como llave...'    
n=0
for p in Profe:
    h4.write(n+1,0,Profe[n])
    h4.write(n+1,1,Profesores[p]['Disponibilidad'])
    h4.write(n+1,2,Profesores[p]['Max_Sobrecarga'])
    h4.write(n+1,3,Profesores[p]['Costo_Sobrecarga'])
    n+=1
'------------------------------'
'Guardar excel...'
book.save('prueba.xls')
'------------------------------'
    


   





'Rescatar matriz de actividades...'
DATA_matrix_A = fn.F_get_act_data(xl_sheet['Actividad'])
'------------------------------'

'Crear parámetro e_p_k (match entre especialidades profesor-actividad)...'
PARAM_ematch_PA = fn.F_ematch_prof_act(Profesores, DATA_matrix_A)
'------------------------------'