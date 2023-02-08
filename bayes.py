import numpy as np
from math import sqrt
from math import pi
from math import exp

# nalaganje podatkov

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

    del podatki[0] # brisanje prve vrstice

    for podatek in podatki:
        for x in range(len(podatek) - 1):
            podatek[x] = float(podatek[x])

        podatek[-1] = 0 if podatek[-1] == 'False' else 1 # če je nevaren, mu določi vrednost 1 in če ni nevaren, mu določi vrednost 0

    return podatki

# funkcija za razporeditev podatkov v razrede

def klasifikacija(podatki, napovedi):
    razredi = dict()

    for i, podatek in enumerate(podatki):
        vrednost = napovedi[i]

        if(vrednost not in razredi): # če še vrednost ni v nekem razredu, potem ta if stavek ustvari nov razred in ga dodeli notri
            razredi[vrednost] = list()
        
        razredi[vrednost].append(podatek)
    
    return razredi

# funkcija za izračun potrebnih podatkov (mean, stdev, st instanc) 

def data(podatki):
    povzetki = [(np.mean(vrstica), np.std(vrstica), len(vrstica)) for vrstica in zip(*podatki)]
    del(povzetki[-1])

    return povzetki

# funkcija za naucenje modela

def ucenje(podatki, napovedi):
    razbitje = klasifikacija(podatki, napovedi)

    slovar = dict()

    for instanca, vrstice in razbitje.items():
        slovar[instanca] = data(vrstice)

    return slovar

# funkcija za izračun verjetnosti, ali neka instanca spada v določen razred

def verjetnost(x, povprecje, odstop):
    eksponent = exp(-((x - povprecje)**2 / (2 * odstop**2))) # Gaussian Probability Distribution Function

    return (1 / (sqrt(2 * pi) * odstop)) * eksponent

# funkcija za določitev, kateremu razredu pripada neka instanca

def pripadanje(povzetek, vrstica):
    sestevek = sum([povzetek[instanca][0][2] for instanca in povzetek])

    pripadnost = dict()

    for instanca, povzetki in povzetek.items():
        pripadnost[instanca] = povzetek[instanca][0][2] / float(sestevek)

        for i in range(len(povzetki)): # za vsak razred izračuna verjetnost, kateremu bi lahko pripadalo s pomočjo Gaussian PDF
            povprecje, odstop, _ = povzetki[i]
            pripadnost[instanca] *= verjetnost(vrstica[i], povprecje, odstop)
    
    return pripadnost

# napovedna funkcija

def napoved(model, vrstica):
    rezultat = pripadanje(model, vrstica)

    best_label, best_prob = None, -1
    for class_value, probability in rezultat.items():
        if best_label is None or probability > best_prob:
            best_prob = probability
            best_label = class_value
    
    return best_label

# implementacija train test split

def splitting(podatki):
    x_train, x_test = np.split(podatki, [int(0.8 * len(podatki))]) # razbitje podatkovne množice v razmerju 4:1 (80% : 20%)

    y_train = []

    y_test = []

    for element in x_train:
        y_train.append(element[-1])

    for element in x_test:
        y_test.append(element[-1])

    x_train = np.delete(x_train, x_train.shape[1]-1, 1)
    x_test = np.delete(x_test, x_test.shape[1]-1, 1)

    return x_train, y_train, x_test, y_test

# funkcija za izračun točnosti modela

def tocnost(napoved, test):
    stevec = 0

    for i in range(len(napoved)):
        stevec += 1 if napoved[i] == test[i] else 0

    return  stevec / float(len(napoved)) * 100.0

# funkcija za izračun senzitivnosti

def senzitivnost(napoved, test):
    stevec = 0
    stevec2 = 0

    for i in range(len(napoved)):
        stevec += 1 if napoved[i] == 1.0 and test[i] == 1.0 else 0
        stevec2 += 1 if napoved[i] == 1.0 else 0

    return stevec / float(stevec2) * 100.0

# funkcija za izračun specifičnosti

def specificnost(napoved, test):
    stevec = 0
    stevec2 = 0

    for i in range(len(napoved)):
        stevec += 1 if napoved[i] == 0.0 and test[i] == 0.0 else 0
        stevec2 += 1 if napoved[i] == 0.0 else 0

    return stevec / float(stevec2) * 100.0

# funkcija za izračun priciznosti

def precision(napoved, test):
    stevec = 0
    stevec2 = 0

    for i in range(len(napoved)):
        stevec += 1 if napoved[i] == 1.0 and test[i] == 1.0 else 0
        stevec2 += 1 if test[i] == 1.0 else 0

    return stevec / float(stevec2) * 100.0

# funkcija za izračun matrike zmede

def matrika(napoved, test):
    matrika = dict.fromkeys(['TP', 'FP', 'TN', 'FN'], 0)

    key1 = 'TP'
    key2 = 'FP'
    key3 = 'TN'
    key4 = 'FN'

    for i in range(len(napoved)):
        if(napoved[i] == 1.0 and test[i] == 1.0):
            matrika[key1] += 1
        elif (napoved[i] == 1.0 and test[i] == 0.0):
            matrika[key4] += 1
        elif (napoved[i] == 0.0 and test[i] == 0.0):
            matrika[key3] += 1
        else:
            matrika[key2] += 1

    array = [[matrika['TP'], matrika['FN']], [matrika['FP'], matrika['TN']]]

    print(np.matrix(array))

    return matrika

# implementacija algoritma

def algoritem():
    podatki = file_load('./neo.csv')

    x_train, y_train, x_test, y_test = splitting(podatki) # razdelitev podatkov na učno in testno množico

    model = ucenje(x_train, y_train) # učenje modela

    napovedi = [] # nabor vseh napovedi

    for vrstica in x_test:
        rezultat = napoved(model, vrstica)
        napovedi.append(rezultat)

    print(f'~ Točnost našega modela znaša -> {tocnost(napovedi, y_test)}')
    print(f'~ Senzitivnost = priklic našega modela znaša -> {senzitivnost(napovedi, y_test)}')
    print(f'~ Specifičnost našega modela znaša -> {specificnost(napovedi, y_test)}')
    print(f'~ Priciznost našega modela znaša -> {precision(napovedi, y_test)}')

    print('Matrika zmede za naš model:')

    print(matrika(napovedi, y_test))
    
    return 0

algoritem()