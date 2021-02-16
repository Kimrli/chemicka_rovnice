# Program, který vytvoří tabulku (pole) periodické soustavy prvků (PSP), pomocí informací z textového souboru
# 'periodicka_tabulka_prvku.txt'

import os


class ChemPrvek:
    # Třída objektů představující jednotlivé chemické prvky.
    def __init__(self, protonove_cislo, znacka_prvku, cs_nazev_prvku, la_nazev_prvku, rel_atom_hmot):
        self.protonove_cislo = int(protonove_cislo)
        self.znacka_prvku = znacka_prvku
        self.cs_nazev_prvku = cs_nazev_prvku  # český název prvku
        self.la_nazev_prvku = la_nazev_prvku  # latinský název prvku
        self.rel_atom_hmot = float(rel_atom_hmot)  # relativní atomová hmotnost prvku

    def print_info(self, soubor):
        # Vypíše informace o chemickém prvku na konzoli a do textového souboru.
        info = f"{self.znacka_prvku}: {self.cs_nazev_prvku} ({self.la_nazev_prvku}), {self.protonove_cislo}, " \
               f"{self.rel_atom_hmot} g/mol"
        soubor.write(info + "\n")
        print(info)


def vytvor_prvek(soubor):
    # Načte z textového souboru informace o chemickém prvku a vrátí objekt třídy ChemPrvek.
    soubor.readline()  # Před každým chemickým prvkem je prázdný řádek.
    protonove_cislo = soubor.readline().strip("\n")
    znacka_prvku = soubor.readline().strip("\n")
    cs_nazev_prvku = soubor.readline().strip("\n")
    la_nazev_prvku = soubor.readline().strip("\n")
    rel_atom_hmot = soubor.readline().strip("\n")
    prvek = ChemPrvek(protonove_cislo, znacka_prvku, cs_nazev_prvku, la_nazev_prvku, rel_atom_hmot)
    return prvek


def vytvor_PSP(soubor):
    # Vytvoří pole prvků z textového souboru.
    pocet_prvku = int(soubor.readline())  # Velikost tabulky (pole) prvků
    tabulka = [ChemPrvek(0, "", "", "", 0)]  # Prázdný prvek, díky kterému budou protonová čísla prvků odpovídat
    # indexům v poli.
    for _ in range(pocet_prvku):
        prvek = vytvor_prvek(soubor)
        tabulka.append(prvek)
    return tabulka


def najdi_prvek(znacka_hledaneho, pole_prvku):
    # Prohledá pole prvků (objekty třídy ChemickyPrvek) podle jejich značek a buď vrátí odpovídající chemický prvek,
    # nebo vrátí False, pokud hledaný prvek v daném poli neexistuje.
    for prvek in pole_prvku:
        if prvek.znacka_prvku == znacka_hledaneho:
            return prvek
    return False


# Načtení periodické tabulky prvků
while not os.path.isfile("periodicka_tabulka_prvku.txt"):
    print("Zdrojová složka neobsahuje soubor 'periodicka_tabulka_prvku.txt' potřebnou pro fungování programu.")
    input("Doplňte soubor 'periodicka_tabulka_prvku.txt' (viz README.txt) a stiskněte ENTER.")
with open("periodicka_tabulka_prvku.txt", "r") as zdrojovy_soubor:
    PSP = vytvor_PSP(zdrojovy_soubor)
