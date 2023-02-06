import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from math import sqrt
from math import pi
from math import exp
from csv import reader
import random

def file_load(path):
    podatki = []
    with open(path, 'r') as datoteka:
        for element in datoteka:
            podatki.append(element)

    return podatki

def klasifikacija(podatki):
    classes = dict()

    for podatek in podatki:
        vrednost = podatek[-1]
        if(vrednost not in classes):
            classes[vrednost] = list()
        classes[vrednost].append(podatek)
    
    return classes

def povzemanje(podatki):
    # return [(np.mean(vrstica), np.std(vrstica), len(vrstica)) for vrstica in zip(*podatki)]
    povzetki = [(np.mean(vrstica), np.std(vrstica), len(vrstica)) for vrstica in zip(*podatki)]
    del(povzetki[-1])
    return povzetki

def class_povzetek(podatki):
    razbitje = klasifikacija(podatki)

    slovar = dict()

    for instanca, vrstice in razbitje.items():
        slovar[instanca] = povzemanje(vrstice)

    return slovar

def verjetnost(x, povprecje, deviation):
    eksponent = exp(-((x - povprecje)**2 / (2 * deviation**2)))

    return (1 / (sqrt(2 * pi) * deviation)) * eksponent

def pripadanje(povzetek, vrstica):
    sestevek = sum([povzetek[instanca][0][2] for instanca in povzetek])

    pripadnost = dict()

    for instanca, povzetki in povzetek.items():
        pripadnost[instanca] = povzetek[instanca][0][2] / float(sestevek)

        for i in range(len(povzetki)):
            povprecje, deviation, _ = povzetki[i]
            pripadnost[instanca] *= verjetnost(vrstica[i], povprecje, deviation)
    
    return pripadnost

def navkriznaValidacija(podatki, stKosov):
    data = list()
    kopija = list(podatki)

    velikostKosa = int(len(podatki) / stKosov)

    preurejeno = random.sample(podatki, len(podatki))

    stevec = 0

    for i in range(stKosov):
        kos = list()

        for j in range(velikostKosa):
            kos.append(preurejeno[stevec])
            stevec += 1

        data.append(kos)

    return data


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

rezultat2 = pripadanje(rezultat, dataset[1])

print(rezultat)
print(rezultat2)

print(navkriznaValidacija(dataset, 3))