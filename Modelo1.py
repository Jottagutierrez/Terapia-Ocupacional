from gurobipy import *
import xlrd

#Arreglos de parámetros
book = xlrd.open_workbook('Modelo1_db.xlsx')
sheet_1 = book.sheet_by_index(0)
sheet_2 = book.sheet_by_index(1)
sheet_3 = book.sheet_by_index(2)
sheet_4 = book.sheet_by_index(3)
sheet_5 = book.sheet_by_index(4)
sheet_6 = book.sheet_by_index(5)
sheet_7 = book.sheet_by_index(6)


def parametro1(sheet,col):
    Var={}
    key=0
    for k in range(1,sheet.nrows):
        key=sheet.cell(k,0).value
        Var.setdefault(key,[])
        Var[key].append(sheet.cell(k,col).value)
    return Var


def parametro2(sheet):
    Var={}
    key=0
    for k in range (1,sheet.nrows):
        if sheet.cell(k,0).value.isnumeric:
            key=int(sheet.cell(k,0).value)
        else:
            key=sheet.cell(k,0).value
        Var.setdefault(key,[])
        for i in range(1,sheet.ncols):
            cell=sheet.cell(k,i)
            Var[key].append(cell.value)
    return Var


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
    return Var

T = parametro1(sheet_1,1)
print(T['2'])

D = parametro1(sheet_2,1)
S = parametro1(sheet_2,2)
H = parametro1(sheet_2,3)

Y = parametro1(sheet_5,1)
M = parametro1(sheet_5,2)

U = parametro2(sheet_3)
C = parametro2(sheet_4)
E = parametro2(sheet_7)
print(C['carlos'])

B = parametroB(sheet_6)




  Var.append([])
            Var.append([])
            Var.append([])
            cell_1=sheet.cell(k,1).value
            cell_2=sheet.cell(k,2).value
            
            if cell_1 == 'supervision':
                if cell_2 == 'correccion'















