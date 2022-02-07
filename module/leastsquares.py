import numpy as np
import re
from os import listdir

def matrixbuild(X):
    'quadratischer Teil'
    xquad    =      []
    for q in range(len(X)):
        xquadrow         =   []
        for i in range(len(X[q])):
            for e in range(i,len(X[q])):
                xquadrow.append(X[q][i]*X[q][e])
        
        xquad.append(xquadrow)

    xquad =   np.asarray(xquad)

    X     = np.c_[np.ones((len(X),1)), X,xquad]  #Volle Quadratische Ansatz 'xquad' hinzufügen
    return X

def matrixbuildall(X,entferntespalten):
    'quadratischer Teil'
    xquad    =      []
    for q in range(len(X)):
        xquadrow         =   []
        for i in range(len(X[q])):
            for e in range(i,len(X[q])):
                xquadrow.append(X[q][i]*X[q][e])
        
        xquad.append(xquadrow)

    xquad =   np.asarray(xquad)

    for i in range(len(entferntespalten)):
        xquad =   np.delete(xquad, np.s_[entferntespalten[i]:entferntespalten[i]+1], axis=1)
        
            
    X   =   np.c_[np.ones((len(X),1)), X,xquad]
            
    return X


def buildmodel(D,lenvar,info,datetime,alllogs,ent_sp):
    
    ergebnis    =   []

    if alllogs      == True:
        l = listdir('.\\logs\\logs_PMSM\\results')
        for i in range(len(l)):
            out_lesen = open(".\\logs\\logs_{0}\\results\\{1}".format(info[1],l[i]),"r")
            e       =   (out_lesen.read()).split("\n")
            for q in range(len(e)):
                e[q] = e[q].replace(",", "")
                e[q] = e[q].replace("[", "")
                e[q] = e[q].replace("]", "")
                e[q] = e[q].split(" ")
                if q == 1:
                    e[q] = e[q][:lenvar]
                    for z in range(len(e[q])):
                        e[q][z] =   float(e[q][z])
                else:
                    for z in range(len(e[q])):
                        e[q][z] =   float(e[q][z])


            ergebnis.append(e)
            out_lesen.close()



    else:
        for i in range(len(D)):
            out_lesen = open(".\\logs\\logs_{0}\\results\\{1}-time-{2}-num.txt".format(info[1],datetime,i),"r")
            e       =   (out_lesen.read()).split("\n")
            for q in range(len(e)):
                e[q] = e[q].replace(",", "")
                e[q] = e[q].replace("[", "")
                e[q] = e[q].replace("]", "")
                e[q] = e[q].split(" ")
                if q == 1:
                    e[q] = e[q][:lenvar]
                    for z in range(len(e[q])):
                        e[q][z] =   float(e[q][z])
                else:
                    for z in range(len(e[q])):
                        e[q][z] =   float(e[q][z])


            ergebnis.append(e)
            out_lesen.close()


    lenev   =   len(ergebnis[0][0])


    for i in range(len(ergebnis)):
        for q in range(len(ergebnis[i])):
            ergebnis[i][q]  =   np.asarray(ergebnis[i][q])



    for i in range( len(ergebnis)):
        ergebnis[i]     =  np.concatenate((ergebnis[i][0],ergebnis[i][1]),axis=None)

    dellist =   list(range(0,lenev))
    x   =   np.delete(ergebnis,dellist,axis=1)

    X   =   matrixbuildall(x,ent_sp)

    stacks  =   []


    for i in range(lenev):

        dellist =   list(range(0,lenev+lenvar))
        dellist.remove(i)
        E           =   np.copy(ergebnis)
        stacks.append(np.delete(E, dellist, axis=1))
        del E



    Y       =   np.stack(stacks)


    return Y,X


def regkoeff(Y,X):
    
    xc      =   np.copy(X)
    xt      =   np.transpose(X)
    XtXi    =   np.linalg.inv(np.dot(xt, xc))

    koeff   =   []

    for i in range(len(Y)):
        koeff.append(np.dot(XtXi,np.dot(xt,Y[i])))

    B       =   np.asarray(koeff)

    



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

    return B
