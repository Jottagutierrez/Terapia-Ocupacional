# -*- coding: utf-8 -*-

#Importar librerías y paquetes...
from gurobipy import *
import json
import settings as st
import model_export as mexp

#Obtener los parámetros guardados en archivos JSON...
T = json.load(open(st.param_path_list['T']))
    #Tiempo de la actividad 'k'... T = {actividad: tiempo}
D = json.load(open(st.param_path_list['D']))
    #Disponibilidad del profesor 'p'... D = {profesor: disponibilidad}
S = json.load(open(st.param_path_list['S']))
    #Sobrecarga máxima que acepta el profesor 'p'... S = {profesor: sobrecarga}
H = json.load(open(st.param_path_list['H']))
    #"Costo" por hora de sobrecarga... H = {profesor: "costo"/epsilon}
C_b = json.load(open(st.param_path_list['C_b']))
    #Costo base para cada actividad (aplica solo para profesores externos)...
    #C_b = {actividad: costo base}
C_t = json.load(open(st.param_path_list['C_t']))
    #Costo de traslado para cada actividad (aplica solo para profesores externos)...
    #C_t = {actividad: costo traslado}
Conj_U = json.load(open(st.param_path_list['Conj_U']))
    #Conjunto de actividades 'k' que se realizan en cada semana 's'...
    #U = {semana: [actividades]}
Conj_A = json.load(open(st.param_path_list['Conj_A']))
    #Conjunto de actividades 'k' de tipo 'supervisión' que se realizan en
    #el centro 'j'...
    #A = {centro: [actividades]
Conj_B = json.load(open(st.param_path_list['Conj_B']))
    #Conjunto con la información de cada actividad 'k'...
Conj_P = json.load(open(st.param_path_list['Conj_P']))
    #Conjunto de profesores, agrupados por INTERNOS o EXTERNOS...
Conj_S = json.load(open(st.param_path_list['Conj_S']))
    #Conjunto de actividades que son de tipo Examen y Supervision...
Conj_E = json.load(open(st.param_path_list['Conj_E']))
    #Conjunto de actividades 'k' que se le permite al profesor 'p' realizar
    #de acuerdo con el criterio de match de especialidades (cuando este es
    #pertinente: Correcciones, Examenes, actividades de Mención, etc.)...
    #E = {profesor: [actividades]}

prof_keys = json.load(open(st.param_path_list['prof_keys']))
    #listado de todos los profesores...
cent_keys = json.load(open(st.param_path_list['cent_keys']))
    #listado de todos los centros...
week_keys = json.load(open(st.param_path_list['week_keys']))
    #listado de todas las semanas en las que hay actividades...
act_keys = json.load(open(st.param_path_list['act_keys']))
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
            x_var_des[p][k] = m.addVar(vtype=GRB.BINARY, name="X[%s,%d]"%(p,k))            
            #Solo se crea la variable si se cumple la condición de
            #match de especialidad, lo cual está detallado en el conjunto E...            
x_var_des = dict( [(k,v) for k,v in x_var_des.items() if len(v)>0])
    #elimina las posiciones [p,k] vacías...
######################################################


#Definir las variables de estado...
    #Cantidad de horas de sobrecarga asignadas al profesor 'p' en la semana 's'...
y_var_est = {}
#for p in prof_keys:
for p in prof_keys:
    y_var_est[p] = {}
    for s in week_keys:
        y_var_est[p][s] = m.addVar(vtype=GRB.INTEGER, name="Y[%s,%s]"%(p,s))

    #Si el profesor 'p' visita/realiza una supervisión en el centro 'j'...
g_var_est = {}
for p in prof_keys:
    g_var_est[p] = {}
    for j in cent_keys:
        g_var_est[p][j] = m.addVar(vtype=GRB.BINARY, name="G[%s,%s]"%(p,j))
        
z_var_est = {}
for s in week_keys:
    z_var_est[s] = {}
    for j in cent_keys:
        z_var_est[s][j] = {}
        #for p in prof_keys:
        for p in Conj_P['EXTERNO']:
            z_var_est[s][j][p] = m.addVar(vtype=GRB.BINARY, name="Z[%s,%s,%s]"%(s,j,p))
######################################################


#Restricción/Condición 1 - Disponibilidad horaria de cada profesor...
for p in prof_keys:
    if D[p] != 'N/A':
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



#Restricción/Condición 6 - Verificación si el profesor 'p' realiza supervisiones
#o examenes en el centro 'j', en la semana 's'...
for s in week_keys:
    for j in cent_keys:
        for p in Conj_P['EXTERNO']:
            for k in Conj_U[str(s)]:
                if k in Conj_S:
                    try:
                        m.addConstr(x_var_des[p][k], GRB.LESS_EQUAL,
                                    z_var_est[s][j][p])
                    except KeyError:
                        pass
######################################################


#Función Objetivo...    
Obj={}
Obj['Arg_1'] = LinExpr()
Obj['Arg_1.1'] = LinExpr()
    #Primer argumento, que indica la suma de los costos por asignarle
    #a un profesor 'p' la actividad 'k'...
Obj['Arg_1.2'] = LinExpr()
Obj['Arg_2'] = LinExpr()
    #Segundo argumento, que indica el total de horas de sobrecarga asignadas
    #a los profesores...

for p in prof_keys:
    for k in act_keys:
        #if p in Conj_P['EXTERNO']:
            try:            
                Obj['Arg_1.1'].addTerms(C_b[str(k)], x_var_des[p][k])
            except KeyError:
                pass    
    for s in week_keys:
        for j in cent_keys:        
            try:
                Obj['Arg_1.2'].addTerms(C_t[str(k)], z_var_est[s][j][p])
            except KeyError:
                pass    
        #if p in Conj_P['INTERNO']:
            Obj['Arg_2'].addTerms(H[p], y_var_est[p][s])

Obj['Arg_1'].add(Obj['Arg_1.1'], 1)
Obj['Arg_1'].add(Obj['Arg_1.2'], 1)

Delta = 0.4
    #indicador de preferencia de un argumento por sobre el otro...

model_Objective = LinExpr()
model_Objective.add(Obj['Arg_1'], Delta)
model_Objective.add(Obj['Arg_2'], 1 - Delta)
    #Expresión lineal que reune ambos objetivos...

m.setObjective(model_Objective, GRB.MINIMIZE)
m.write('model_view.rlp')
m.optimize()
######################################################


#Visualización del resultado...

result_x = {}
result_tiempo = 0
for p in prof_keys:    
    for k in act_keys:        
        try:
            #print(x_var_des[p][k])
            var_name = "X[%s,%d]"%(p,k)
            v = m.getVarByName(var_name) 
            if v.x == 1:
                result_x[v.varName] = v.x                
                result_tiempo = result_tiempo + v.x * T[str(k)]
        except:
            pass        

result_y = {}    
for p in prof_keys:    
    for s in week_keys:        
        try:
            var_name = "Y[%s,%s]"%(p,s)
            v = m.getVarByName(var_name)            
            result_y[v.varName] = v.x
        except:
            pass

result_g = {}    
for p in prof_keys:    
    for j in cent_keys:
        try:
            var_name = "G[%s,%s]"%(p,j)
            v = m.getVarByName(var_name)            
            result_g[v.varName] = v.x
        except:
            pass

result_z = {}    
for p in prof_keys:    
    for j in cent_keys:
        for s in week_keys:
            try:
                var_name = "Z[%s,%s,%s]"%(s,j,p)
                v = m.getVarByName(var_name)            
                result_g[v.varName] = v.x
            except:
                pass

with open('model_result_X.txt', 'w') as outfile:
    json.dump(result_x, outfile)
with open('model_result_Y.txt', 'w') as outfile:
    json.dump(result_y, outfile)
with open('model_result_G.txt', 'w') as outfile:
    json.dump(result_g, outfile)
with open('model_result_Z.txt', 'w') as outfile:
    json.dump(result_z, outfile)

X = result_x
Y = result_y
G = result_g
Z = result_z

total_asignaciones = 0
for key in X.keys():
    total_asignaciones = total_asignaciones + X[key]

total_sobrecarga = 0
for key in Y.keys():
    total_sobrecarga = total_sobrecarga + Y[key]

total_profcentros = 0
for key in G.keys():
    total_profcentros = total_profcentros + G[key]

var_res={}
for v in m.getVars():
    if v.x == 1:
        var_res[v.varName]=v.x
with open('resultado1.txt', 'w') as file:
     file.write(json.dumps(var_res))


conteo = []
for p in prof_keys:
    for k in Conj_E[p]:
        conteo.append(k)
conteo = list(set(conteo))

print('Actividades asignadas: ' + str(total_asignaciones))
print('Hrs sobrecarga: ' + str(total_sobrecarga))
print('Centros: ' + str(total_profcentros))
print('Tiempo total demandado: ' + str(result_tiempo))
print(len(conteo))

mexp.F_export_model_results(Conj_B, Conj_U, X)

#######################


'''
lista = list(X.keys())
    
diccionario={}        
name=[]
activity=[]
for k in range(len(lista)):    
    key_1=str(lista[k]).replace('X[','')
    key_2=key_1.replace(']','')
    Nombre, Actividad= key_2.split(',')
    name.append(Nombre)
    activity.append(Actividad)
        

Profes=list(set(name))
for j in range(len(Profes)):
    diccionario[Profes[j]]=[]
    for e in range(len(name)): 
        if Profes[j] == name[e]:
            diccionario[Profes[j]].append(activity[e])


workbook = xlsxwriter.Workbook('Calendario.xlsx')

for docente in diccionario.keys():
    worksheet = workbook.add_worksheet(docente)

    row=0
    for s in Conj_U.keys(): #en todas las semanas posibles
        for k in Conj_U[s]: #en todas las actividades de esa semana
            for act in diccionario[docente]:#todas las atividades realizados por el profesor
                if k == int(act): #si la actividad realizada corresponde a las actividades realizadas esa semana
                    worksheet.write(row, 0, s)
                    worksheet.write(row, 1, act)
                    worksheet.write(row, 2,Conj_B[k]['Centro'])
                    row += 1
workbook.close()'''