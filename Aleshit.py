from gurobipy import *
import xlrd


book = xlrd.open_workbook('test_08.xlsx')
sheet_1 = book.sheet_by_index(0)
sheet_2 = book.sheet_by_index(1)
sheet_3 = book.sheet_by_index(2)
sheet_4 = book.sheet_by_index(3)

a={}
b={}
c={}
d={}


## Guardar como diccionario
##considera excel con rótulos
key=0
for k in range(1,sheet_1.nrows):
    key=sheet_1.cell(k,0).value
    a.setdefault(key,[])
    for i in range(1,sheet_1.ncols):
        cell=sheet_1.cell(k,i)
        a[key].append(cell.value)
print(a)

'''
for k in range(1,sheet_1.ncols):
    c1.append([])
    for i in range(sheet_1.nrows):
        c1[k].append(sheet_1.cell(i,k))
    

for k in range(sheet_2.ncols):
    c2.append([sheet_2.row_values(i)[k] for i in range(sheet_2.nrows)])
'''

P=len(a)
S=len(b)

for p in range(len(a)):
    lexp = m.LinExpr()
    for s in range(S):
        
        
        
        
        
     for i in range(I):
        # for each patient add a constraint
        lexp = gp.LinExpr()
        for j in range(J):
            for k in x[i][j].keys():
                for t in x[i][j][k].keys():
                    lexp.addTerms(1.0, x[i][j][k][t])
        # add constraints
        orMo.addConstr(lexp, gp.GRB.LESS_EQUAL, 1.0, "patient[%d]"%(i))
