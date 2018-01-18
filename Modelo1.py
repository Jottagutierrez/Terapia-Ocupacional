#Se importan las librerías
from gurobipy import *
import xlrd

#Se importan las hojas del excel
book = xlrd.open_workbook('Modelo1_db.xlsx')
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
def parametro1(sheet,col): 
    Var={}
    key=0
    for k in range(1,sheet.nrows):
        key=sheet.cell(k,0).value
        Var.setdefault(key,[])
        Var[key].append(sheet.cell(k,col).value)
    return Var

#Función para llamar variables de 2 subindices. Requiere solo la hoja de la variable
#Lee una matriz cruzada
def parametro2(sheet): 
    Var={}
    key=0
    for k in range (1,sheet.nrows):
        key=sheet.cell(k,0).value
        Var.setdefault(key,[])
        for i in range(1,sheet.ncols):
            cell=sheet.cell(k,i)
            Var[key].append(cell.value)
    return Var

'''#Función para llamar el parámetro B
#Tabula el año y el tipo de practica como un vector tridimensional
#Usa como llave el numero de la práctica
def parametroB(sheet):
    Var={}
    key=0
    for k in range(1,sheet.nrows):
        key=int(sheet.cell(k,0).value)
        Var[key]=[]
        
        if sheet.cell(k,1).value == 'Supervision':
            Var[key].append([])
            Var[key].append([0,0,0])
            Var[key].append([0,0,0])
            if sheet.cell(k,2).value == 'Cuarto':
                Var[key][0].append(1)
                Var[key][0].append(0)
                Var[key][0].append(0)
            elif sheet.cell(k,2).value == 'Mencion':
                Var[key][0].append(0)
                Var[key][0].append(1)
                Var[key][0].append(0)
            elif sheet.cell(k,2).value == 'Internado':
                Var[key][0].append(0)
                Var[key][0].append(0)
                Var[key][0].append(1)
                
        if sheet.cell(k,1).value == 'Correccion':
            Var[key].append([0,0,0])
            Var[key].append([])
            Var[key].append([0,0,0])
            if sheet.cell(k,2).value == 'Cuarto':
                Var[key][1].append(1)
                Var[key][1].append(0)
                Var[key][1].append(0)
            elif sheet.cell(k,2).value == 'Mencion':
                Var[key][1].append(0)
                Var[key][1].append(1)
                Var[key][1].append(0)
            elif sheet.cell(k,2).value == 'Internado':
                Var[key][1].append(0)
                Var[key][1].append(0)
                Var[key][1].append(1)
                    
        if sheet.cell(k,1).value == 'Examen':
            Var[key].append([0,0,0])
            Var[key].append([0,0,0])
            Var[key].append([])
            if sheet.cell(k,2).value == 'Cuarto':
                Var[key][2].append(1)
                Var[key][2].append(0)
                Var[key][2].append(0)
            elif sheet.cell(k,2).value == 'Mencion':
                Var[key][2].append(0)
                Var[key][2].append(1)
                Var[key][2].append(0)
            elif sheet.cell(k,2).value == 'Internado':
                Var[key][2].append(0)
                Var[key][2].append(0)
                Var[key][2].append(1)
    return Var'''

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


#Funcion para llamar la variable U (realizaccion de la actividad k en la semana s)
#Transforma la semana s en un vector del tamaño del horizonte de semanas donde la semana de realización vale 1
def parametroU(sheet):
    Var={}
    key=0
    semanas=[]
    for i in range (1,sheet_3.nrows):
        semanas.append(int(sheet_3.cell(i,1).value))
    s_max=max(semanas)
    
    for k in range(1,sheet_3.nrows):
        key=int(sheet_3.cell(k,0).value)
        Var[key]=[]    
        sem=semanas[k-1]
        for s in range(s_max):
            if sem-1 == s:
                Var[key].append(1)
            else:
                Var[key].append(0)
    return Var


##Generación de parámetros en sus respectivas variables
T = parametro1(sheet_1,1) #tiempo de realización de la actividad "k" en horas

D = parametro1(sheet_2,1) #Disponibilidad horaria semanal del profesor "p"
S = parametro1(sheet_2,2) #Holgura de cantidad de horas de sobrecarga profesor "P"
H = parametro1(sheet_2,3) #Costo por hora de sobrecarga del profesor "p"

Y = parametro1(sheet_5,1) #Puede mas de in profesor visitar el centro "j"? 1=si 0=no
M = parametro1(sheet_5,2) # Numero de supervisiones totales que se realizan en el centro "j"

U = parametroU(sheet_3) # 1 si la actividad "k" se realiza en la semana "s"
C = parametro2(sheet_4) # Costo de que el profesor "p" realice la actividad "k"
E = parametro2(sheet_7) # Si el profesor posee la misma specialidad de la actividad "k"

B = parametroB(sheet_6) # Tipo y año de la actividad "k"



##Prioridades y pesos de la función objetivo. Valores ejemplo
SetObjPriority = [  3,    2]
SetObjWeight   = [1.0, 0.25]


##Crear Modelo
m = Model("modelo1")


##Largos
Especialidades = Lista1(sheet_8)
P=len(D) #P: cantidad total de profesores 
K=len(Especialidades) #K: cantidad de especialidades diferentes

semanas=[]
for i in range (1,sheet_3.nrows):
    semanas.append(int(sheet_3.cell(i,1).value))
S=max(semanas)

R=len(B[1]['Internado'])

    
## Variable de decision
x = []
# Para cada profesor
for p in range(P):
    # agregar una lista
    x.append([])
    # para cada especialidad crear lista y añadir variable binaria. 1 si el profesor realiza la actividad k
    for k in range(K):
        x[p].append([])
        x[p][k]=m.addVar(vtype=GRB.BINARY, name="x[%d,%d]"%(p,k))

#Setea el objetivo del modelo
m.ModelSense = GRB.MINIMIZE


## Restricciones
#1. Capacidad profesor. Un profesor no puede realizar más actividades que su capacidad + holgura
for p in range(P):
    for s in range(S):
        lexp = LinExpr()
        rhs_1 = D[p]+Z[p][s]
        for k in range(K):
            lexp.addTerms(1.0, U[k][s]*T[k]*x[p][k])
        m.addConstr(lexp, GRB.LESS_EQUAL, rhs_1, name='')
        
        
##2. La cantidad de sobrecarga asignada debe ser menor o igual a la maxima carga extra
for p in range(P):
    for s in range(S):
        lexp_2=LinExpr()
        lexp_2.add(Z[p][s])
        m.addConstr(lexp_2, GRB.LESS_EQUAL, D[p], name='')
        
##3.1
for j in range(J):
    for p in range(P):
        lexp_1 = LinExpr()
        for k in range(K):
            for r in range(R):
                lexp.addTerms(1.0,B[k][r]['Supervision']*x[p][k])
        m.addConstr(lexp_1,GRB.LESS_EQUAL,100*G[p][j], name='')
            
    













###
## 3. each patient can have surgery at most once
    for i in range(I):
        # for each patient add a constraint
        lexp = gp.LinExpr()
        for j in range(J):
            for k in x[i][j].keys():
                for t in x[i][j][k].keys():
                    lexp.addTerms(1.0, x[i][j][k][t])
        # add constraints
        orMo.addConstr(lexp, gp.GRB.LESS_EQUAL, 1.0, "patient[%d]"%(i))











