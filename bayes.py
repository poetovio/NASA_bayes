import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from math import sqrt
from math import pi
from math import exp

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

def class_povzetek(podatki):
    razbitje = klasifikacija(podatki)

    slovar = dict()

    for instanca, vrstice in razbitje.items():
        slovar[instanca] = povzemanje(vrstice)

    return slovar

def verjetnost(x, povprecje, deviation):
    eksponent = exp(-((x - povprecje)**2 / (2 * deviation**2)))

    return (1 / (sqrt(2 * pi) * deviation)) * eksponent


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

rezultat = class_povzetek(dataset)

for i in rezultat:
    print(i)
    for j in rezultat[i]:
        print(j)

print(verjetnost(1.0, 1.0, 1.0))
print(verjetnost(2.0, 1.0, 1.0))
print(verjetnost(0.0, 1.0, 1.0))