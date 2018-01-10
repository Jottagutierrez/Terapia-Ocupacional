from gurobipy import *
import xlrd

book = xlrd.open_workbook('Matriz.xlsx')
first_sheet = book.sheet_by_index(0)

c0=[]
## Tabula el excel y recopila las especialidades sin repetir
 for k in range(first_sheet.ncols):
    c0[k] = [first_sheet.row_values(i)[k] for i in range(first_sheet.nrows) if first_sheet.row_values(i)[k]] #c0 es la tabulación del excel

especialidades=list(set(c0[2])) #transforma en lista el set de especialidades distintas
print(especialidades[1])



'''
count=0 
for e in range(0,len(especialidades)):
    for i in range(len(c0[2])):
        if c0[2][i]==especialidades[e]:
            print(especialidades[e])
            count=count+1
'''
            
      ##Contar cantidad de profesores con cierta especialidad      
count=[]
for e in range(0,len(especialidades)): #para cada especialidad
    cuenta=0 #creamos variable que empieza en cero
    for i in range(len(c0[2])): #para todos los profesores
        if c0[2][i]==especialidades[e]: #si la especialidad es igual a la especialidad e
            cuenta=cuenta+1 #contamos uno más
    count.append(cuenta) #agregar el numero de profesores de la especialidad e
print(count)


#Hacer vectores de profesores donde cada columna es la especialidad
Esp=[]
for e in range(0,len(especialidades)): #para cada especialidad
    Esp.append([]) #crea los 5 vectores de especialidades
    for i in range(len(c0[2])):#para todos los profesore
        if c0[2][i]==especialidades[e]: #si la especialidad es igual a la especialidad e
            Esp[e].append(c0[0][i]) #agregar al profesor correspondiente a ese vector
print(Esp)
    
    
#crea el modelo
m=Model('modelo2')

##Variable de decisión
P=5 #P: cantidad total de profesores 
K=4 #K: cantidad de especialidades diferentes
x = []
# Para cada profesor
for p in range(P):
    # agregar una lista
    x.append([])
    # para cada especialidad crear lista y añadir variable binaria. 1 si el profesor realiza la actividad k
    for k in range(K):
        x[p].append([])
        x[p][k]=m.addVar(vtype=GRB.BINARY, name="x[%d,%d]"%(p,k))
        ##x[p][k] = first_sheet.cell(p,k)
        
