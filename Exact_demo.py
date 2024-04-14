import sympy
import dimod
solver = dimod.ExactSolver()
#y=p0,x0=p1,x1=p2...
#args=[a1,a2]
def weights(*args):

    sympy.var("p0,p1,p2,p3,p4")
    sympy.var("y,x0,x1,x2,x3")
    sympy.var("a1,a2")
    expr = 3 - x0*(2-a1-a2+y) -x1*(1-a1+a2+y) -x2*(1+a1-a2+y) -x3*(1+a1+a2-y) +10*(x0+x1+x2+x3-1)**2
    expr_substituted = expr.subs([(x0,(p1+1)/2),(x1,(p2+1)/2),(x2,(p3+1)/2),(x3,(p4+1)/2),(y,(p0+1)/2),(a1,args[0]),(a2,args[1])])
    expr_poly = sympy.poly(expr_substituted, p0, p1, p2, p3, p4)*4

    index_list=[]
    for i in range(5):
        for j in range(i,5):
            if i != j:
                my_list = [0]*5
                my_list[i],my_list[j] = 1,1
                index_list.append(my_list)
            else:
                my_list = [0]*5
                my_list[i] = 2
                index_list.append(my_list.copy())
                my_list[i] = 1
                index_list.append(my_list.copy())


    h_dict={}
    g_dict={}
    for i in index_list:
        indices = [j for j,x in enumerate(i) if x == 1]
        if len(indices) == 2:
            g_dict[("p"+str(indices[0]), "p"+str(indices[1]))] = expr_poly.nth(*i)
        elif len(indices) == 1:
            h_dict["p"+str(indices[0])] = expr_poly.nth(*i)
        else:
            ind2 = [n for n,x in enumerate(i) if x == 2]
            g_dict[("p"+str(ind2[0]),"p"+str(ind2[0]))] = expr_poly.nth(*i)

    return {"h":h_dict, "g":g_dict}

for i in range(2):
    for j in range(2):
        res_dict = weights(i,j)
        res = solver.sample_ising(res_dict["h"],res_dict["g"])
        print(f"<a1:{i},a2:{j}>")
        for sample, energy, num_occurrences in res.data(['sample', 'energy', 'num_occurrences']):
            print(f"Sample: {sample}, Energy: {energy}, Occurrences: {num_occurrences}")
    