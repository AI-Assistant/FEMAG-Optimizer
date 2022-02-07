'femagfunction.py'
'FEMAG-DC wird hier über Python angesteuert'

# FEMAG Funktion benötigt folgende Inputvariablen



import os, sys
import shutil
import time
import subprocess 
import time
import numpy as np




class Femag:

    def __init__(self,var,Lock):
        self.var        =   var[0]
        self.itter_num  =   var[1]
        self.info       =   var[2]
        self.nodedist   =   var[3]
        self.Lock       =   Lock

    def skripterstellen(self):

        skriptrohling_open  =   open('.\\Stammdaten\\Skriptrohling\\M-Model-PM-0.fsl',"r")
        skriptrohling       =   skriptrohling_open.read().split('\n')
        skriptrohling_open.close()

        skriptrohling[3]    =   'new_model_force("{0}","{1}")'.format(self.info[0],self.info[1])
        skriptrohling[11]   =   'm.fc_radius    = {0}'.format(self.var[3]+1)
        skriptrohling[23]   =   'm.nodedist     = {0}'.format(self.nodedist[0])
        skriptrohling[40]   =   'm.nodedist     = {0}'.format(self.nodedist[1])
        skriptrohling[13]   =   'm.yoke_diam    = {0}'.format(self.var[0])
        skriptrohling[14]   =   'm.inside_diam  = {0}'.format((self.var[3]*2)+4)  
        skriptrohling[15]   =   'm.slot_height  = {0}'.format(self.var[1]) 
        skriptrohling[16]   =   'm.slot_h1      = {0}'.format(1.2)
        skriptrohling[17]   =   'm.slot_h2      = {0}'.format(3.84)
        skriptrohling[18]   =   'm.slot_width   = {0}'.format(1.0)
        skriptrohling[19]   =   'm.slot_r1      = {0}'.format(0.0)
        skriptrohling[20]   =   'm.slot_r2      = {0}'.format(0.0)
        skriptrohling[21]   =   'm.wedge_width1 = {0}'.format(0.0)
        skriptrohling[22]   =   'm.wedge_width2 = {0}'.format(0.0)
        skriptrohling[25]   =   'm.tooth_width  = {0}'.format(self.var[2])
        skriptrohling[36]   =   'm.magn_rad     = {0}'.format(self.var[3])
        skriptrohling[37]   =   'm.yoke_rad     = {0}'.format(120)
        skriptrohling[38]   =   'm.magn_height  = {0}'.format(self.var[5])
        skriptrohling[39]   =   'm.magn_width   = {0}'.format(85)
        skriptrohling[41]   =   'm.condshaft_r  = {0}'.format(120)
        skriptrohling[43]   =   'm.magn_perm    = {0}'.format(self.var[3]-self.var[5])
        skriptrohling[137]  =   'm.arm_length   = {0}'.format(self.var[4])
        skriptrohling[176]  =   'outputfile = io.open("output-{0}.txt","w+")'.format(self.itter_num)
           



        return  skriptrohling


        
    def ordnererstellen(self):
    
        unterordner =   "Prozess{0}".format(self.itter_num)
        pfad        =   ".\\Prozesse"
        p           =   os.path.join(pfad,unterordner)

        os.makedirs(p,exist_ok=True)
        
        shutil.copy2(".\\Stammdaten\\Femagdatei\\wfemagw64-eval-8.4.0.exe", ".\\Prozesse\\Prozess{0}".format(self.itter_num))



    def skriptschreiben(self,skript):

        fobj_schreiben  =   open(".\\Prozesse\\Prozess{0}\\M-Model-PM-{1}.fsl".format(self.itter_num,self.itter_num),"w")

        for zeile in skript:
            fobj_schreiben.write(zeile +"\n")
        fobj_schreiben.close()


    def programmstart(self):   
        self.Lock.acquire()       
        command = "wfemagw64-eval-8.4.0 open M-Model-PM-{0}.fsl".format(self.itter_num)#-b beide Fenster unterdrücken -g Maske unterdrücken 
        p = subprocess.run(command,shell=True,cwd="C:/Users/kande/Desktop/FEMAG Python/Prozesse/Prozess{0}".format(self.itter_num))
        self.Lock.release()
        return p
    
    def output_lesen(self):
        out_lesen = open("C:/Users/kande/Desktop/FEMAG Python/Prozesse/Prozess{0}/output-{1}.txt".format(self.itter_num,self.itter_num),"r")
        ergebnis = (out_lesen.read()).split(" ")
        out_lesen.close()

        ergebnis_neu    =   []
        for e in range(len(ergebnis)):
            ergebnis_neu.append(float(ergebnis[e]))

        return ergebnis_neu




    def run(self):

        skript      =   self.skripterstellen() 

        self.ordnererstellen()
        self.skriptschreiben(skript)
        self.programmstart()

        ergebnis    =   self.output_lesen()


        return ergebnis