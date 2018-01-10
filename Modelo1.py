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
        cell=sheet.cell(k,col)
        Var[key].append(cell.value)
    return Var


T = parametro1(sheet_1,1)
print(T)

print(T['3'])







T={}
key_T=0
for k in range(1,sheet_1.nrows):
    key_T=sheet_1.cell(k,0)
    T.setdefault(key_T,[])
    cell=sheet_1.cell(k,1)
    T[key_T].append(cell.value)
print(T.get('1'))


D={}
key_D=0
for k in range(1,sheet_2.nrows):
    key_D=sheet_2.cell(k,0)
    D.setdefault(key_D,[])
    cell=sheet_2.cell(k,1)
    D[key_D].append(cell.value)
print(D)


S={}
key_S=0
for k in range(1,sheet_2.nrows):
    key_S=sheet_2.cell(k,0)
    S.setdefault(key_S,[])
    cell=sheet_2.cell(k,2)
    S[key_S].append(cell.value)
print(S)


H={}
key_H=0
for k in range(1,sheet_2.nrows):
    key_H=sheet_2.cell(k,0)
    H.setdefault(key_H,[])
    cell=sheet_2.cell(k,3)
    H[key_H].append(cell.value)
print(H)

U={}
key_U=0
for k in range(1,sheet_3.nrows):
    key_U=sheet_1.cell(k,0)
    U.setdefault(key_U,[])
    for i in range(1,sheet_3.ncols):
        cell=sheet_1.cell(k,i)
        a[key].append(cell.value)
print(a)