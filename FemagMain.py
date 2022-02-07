from module.d_optimal_design import Doptimaldesign
from module.parallelcomp     import run
import numpy as np


var   =   [596.0, 40.0, 1.2, 3.6, 1.0, 0.0, 0.0, 0.0, 0.0, 4.0]


inside_diam     =   390.00
minJoch         =   10.00
minSlot         =   10.0
total_num_slot  =   48
minopHeight     =   1.00
slotwidthMin    =   5

ub  =   [700, (var[0]  -   inside_diam)*0.5 -   minJoch, var[1]    -   minSlot -   var[2]  -   var[3],
        var[1]   -  minSlot -   var[2],    (np.pi * inside_diam/total_num_slot) -   var[9], 3,5,(((inside_diam + var[1])*np.pi)/total_num_slot) - var[9]    -   2*var[2],
        (((-var[6] + inside_diam + var[1])*np.pi)/total_num_slot) - var[9]-2*var[3], (inside_diam*np.pi/total_num_slot)-var[4]]

if slotwidthMin ==  0:
    lb  =   [inside_diam   +   var[1]  +   minJoch, minSlot,minopHeight,var[2]+var[5], slotwidthMin,0,0,0,0,3]
else:
    lb  =  [inside_diam   +   var[1]  +   minJoch, minSlot,minopHeight,var[2]+var[5], -var[2],0,0,0,0,3] 


info            =       ['example','PMSM']# Dateiname/Typname(sehr wichtig für das Logfile da diese Bezeichnung die zugehörigkeit bestimmt)
nodedist        =       [3.00,3.00]#FE Genauigkeit Strator/Genauigkeit Rotor


var       = [579,40,18]


if __name__ == "__main__":


    D,optimale_stuetzstellen    =   Doptimaldesign(var).run()

    #optimale_stuetzstellen.tolist
    op  =   optimale_stuetzstellen.tolist()

    logs                        =   run(info,nodedist,op)
    print(logs)
