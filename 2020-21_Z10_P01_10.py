import numpy as np
import math


def unos_vece_od(poruka, donja_granica):
    while True:
        try:
            podatci = int(input(poruka))
            if podatci >= donja_granica:
                return podatci
            else:
                print("Neispravan unos!")
        except ValueError:
            print("Neispravan unos!")
            continue


def unos_jedan_ili_nula():
    while True:
        try:
            podatci = int(input("Unesi 0 ili 1: "))
            if podatci == 0 or podatci == 1:
                return podatci
            else:
                print("Neispravan unos!")
        except ValueError:
            print("Neispravan unos!")
            continue


def unos_matrice(redci, stupci):
    print("unesi elemente generirajuce matrice (s lijeva na desno, od vrha prema dnu):")
    return np.array([[int(unos_jedan_ili_nula()) for _x in range(stupci)] for _y in range(redci)])


def ima_jedinicnu_matricu(k, generirajuca_matrica):
    for i in range(k):
        for j in range(k):
            if (i != j and generirajuca_matrica[i][j] != 0) or (i == j and generirajuca_matrica[i][j] != 1):
                return False

    return True


def ima_standardni_oblik(k, generirajuca_matrica):
    return np.linalg.matrix_rank(generirajuca_matrica) == k


def nabavi_standardni_oblik(generirajuca_matrica):
    matrica = np.array(generirajuca_matrica)
    redci, stupci = matrica.shape
    lista_redci = list(np.arange(redci))

    while lista_redci:
        polozaj = lista_redci[0]

        if matrica[polozaj, polozaj] == 0:

            zamjena_redci = provjera_stupci(matrica, polozaj)
            if zamjena_redci != -1:
                matrica[[polozaj, zamjena_redci]] = matrica[[zamjena_redci, polozaj]]

            else:
                zamjena_stupci = nabavi_zamjena_stupca(matrica, polozaj)
                matrica[:, [polozaj, zamjena_stupci]] = matrica[:, [zamjena_stupci, polozaj]]

        for i in range(redci):
            if matrica[i, polozaj] == 1 and i != polozaj:
                matrica[i, :] = matrica[i, :] - matrica[polozaj, :]
        matrica = np.where(matrica == -1, 1, matrica)
        lista_redci.pop(0)

    return matrica


def provjera_stupci(matrica, stupac):
    redci = matrica.shape[0]
    for i in range(stupac, redci):
        if matrica[i][stupac] == 1:
            return i
    return -1


def nabavi_zamjena_stupca(matrica, redak):
    stupci = matrica.shape[1]
    for i in range(redak, stupci):
        if matrica[redak][i] == 1:
            return i


def nabavi_kodove(matrica, k, n):
    izlaz = []
    matrica = ["".join(item) for item in matrica.astype(str)]

    for i in range(2 ** k):
        tmp = i - 2 ** k
        kod = 0
        for j in range(k):
            kod = kod ^ (((tmp & (1 << j)) >> j) * int(matrica[j], 2))
        izlaz.append([format(kod, "0" + str(n) + "b")])

    return np.array(izlaz)


def provjera_linearnost(kodovi, n):
    if ("0" * n) not in kodovi:
        return False

    for i in range(len(kodovi)):
        for j in range(len(kodovi)):
            if format((int(kodovi[i][0], base=2) ^ int(kodovi[j][0], base=2)), "0" + str(n) + "b") not in kodovi:
                return False

    return True


def hammingova_udaljenost(x, y, n):
    ans = 0
    for i in range(n - 1, -1, -1):
        ans += not (x >> i & 1 == y >> i & 1)
    return ans


def provjera_perfektan(kodovi, k, n):
    _min = n

    for i in range(len(kodovi)):
        for j in range(len(kodovi)):
            if i != j and hammingova_udaljenost(int(kodovi[i][0], base=2), int(kodovi[j][0], base=2), n) < _min:
                _min = hammingova_udaljenost(int(kodovi[i][0], base=2), int(kodovi[j][0], base=2), n)

    t = math.floor((_min - 1) / 2)
    tmp_sum = 0

    for i in range(t + 1):
        tmp_sum += math.factorial(n) / (math.factorial(i) * math.factorial(n - i))

    return 2 ** k == 2 ** n / tmp_sum


def kodna_brzina(k, n):
    return k / n


def kodiraj_poruku(k, n, generirajuca_matrica):
    poruka = []
    print("Unesi poruku: ")

    for _ in range(k):
        poruka.append(unos_jedan_ili_nula())

    poruka = np.dot(np.array(poruka), generirajuca_matrica)
    for i in range(n):
        poruka[i] %= 2

    return ["".join(poruka.astype(str))]


def main():
    redci = unos_vece_od("Unesi broj redaka: ", 1)
    print()
    stupci = unos_vece_od("Unesi broj stupaca: ", redci + 1)
    print()

    print("Za ovaj kod k je {} a n je {}!".format(redci, stupci))
    print()

    generirajuca_matrica = unos_matrice(redci, stupci)
    print()
    print("Ovo je generirajuca matrica: ")
    print(generirajuca_matrica)
    print()

    if ima_jedinicnu_matricu(redci, generirajuca_matrica):
        print("Ova generirajuca matrica je vec u standardnom obliku!")
    else:
        print("Ova generirajuca matrica nije u standardnom obliku, pokusavam ispraviti!")
        if ima_standardni_oblik(redci, generirajuca_matrica):
            generirajuca_matrica = nabavi_standardni_oblik(generirajuca_matrica)
            print(generirajuca_matrica)
        else:
            raise Exception("Matrica nije ispravna!")
    print()

    kodovi = nabavi_kodove(generirajuca_matrica, redci, stupci)
    print("Ovo su svi kodovi: ")
    print(kodovi)
    print()

    print("Ovaj kod je linearan!") if provjera_linearnost(kodovi, stupci) else print("Ovaj kod nije linearan!")
    print()

    print("Ovaj kod je perfektan!") if provjera_perfektan(kodovi, redci, stupci) else print("Ovaj kod nije perfektan!")
    print()

    print("Brzina ovog koda je: {:.2f}%".format(kodna_brzina(redci, stupci) * 100))
    print()

    kodirana_poruka = kodiraj_poruku(redci, stupci, generirajuca_matrica)
    print()
    print("Tvoja poruka je kodirana kao: {}".format(kodirana_poruka))
    print()
    input("Pritisni Enter za nastavak...")


if __name__ == "__main__":
    main()
