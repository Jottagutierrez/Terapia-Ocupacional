# -*- coding: utf-8 -*-
#Se importan las librerías
from gurobipy import *
import xlrd
import pandas as pd
import json
#Se importan las hojas del excel
book = xlrd.open_workbook('prm.xls')
sheet_1 = book.sheet_by_index(0)
sheet_2 = book.sheet_by_index(1)
sheet_3 = book.sheet_by_index(2)
sheet_4 = book.sheet_by_index(3)
sheet_5 = book.sheet_by_index(4)
sheet_6 = book.sheet_by_index(5)
sheet_7 = book.sheet_by_index(6)
sheet_8 = book.sheet_by_index(7)


def Lista1(sheet):
    Var=[]
    for k in range(1,sheet.nrows):
        Var.append(sheet.cell(k,0).value)
    return Var

#Funcion para llamar variables de 1 subindice requiere la hoja de la variable y la columna
def parametro1int(sheet,col): 
    Var={}
    key=0
    for k in range(1,sheet.nrows):    
        key=int(sheet.cell(k,0).value)
        Var[key]=sheet.cell(k,col).value
    return Var

def parametro1str(sheet,col): 
    Var={}
    key=0
    for k in range(1,sheet.nrows):    
        key=str(sheet.cell(k,0).value)
        Var[key]=sheet.cell(k,col).value
    return Var

#Función para llamar variables de 2 subindices. Requiere solo la hoja de la variable
#Lee una matriz cruzada
def parametro2(sheet): 
    Var={}
    for k in range (1,sheet.nrows):
        key=sheet.cell(k,0).value
        Var[key]={}
        for i in range(1,sheet.ncols):
            Var[key][i] = sheet.cell(k,i).value
    return Var

def parametroE(sheet): 
    Var={}
    for i in range(1,sheet.ncols):
        key = sheet.cell(0,i).value
        Var[key]={}
        for k in range (1,sheet.nrows):
            key_1=int(sheet.cell(k,0).value) + 1       #Modificar el excel, llaves comienzan desde 0        
            Var[key][key_1] = sheet.cell(k,i).value
    return Var

def parametroB(sheet):
    Var = {}
    Tipo = ['Correccion','Supervision','Examen']
    Anos = ['Cuarto','Mencion','Internado']
    
    for k in range(1,sheet.nrows):
        Var[k]={}
        for a in Anos:
            Var[k][a]={}
            for t in Tipo:
                if sheet.cell(k,0).value == k and sheet.cell(k,1).value == a and sheet.cell(k,2).value == t:
                    Var[k][a][t] = 1
                else:
                    Var[k][a][t] = 0
    return Var


def parametroU(sheet):
    Var={}
    sem=[]    
    for s in range(1,sheet.nrows):
        sem.append(int(sheet.cell(s,2).value))
        
    Semanas_activas = list(set(sem))

    for s in range(len(Semanas_activas)):
        Var[Semanas_activas[s]]=[]
        for k in range(len(sem)):
            if int(sem[k]) == Semanas_activas[s]:
                Var[Semanas_activas[s]].append(sheet.cell(k+1,0).value)
            
    return Var

##Generación de parámetros en sus respectivas variables
T = parametro1int(sheet_1,1) #tiempo de realización de la actividad "k" en horas

D = parametro1str(sheet_2,1) #Disponibilidad horaria semanal del profesor "p"
N = parametro1str(sheet_2,2) #Holgura de cantidad de horas de sobrecarga profesor "P"
H = parametro1str(sheet_2,3) #Costo por hora de sobrecarga del profesor "p"

#   Y = parametro1str(sheet_5,1) #Puede mas de in profesor visitar el centro "j"? 1=si 0=no
M = parametro1str(sheet_5,2) # Numero de supervisiones totales que se realizan en el centro "j"

U = parametroU(sheet_3) #Que actividades se realizan la semana s.
#C = parametro2(sheet_4) # Costo de que el profesor "p" realice la actividad "k"
E = parametroE(sheet_7) # Si el profesor posee la misma specialidad de la actividad "k"

B = parametroB(sheet_6) # Tipo y año de la actividad "k"


#Hace un diccionario con llave los centros y valores son las actividades que se realizan en ese centro
Aj={}
for j in M.keys(): #Para cada centro
    Aj[j]=[]
    for k in range(1,sheet_3.nrows): #Para cada actividad
        if sheet_3.cell(k,1).value == j: #Si la actividad corresponde al centro
            Aj[j].append(k)           

##Prioridades y pesos de la función objetivo. Valores ejemplo
SetObjPriority = [3, 2]
SetObjWeight   = [1.0, 0.25]


##Crear Modelo
m = Model("modelo1")


##Largos
#Especialidades = Lista1(sheet_8)
P=len(D) #P: cantidad total de profesores 


semanas=[]
for i in range (1,sheet_3.nrows):
    semanas.append(int(sheet_3.cell(i,2).value))
S=max(semanas)

R=len(B[1])
L=len(B[1]['Cuarto'])
J =len(M)


    
## Variable de decision
x = {}
# Para cada profesor
for p in N.keys():
    # agregar una lista
    x[p]={}
    # para cada especialidad crear lista y añadir variable binaria. 1 si el profesor realiza la actividad k
    for k in B.keys():
        x[p][k]=m.addVar(vtype=GRB.BINARY, name="x[%s,%d]"%(p,k))
        
        
        
Z = {}
# Para cada profesor
for p in N.keys():
    # agregar una lista
    Z[p]={}
    # para cada especialidad crear lista y añadir variable binaria. 1 si el profesor realiza la actividad k
    for s in U.keys():
        Z[p][s]=m.addVar(vtype=GRB.BINARY, name="Z[%s,%d]"%(p,s))
        
        
        
G = {}
# Para cada profesor
for p in N.keys():
    # agregar una lista
    G[p]={}
    for j in Aj.keys():
        G[p][j]=m.addVar(vtype=GRB.BINARY, name="G[%s,%s]"%(p,j))
        
        

#Setea el objetivo del modelo
m.ModelSense = GRB.MINIMIZE



## Restricciones
#1. Capacidad profesor. Un profesor no puede realizar más actividades que su capacidad + holgura
for p in N.keys():    
    for s in U.keys():
        lexp = LinExpr()      
        for k in U[s]:
            for j in M.keys():                
                lexp.addTerms(T[k], x[p][k])                
        m.addConstr(lexp, GRB.LESS_EQUAL, D[p] + Z[p][s], name='C1')

        
##2. La cantidad de sobrecarga asignada debe ser menor o igual a la maxima carga extra
for p in N.keys():
    for s in U.keys():
        m.addConstr(Z[p][s], GRB.LESS_EQUAL, 150, name='C2')
                    
    
##3
for j in Aj.keys():
    for p in N.keys():
        for k in Aj[j]:
            for r in B[1].keys():
                if B[k][r]['Supervision'] == 1:            
                    m.addConstr(x[p][k], GRB.LESS_EQUAL, G[p][j], name= 'C3')

##4 no contiene a Yj todavía
for j in Aj.keys():
    lexp_4=LinExpr()
    for p in N.keys():
        lexp_4.addTerms(1.0, G[p][j]) 
    m.addConstr(lexp_4, GRB.LESS_EQUAL, 1, name= 'C4')
    

##5
for k in B.keys():
    lexp_5=LinExpr()
    for p in N.keys():
        lexp_5.addTerms(1.0, x[p][k])
    m.addConstr(lexp_5, GRB.EQUAL, 1, name= 'C5')

'''##6
for p in N:
    for k in B.keys():
        for r in B[1]:
            if B[k][r]['Correccion'] == 1:
            m.addConstr(x[p][k], GRB.LESS_EQUAL,E[p][k], name= 'C6')
##7
for p in N:
    for k in range(1,K+1):
        for r in B[1]:
            if B[k][r]['Examen'] == 1:
            m.addConstr(x[p][k], GRB.LESS_EQUAL, E[p][k], name= 'C7')
            '''


##Funcion Objetivo
Obj={}
Obj[0]=LinExpr()
Obj[1]=LinExpr()

for p in N.keys():
    for k in B.keys():
        Obj[0].addTerms(10, x[p][k])
    for s in U.keys():
        Obj[1].addTerms(H[p], Z[p][s])

for e in Obj.keys():
    m.setObjectiveN(Obj[e], e, SetObjPriority[e], SetObjWeight[e], name='Set' + str(e))

#Resolver Modelo
m.write('modelo.lp')
m.optimize()

df = pd.DataFrame(x)

'''
SUM_Valores = {}
for p in N.keys():
    SUM_Valores[p] = 0
    for i in B.keys():
        SUM_Valores[p]+=x[p][i].X
print (SUM_Valores)
'''

vars={}
for v in m.getVars():
    if v.x == 1:
        vars[v.varName]=v.x
       # print('%s %g' % (v.varName, v.x))
        
print('Obj: %g' % m.objVal)

with open('resultado1.txt', 'w') as file:
     file.write(json.dumps(vars))
     
     
     
     
'''
for k in range(1,K+1):
    lexp_5=LinExpr()
    for p in N:
        lexp_5.addTerms(1.0, x[p][k])
    m.addConstr(lexp_5, GRB.EQUAL, 1, name= 'C4')
    '''
    
#m.feasRelaxS(0, True, False, True);
#m.optimize()