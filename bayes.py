import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def klasifikacija(podatki):
    classes = dict()

    for podatek in podatki:
        vrednost = podatek[-1]
        if(vrednost not in classes):
            classes[vrednost] = list()
        classes[vrednost].append(podatek)
    
    return classes

def povzemanje(podatki):
    return [(np.mean(vrstica), np.std(vrstica), len(vrstica)) for vrstica in zip(*podatki)]


def algoritem():
    # TODO: -> potrebno implementirati
    return 0

#test

dataset = [[3.393533211,2.331273381,0],
 [3.110073483,1.781539638,0],
 [1.343808831,3.368360954,0],
 [3.582294042,4.67917911,0],
 [2.280362439,2.866990263,0],
 [7.423436942,4.696522875,1],
 [5.745051997,3.533989803,1],
 [9.172168622,2.511101045,1],
 [7.792783481,3.424088941,1],
 [7.939820817,0.791637231,1]]

print(povzemanje(dataset)) 