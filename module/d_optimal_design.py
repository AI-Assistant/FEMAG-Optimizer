import numpy as np
import sys
from operator import itemgetter
import itertools
sys.path.insert(0,'.\module')
from boundaries import ub, lb



class Doptimaldesign():

    def __init__(self, var):
        self.var = var
        self.schritte = round(5000**(1/len(self.var)))

    def rasterbau(self):  # Skalare vektor für jede var ein Skalar /Schritte default wert eher niedrig wählen

        var_bereich = []

        for i in range(len(self.var)):
            LB = lb(self.var, i)
            UB = ub(self.var, i)
            var_bereich.append(np.linspace(LB, UB, self.schritte))
            #var_bereich.append(np.linspace(0.8 * self.var[i], 1.2 * self.var[i],self.schritte))
        all_comb = list(itertools.product(*var_bereich))

        #print('Kombinationen werden erstellt  {0}/{1}'.format(len(all_comb),(self.schritte**(len(self.var)))),end="\r", flush=True)
        stuetzpunkte = []
        print(' ')
        print('Randpunkte werden erstellt')

        stuetzpunkte = self.bereichabfrage(all_comb)

        stuetzpunkte = np.asarray(stuetzpunkte)

        stuetzpunkte = np.unique(stuetzpunkte, axis=0)

        return stuetzpunkte

        #arrays = [np.asarray(x) for x in arrays]

    def rand_punkte_kombinieren(self, var):

        randpunkte = []

        lst = list(itertools.product([0, 1], repeat=len(var)))

        for q in range(2**len(var)):
            varcal = np.copy(var)
            for i in range(len(var)):
                if lst[q][i] == 1:
                    varcal[i] = ub(varcal, i)
                else:
                    varcal[i] = lb(varcal, i)

            randpunkte.append(varcal)
            del varcal

       
        randpunkte = np.asarray(randpunkte)
        randpunkte = np.unique(randpunkte, axis=0)

        return randpunkte

    def rand_stuetzpunkte(self, stuetzpunkte):

        randpunkte = []
        i = 0
        a, _ = stuetzpunkte.shape
        while i < a:

            randpunkte.append(self.rand_punkte_kombinieren(stuetzpunkte[i]))

            i += 1

        randpunkteproof = []
        rand = []

        for i in range(len(randpunkte)):
            randpunkteproof.append(self.bereichabfrage(randpunkte[i]))

        for i in range(len(randpunkteproof)):
            for q in range(len(randpunkteproof[i])):
                rand.append(randpunkteproof[i][q])

        rand = np.asarray(rand)
        arrayrandpunkte = np.unique(rand, axis=0)

        return arrayrandpunkte

    def bereichabfrage(self, X):

        stuetzpunkte = []

        for var in X:
            status = True
            i = 0
            while status == True and i != len(var):
                status = var[i] <= ub(var, i) and var[i] >= lb(var, i)
                i += 1

            if status == True:

                stuetzpunkte.append(var)

            else:
                pass

        return stuetzpunkte

    def scale(self, var):

        varscale = np.copy(var)

        for q in range(len(var)):
            for i in range(len(var[q])):
                varscale[q][i] = (
                    var[q][i]-((ub(var[q], i)+lb(var[q], i))/2))/((ub(var[q], i)-lb(var[q], i))/2)

        # print("Values bigger than 10 =", varscale[varscale>1])
        # print("Their indices are ", np.nonzero(varscale > 1))

        return varscale

    def descale(self, var, random):

        var = var[:, 1:(len(self.var)+1)]

        for q in range(len(var)):
            for i in range(len(var[q])):
                var[q][i] = (var[q][i]*(ub(var[q], i)-lb(var[q], i)
                                        )/2) + (ub(var[q], i)+lb(var[q], i))/2

        return var

    def matrixbuildall(self, X, anzahl_exp, entferntespalten):
        'quadratischer Teil'
        xquad = []
        for q in range(len(X)):
            xquadrow = []
            for i in range(len(X[q])):
                for e in range(i, len(X[q])):
                    xquadrow.append(X[q][i]*X[q][e])

            xquad.append(xquadrow)

        xquad = np.asarray(xquad)

        for i in range(len(entferntespalten)):
            xquad = np.delete(
                xquad, np.s_[entferntespalten[i]:entferntespalten[i]+1], axis=1)

        X = np.c_[np.ones((anzahl_exp, 1)), X, xquad]

        return X

    def matrixbuild(self, X, anzahl_exp):
        'quadratischer Teil'
        xquad = []
        for q in range(len(X)):
            xquadrow = []
            for i in range(len(X[q])):
                for e in range(i, len(X[q])):
                    xquadrow.append(X[q][i]*X[q][e])

            xquad.append(xquadrow)

        xquad = np.asarray(xquad)

        print("\n-----------Koeffizienten großer Korelation werden entfernt------------\nBis Det(X'X) > 1\nDet(Xn'Xn) = {}".format(self.detmatrix(np.c_[np.ones((anzahl_exp, 1)), X, xquad])))
        entferntespalten = []

        while self.detmatrix(np.c_[np.ones((anzahl_exp, 1)), X, xquad]) < 1:
            Xlist = []

           # Xlist.append([self.detmatrix(np.c_[np.ones((anzahl_exp,1)), X,xquad]),0,xquad])

            for i in range(len(xquad[0])):

                xquadneu = np.copy(xquad)
                xq = np.delete(xquadneu, np.s_[i:i+1], axis=1)

                Xlist.append(
                    [self.detmatrix(np.c_[np.ones((anzahl_exp, 1)), X, xq]), i, xq])

            Xlist = sorted(Xlist, key=itemgetter(0), reverse=True)
            xquad = Xlist[0][2]
            print("\nDet(X'X):  {0}     Regressionskoeffizient No. {1} entfernt  ".format(self.detmatrix(
                np.c_[np.ones((anzahl_exp, 1)), X, xquad]), Xlist[0][1]+len(X[0])+1), end="\r", flush=True)

            entferntespalten.append(Xlist[0][1])

        X = np.c_[np.ones((anzahl_exp, 1)), X, xquad]

        return X, entferntespalten

    def detmatrix(self, X):
        XtX = np.dot(np.transpose(X), X)
        d = np.linalg.det(XtX)
        return d

    def deltamaker(self, xi, xj, Xn):

        XtXi = np.linalg.inv(np.dot(np.transpose(Xn), Xn))
        added_variance = np.dot(xj, np.dot(XtXi, np.transpose(xj)))
        removed_variance = np.dot(xi, np.dot(XtXi, np.transpose(xi)))
        covariance = np.dot(xi, np.dot(XtXi, np.transpose(xj)))
        return (1 + (added_variance - removed_variance) + (covariance * covariance - added_variance * removed_variance))

    def fedorof(self, stuetzpunkte, randstuezpunkte):
        'Zusammenfügen der beiden Stützstellen-Gruppen'
        C = np.append(stuetzpunkte, randstuezpunkte, axis=0)

        'Berechnung der Anzahl der nötigen Experimente'
        k = len(self.var)
        'Lineare Haupteffekte'
        anzahl_exp = k + 1
        '2 Faktor-Wechselwirkung'
        anzahl_exp += k*(k-1)/2
        'Quadratische Effekte'
        anzahl_exp += k
        'Versuchvarianz'
        anzahl_exp += k+1

        anzahl_exp = int(anzahl_exp)
        #anzahl_exp      =   len(self.var)*2

        #regkoeff        =   1   +   len(self.var)      + len(self.var)**2

        'Skalieren der Werte zwischen -1 und 1'
        Cscaled = self.scale(C)

        idx_list = np.random.choice(
            Cscaled.shape[0], anzahl_exp, replace=False)

        random = C[idx_list, :]
        randomscaled = self.scale(random)

        X, ent_sp = self.matrixbuild(randomscaled, anzahl_exp)
        Xall = self.matrixbuildall(Cscaled, len(Cscaled), ent_sp)

        status = True
        durchlauf = 0

        print("\n-----------Zeilenaustauschverfahren------------\n")

        while status == True:
            deltamaxlist = []
            print(' ')
            for i in range(len(X)):
                deltalist = []

                print("Det(X'X):  {0}             Durchlauf: {1}            IndexX: {2}".format(
                    self.detmatrix(X), durchlauf+1, i+1))

                # print("Det(X'X):  {0}             Durchlauf: {1}            IndexX: {2}".format(
                #     self.detmatrix(X), durchlauf+1, i+1), end="\r", flush=True)

                for j in range(len(Xall)):

                    delta = self.deltamaker(X[i], Xall[j], X)
                    deltalist.append([delta, i, j])

                deltalist = sorted(deltalist, key=itemgetter(0), reverse=True)
                deltamax = deltalist[0]

                if deltalist[0][0] > 1:
                    X[deltamax[1]] = Xall[deltamax[2]]
                    random[deltamax[1]] = C[deltamax[2]]

                    deltamaxlist.append(deltamax)
                else:
                    deltamaxlist.append(deltamax)
                    pass

            if deltamaxlist[0][0] > 1+1e-2:
                status = True
            else:
                status = False
            durchlauf += 1

        D = np.copy(X)

        return D, random, ent_sp

    def run(self):
        stuetzpunkte = self.rasterbau()

        randstuetzpunkte = self.rand_stuetzpunkte(stuetzpunkte)

        D, optimal_set, ent_sp = self.fedorof(stuetzpunkte, randstuetzpunkte)

        optimal_set = np.around(optimal_set, decimals=2)

        return D, optimal_set, ent_sp
