from gurobipy import *
import xlrd


book = xlrd.open_workbook('test_08.xlsx')
sheet_1 = book.sheet_by_index(0)
sheet_2 = book.sheet_by_index(1)
sheet_3 = book.sheet_by_index(2)
sheet_4 = book.sheet_by_index(3)

c1=[]
c2=[]
c3=[]
c4=[]


a=0
a={}
key=sheet_1.cell(1,0)
a.setdefault(key,[])
for i in range(1,sheet_1.ncols):
    a[key].append(sheet_1.cell(1,i))
print (a)


a={}
key=0
for k in range(1,sheet_1.nrows):
    key=sheet_1.cell(k,0)
    a.setdefault(key,[])
    for i in range(1,sheet_1.ncols):
        cell=sheet_1.cell(k,i)
        a[key].append(cell.value)
print(a)

for k in range(1,sheet_1.ncols):
    c1.append([])
    for i in range(sheet_1.nrows):
        c1[k].append(sheet_1.cell(i,k))
    


for k in range(sheet_2.ncols):
    c2.append([sheet_2.row_values(i)[k] for i in range(sheet_2.nrows)])


for k in range(sheet_3.ncols):
    c3.append([sheet_3.row_values(i)[k] for i in range(sheet_3.nrows)])


for k in range(sheet_4.ncols):
    c4.append([sheet_4.row_values(i)[k] for i in range(sheet_4.nrows)])



for p in range(len())


     for i in range(I):
        # for each patient add a constraint
        lexp = gp.LinExpr()
        for j in range(J):
            for k in x[i][j].keys():
                for t in x[i][j][k].keys():
                    lexp.addTerms(1.0, x[i][j][k][t])
        # add constraints
        orMo.addConstr(lexp, gp.GRB.LESS_EQUAL, 1.0, "patient[%d]"%(i))
