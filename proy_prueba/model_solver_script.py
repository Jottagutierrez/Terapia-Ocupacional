# -*- coding: utf-8 -*-

#Importar librerías y paquetes...

from gurobipy import *
import json
from pprint import pprint

#Detallar todas las direcciones de los archivos...
files_folder_path = 'proy_files'
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


#Obtener los parámetros guardados en archivos JSON...
T = json.load(open(param_path_list['T']))
    #Tiempo de la actividad 'k'... T = {actividad: tiempo}
D = json.load(open(param_path_list['D']))
    #Disponibilidad del profesor 'p'... D = {profesor: disponibilidad}
S = json.load(open(param_path_list['S']))
    #Sobrecarga máxima que acepta el profesor 'p'... S = {profesor: sobrecarga}
H = json.load(open(param_path_list['H']))
    #"Costo" por hora de sobrecarga... H = {profesor: "costo"/epsilon}
C = json.load(open(param_path_list['C']))
    #Costo por subcontratación... C = {profesor: costo}

Conj_U = json.load(open(param_path_list['Conj_U']))
    #Conjunto de actividades 'k' que se realizan en cada semana 's'...
    #U = {semana: [actividades]}
Conj_A = json.load(open(param_path_list['Conj_A']))
    #Conjunto de actividades 'k' de tipo 'supervisión' que se realizan en
    #el centro 'j'...
    #A = {centro: [actividades]
Conj_E = json.load(open(param_path_list['Conj_E']))
    #Conjunto de actividades 'k' que se le permite al profesor 'p' realizar
    #de acuerdo con el criterio de match de especialidades (cuando este es
    #pertinente: Correcciones, Examenes, actividades de Mención, etc.)...
    #E = {profesor: [actividades]}

prof_keys = json.load(open(param_path_list['prof_keys']))
    #listado de todos los profesores...
cent_keys = json.load(open(param_path_list['cent_keys']))
    #listado de todos los centros...
week_keys = json.load(open(param_path_list['week_keys']))
    #listado de todas las semanas en las que hay actividades...
act_keys = json.load(open(param_path_list['act_keys']))
    #listado de todas las actividades...
######################################################


#Iniciar el modelo...
m = Model('modelo')
######################################################


#Definir la variable de desición...
#Si el profesor 'p' realiza la actividad 'k'...
x_var_des = {}
for p in prof_keys:
    x_var_des[p] = {}
    for k in act_keys:
        if k in Conj_E[p]:
            x_var_des[p][k] = m.addVar(vtype=GRB.BINARY, name="x_var_des[%s,%d]"%(p,k))
            #Solo se crea la variable si se cumple la condición de
            #match de especialidad, lo cual está detallado en el conjunto E...            
x_var_des = dict( [(k,v) for k,v in x_var_des.items() if len(v)>0])
    #elimina las posiciones [p,k] vacías...
######################################################


#Definir las variables de estado...
    #Cantidad de horas de sobrecarga asignadas al profesor 'p' en la semana 's'...
y_var_est = {}
for p in prof_keys:
    y_var_est[p] = {}
    for s in week_keys:
        y_var_est[p][s] = m.addVar(vtype=GRB.INTEGER, name="y_var_est[%s,%s]"%(p,s))

    #Si el profesor 'p' visita/realiza una supervisión en el centro 'j'...
g_var_est = {}
for p in prof_keys:
    g_var_est[p] = {}
    for j in cent_keys:
        g_var_est[p][j]=m.addVar(vtype=GRB.BINARY, name="g_var_est[%s,%s]"%(p,j))
######################################################


#Restricción/Condición 1 - Disponibilidad horaria de cada profesor...
for p in prof_keys:
    for s in week_keys:
        cond_1 = LinExpr()
        for k in Conj_U[str(s)]:            
            try:
                cond_1.addTerms(T[str(k)], x_var_des[p][k])
            except KeyError:
            #para el caso en que se busque en la llave 'k'
            #dentro de la variable X y esta no exista...
                pass
        m.addConstr(cond_1, GRB.LESS_EQUAL, D[p] + y_var_est[p][s], name='')
######################################################


#Restricción/Condición 2 - Sobrecarga permitida para cada profesor...
for p in prof_keys:
    for s in week_keys:
        m.addConstr(y_var_est[p][s], GRB.LESS_EQUAL, S[p], name='')
######################################################


#Restricción/Condición 3 - Verificación de si el profesor 'p' visita al
#centro 'j'...
for j in cent_keys:
    for p in prof_keys:
        for k in Conj_A[j]:            
            try:
                m.addConstr(x_var_des[p][k], GRB.LESS_EQUAL, g_var_est[p][j], name='')
            except KeyError:
            #para el caso en que se busque en la llave 'k'
            #dentro de la variable X y esta no exista...
                pass
######################################################


#Restricción/Condición 4 - Restringir la cantidad de profesores que visitan
#un centro 'j'...
for j in cent_keys:
    cond_4 = LinExpr()
    for p in prof_keys:
        cond_4.addTerms(1.0, g_var_est[p][j])
    m.addConstr(cond_4, GRB.LESS_EQUAL, 1, name='')
######################################################


#Restricción/Condición 5 - Todas las actividades deben realizarse...
for k in act_keys:
    cond_5 = LinExpr()
    for p in prof_keys:
        try:
            cond_5.addTerms(1.0, x_var_des[p][k])
        except KeyError:
        #para el caso en que se busque en la llave 'k'
        #dentro de la variable X y esta no exista...
            pass
    m.addConstr(cond_5, GRB.EQUAL, 1, name='')
######################################################


#Función Objetivo...    
Obj={}
Obj['Arg_1'] = LinExpr()
    #Primer argumento, que indica la suma de los costos por asignarle
    #a un profesor 'p' la actividad 'k'...
Obj['Arg_2'] = LinExpr()
    #Segundo argumento, que indica el total de horas de sobrecarga asignadas
    #a los profesores...

for p in prof_keys:
    for k in act_keys:
        try:
            Obj['Arg_1'].addTerms(C[p], x_var_des[p][k])
        except KeyError:
            pass
    for s in week_keys:
        Obj['Arg_2'].addTerms(H[p], y_var_est[p][s])

Delta = 0.4
    #indicador de preferencia de un argumento por sobre el otro...

model_Objective = LinExpr()
model_Objective.add(Obj['Arg_1'], Delta)
model_Objective.add(Obj['Arg_2'], 1 - Delta)
    #Expresión lineal que reune ambos objetivos...

m.setObjective(model_Objective, GRB.MINIMIZE)
m.optimize()
######################################################