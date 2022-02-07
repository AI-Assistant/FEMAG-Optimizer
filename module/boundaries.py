import numpy as np

def ub(var,i):

    ub        = [(var[3]*2)+4+var[1]+200,((var[0]-390)/2)-10,(np.pi*390/48)-10,250,300,var[3]-140]

    return ub[i]


def lb(var,i):
    lb        = [(var[3]*2)+4+(var[1]*2)+40,30,10,120+13+20,50,15]
    return lb[i]



