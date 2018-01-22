import json
leer = json.loads(open('resultado.txt').read())


lista = list(leer.keys())

'''lista=[]
for i in lectura:
    key = str(i)
    lista.append(key)'''
    
diccionario={}    
lista_2=[]
name=[]
activity=[]
for k in range(len(lista)):
    if str(lista[k])[0]== 'x':
        key_1=str(lista[k]).replace('x[','')
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
