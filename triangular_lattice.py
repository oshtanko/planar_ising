from __future__ import division  
import numpy as np
from numpy import logical_and as AND
from numpy import logical_or as OR
import itertools
import matplotlib.pyplot as plt

#=====================================================================================================================================

def add(a,B):
    if len(B)==0:
        B = a
    else:
        B = np.vstack((B,a))  
    return B

def angle(n):
    n = n-1e-12
    n = n/np.sqrt(np.sum(n**2))
    phi = 2*np.pi*(n[1]<0)+np.arccos(n[0])*np.sign(n[1])
    return phi%(2*np.pi)

def trnglr_lattice(L,T,p):
    #-------------------------------------------------------------------------
    basisx = np.tile(np.hstack((np.arange(L),np.arange(-p,L-1+p))),int(T/2))
    basisy = np.repeat(np.arange(T),np.tile([L,L-1+2*p],int(T/2)))
    #--------------------------------------------------------------------------
    X,Y = np.meshgrid(basisx,basisy)
    adjmatrix1 = AND(AND(np.abs(X-X.T)==1,np.abs(Y-Y.T)==0),AND(Y!=T-1,Y!=0))
    adjmatrix2 = AND(AND(np.abs(X-X.T)==1,np.abs(Y-Y.T)==0),AND(Y==0,X<int(L/2))
    adjmatrix3 = AND(AND(np.abs(X-X.T)==1,np.abs(Y-Y.T)==0),Y==T-1)
    adjmatrix4 = OR(AND(X-X.T==0,np.abs(Y-Y.T)==1),(X-X.T)*(Y-Y.T)==1-2*(Y%2))
    adjmatrix4 = np.triu(adjmatrix4)
    adjmatrix4 += adjmatrix4.T
    return basisx,basisy,adjmatrix1,adjmatrix2,adjmatrix3,adjmatrix4

def list_edges(adjmatrix):
    S = len(adjmatrix)
    edges = []
    for i in range(S):
        for j in range(i+1,S):
            if adjmatrix[i][j]!=0:
                edges = add([i,j],edges)
    E = len(edges)
    database = np.zeros([E,7],int)
    for i in range(E):
        database[i][0] = i
        database[i][1:3] = edges[i]
        #---------------------------------------
        vertex = edges[i][0]
        nn = np.arange(S)[adjmatrix[vertex]]
        nnidx, nnang = np.zeros(len(nn),int),np.zeros(len(nn))
        for s in range(len(nn)):
            nnidx[s] = np.arange(E)[OR(AND(edges.T[0]==vertex,edges.T[1]==nn[s]),AND(edges.T[1]==vertex,edges.T[0]==nn[s]))][0]
            n = np.array([basisx[nn[s]]-basisx[vertex],basisy[nn[s]]-basisy[vertex]])
            nnang[s] = angle(n)
        nnidx = nnidx[np.argsort(nnang)]
        indx0 = np.arange(len(nnidx))[nnidx==i][0]
        database[i][3],database[i][4] = nnidx[(indx0+1)%len(nnidx)],nnidx[(indx0-1)%len(nnidx)]
        #---------------------------------------
        vertex = edges[i][1]
        nn = np.arange(S)[adjmatrix[vertex]]
        nnidx, nnang = np.zeros(len(nn),int),np.zeros(len(nn))
        for s in range(len(nn)):
            nnidx[s] = np.arange(E)[OR(AND(edges.T[0]==vertex,edges.T[1]==nn[s]),AND(edges.T[1]==vertex,edges.T[0]==nn[s]))][0]
            n = np.array([basisx[nn[s]]-basisx[vertex],basisy[nn[s]]-basisy[vertex]])
            nnang[s] = angle(n)
        nnidx = nnidx[np.argsort(nnang)]
        indx0 = np.arange(len(nnidx))[nnidx==i][0]
        database[i][5],database[i][6] = nnidx[(indx0+1)%len(nnidx)],nnidx[(indx0-1)%len(nnidx)]
    return database

def visualize(database,basisx,basisy,adjmatrix):
    for i in range(len(adjmatrix)):
        for j in range(i+1,len(adjmatrix)):
            #if jmatrix[i][j]==G1-G2:
            #    plt.plot([basisx[i]+0.5*(basisy[i]%2),basisx[j]+0.5*(basisy[j]%2)],[basisy[i],basisy[j]],c='b')
            #if jmatrix[i][j]==G1+G2:
            #    plt.plot([basisx[i]+0.5*(basisy[i]%2),basisx[j]+0.5*(basisy[j]%2)],[basisy[i],basisy[j]],c='b',ls="--")
            #if jmatrix[i][j]==G1:
            #    plt.plot([basisx[i]+0.5*(basisy[i]%2),basisx[j]+0.5*(basisy[j]%2)],[basisy[i],basisy[j]],c='g',ls="--")
            #if abs(jmatrix[i][j]+0.5+G3)<1e-5:
            #    plt.plot([basisx[i]+0.5*(basisy[i]%2),basisx[j]+0.5*(basisy[j]%2)],[basisy[i],basisy[j]],c='purple',ls=":")
            if adjmatrix[i][j]:#==-0.5-G1:
                plt.plot([basisx[i]+0.5*(basisy[i]%2),basisx[j]+0.5*(basisy[j]%2)],[basisy[i],basisy[j]],c='k')
    plt.axis('off')
    for i in range(len(adjmatrix)):
        plt.text(basisx[i]+0.5*(basisy[i]%2)-0.05,basisy[i]+0.1,str(i))
    for k in range(len(database)):
        i,j = database[k][1:3]
        #plt.text(0.5*(basisx[i]+basisx[j])+0.25*(basisy[j]%2)+0.25*(basisy[i]%2)-0.025,0.5*(basisy[i]+basisy[j])-0.025,str(k),bbox={'facecolor': 'white', 'alpha': 1, 'pad': 1})
        plt.text(0.5*(basisx[i]+basisx[j])+0.25*(basisy[j]%2)+0.25*(basisy[i]%2)-0.025,0.5*(basisy[i]+basisy[j])-0.025,jmatrix[i,j],bbox={'facecolor': 'white', 'alpha': 1, 'pad': 1})
    return 0

def plot_conf(state,basisx,basisy,jmatrix):
    plt.scatter(basisx+0.5*(basisy%2),basisy,s=1/max(L,T)*4000,edgecolors='k',c=state,cmap='gray')
    plt.axis('off')
    return 0

#=====================================================================================================================================
# generate random couplings from adjacency matrix
def random_couplings(adjmatrix):
    jmatrix = np.zeros([len(adjmatrix),len(adjmatrix)])
    for i in range(len(adjmatrix)):
        for j in range(i+1,len(adjmatrix)):
            if adjmatrix[i][j]!=0:
                jmatrix[i,j] = 0.5*np.random.normal(0,1)
                jmatrix[j,i] = jmatrix[i,j]
    return jmatrix


def EE_model_couplings(adjmatrix1,adjmatrix2,adjmatrix3,adjmatrix4):
    Delta = 0
    jmatrix = -(0.5+G1)*np.float_(adjmatrix)#np.zeros([len(adjmatrix),len(adjmatrix)])
    ibp,jbp = int(L/2)-1,int(L/2)
    for i in range(L-1):
        jmatrix[i,i+1] += -G2
        jmatrix[i+1,i] += -G2
        #Delta += G2
    for i in range(len(adjmatrix)-1-L-p):
        if jmatrix[i,i+1]!=0:
            jmatrix[i,i+1] += 2*G1+0.5
            jmatrix[i+1,i] += 2*G1+0.5
            Delta += G1-0.5
    for i in range(len(adjmatrix)-L-p,len(adjmatrix)-1):
        if jmatrix[i,i+1]!=0:
            jmatrix[i,i+1] += +0.5+G1
            jmatrix[i+1,i] += +0.5+G1
    for k in np.arange(0,int(T/2)-1+p):
        i =  (L-1)*(1-p)+k*(2*L+1-2+2*p)+1-p
        j = i+L-1+p
        jmatrix[i,j] += -G3+G1
        jmatrix[j,i] += -G3+G1
        Delta += G3-G1
    for k in np.arange(0,int(T/2)-1+p):
        i =  (L-1)*(1-p)+k*(2*L+1-2+2*p)+1-p+L-2+p
        j = i+L+p
        jmatrix[i,j] += -G3+G1
        jmatrix[j,i] += -G3+G1
        Delta += G3-G1
    jmatrix[ibp,jbp],jmatrix[jbp,ibp] = G1+G2,G1+G2
    #Delta += G2
    return jmatrix,Delta

#def EE_model_couplings(adjmatrix,x0):
#    Delta = 0
#    jmatrix = -(0.5+G1)*np.float_(adjmatrix)#np.zeros([len(adjmatrix),len(adjmatrix)])
#    ibp,jbp = int(L/2)-1,int(L/2)
#    for i in range(L-1):
#        jmatrix[i,i+1] += -G2
#        jmatrix[i+1,i] += -G2
#        #Delta += G2
#    for i in range(len(adjmatrix)-1-L-p):
#        if jmatrix[i,i+1]!=0:
#            jmatrix[i,i+1] += 2*G1+0.5
#            jmatrix[i+1,i] += 2*G1+0.5
#            Delta += G1-0.5
#    for i in range(len(adjmatrix)-L-p,len(adjmatrix)-1):
#        if jmatrix[i,i+1]!=0:
#            jmatrix[i,i+1] += +0.5+G1
#            jmatrix[i+1,i] += +0.5+G1
#    for k in np.arange(0,int(T/2)-1+p):
#        i =  (L-1)*(1-p)+k*(2*L+1-2+2*p)+1-p
#        j = i+L-1+p
#        jmatrix[i,j] += -G3+G1
#        jmatrix[j,i] += -G3+G1
#        Delta += G3-G1
#    for k in np.arange(0,int(T/2)-1+p):
#        i =  (L-1)*(1-p)+k*(2*L+1-2+2*p)+1-p+L-2+p
#        j = i+L+p
#        jmatrix[i,j] += -G3+G1
#        jmatrix[j,i] += -G3+G1
#        Delta += G3-G1
#    jmatrix[ibp,jbp],jmatrix[jbp,ibp] = G1+G2,G1+G2
#    #Delta += G2
#    return jmatrix,Delta

# basis of classical spins
def spin_basis(num_sites):
    full_basis = np.array(list(itertools.product([-1,1], repeat=num_sites))) 
    return full_basis

def partition_function(jmatrix):
    basis = spin_basis(len(jmatrix))
    Z = 0
    for si in range(len(basis)):
        vec = basis[si]
        Z += np.exp(-np.dot(vec,np.dot(jmatrix,vec)))
    return Z

#======================================================================================================================================
G1 = 0#1000.00000003525#10000.000037
G2 = 100#100.000000005233#1000.00001824
G3 = 0#10000.0000000032452#100.00027152#1300.0992
#length and time for the lattice 
Lph,T = 4,6
x0 = 6
L = int(Lph/2)+(int(Lph/2)%2)
p = 1-(int(Lph/2)%2)

#print L,p
#L,T,p=5,6,1
# x-positions of vertices, y-positions of vertices, adjacency matrix for triagular lattice
basisx,basisy,adjmatrix1,adjmatrix2,adjmatrix3,adjmatrix4 = trnglr_lattice(L,T,p)
adjmatrix = OR(OR(adjmatrix1,adjmatrix2),OR(adjmatrix3,adjmatrix4))

# database of the edges is in the format:
# [index,vertex1,vertex2,c1,cc1,c2,cc2]
jmatrix,Delta = EE_model_couplings(adjmatrix1,adjmatrix2,adjmatrix3,adjmatrix4)
database = list_edges(adjmatrix)


##print jmatrix[11,14]
##state=np.random.randint(2,size=len(adjmatrix))
#E = np.array([])
#basis = spin_basis(len(adjmatrix))
#for i in range(len(basis)):
#    state = basis[i]
#    E = np.append(E,G2+0.5*np.dot(state,np.dot(jmatrix,state)))
#Esort = np.sort(E)
#
##print jmatrix[0,1]
#
## visualize the lattice with labels for edges and vertices
#plt.subplot(1,2,1)
visualize(database,basisx,basisy,adjmatrix)
#plt.subplot(1,2,2)
##plt.hist(E,100)
#indx = 0
#state = basis[np.argsort(E)[indx]]
#print Esort[indx]-Esort[0]
#print Esort[0]
#plot_conf(state,basisx,basisy,jmatrix)

## jmatrix -- matrix of couplings, generate randomly for all edges
#jmatrix = random_couplings(adjmatrix)
## computing partition 
#Z = partition_function(jmatrix)
#print Z


        

