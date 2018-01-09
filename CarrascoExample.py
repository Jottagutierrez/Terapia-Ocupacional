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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        



x = []

print(W)
print("Adding Variables x[ijkt]")
# for each patient in queue
for i in range(I):
    # add variable storage
    x.append([])

    # for each OR for that patient
    for j in range(J):
        # add variable storage
        x[i].append({})
        # for each MD that can perform the surgery (now all of them do)
        for k in MD:
            # add variable if physician does the corresponding surgery
            if Q[i] in P[k]:
                # get average surgery time
                p_i = instance.getQuantP(Q[i], met, k, mode)
                # add variable storage
                x[i][j][k] = {}
                # for each time-slot in which the MD is available to start
                for t in range(MD[k][0], MD[k][1]-p_i+2):
                    # set objective
                    if conf.isUtilization():
                        x[i][j][k][t] = orMo.addVar(obj=p_i, vtype=gp.GRB.BINARY, name="x[%d,%d,%s,%d]"%(i,j,k,t))

                    elif conf.isThroughput():
                        x[i][j][k][t] = orMo.addVar(obj=1.0, vtype=gp.GRB.BINARY, name="x[%d,%d,%s,%d]"%(i,j,k,t))

                    elif conf.isWThroughput():
                        x[i][j][k][t] = orMo.addVar(obj=int(W[i]), vtype=gp.GRB.BINARY, name="x[%d,%d,%s,%d]"%(i,j,k,t))
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
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