import numpy as np
import networkx as nx
from collections import Counter
import scipy.stats as stats


#1 define NFD function (unweighted): input:G,Q; output:tau_list
def NFD(G, Q):
    N_list = []
    rmax_list = []
    for node in G.nodes():
        #print("node = ", node)
        grow = []
        r_g_all = []
        num_g_all = []
        num_nodes = 0
        num_nodes_all = 0
        spl = nx.single_source_shortest_path_length(G, node)
        #print("node = ", node)#, ", spl = ", spl)
        for s in spl.values():
            if s > 0:
                grow.append(s)
        grow.sort()
        #print("grow = ", grow)
        num = Counter(grow)
        #print("num = ", num)
        rmax_list.append(grow[-1])
        for k, h in num.items():
            num_nodes_all += h
            #print("h = ", h)
        #print("num_nodes_all = ", num_nodes_all)
        #num_nodes_all += 1
        #num_nodes += 1
        for i, j in num.items():
            #print(i, j)
            num_nodes += j
            if i > 0:
                #print("p = ", (num_nodes/num_nodes_all))
                r_g_all.append(i)
                num_g_all.append(num_nodes/num_nodes_all)
        #print("N_list[] = ", num_g_all)
        N_list.append(num_g_all)
    #print("N_list[] = ", N_list)
    diameter = np.max(rmax_list)
    #print(diameter)
##Calculate tau
#     plt.figure(figsize=(5,5))
    new_k = {}
    for elem in N_list:
        elem = tuple(elem)
        if elem not in new_k.keys():
            new_k[elem] = 0
        else:
            new_k[elem] += 1

    cnt1 = 1
    for key in new_k.keys():
        lst = list(key)
        #print("num(",cnt1,") = ", new_k[key])  
        #print("P(",cnt1,", :) = ", lst)  
        cnt1 += 1                  

    #print("nums = ", nums)
    #print("nums = ", nums)
    #print("N_list[] = ", temp)
    r_max = diameter
    r_min = 0
    tau_list = []
    q_list = []
    dim_list = []
    cnt = 0
    a_list = []
    cnt2 = 1
    for q in Q:
        Zq_list = []
        for j in range(r_min, r_max):
            #print(j)
            Zq = 0
            for k in range(len(N_list)):
                if j < len(N_list[k]):
                    Zq += (N_list[k][j]) ** q
                else:
                    Zq += 1
            Zq_list.append(Zq)
        #print("q = ", q)        
        #print("Zq(",cnt2,",:) = ", Zq_list)
        cnt2 += 1
        x = np.log(range(r_min+1, r_max+1)/diameter)
        y = np.log(Zq_list)
#         q = format (q, '.0f' ) 
#         plt.plot(x,y,'*',label='q='+str(q))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        a_list.append(np.exp(intercept))
        #print("slope = ", slope)        
        tau_list.append(slope)
#         plt.xlabel('ln(r/d)')
#         plt.ylabel('ln(sum function)')
        #plt.savefig('/Users/xiongyex/Downloads/brain network'+'/tau.png',bbox_inches = 'tight',dpi=600)
        cnt += 1
#         if q != 0:
#             dim = slope/q
#             dim_list.append(dim)
    #print("A = ", a_list)
    #print("tau = ", tau_list)
    return tau_list      

def nspectrum(tau_list, q_list):
    al_list = []
    fal_list = []
    for i in range(1, len(q_list)):
        al = (tau_list[i]-tau_list[i-1])/(q_list[i]-q_list[i-1])
        al_list.append(al)
    for j in range(len(q_list)-1):
        fal = q_list[j]*al_list[j]-tau_list[j]
        fal_list.append(fal)
    #print("alpha = ", al_list)
    #print("falpha = ", fal_list)
    #plt.figure(figsize=(10,10))
    #plt.plot(al_list,fal_list,label=name[k],linewidth=5,color=color[k])
    #plt.plot(al_list,fal_list,linewidth=5)
    #plt.xlabel('Lipschiz-Holder exponent, 'r'$\alpha$')
    #plt.ylabel('Multi-fractal spectrum, 'r'$f(\alpha)$')
    return al_list, fal_list

def ndimension(tau_list,q_list,size):
    dim_list = []
    qd_list = []
    for i in range(len(q_list)):
        if (q_list[i]) != 0:
            dim = tau_list[i]/(q_list[i])
            if (np.isnan(dim)):
                dim = size
            else:
                dim += size
            dim_list.append(dim)
            qd_list.append(q_list[i])
    #print("dim = ", dim_list)
    #plt.figure(figsize=(10,10))
    #plt.plot(qd_list,dim_list,label=name[k],linewidth=5,color=color[k])
    #plt.plot(qd_list,dim_list,linewidth=5)
    #plt.xlabel('Distorting exponent, 'r'$q$')
    #plt.ylabel('Generalized fractal dimension, 'r'$D(q)$')
    #plt.legend()
    return qd_list, dim_list

#Q = [q for q in range(-10,11,1)]
#lst = []
#ntau = NFD(G, Q)

#al_list, fal_list = nspectrum(ntau, Q)
#dim_list = ndimension(ntau, Q)
#lst.extend(al_list)
#lst.extend(fal_list)
#lst.extend(dim_list)
#print(len(lst))
