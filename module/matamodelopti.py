import numpy as np
from scipy import optimize
from boundaries import ub,lb
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy.random as rnd


ent_sp  =   []
x0      =   [579,40,18,193,195,13]



e           =   [] 
yc          =   [] 

for i in range(len(B)):

    Ycal    =   np.dot(X, B[i])

    E       =   Y[i]-Ycal

    SSe     =   np.dot(np.transpose(E),E)

    MSe     =   SSe/(len(X)-len(B[0]))

    Ym      =   sum(Y[i])/len(X)

    SSt     =    np.dot(np.transpose(Y[i]),Y[i])-((sum(Y[i])**2)/len(X))

    SSr     =   np.dot(np.dot(np.transpose(B[i]),np.transpose(X)),Y[i])  - ((sum(Y[i])**2)/len(X))

    R2      =   SSr/SSt

    v       =   len(X)-1
    c       =   len(X)-len(B[0])

    Radj    =   1-((SSe/c)/(SSt/v))

    print('Adjustiertes Bestimmtheitsmaß der Regression von Ergebnis{0}'.format(i),Radj[0][0])

    e.append(E)
    yc.append(Ycal)

for i in range(len(e)):
    for q in range(len(e[i])):
        e[i][q] = 100/(yc[i][q]/ e[i][q])


fig = plt.figure(figsize=(12, 6))
vax = fig.add_subplot(221)
hax = fig.add_subplot(222)
rax = fig.add_subplot(223)
kax = fig.add_subplot(223)
lax = fig.add_subplot(224)


vax.plot(yc[0],e[0], 'o')
#vax.plot([0, 2500], [0, 0], 'k-', lw=1)
vax.grid(True)
vax.set_xlabel('Approximiertes Moment M')
vax.set_ylabel('Residuen e in Prozent')


hax.plot(yc[1],e[1], 'o')
#hax.plot([0, 500], [0, 0], 'k-', lw=1)
hax.grid(True)
hax.set_xlabel('Approximierte Spannung U')
hax.set_ylabel('Residuen e in Prozent')


rax.plot(yc[2],e[2], 'o')
#rax.plot([0, 500], [0, 0], 'k-', lw=1)
rax.grid(True)
rax.set_xlabel('Approximierte Eisenverluste Pve')
rax.set_ylabel('Residuen e in Prozent')

kax.plot(yc[3],e[3], 'o')
#kax.plot([0, 500], [0, 0], 'k-', lw=1)
kax.grid(True)
kax.set_xlabel('Approximierte Verluste Pve Pvw ')
kax.set_ylabel('Residuen e in Prozent')

lax.plot(yc[5],e[5], 'o')
#lax.plot([0, 1], [0, 0], 'k-', lw=1)
lax.grid(True)
lax.set_xlabel('Approximierter Leistungsfaktor cosphi')
lax.set_ylabel('Residuen e in Prozent')


#plt.show()



def matrixbuildall(x,entferntespalten):
    'quadratischer Teil'
    
    xquad = []

    for i in range(len(x)):
        for j in range(i,len(x)):
            xquad.append(x[i]*x[j])



    xquad =   np.asarray(xquad)

    if len(entferntespalten) != 0:
        for i in range(len(entferntespalten)):
            xquad =   np.delete(xquad, np.s_[entferntespalten[i]:entferntespalten[i]+1], axis=1)
    else:
        pass
    

    
    X  =   np.concatenate((np.array([1]), x,xquad))
            
    return X

def optimierungsfunktion(x,B,entferntespalten):
    
    
    x   =   matrixbuildall(x,entferntespalten)
    y   =   []

    for i in range(len(B)):
        y.append(np.dot(x, B[i]))


    Pab =   y[0]*2*np.pi*50
    n   =   Pab/(abs(y[2])+abs(y[3]))
    Vm  =   x[5]*x[6]*2*np.pi*0.85*(x[4]-x[6])
    z1  =   ((1-(Pab/36500))**2)*10   
    z2  =   ((1-y[5])**2)*10
    z3  =   ((1-(y[1]/400))**2)*10000   
    z4  =   ((1-n)**2)*1
    z5  =   Vm*0.001

    z   =   z1+z2+z3+z4+z5
    
    
    
    return z

def constraint00(x):
    return x[0]-((x[3]*2)+4+x[1]+200)

def constraint01(x):
    return x[0]+((x[3]*2)+4+(x[1]*2)+40)

def constraint02(x):
    return (((x[0]-390)/2)-10)-x[1]

def constraint03(x):
    return (x[3]-140)-x[5]

def bereichabfrage(X):

    for i in range(len(X)):
        
        
        status = X[i] <= ub(X, i) and X[i] >= lb(X, i)
        
        status1 = X[i] >= lb(X, i)

        if status != True:
            if status1 == True:
                return False,i-1,'ub'
            else:
                return False,i-1,'lb'
        else:
            pass
    
    return True,i







X         =      X[:,[1,2,3,4,5,6]]

E         =      []

cons = ({'type':'ineq','fun':constraint00},
        {'type':'ineq','fun':constraint01},
        {'type':'ineq','fun':constraint02},
        {'type':'ineq','fun':constraint03})



bnd       =     ((-np.inf,np.inf),(30,np.inf),(10,15.525),(153,250),(50,300),(5,np.inf))

for i in range(len(X)):
    
    x0  =   X[i]

    op  =   optimize.minimize(optimierungsfunktion, x0, args=(B,ent_sp), method='SLSQP', bounds=bnd,constraints=cons,options={'disp':True})
    print(bereichabfrage(op.x))
    optimalx    =   op.x
    for i in range(len(optimalx)):
        optimalx[i]=round(optimalx[i],2)
        
    E.append([round(op.fun,2),list(op.x)])


E       =   sorted(E, key=itemgetter(0), reverse=False)

Eopt    =   E[1]

xfin    =  E[0][1]
xfin    =   [526.27, 46.44, 15.52, 153.0, 50.0, 5.0]
Xfin    =   matrixbuildall(xfin,ent_sp)

yfin    =   np.dot(Xfin, B)
#print(bereichabfrage(xfin))
print('{0}\n\n{1}\n	DA: Außen Durchmesser (m.yoke_diam) \n•	H: Nut tiefe (m.slot_height)\n•	TW: Zahnbreite (m.tooth_width)\n•	RA: Magnet außen Radius (m.mag_rad)\n•	BT: Bautiefe (m.arm_lenght)\n•	HM: Magnet Höhe (m.mag_height)'.format(yfin,xfin))