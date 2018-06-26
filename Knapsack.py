#12253030
#Erdem Gencoglu

import Dosyadan
import sys

populasyon = []

print("Hesaplama bitmistir....")
print ('Out.txt cikti dosyayasini kontrol edniz!!!')

def KnapsackGA(populasyonlar):
    for i in populasyonDict(populasyonlar):
        #yazdirma
        ff = ""
        for ix in i[0]:
            ff = ff + str(ix)
        print("(", ff, "),", i[1])

    parents = parentSelect(populasyonlar) # Ebeveynleri sec (PARENT SELECT)
    cocuklar = recombineAndMutate(parents)  # Ebeveynleri caprazla (RECOMBINE) ve yavrulari mutasyona tabi tut (MUTATE)
    populasyonlarx = survivalSelect(cocuklar + populasyonlar)  # Tum listenin(100 ebevyn) degerlerini hesaplayip dictionary yapar ve sortladiktan sonra ilk 50 doner.
    # print ('\n')
    # print ('Toplam populasyon::::::::::',len(populasyonlarx))
    return populasyonlarx

#---------------------------- Canta ve Birey Kontrol metodlari --------------------------------------

# Random sayilari random listesinden getirir ve basa donmesini saglar.
def randomList():
    if Dosyadan.RANDOMITERASYONU == 10:
        Dosyadan.birle()
        return Dosyadan.RANDOMLAR[Dosyadan.RANDOMITERASYONU]
    Dosyadan.artir()
    return Dosyadan.RANDOMLAR[Dosyadan.RANDOMITERASYONU]


# Gelen birey cantaya sigip sigmadigi?
def weightCheck(gelenBirey):
    toplam = 0
    for iterator in range(len(Dosyadan.w)):

        if gelenBirey[iterator] == 1:
            toplam = toplam + Dosyadan.w[iterator]

    if toplam > Dosyadan.CANTABOYUTU:
        return False
    else:
        return True

# Gelen bireyin toplam degerini hesaplama
def valueCheck(gelenBireyx):
    toplamx = 0

    if weightCheck(gelenBireyx):
        for iterators in range(len(Dosyadan.w)):

            if gelenBireyx[iterators] == 1:
                toplamx = toplamx + Dosyadan.v[iterators]
        return toplamx
    else:
        return 0


# r'li formulden oran hesaplar
# min + (rand()*(max-min))
def calculateRrate(populasyonSayisi):
    return int(1 + (randomList() * (populasyonSayisi - 1)))


# Verilen arraydeki bireylerin valuelerini hesaplayip dictionary olarak dondurur.
def populasyonDict(populasyon):
    temmm = list()

    for b in range(len(populasyon)):
        str1 = []
        for i in populasyon[b]:
            str1.append(int(i))
        temmm.append((str1, valueCheck(populasyon[b])))
    return temmm

#------------------------------- Caprazlama Mutasyon Survival select metodlari ----------------------------

ths = open("out.txt", "a")
# ilk populasyon olusturulmasi 1000100011 gibi random listesine gore
def Initialise():
    birey = []
    bireyler = []

    while len(bireyler) < Dosyadan.POPULASYONBOYUTU:
        for i in range(len(Dosyadan.w)):
            if randomList() >= Dosyadan.BASLANGICOLASILIGI:
                birey.append(1)
            else:
                birey.append(0)
        bireyler.append(birey)
        birey = []
    return bireyler


# Ebeveyn secilmede uygun bireylerlerin hesaplanmasi
def parentSelect(bireyler):
    ebeveynler = []
    for xx in range(Dosyadan.EBEBEYNSAYISI):
        ind = calculateRrate(len(bireyler)) #r li formule gore ebevyn sec
        ebeveynler.append(bireyler[ind])
    return ebeveynler


# Cocuklara caprazlama yapar ve geri dondorur
def recombineAndMutate(parents):
    tempParents = []

    while len(parents) > 0:
        print("\nApplying Crossover")

        c1 = []#cocuk 1
        c2 = []#cocuk 2

        p1 = parents.pop()
        p2 = parents.pop()

        oran = calculateRrate(len(p1))

        # yazdirma
        ff111 = ""
        for ix in p1:
            ff111 = ff111 + str(ix)
        ff222 = ""
        for ix in p2:
            ff222 = ff222 + str(ix)
        # yazdirma sonu

        print("Parents:", ff111, ",", ff222, " at point ", oran)

        for iterator in range(oran):
            c1.append(p1[iterator])
            c2.append(p2[iterator])

        for iterator in range(oran, len(p1)):
            c2.append(p1[iterator])
            c1.append(p2[iterator])

        # yazdirma
        ff11 = ""
        for ix in c1:
            ff11 = ff11 + str(ix)
        ff22 = ""
        for ix in c2:
            ff22 = ff22 + str(ix)
        print("Offsprings:", ff11, ",", ff22)

        mutasyonlucocuk1 = Mutation(c1)
        mutasyonlucocuk2 = Mutation(c2)


        ff1 = ""
        for ix in mutasyonlucocuk1:
            ff1 = ff1 + str(ix)
        ff2 = ""
        for ix in mutasyonlucocuk2:
            ff2 = ff2 + str(ix)

        print("Mutated offsprings:", ff1, ",", ff2)

        tempParents.append(mutasyonlucocuk1)
        tempParents.append(mutasyonlucocuk2)
    return tempParents

#Cocuga mutasyon uygulama
def Mutation(cocuk):
    for iterasyon in range(len(cocuk)):
        if Dosyadan.MUTASYONOLASILIGI > randomList():
            if cocuk[iterasyon] == 0:
                cocuk[iterasyon] = 1
            else:
                cocuk[iterasyon] = 0
    return cocuk

#survival select uygulanmasi
def survivalSelect(nonCheckPopulation):
    yeniAdaylar = []

    allPopulation = populasyonDict(nonCheckPopulation)

    allPopulationx = sorted(allPopulation, key=lambda tup: tup[1])

    for i in range(Dosyadan.POPULASYONBOYUTU):
        at = allPopulationx.pop()[0]

        yen = []
        for x in range(len(at)):
            yen.append(at[x])

        yeniAdaylar.append(yen)
    return yeniAdaylar

#------------------------------- Ana Fonksiyon ---------------------------------
def main():
    global populasyon

    # Dosyadan gelen iterasyon sayisina gore islemleri tekrarla
    for iterasyon in range(Dosyadan.ITERASYONSAYISI):
        print("\n\n\n--------------------------- Generation: " + str(iterasyon) + " -----------------------------")

        if iterasyon == 0:
            # Baslangic populasyonunu rastgele olustur (INITIALISE)
            populasyon = Initialise()
            populasyon = KnapsackGA(populasyon)
        elif iterasyon == Dosyadan.ITERASYONSAYISI-1: #test 1 dosyasindan geliyor
            print("\n\nFinal Population:")

            # guzel yazdirma
            ff = ""
            for ix in populasyonDict(populasyon):
                ff = ff + str(ix) + "\n"
            print(ff)
            # guzel yazdirma sonu

        else:
            populasyon = KnapsackGA(populasyon)

if __name__ == '__main__':
    f = open("out.txt", "w")
    sys.stdout = f
    main()

