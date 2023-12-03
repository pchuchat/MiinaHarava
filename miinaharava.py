import random as r
import haravasto as ha
import time as t
from copy import deepcopy

"""
Määritellään globaalit sanakirjat, joita pelissä tarvitaan.
"""
kentan_miinat = {"kentta": None}
pelikentta = {"kentta": None}

sanakirja = {
    "leveys": 0,
    "korkeus": 0,
    "miinat": 0,
    "vapaat": 0,
    "eka_klik": True,
    "muuvit": 0,
    "lopputulos": None,
    "lopetus": False

}

def kysy_ikkuna():
    """
    Kysyy pelaajalta peli-ikkunan korkeuden ja leveyden.
    """
    while True:
        try:
            syote1 = input("Anna ruudukon leveys positiivisena kokonaislukuna: ")
            leveys = int(syote1)

            if leveys > 0:
                sanakirja["leveys"] = leveys
                break
            else:
                print("Leveyden tulee olla positiivinen kokonaisluku.")
        except ValueError:
            print("Virheellinen syöte. Anna positiivinen kokonaisluku.")

    while True:
        try:
            syote2 = input("Anna ruudukon korkeus positiivisena kokonaislukuna: ")
            korkeus = int(syote2)

            if korkeus > 0:
                sanakirja["korkeus"] = korkeus
                break
            else:
                print("Korkeuden tulee olla positiivinen kokonaisluku.")
        except ValueError:
            print("Virheellinen syöte. Anna positiivinen kokonaisluku.")

def kysy_miinojenlkm():
    """
    Kysyy pelaajalta miinojen lukumäärän.
    """

    while True:
        try:
            syote3 = input("Anna miinojen lukumäärä: ")
            lkm = int(syote3)

            if lkm > 0 and lkm <= (sanakirja["leveys"] * sanakirja["korkeus"]):
                sanakirja["miinat"] = lkm
                break
            else:
                print("Lukumäärän tulee olla positiivinen ja pienempi kuin ikkunan ruutujen lukumäärän.")
        except ValueError:
            print("Virheellinen syöte. Anna positiivinen kokonaisluku.")



def luo_kentat(sanakirja):
    """
    Luo ruudukot pelikentälle ja miinoille pelaajan valintojen mukaisesti.
    """

    peli_ikkuna = []
    miinaikkuna = []

    for rivi in range(sanakirja["korkeus"]):
        peli_ikkuna.append([])
        miinaikkuna.append([])

        for sarake in range(sanakirja["leveys"]):
            peli_ikkuna[-1].append(" ")
            miinaikkuna[-1].append(" ")

    pelikentta["kentta"] = peli_ikkuna
    kentan_miinat["kentta"] = miinaikkuna
    sanakirja["vapaat"] = deepcopy(pelikentta)

def miinoita(kentta, miinat, aloituskohta):
    """
    Asettaa kentälle n kpl miinoja satunnaisiin paikkoihin.
    """
    vapaat = []
    for y in range(len(kentta)):
        for x in range(len(kentta[0])):
            if (y, x) != aloituskohta:
                vapaat.append((y, x))

    while miinat > 0 and vapaat:
        y, x = r.choice(vapaat)
        vapaat.remove((y, x))
        kentta[y][x] = "x"
        miinat -= 1


def klikkausfunktio(x, y, hiiren_painike, muokkaustoiminto):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa hiirellä jotain ruutua. Riippuen siitä mistä pelaaja klikkaa ja onko klikkaus ensimmäinen tekee tarvittavan toiminnan.
    skenaariot vasen painike: ruuudssa on miina tai ruutu on tyhjä ja alkaa tulvatäyttö. Jos kyseessä on eka klikkaus täytyy miinoittaa ensin.
    skenaariot oikea painike: liputetaan tai oteaan lippu pois
    """

    hiiren_painikkeet = {
        ha.HIIRI_VASEN: "vasen",
        ha.HIIRI_KESKI: "keski",
        ha.HIIRI_OIKEA: "oikea"
    }.get(hiiren_painike, "tuntematon")

    x = int(x/40)
    if x >= sanakirja["leveys"]:
        x -= 1
    y = int(y/40)
    if y >= sanakirja["korkeus"]:
        y -= 1

    if sanakirja["lopetus"]:
        return 
    
    print(f"Klikkaus: x={x}, y={y}, painike={hiiren_painike}, muokkaustoiminto={muokkaustoiminto}")


    if hiiren_painikkeet == "vasen":
        if kentan_miinat["kentta"][y][x] == "x":
            if pelikentta["kentta"][y][x] != "f":
                pelikentta["kentta"][y][x] = "x"
                paljasta_miinat()
                ha.aseta_piirto_kasittelija(piirra_kentta)
                sanakirja["lopputulos"] = "Häviö"
                sanakirja["lopetus"] = True
                print("Hävisit pelin, haravoi tarkemmin ensi kerralla!")

        if kentan_miinat["kentta"][y][x] == " ":
            if sanakirja["eka_klik"]:
                miinoita(kentan_miinat["kentta"], sanakirja["miinat"], (x, y))
                sanakirja["eka_klik"] = False

            tulvataytto(kentan_miinat["kentta"], y, x)
            ha.aseta_piirto_kasittelija(piirra_kentta)
            sanakirja["muuvit"] += 1
            if not sanakirja["vapaat"]:
                sanakirja["lopputulos"] = "Voitto"
                sanakirja["lopetus"] = True
                print("Voitit pelin, hienosti haravoitu!")

    if hiiren_painikkeet == "oikea":

        if pelikentta["kentta"][y][x] == " ":
           pelikentta["kentta"][y][x] = "f"

        elif pelikentta["kentta"][y][x] == "f":
           pelikentta["kentta"][y][x] = " "

        ha.aseta_piirto_kasittelija(piirra_kentta)

def paljasta_miinat():
    for y in range(len(kentan_miinat["kentta"])):
        for x in range(len(kentan_miinat["kentta"][0])):
            if kentan_miinat["kentta"][y][x] == "x":
                pelikentta["kentta"][y][x] = "x"


def tulvataytto(kentta, y, x):
    """
    Tarkistaa onko klikatun kohdan ympärillä miinoja ja paljastaa lähialueen tyhjät kohdat.
    """
    alku_lista = [(y, x)]
    leveys = len(kentta[0])
    pituus = len(kentta)
    while alku_lista:
        y, x = alku_lista.pop()
        if kentta[y][x] == " ":
            vierus_miinat_lkm = 0
            for y_1 in range(-1, 2):
                for x_1 in range(-1, 2):
                    uusi_x = x + x_1
                    uusi_y = y + y_1
                    if 0 <= uusi_x < leveys and 0 <= uusi_y < pituus:
                        if kentta[uusi_y][uusi_x] == "x":
                            vierus_miinat_lkm += 1

            if vierus_miinat_lkm == 0:
                kentta[y][x] = "0"
                for y_1 in range(-1, 2):
                    for x_1 in range(-1, 2):
                        uusi_x = x + x_1
                        uusi_y = y + y_1
                        if 0 <= uusi_x < leveys and 0 <= uusi_y < pituus:
                            if kentta[uusi_y][uusi_x] == " " and (uusi_y, uusi_x) not in alku_lista:
                                alku_lista.append((uusi_y, uusi_x))
            else:
                kentta[y][x] = str(vierus_miinat_lkm)

def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    ha.tyhjaa_ikkuna()
    ha.piirra_tausta()
    ha.aloita_ruutujen_piirto()

    for j in range(len(pelikentta["kentta"])):
        for i, avain in enumerate(pelikentta["kentta"][j]):
            ha.lisaa_piirrettava_ruutu(avain, i * 40, j * 40)
            
    
    
    ha.piirra_ruudut()



def main():
    kysy_ikkuna()
    kysy_miinojenlkm()
    luo_kentat(sanakirja)

    ha.lataa_kuvat("spritet")
    ha.luo_ikkuna(sanakirja["leveys"] * 40, sanakirja["korkeus"] * 40)
    ha.aseta_piirto_kasittelija(piirra_kentta)
    ha.aseta_hiiri_kasittelija(klikkausfunktio)

    ha.aloita()

if __name__ == "__main__":
    main()
