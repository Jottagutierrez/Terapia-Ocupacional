from gurobipy import *

##Ejemplo Multidict para subindice k
#preguntar como hacerlo con 2 subindices
Actividad, Tiempos, Especialidad, Visita = multidict({
  '1': [60, 1, 1],
  '2': [90, 2, 0],
  '3': [45, 5, 0],
  '4': [45, 3, 0],
  #...
  })

Realizacion = ({
  ('1', '1'): 1,
  ('1', '2'): 0,
  ('1', '3'): 0,
  ('2', '1'): 0,
  ('2', '2'): 1,
  #...
  })

Profesor, Disponibilidad, Sobrecarga, CostoSobrecarga, Especialidad, CostoProfesor = multidict({
  '1': [15, 2, 15000, 1, 15000],
  '2': [12, 2, 15000, 5, 15000],
  '3': [15, 1, 14000, 4, 15000],
  '4': [13, 3, 14000, 4, 15000],
  #...
  })


Centro, MaximoDocentes = multidict({
  '1': 2,
  '2': 3,
  '3': 5,
  '4': 2,
  #...
  })

#prioridades y pesos de la función objetivo. Valores ejemplo
SetObjPriority = [  3,    2,    2,   1]
SetObjWeight   = [1.0, 0.25, 1.25, 1.0]


#Crear Modelo
m = Model("modelo1")

## Parámetros listados con multidict
#Agregar los listados k=actividad, s=semana, p=profesor, j=Centro
T = m.addVar(Tiempos, name="T")          #Tiempo requerido para realizar la actividad "k".
E = m.addVar(Especialidad, name="E")     #Especialidad de la actividad "k".
V = m.addVar(Visita, name="V")           #Si la actividad "k" requiere de una visita al centro.
U = m.addVar(Realizacion, name="U")      #Si la actividad "k" se realiza en la semana "s".

D = m.addVar(Disponibilidad, name="D")   #Disponibilidad horaria del profesor "p".
S = m.addVar(Sobrecarga, name="S")       #Cantidad máx. de horas de sobrecarga que se pueden asignar al profesor "p".
H = m.addVar(CostoSobrecarga, name="H")  #Costo por hora de sobrecarga asignada al profesor "p".
E = m.addVar(Especialidad, name="E")     #Especialidad del profesor "p".
C = m.addVar(CostoProfesor, name="C")    #Costo de que el profesor "p" realice la actividad "k".

M = m.addVar(MaximoDocentes, name="M")  #Máximo de docentes que pueden visitar al centro "j".

##Variables de Decisión
P= len(Profesor)
K= len(Actividad)
#Preguntar como hacerla con 2 sub-indices, si es que no se hace así
X = m.addVar(P, K, vtype=GRB.BINARY)




#Variables de Estado (Crear restricciones pertinentes)




# Limit how many solutions to collect
model.setParam(GRB.Param.PoolSolutions, 100)
##Qué es esto?


##Restricciones




#Función Objetivo
m.ModelSense = GRB.MINIMIZE

obj={}

obj[0] = (sum(sum(X[p][k]*C[p] for k in range (K)) for p in range(P)) + sum(sum(Y[p][s]*H[p] for s in range(S)) for p in range(P)))
#obj[1] = #estudiar castigo por discordancia
obj[2] = (sum(sum(sum(W[p][k][q]) for p in range(P)) for k in range(K)) for q in range(Q))

for i in range(3):
    model.setObjectiveN(obj[i], i, SetObjPriority[i], SetObjWeight[i], name='Set' + str(i))

#abstol (float, optional): Absolute tolerance for the alternative objective. This initializes the ObjNAbsTol attribute for this objective.
#reltol (float, optional): Relative tolerance for the alternative objective. This initializes the ObjNRelTol attribute for this objective.






