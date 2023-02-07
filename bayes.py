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
    
    indeksi = [0, 1, 6, 7] # indeksi irelevantnih stolpcev

    with open(path, 'r') as datoteka:
        for element in datoteka:

            podatek = element.split(",")

            podatek[9] = ''.join(podatek[9].splitlines()) # odstrani \n v vrednosti

            for i in sorted(indeksi, reverse=True): # zanka odstrani nepomembne stolpce, ki se ne bodo uporabili v učenju
                del podatek[i]

            podatki.append(podatek)

    del podatki[0]

    for podatek in podatki:
        for x in range(len(podatek) - 1):
            podatek[x] = float(podatek[x])

        podatek[-1] = 0 if podatek[-1] == 'False' else 1 # če je nevaren, mu določi vrednost 1 in če ni nevaren, mu določi vrednost 0

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

def verjetnost(x, povprecje, odstop):
    eksponent = exp(-((x - povprecje)**2 / (2 * odstop**2)))

    return (1 / (sqrt(2 * pi) * odstop)) * eksponent

def pripadanje(povzetek, vrstica):
    sestevek = sum([povzetek[instanca][0][2] for instanca in povzetek])

    pripadnost = dict()

    for instanca, povzetki in povzetek.items():
        pripadnost[instanca] = povzetek[instanca][0][2] / float(sestevek)

        for i in range(len(povzetki)):
            povprecje, odstop, _ = povzetki[i]
            pripadnost[instanca] *= verjetnost(vrstica[i], povprecje, odstop)
    
    return pripadnost

def navkriznaValidacija(podatki, stKosov):
    data = list()

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
    podatki = file_load('./neo.csv')
    
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

print(file_load('./neo.csv')[1])