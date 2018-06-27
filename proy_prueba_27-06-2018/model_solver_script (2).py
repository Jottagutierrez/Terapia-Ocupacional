# -*- coding: utf-8 -*-
#Importar librerías y paquetes...
import gurobipy as gp
import json
import settings as st
import module_export as mexp
import pylab as pl
#import numpy as np

def listifyDict(a):
    # get keys and sort them
    k = list(a.keys())
    k = sorted(k)
    
    # make an array with sorted keys
    v = []
    for value in k:
        v.append(a[value])
    # return list
    return v

######################################################
#   PARAMETROS DEL MODELO
######################################################
#Obtener los parámetros guardados en archivos JSON...
    
fileName = str(st.result_folder_path + '/Calendario.xlsx')

T = json.load(open(st.param_path_list['T']))
    #Tiempo de la actividad 'k'... T = {actividad: tiempo}
    
D = json.load(open(st.param_path_list['D']))
    #Disponibilidad del profesor 'p'... D = {profesor: disponibilidad}
    
Conj_U = json.load(open(st.param_path_list['Conj_U']))
    #Conjunto de actividades 'k' que se realizan en cada semana 's'...
    #U = {semana: [actividades]}
    
Conj_Sup = json.load(open(st.param_path_list['Conj_Sup']))
    #Conjunto de actividades 'k' de tipo 'supervisión'
    #Sup = [actividades]
    
Conj_Ex = json.load(open(st.param_path_list['Conj_Ex']))
    #Conjunto de actividades 'k' de tipo 'examen'
    #Ex = [actividades]
    
Conj_Corr = json.load(open(st.param_path_list['Conj_Corr']))
    #Conjunto de actividades 'k' de tipo 'corrección'
    #Corr = [actividades]
    
Act_List = json.load(open(st.param_path_list['Act_List']))
    #Conjunto con la información de cada actividad 'k'...
    
Conj_P = json.load(open(st.param_path_list['Conj_P']))
    #Conjunto de profesores, agrupados por INTERNOS o EXTERNOS...
    
Week_List = json.load(open(st.param_path_list['Week_List']))
    #
    
Conj_E = json.load(open(st.param_path_list['Conj_E']))
    #Conjunto de actividades 'k' que se le permite al profesor 'p' realizar
    #de acuerdo con el criterio de match de especialidades (cuando este es
    #pertinente: Correcciones, Examenes, actividades de Mención, etc.)...
    #E = {profesor: [actividades]}
    
Conj_Lin = json.load(open(st.param_path_list['Conj_Lin']))
    #Conjunto de actividades que pertenecen a la misma "linea". Esto se refiere a
    #actividades que corresponden a la misma secuencia, para el mismo alumno, práctica,
    #rotativa y centro...

Conj_J = json.load(open(st.param_path_list['Conj_J']))
Conj_I = json.load(open(st.param_path_list['Conj_I']))

prof_keys = json.load(open(st.param_path_list['prof_keys']))
    #listado de todos los profesores...
    
cent_keys = json.load(open(st.param_path_list['cent_keys']))
    #listado de todos los centros...
    
cent_info = json.load(open(st.param_path_list['cent_info']))
    #información de la especialidad de todos los centros...

week_keys = json.load(open(st.param_path_list['week_keys']))
    #listado de todas las semanas en las que hay actividades...
    
act_keys = json.load(open(st.param_path_list['act_keys']))
    #listado de todas las actividades...

pr_info = ['Practica - I', 'Practica Profesional', 'Internado', 'Mencion']

deltaOptions = [.9]
#deltaOptions = [.1, .2, .3, .4, .44, .46, .5, .6, .7, .8, .9]
#deltaOptions = np.arange(0.02,1,0.02)
    #Lista de valores de Delta...

ROpt = {'Correccion': 'M', 'Examen': 'M', 'Plot': 'bx-'}
    #Arreglo con los parámetros para determinar si los exámenes y/o correcciones son
    #móviles o fijos...
    
mpc = 1 #máximo de profesores que pueden corregir en un centro

Mgap = .05

H = 10000
    #Ponderador de peso (va multiplicado al total/suma de horas de sobrecarga, con el
    #objetivo de que el valor resultante sea de la misma escala y comparable al total
    #de costo monetario por externalizaciones)...

#Variables de almacenamiento de resultados...
list_sobrecarga = {}
    #Lista con todos los totales de sobrecarga para los valores de delta propuestos...
list_costo = {}
    #Lista con todos los totales de costo por externalizaciones para los valores de delta propuestos...
######################################################


######################################################
#   MODELO
######################################################
#Loop que itera el modelo para cada valor de delta...

#Para cada valor de delta, se crea un arreglo/diccionario dentro de las variables
#de almacenamiento para guardar los resultados de cada iteración...

for deltaValue in deltaOptions:
    print("\n\nrunning model with delta=%f"%deltaValue)
    
    #Iniciar el modelo...
    m = gp.Model('modelo')
    ######################################################
    
    
    #Definir la variable de desición...
    #Si el profesor 'p' realiza la actividad 'k'...
    x_var_des = {}
    for p in prof_keys:
        x_var_des[p] = {}
        for k in Conj_E[p]:
            x_var_des[p][k] = m.addVar(vtype=gp.GRB.BINARY, name="X[%s,%d]"%(p,k))            
            #Solo se crea la variable si se cumple la condición de
            #match de especialidad, lo cual está detallado en el conjunto E...            
    x_var_des = dict( [(k,v) for k,v in x_var_des.items() if len(v)>0])
        #elimina las posiciones [p,k] vacías...
    ######################################################
    
    
    #Definir las variables de estado...
    #Cantidad de horas de sobrecarga asignadas al profesor 'p' en la semana 's'...
    y_var_est = {}
    for p in prof_keys:
    #for p in Conj_P['INTERNO']:
        y_var_est[p] = {}
        #for s in week_keys:
        for s in range(0, max(week_keys)+1):
            y_var_est[p][s] = m.addVar(vtype=gp.GRB.CONTINUOUS, name="Y[%s,%s]"%(p,s))
    
    #Si el profesor 'p' visita/realiza una supervisión en el centro 'j'...
    g_var_est = {}
    for p in prof_keys:
        g_var_est[p] = {}
        for j in cent_keys:
            g_var_est[p][j] = m.addVar(vtype=gp.GRB.BINARY, name="G[%s,%s]"%(p,j))
    
    #Si el profesor 'p' realiza correcciones de la práctica 'pr' en el centro 'j'...
    r_var_est = {}
    for j in cent_keys:
        r_var_est[j] = {}
        for pr in pr_info:
            r_var_est[j][pr] = {}
            for p in prof_keys:
                r_var_est[j][pr][p] = m.addVar(vtype=gp.GRB.BINARY, name="R[%s,%s,%s]"%(j,pr,p))
    
    #Cantidad de horas de sub-carga que tiene el profesor 'p' en la semana 's'...
    w_var_est = {}
    for p in prof_keys:
        w_var_est[p] = {}
        for s in range(0, max(week_keys)+1):
            w_var_est[p][s] = m.addVar(vtype=gp.GRB.CONTINUOUS, name="W[%s,%s]"%(p,s))
    
    ######################################################
    
    
    #Restricción/Condición 1 - Disponibilidad horaria de cada profesor...
    #for p in prof_keys:
    cond_1_check = {}
    for p in Conj_P['INTERNO']:
        cond_1_check[p] = {}
        if D[p] != 'N/A':
            for s in week_keys:
                cond_1_check[p][s] = gp.LinExpr()
                
                cond_1_sup = gp.LinExpr()
                cond_1_ex = gp.LinExpr()
                cond_1_corr = gp.LinExpr()
                
                cond_1_Fijo = gp.LinExpr()
                cond_1_Movil = gp.LinExpr()
                for k in Conj_U[str(s)]:
                    if k in Conj_Sup['Total']:
                        try:
                            cond_1_sup.addTerms(T[str(k)], x_var_des[p][k])
                        except KeyError:
                        #para el caso en que se busque en la llave 'k'
                        #dentro de la variable X y esta no exista...
                            pass
                    elif k in Conj_Ex['Total']:
                        try:
                            cond_1_ex.addTerms(T[str(k)], x_var_des[p][k])
                        except KeyError:
                        #para el caso en que se busque en la llave 'k'
                        #dentro de la variable X y esta no exista...
                            pass
                    elif k in Conj_Corr['Total']:
                        try:
                            cond_1_corr.addTerms(T[str(k)], x_var_des[p][k])
                        except KeyError:
                        #para el caso en que se busque en la llave 'k'
                        #dentro de la variable X y esta no exista...
                            pass
                
                #Determinar si las actividades con móviles o fijas (si se considerarán dentro de
                #la capacidad de las semanas adyacentes para poder sobrecargar)...
                if ROpt['Correccion'] == 'F':
                    cond_1_Fijo.add(cond_1_corr, 1)
                    #Correcciones Fijas...
                elif ROpt['Correccion'] == 'M':
                    cond_1_Movil.add(cond_1_corr, 1)
                    #Correcciones Móviles...
                if ROpt['Examen'] == 'F':
                    cond_1_Fijo.add(cond_1_ex, 1)
                elif ROpt['Examen'] == 'M':
                    cond_1_Movil.add(cond_1_ex, 1)
                cond_1_Movil.add(cond_1_sup, 1)
                
                m.addConstr(cond_1_Fijo, gp.GRB.LESS_EQUAL, D[p], name='')
                m.addConstr(cond_1_Movil, gp.GRB.LESS_EQUAL, D[p] - cond_1_Fijo
                            + y_var_est[p][s], name='')
                
                cond_1_check[p][s].add(cond_1_Fijo, 1)
                cond_1_check[p][s].add(cond_1_Movil, 1)
    ######################################################
    
    
    #Restricción/Condición 2 -
    cond_2_check = {}
    for p in prof_keys:
        cond_2_check[p] = {}
        for lin in Conj_Lin.keys():
            cond_2_check[p][lin] = {'CC': gp.LinExpr(), 'SE': gp.LinExpr()}
            #cond_2_check[p][lin] = {}
            if ((Conj_Lin[lin]['Practica'] == 'Internado') or
                Conj_Lin[lin]['Practica'] == 'Mencion'):
                try:
                    if ((Conj_Lin[lin]['Correccion'][0] in Conj_E[p]) and
                        (Conj_Lin[lin]['Correccion'][1] in Conj_E[p])):
                        m.addConstr(x_var_des[p][Conj_Lin[lin]['Correccion'][0]], gp.GRB.EQUAL,
                                    x_var_des[p][Conj_Lin[lin]['Correccion'][1]], name='')
                    else:
                        m.addConstr(x_var_des[p][Conj_Lin[lin]['Correccion'][0]], gp.GRB.EQUAL,
                                    0, name='')
                        m.addConstr(x_var_des[p][Conj_Lin[lin]['Correccion'][1]], gp.GRB.EQUAL,
                                    0, name='')
                    
                    cond_2_check[p][lin]['CC'].add(x_var_des[p][Conj_Lin[lin]['Correccion'][0]], 1)
                    cond_2_check[p][lin]['CC'].add(x_var_des[p][Conj_Lin[lin]['Correccion'][1]], 1)
                    
                    if ((Conj_Lin[lin]['Supervision'] in Conj_E[p]) and
                        (Conj_Lin[lin]['Examen'] in Conj_E[p])):
                        m.addConstr(x_var_des[p][Conj_Lin[lin]['Supervision']], gp.GRB.EQUAL,
                                    x_var_des[p][Conj_Lin[lin]['Examen']], name='')
                    else:
                        m.addConstr(x_var_des[p][Conj_Lin[lin]['Supervision']], gp.GRB.EQUAL,
                                    0, name='')
                        m.addConstr(x_var_des[p][Conj_Lin[lin]['Examen']], gp.GRB.EQUAL,
                                    0, name='')
                    
                    cond_2_check[p][lin]['SE'].add(x_var_des[p][Conj_Lin[lin]['Supervision']], 1)
                    cond_2_check[p][lin]['SE'].add(x_var_des[p][Conj_Lin[lin]['Examen']], 1)
                except KeyError:
                    pass
    ######################################################
    
    
    #Restricción/Condición 3.1 - Verificación de si el profesor 'p' visita al
    #centro 'j'...
    for j in cent_keys:
        for p in prof_keys:
            for k in Conj_Sup[j]:
                try:
                    m.addConstr(x_var_des[p][k], gp.GRB.LESS_EQUAL, g_var_est[p][j], name='')
                except KeyError:
                #para el caso en que se busque en la llave 'k'
                #dentro de la variable X y esta no exista...
                    pass
    ######################################################
    
    
    #Restricción/Condición 3.2 - Verificación de si el profesor 'p' corrige para
    #la práctica 'pr' en el centro 'j'...
    for j in cent_keys:
        for pr in pr_info:
            for k in Conj_Corr[j]:
                if (k in Conj_I[pr]):
                    for p in prof_keys:
                        try:
                            m.addConstr(x_var_des[p][k], gp.GRB.LESS_EQUAL, r_var_est[j][pr][p], name='')
                        except KeyError:
                        #para el caso en que se busque en la llave 'k'
                        #dentro de la variable X y esta no exista...
                            pass
    ######################################################
    
    
    #Restricción/Condición 4.1 - Restringir la cantidad de profesores que
    #realizan correcciones en cada centro 'j'...
    cond_4_check = {'Corr': {}, 'Sup': {}}
    term_regist = {}
    for j in cent_keys:
        term_regist[j] = {'4to': {}, '5to': {}}
        cond_4_check['Corr'][j] = {}
        cond_4_1_4to = gp.LinExpr()
        cond_4_1_5to = gp.LinExpr()
        for p in prof_keys:
            term_regist[j]['4to'][p] = 0
            term_regist[j]['5to'][p] = 0
        for pr in pr_info:
            for k in Conj_Corr[j]:
                if (k in Conj_I[pr]):
                    for p in prof_keys:
                        try:
                            if ((('Practica - I' in pr) or
                                ('Practica Profesional' in pr)) and
                                (term_regist[j]['4to'][p] != 1)):
                                cond_4_1_4to.addTerms(1, r_var_est[j][pr][p])
                                term_regist[j]['4to'][p] = 1
                            elif ((('Internado' in pr)or
                                  ('Mencion' in pr)) and
                                  (term_regist[j]['5to'][p] != 1)):
                                cond_4_1_5to.addTerms(1, r_var_est[j][pr][p])
                                term_regist[j]['5to'][p] = 1
                        except KeyError:
                            pass
        m.addConstr(cond_4_1_4to, gp.GRB.LESS_EQUAL, mpc, name='')
        m.addConstr(cond_4_1_5to, gp.GRB.LESS_EQUAL, mpc, name='')
            
        cond_4_check['Corr'][j]['4to'] = cond_4_1_4to
        cond_4_check['Corr'][j]['5to'] = cond_4_1_5to
    ######################################################
    
    
    #Restricción/Condición 4.2 - Restringir la cantidad de profesores que visitan
    #un centro 'j'...
    for j in cent_keys:
        cond_4_2 = gp.LinExpr()
        for p in prof_keys:
            cond_4_2.addTerms(1.0, g_var_est[p][j])
        m.addConstr(cond_4_2, gp.GRB.LESS_EQUAL, 1, name='')
        cond_4_check['Sup'][j] = cond_4_2
    ######################################################
    
    
    #Restricción/Condición 5 - Todas las actividades deben realizarse...
    cond_5_check = {}
    for k in act_keys:
        cond_5 = gp.LinExpr()
        for p in prof_keys:
            if k in Conj_E[p]:
                cond_5.addTerms(1.0, x_var_des[p][k])
        cond_5_check[k] = cond_5
        m.addConstr(cond_5, gp.GRB.EQUAL, 1, name='')
    ######################################################
    
    
    #Restricción/Condición 7 -
    
    cond_7_check = {}
    for s in range(0, max(week_keys)+1):  
        cond_7_check[str(s)] = {}
        for p in Conj_P['INTERNO']:
            cond_7_check[str(s)][p] = 0
            v1 = gp.LinExpr()
            v2 = m.addVar(name='maxvar', vtype = gp.GRB.CONTINUOUS)
            v3 = m.addVar(name='lexpvar', vtype = gp.GRB.CONTINUOUS,
                          lb = -gp.GRB.INFINITY)
            if str(s) in Conj_U.keys():
                for k in Conj_U[str(s)]:
                    if k in Conj_E[p]:
                        v1.addTerms(T[str(k)], x_var_des[p][k])
            else:
                #para cuando se intente acceder a Conj_U[s] y esa semana
                #no exista...
                v1.addConstant(0)
            m.addConstr(v3, gp.GRB.EQUAL, (D[p] - v1))
            m.addGenConstrMax(v2, [v3, 0])
            m.addConstr(w_var_est[p][s], gp.GRB.EQUAL, v2)
            cond_7_check[str(s)][p] = v3
    ######################################################


    #Restricción/Condición 8 - 
    for p in prof_keys:
        for s in range(1, max(week_keys)):
            #try:
            '''
            m.addConstr(y_var_est[p][s], gp.GRB.LESS_EQUAL,
                            w_var_est[p][s-1] + w_var_est[p][s+1])
            '''
            
            m.addConstr(y_var_est[p][s], gp.GRB.LESS_EQUAL,
                            w_var_est[p][s-1])
            #except KeyError:
            #    pass
        #try:
        #m.addConstr(y_var_est[p][0], gp.GRB.LESS_EQUAL, w_var_est[p][1])
        '''
        m.addConstr(y_var_est[p][max(week_keys)], gp.GRB.LESS_EQUAL,
                    w_var_est[p][max(week_keys)-1])'''
        #except KeyError:
        #    pass
    '''
    for p in prof_keys:
            for s in range(1, max(week_keys)):
                #try:            
                m.addConstr(w_var_est[p][s], gp.GRB.GREATER_EQUAL,
                                y_var_est[p][s-1] + y_var_est[p][s+1])
                #except KeyError:
                #    pass'''
    ######################################################
    
    
    #Función Objetivo...    
    Obj={}
    Obj['Arg_1'] = gp.LinExpr()
    Obj['Arg_1.1'] = gp.LinExpr()
        #Primer argumento, que indica la cantidad total de horas de actividades
        #no asignadas a los profesores internos...
    Obj['Arg_2'] = gp.LinExpr()
        #Segundo argumento, que indica el total de horas de sobrecarga asignadas
        #a los profesores internos...
    
    for p in prof_keys:
        for k in act_keys:
            if p in Conj_P['EXTERNO']:
                try:
                    Obj['Arg_1.1'].addTerms(T[str(k)], x_var_des[p][k])
                except KeyError:
                    pass    
        for s in week_keys:
            if p in Conj_P['INTERNO']:
                Obj['Arg_2'].addTerms(H, y_var_est[p][s])        
    Obj['Arg_1'].add(Obj['Arg_1.1'], H)
    
    model_Objective = gp.LinExpr()
    model_Objective.add(Obj['Arg_1'], deltaValue)
    model_Objective.add(Obj['Arg_2'], 1 - deltaValue)
        #Expresión lineal que reune ambos objetivos...
        #deltaValue indicador de preferencia de un argumento por sobre el otro...
    
    m.setObjective(model_Objective, gp.GRB.MINIMIZE)
    #m.setParam('OutputFlag', False)
    m.setParam('MIPGap', Mgap)
    m.write('model_view.lp')
    m.optimize()
                    
    if m.status != gp.GRB.status.OPTIMAL:
        print('\nError - Optimal not found')
    else:
        print('\nDone - Solution found')

    ######################################################


    #Visualización del resultado...
    
    result_x = {}
    result_tiempo = 0
    for p in prof_keys: 
        result_x[p] = []
        for k in act_keys:
            try:       
                v = x_var_des[p][k]
                if v.x > 0.5:
                    result_x[p].append(k)
                    if p in Conj_P['INTERNO']:
                        result_tiempo = result_tiempo + T[str(k)]
            except KeyError:
                pass
    #result_x = dict( [(k,v) for k,v in result_x.items() if len(v)>0])
    
    result_y = {}    
    for p in prof_keys:
        result_y[p] = {}
        for s in range(0, max(week_keys)+1):
            try:
                v = y_var_est[p][s]
                result_y[p][s] = v.x
            except:
                pass
    #result_y = dict( [(k,v) for k,v in result_y.items() if len(v)>0])
    
    result_g = {}    
    for p in prof_keys:
        result_g[p] = {}
        for j in cent_keys:
            try:
                v = g_var_est[p][j]
                if v.x > 0.5:
                    result_g[p][j] = v.x
            except:
                pass
    result_g = dict([(k,v) for k,v in result_g.items() if len(v)>0])
    
    result_r = {}
    for j in cent_keys:
        result_r[j] = {}
        for pr in pr_info:
            result_r[j][pr] = {}
            for p in prof_keys:
                try:
                    v = r_var_est[j][pr][p]
                    if v.x > 0.5:
                        result_r[j][pr][p] = v.x
                except:
                    pass
        result_r[j] = dict([(k,v) for k,v in result_r[j].items() if len(v)>0])
    result_r = dict([(k,v) for k,v in result_r.items() if len(v)>0])
    
    result_w = {}    
    for p in prof_keys:    
        result_w[p] = {}
        for s in range(0, max(week_keys)+1):
            try:
                v = w_var_est[p][s]
                if v.x >= 0:
                   result_w[p][s] = v.x
            except:
                pass
    #result_w = dict( [(k,v) for k,v in result_w.items() if len(v)>0])
    
    with open((st.result_folder_path + '/model_result_X.txt'), 'w') as outfile:
        json.dump(result_x, outfile)
    with open((st.result_folder_path + '/model_result_Y.txt'), 'w') as outfile:
        json.dump(result_y, outfile)
    with open((st.result_folder_path + '/model_result_G.txt'), 'w') as outfile:
        json.dump(result_g, outfile)
    
    X = result_x
    Y = result_y
    G = result_g
    W = result_w
    
    total_asignaciones = 0
    for p in X.keys():
        for k in X[p]:
            total_asignaciones = total_asignaciones + 1
    
    total_sobrecarga = 0
    for p in Y.keys():
        for s in Y[p].keys():
            total_sobrecarga = total_sobrecarga + Y[p][s]
    
    total_profcentros = 0
    for p in G.keys():
        for j in G[p].keys():
            total_profcentros = total_profcentros + G[p][j]
    
    ######################################
    
    print('Año: 2018')
    print('Delta: ' + str(deltaValue))
    print('Actividades asignadas: ' + str(total_asignaciones))
    print('Hrs sobrecarga: ' + str(total_sobrecarga))
    print('Centros: ' + str(total_profcentros))
    print('Tiempo total demandado: ' + str(result_tiempo))
    print('Horas no asignadas: ' + str(Obj['Arg_1'].getValue() / H))
    if m.status != gp.GRB.status.OPTIMAL:
        print ('Estado del modelo: No Optimo - ' + m.status)
    else:
        print ('Estado del modelo: Optimo')
    
    try:
        mexp.F_export_model_results(G, Act_List, Week_List, Conj_U, Conj_Lin, X, Y, W,
                                    week_keys, cent_keys, cent_info, fileName)
    except PermissionError:
        print('Cierre excel antes de continuar.')
    
    list_sobrecarga[deltaValue] = total_sobrecarga
    
    list_costo[deltaValue] = Obj['Arg_1'].getValue()
    ######################################

pl.plot(listifyDict(list_sobrecarga), listifyDict(list_costo), ROpt['Plot'])
pl.xlabel('Excedente profesores internos [hrs]')
pl.ylabel('Costo externalización [CLP]')

'''
#Checkear Restriccion 1
for p in prof_keys:
    for s in week_keys:
        try:
            if (cond_1_check[p][s].getValue() > (D[p] + W[p][s+1] + W[p][s-1] + 0.1)):
                print ('Profesor: ' + p + '; Semana: ' + str(s) + '; Asignación: ' + str(cond_1_check[p][s].getValue()))
        except KeyError:
            pass

#Checkear Restriccion 2
for p in prof_keys:
    for lin in Conj_Lin.keys():
        if ((cond_2_check[p][lin]['CC'].getValue() >= 0.1) and
            (cond_2_check[p][lin]['CC'].getValue() <= 1.9)):
            print('Profesor: ' + p + '; Linea: ' + str(lin) +'; Correcciones: '
                  + str(cond_2_check[p][lin]['CC'].getValue()))

for p in prof_keys:
    for lin in Conj_Lin.keys():
        if ((cond_2_check[p][lin]['SE'].getValue() >= 0.1) and
            (cond_2_check[p][lin]['SE'].getValue() <= 1.9)):
            print('Profesor: ' + p + '; Linea: ' + str(lin) +'; Correcciones: '
                  + str(cond_2_check[p][lin]['SE'].getValue()))

#Checkear Restriccion 4
for j in cent_keys:
    if (cond_4_check['Corr'][j]['4to'].getValue() >= 1.5):
        print('Centro: ' + j + '; Año: 4to; Profesores: ' + str(cond_4_check['Corr'][j]['4to'].getValue()))
    elif (cond_4_check['Corr'][j]['5to'].getValue() >= 1.5):
        print('Centro: ' + j + '; Año: 5to; Profesores: ' + str(cond_4_check['Corr'][j]['5to'].getValue()))

for j in cent_keys:
    print('Centro: ' + j + '; Profesores: ' + str(cond_4_check['Sup'][j].getValue()))

#Checkear Restriccion 7
for s in range(len(week_keys)+1):
    for p in Conj_P['INTERNO']:
        if p == 'JLL':
            print('Profesor: ' + p + '; Semana: ' + str(s+1) + '; D[p] - HRS: ' + str(cond_7_check[str(s)][p].x))
            #print(cond_7_check[str(s)][p].x)

###
for s in range(1, len(week_keys)+1):
    for p in Conj_P['INTERNO']:
        if W[p][s] < (Y[p][s-1] + Y[p][s+1]):
            print('Profesor: ' + p + '; Semana: ' + str(s+1) + '; Wps: ' + str(W[p][s]) + '; Yps-1: ' + str(Y[p][s-1]) + '; Yps+1: ' + str(Y[p][s+1]))

###
for s in range(1, len(week_keys)+1):
    for p in Conj_P['INTERNO']:
        if Y[p][s] > (W[p][s-1] + W[p][s+1]):
            print('Profesor: ' + p + '; Semana: ' + str(s+1) + '; Yps: ' + str(Y[p][s]) + '; Wps-1: ' + str(W[p][s-1]) + '; Wps+1: ' + str(W[p][s+1]))

#
Sem = np.arange(0,28,1)

p = 'JT'
pl.plot(Sem, listifyDict(result_w[p]), 'x')
pl.plot(Sem, listifyDict(result_y[p]), 'x')
for P in prof_keys:
    for s in result_w[P].keys():
        if (result_w[P][s] == result_y[P][s]) and (result_w[P][s]>0):
                print(s)
'''