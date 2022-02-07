import threading
import queue
from femagfunction import Femag
from multiprocessing import Process,Value,Array
import _thread
import os
import shutil
import multiprocessing
import datetime
import time
import math
import numpy as np

from operator import itemgetter



def make_dir(info):
    
    


    unterordner =   "logs_{0}".format(info[1])
    pfad        =   ".\\logs"
    p           =   os.path.join(pfad,unterordner)
    os.makedirs(p,exist_ok=True)


    unterordner =   "results"
    pfad        =   ".\\logs\\logs_{0}".format(info[1])
    p           =   os.path.join(pfad,unterordner)
    os.makedirs(p,exist_ok=True)


    unterordner =   "bchfiles"
    pfad        =   ".\\logs\\logs_{0}".format(info[1])
    p           =   os.path.join(pfad,unterordner)
    os.makedirs(p,exist_ok=True)
    del p,unterordner,pfad

def write_logs(logs):

    date        =   datetime.datetime.now().strftime("%H%M%S-%Y%m%d")

    for i in range(len(logs)):

        erg_w       =   open(".\\logs\\logs_{0}\\results\\{1}-time-{2}-num.txt".format(logs[i][1][2][1],date,logs[i][1][1]),"w")
        
        erg_w.write(str(logs[i][0])+"\n")
        erg_w.write(str(logs[i][1]))

        erg_w.close()
        



        os.rename(r'.\\Prozesse\\Prozess{0}\\{1}_001.BCH'.format(logs[i][1][1],logs[i][1][2][0]),r'.\\Prozesse\\Prozess{0}\\{1}-time-{2}-num-{3}-type.BCH'.format(logs[i][1][1],date,logs[i][1][1],logs[i][1][2][0]))

        shutil.copy2('.\\Prozesse\\Prozess{0}\\{1}-time-{2}-num-{3}-type.BCH'.format(logs[i][1][1],date,logs[i][1][1],logs[i][1][2][0]), ".\\logs\\logs_{0}\\bchfiles".format(logs[i][1][2][1]))


    #shutil.rmtree(".\\Prozesse\\Prozess{0}".format(logs[i][1][1]))
    

    erg_w.close()
    return date

class FemagThread(threading.Thread):

    Inputvar        =   []
    Ergebnis        =   []

    ErgebnisLock    =   threading.Lock()
    Briefkasten     =   queue.Queue()
    

    def run(self):


        while True:

            var_geholt    =     FemagThread.Briefkasten.get()
        
            ergebnis      =     Femag(var_geholt,FemagThread.ErgebnisLock).run()

            FemagThread.ErgebnisLock.acquire()
            FemagThread.Ergebnis.append(ergebnis)
            FemagThread.Inputvar.append(var_geholt)
            FemagThread.ErgebnisLock.release()

            FemagThread.Briefkasten.task_done()    

def thread_cpu(var,  ret_dict, l):
    
    ergebnis    =  []
    for f in range(len(var)):
        FemagThread.Briefkasten.put(var[f])

    meine_threads   =   [FemagThread()for i in range(2)] #Hier kann die Zahl der Threads pro Process erhöht werden. 
    for thread in meine_threads:
        thread.setDaemon(True)
        thread.start()

    FemagThread.Briefkasten.join()


    l.acquire()

    for i in range(len(FemagThread.Ergebnis)):
        ergebnis.append([FemagThread.Ergebnis[i],FemagThread.Inputvar[i]])
    

    ret_dict[int(multiprocessing.current_process().name)]    =   ergebnis

    l.release()
    
def parallel_compute(info,nodedist,varl):

    manager         =       multiprocessing.Manager()
    ret_dict        =       manager.dict()
    lock            =       multiprocessing.Lock()

    var             =       []
    for i in range(len(varl)):
        var.append([varl[i],i,info,nodedist])          


    itter_anzahl    =       len(var)      
    cpu_anzahl      =       multiprocessing.cpu_count()
    thread_in_cpu   =       itter_anzahl/cpu_anzahl



    # for _ in range(itter_anzahl):
    #     arrlist.append(Array('d',(erg_vek_gr + len(var[0]) )))

    processe         =  []  
    
    ganze           =   int(math.floor(thread_in_cpu))
    processe        =   []
    varlist         =   []
    

    for i in range(cpu_anzahl):
        varlist.append(i)
    


    
    u=0
    for t in range(cpu_anzahl):
        varlist[t]      =   var[u:(u+ganze)]  
        u = (u+ganze)

    ru = 0
    for r in range(len(var[u:])):
        varlist[r].append(var[u+ru])
        ru += 1


    if itter_anzahl < cpu_anzahl:
        cpu_anzahl  =   itter_anzahl
    else:
        pass

    for process_num in range(cpu_anzahl):
       

        [processe.append(Process(target=thread_cpu,    
                                    args=(varlist[process_num],  
                                        ret_dict,lock),
                                        name='{0}'.format(process_num)))]

    for process_num in range(cpu_anzahl):    
        processe[process_num].start()
    

    for process_num in range(cpu_anzahl):
        processe[process_num].join()
    


    logs    =   []
    for i in range(len(ret_dict.values())):
        for q in range(len(ret_dict.values()[i])):
            logs.append(ret_dict.values()[i][q])

    datetime = write_logs(logs)

    return logs,datetime

def run(info,nodedist,varl):

    make_dir(info)
    logs,datetime    =   parallel_compute(info,nodedist,varl)
    shutil.rmtree(".\\Prozesse")
    return logs,datetime


