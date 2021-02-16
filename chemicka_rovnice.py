# Program, který zkontroluje platnost chemické rovnice, vyčíslí ji a vypíše informace o reagujících látkách.

import nacteni_PSP  # Program, který umožňuje ověřovat existenci chemických prvků.


class Molekula:
    # Třída objektů představujících jednotlivé reakční látky (molekuly).
    def __init__(self, vzorec_molekuly):
        self.vzorec_molekuly = vzorec_molekuly
        self.stech_koef = 1  # Stechiometrický koeficient
        self.prvky_molekuly = self.slozeni_molekuly()  # Pole obsahující objekty třídy PrvekMolekuly
        self.pocet_castic = self.soucet_castic()  # Celkový počet atomů v molekule
        self.molarni_hmot = self.soucet_hmot()  # Molární hmotnost molekuly
        for prvek in self.prvky_molekuly:
            # Vypočítání molárních a hmnotnostích zlomků jednotlivých prvků vůči molekule.
            prvek.molarni_zlomek = vypocet_zlomek(prvek.pocet_atomu, self.pocet_castic)
            prvek.hmotnostni_zlomek = vypocet_zlomek(prvek.molarni_hmot * prvek.pocet_atomu, self.molarni_hmot)
        self.hmotnostni_zlomek = 0

    def slozeni_molekuly(self):
        # Funkce, která "přečte" vzorec molekuly a vytvoří pole jejích prvků (objekty třídy PrvekMolekuly)
        prvky_molekuly = []
        vzorec_molekuly = self.vzorec_molekuly + "Z"  # Přídáním "Z" bude možné přečíst i poslední znak vzorce
        pocet_atomu = 1  # Výchozí počet atomů prvku v dané molekule
        znacka_start_index = 0
        cislo_start_index = -1
        PSP_prvek = None  # Chemický prvek z PSP odpovídající vytvářenému prvku molekuly

        for i in range(len(vzorec_molekuly)):
            # Cyklus, který čte vzorec molekuly znaku po znaku.
            znak = vzorec_molekuly[i]

            if i > 0 and vzorec_molekuly[i-1].isdigit() and not (znak.isupper() or znak.isdigit()):
                # Ověření správného zápisu molekuly a případná možnost opravy. (Po čísle určující počet atomů musí
                # následovat velké písmeno (další prvek).)
                prvky_molekuly = self.oprava_molekuly("nesprávný zápis")
                return prvky_molekuly

            elif znak.isupper():  # Velké písmeno značí začátek značky prvku.
                if cislo_start_index != -1:
                    # Počet atomů předchozího prvku je větší než jedna.
                    pocet_atomu = int(vzorec_molekuly[cislo_start_index:i])
                    cislo_start_index = -1
                elif vzorec_molekuly[znacka_start_index:i] != "":
                    # Před velkým písmenem je buď číslo, nebo značka jiného prvku, pokud nejde o první znak.
                    znacka_prvku = vzorec_molekuly[znacka_start_index:i]
                    PSP_prvek = nacteni_PSP.najdi_prvek(znacka_prvku, nacteni_PSP.PSP)  # Ověření, že daný prvek
                    # existuje a případná možnost opravy.
                    if PSP_prvek is False:
                        prvky_molekuly = self.oprava_molekuly("neexistující prvek")
                        return prvky_molekuly
                if PSP_prvek is not None:
                    # Pokud nejde o první znak, předchází velkému písmenu jiný chemický prvek.
                    if pocet_atomu == 0:
                        prvky_molekuly = self.oprava_molekuly("nesprávný zápis")
                        return prvky_molekuly
                    prvek = PrvekMolekuly(pocet_atomu, PSP_prvek, self)
                    prvky_molekuly.append(prvek)
                    pocet_atomu = 1
                znacka_start_index = i  # Velké písmeno značí začátek značky prvku.

            elif znak.isdigit() and cislo_start_index == -1:
                # Začátek počtu atomů prvku v dané molekule.
                cislo_start_index = i
                if vzorec_molekuly[znacka_start_index:i] == "":
                    # Před číslem určující počet atomů musí být značka daného prvku, jinak jde
                    # o stechiometrický koeficient.
                    prvky_molekuly = self.oprava_molekuly("stech koeficient")
                    return prvky_molekuly
                znacka_prvku = vzorec_molekuly[znacka_start_index:i]
                PSP_prvek = nacteni_PSP.najdi_prvek(znacka_prvku, nacteni_PSP.PSP)  # Ověření, že daný prvek
                # existuje a případná možnost opravy.
                if PSP_prvek is False:
                    prvky_molekuly = self.oprava_molekuly("neexistující prvek")
                    return prvky_molekuly
        return prvky_molekuly

    def oprava_molekuly(self, chyba):
        # Funkce umožňující opravu vzorce molekuly v případě chybného zápisu.
        oprava = ""
        if chyba == "nesprávný zápis":
            oprava = input(f"{self.vzorec_molekuly} není platná molekula, zadejte molekulu znovu: \n ==>")
        elif chyba == "neexistující prvek":
            oprava = input(f"{self.vzorec_molekuly} není platná molekula! Nějaký prvek molekuly neexistuje. "
                           f"Zadejte molekulu znovu: \n ==> ")
        elif chyba == "stech koeficient":
            oprava = input(f"Zadávejte jednotlivé molekuly bez stechiometrických koeficientů. "
                           f"Zadejte molekulu {self.vzorec_molekuly} znovu: \n ==> ")
        oprava_molekuly = Molekula(oprava)
        oprava_slozeni = oprava_molekuly.slozeni_molekuly()
        self.vzorec_molekuly = oprava_molekuly.vzorec_molekuly
        return oprava_slozeni

    def soucet_castic(self):
        # Spočítá celkový počet atomů v dané molekule
        pocet_castic = 0
        for prvek in self.prvky_molekuly:
            pocet_castic += prvek.pocet_atomu
        return pocet_castic

    def soucet_hmot(self):
        # Spočítá celkovou molární hmotnost molekuly
        molarni_hmot = 0
        for prvek in self.prvky_molekuly:
            molarni_hmot += (prvek.molarni_hmot * prvek.pocet_atomu)
        return molarni_hmot

    def print_info(self, soubor):
        # Vypíše informace o reakční látce na konzoli a do textového souboru.
        info = f"{self.vzorec_molekuly}: {self.molarni_hmot} g/mol, {self.hmotnostni_zlomek} % (hmotnostni zlomek)"
        soubor.write(info + "\n")
        print(info)


class PrvekMolekuly:
    # Třída objektů představujících jednotlivé prvky v daných molekulách.
    def __init__(self, pocet_atomu, PSP_prvek, molekula):
        self.pocet_atomu = pocet_atomu  # Počet atomů prvku vůči molekule, ve které se nachází.
        self.PSP_prvek = PSP_prvek  # Objekt třídy ChemickyPrvek
        self.znacka_prvku = PSP_prvek.znacka_prvku
        self.molarni_hmot = PSP_prvek.rel_atom_hmot  # Molární hmotnost prvku
        self.molekula = molekula  # Molekula, ve které se tento prvek nachází.
        self.molarni_zlomek = 0  # Molární zlomek prvku vůči molekule, ve které se nachází.
        self.hmotnostni_zlomek = 0  # Hmotností zlomek prvku vůči molekule, ve které se nachází.

    def print_info(self, soubor):
        # Vypíše informace o prvku molekuly na konzoli a do textového souboru.
        info = f"-> {self.znacka_prvku}: {self.molarni_zlomek} % (molarni zlomek), {self.hmotnostni_zlomek} % " \
               f"(hmotnostni zlomek)"
        soubor.write(info + "\n")
        print(info)


def vycisleni_reakce():
    # Celý proces vyčíslení reakce od zadání až po vypsání výsledku.
    leva_strana, prava_strana = reakce_vstup()
    prvky_soustavy = souhrn_prvku(leva_strana, prava_strana)

    if prvky_soustavy is not None:
        # Reakce se vyčíslí, pouze pokud je platná.
        reakcni_latky = leva_strana + prava_strana  # Sloučení molekul z obou stran reakce do jednoho pole.
        mat_reakce = matice_reakce(reakcni_latky, prvky_soustavy, len(leva_strana))
        mat_reakce = gaussova_eliminace(mat_reakce, i=0, j=0)
        stech_koeficienty = dosazeni(mat_reakce)
        for i in range(len(reakcni_latky)):
            # Přirazení jednotlivých stechiometrických koeficientům odpovídajícím molekulám.
            reakcni_latky[i].stech_koef = stech_koeficienty[i]
        hmotnost = hmot_soustavy(leva_strana)  # Celková hmotnost soustavy, která je určená součtem hmotností molekul
        # na jedné straně reakce.
        for molekula in reakcni_latky:
            # Přirazení hmotnostních zlomků molekul vůči hmotnosti soustavy.
            molekula.hmotnostni_zlomek = vypocet_zlomek(molekula.molarni_hmot * molekula.stech_koef, hmotnost)

        with open("vystup.txt", "w") as vystup:
            # Vytištění výsledné reakce a informací na konzoli a do textového souboru.
            print_reakce(leva_strana, prava_strana, vystup)
            for molekula in reakcni_latky:
                molekula.print_info(vystup)
                for prvek in molekula.prvky_molekuly:
                    prvek.print_info(vystup)
                vystup.write("\n")
                print("")
            for prvek in prvky_soustavy:
                prvek.print_info(vystup)


def reakce_vstup():
    # Funkce pro zadání chemické reakce.
    leva_strana = input("Zadejte výchozí látky reakce. Např.: H2 + O2; NaCl + H2O:\n==> ").split(" + ")
    prava_strana = input("Zadejte produkty reakce. Např.: H2O; NaOH + HCl:\n==> ").split(" + ")
    if leva_strana == [""] or prava_strana == [""]:
        print("\nChemická reakce musí mít alespoň jeden reaktant a jeden produkt!\n")
        return reakce_vstup()  # Znovu zadání reakce
    for pole in [leva_strana, prava_strana]:
        for i in range(len(pole)):
            # Nahrazení stringů objekty třídy Molekula
            pole[i] = Molekula(pole[i])
    return leva_strana, prava_strana


def souhrn_prvku(leva_strana, prava_strana):
    # Funkce, která vytvoří pole sestavené z pole jednotlivých chemických prvků vyskytujících se v reakci.
    prvky_vlevo = []
    prvky_vpravo = []
    for molekula in leva_strana:
        for prvek in molekula.prvky_molekuly:
            if prvek.PSP_prvek not in prvky_vlevo:
                # Pokud se na jedné straně reakce vyskytuje stejný prvek vícekrát, bude do pole přidán jen jednou.
                prvky_vlevo.append(prvek.PSP_prvek)
    for molekula in prava_strana:
        for prvek in molekula.prvky_molekuly:
            if prvek.PSP_prvek not in prvky_vlevo:
                # Všechny prvky se musí nacházet na obou stranách rovnice, jinak je reakce neplatná.
                print(f"Reakce je neplatná. Prvek {prvek.znacka_prvku} je pouze mezi produkty! Zadejte rovnici znovu: ")
                vycisleni_reakce()  # Znovu zadání reakce
                return None
            elif prvek.PSP_prvek not in prvky_vpravo:
                # Pokud se na jedné straně reakce vyskytuje stejný prvek vícekrát, bude do pole přidán jen jednou.
                prvky_vpravo.append(prvek.PSP_prvek)
    for prvek in prvky_vlevo:
        if prvek not in prvky_vpravo:
            # Všechny prvky se musí nacházet na obou stranách rovnice, jinak je reakce neplatná.
            print(f"Reakce je neplatná. Prvek {prvek.znacka_prvku} je pouze mezi výchozími látkami! Zadejte rovnici "
                  f"znovu: ")
            vycisleni_reakce()  # Znovu zadání reakce
            return None
    return prvky_vlevo  # Obě pole obsahují všechny prvky reakce, stačí vrátit jen jedno pole.


def matice_reakce(sloupce, radky, prechod):
    # Vytvoření matice reprezentující chemickou reakci
    # Sloupce představují molekuly reakce, řádky představují prvky reakce.
    # Prvkem matice je pak počet atomů daného chemického prvku v odpovídající molekule.
    matice = [[0]*len(sloupce) for _ in range(len(radky))]
    for j in range(len(sloupce)):
        molekula = sloupce[j]
        for prvek in molekula.prvky_molekuly:
            for i in range(len(radky)):
                if prvek.znacka_prvku == radky[i].znacka_prvku:
                    prvek_matice = prvek.pocet_atomu
                    if j >= prechod:
                        # Počet atomů jednotlivých chemických prvků musí být na obou stranách stejný (jejich celkový
                        # součet je nulový), proto prvky matice na pozicích produktů musí mít zápornou hodnotu.
                        prvek_matice *= (-1)
                    matice[i][j] = prvek_matice
    return matice


def gaussova_eliminace(matice, i, j):
    # Převedení matice reakce do odstupňovaného tvaru.
    radky = len(matice)
    sloupce = len(matice[0])
    min_l = sloupce - 1
    min_k = i
    nulova_matice = True  # Je-li procházená část matice nulová, je již v odstupňovaném tvaru.
    for k in range(i, radky):
        for l in range(j, sloupce):
            if matice[k][l] != 0:
                nulova_matice = False
                if l < min_l:
                    # Hledání nenulového prvku matice nejvíce vlevo
                    min_l = l
                    min_k = k
                break
    if nulova_matice is True:
        matice = matice[:i]  # Nulová část matice není pro další další výpočty potřebná, naopak by výpočet komplikovala.
        return matice
    j = min_l  # Nastavení indexu sloupce na nenulový prvek nejvíce vlevo.
    for k in range(i, radky):
        if matice[k][j] != 0 and abs(matice[k][j]) < abs(matice[min_k][j]):
            # Hledání prvku s největší absolutní hodnotou v bázickém sloupci.
            min_k = k
    matice[i], matice[min_k] = matice[min_k], matice[i]  # Prohození řádků matice, tak aby na pozici ij byl pivot
    # s největší absolutní hodnotou.
    pivot = matice[i][j]
    for k in range(i + 1, radky):
        # Vynulování daného sloupce a příslušné odečítání řádků.
        if matice[k][j] != 0:
            # Řádky s nulovým prvkem v bázickém sloupci je potřeba přeskočit.
            # Pro zachování celočíselnosti jsou jednotlivé řádky při odečítání pronásobeny příslušnými koeficienty.
            koeficient_i = matice[k][j]
            koeficient_k = pivot
            if matice[k][j] % pivot == 0:
                koeficient_i = matice[k][j] // pivot
                koeficient_k = 1
            for l in range(j, sloupce):
                matice[k][l] = matice[k][l] * koeficient_k - (matice[i][l] * koeficient_i)
    matice = gaussova_eliminace(matice, i + 1, j + 1)  # Odstupňování další části matice
    return matice


def dosazeni(matice):
    # Vypočet stechiometrických koeficientů z odstupňované matice reakce
    reseni_pole = [0]*len(matice[0])
    pocet_koef = len(reseni_pole) - 1  # Počet koeficientů, které je třeba dopočítat.
    if len(matice) <= len(reseni_pole):
        pocet_koef = len(matice) - 1
        for i in range(len(reseni_pole)-1, pocet_koef, -1):
            # U reakcí bude vždy alespoň jeden koeficient jako volná proměnná, pro kterou je třeba zvolit výchozí
            # hodnotu.
            reseni_pole[i] = 1
    for index in range(pocet_koef, -1, -1):
        suma = 0
        for j in range(len(reseni_pole)-1, index, -1):
            suma += matice[index][j]*reseni_pole[j]
        if suma % matice[index][index] != 0:
            # Stechiometrické koeficienty musí být celočíselné.
            posun = abs(matice[index][index]) // nsd(abs(suma), abs(matice[index][index]))
            # Pronásobením výchozích hodnot celočíselným podílem pivotu (matice[index][index]) a největšího společného
            # dělite pivotu a sumy zůstane řešení celočíselné.
            for i in range(len(reseni_pole)):
                # Posun výchozích hodnot, tak aby řešení zůstalo celočíselné
                reseni_pole[i] *= posun
            for j in range(len(reseni_pole) - 1, index, -1):
                # Vypočítání jednotlivých stechiometrických koeficientů
                reseni_pole[index] -= matice[index][j]*reseni_pole[j]//matice[index][index]
        else:
            # Vypočítání jednotlivých stechiometrických koeficientů
            reseni_pole[index] -= suma//matice[index][index]
    return reseni_pole


def nsd(x, y):
    # Hledání nejvetšího společného dělitele.
    if x > y:
        return nsd(x-y, y)
    elif x < y:
        return nsd(x, y-x)
    else:
        return x


def print_reakce(leva_strana, prava_strana, soubor):
    # Vypíše chemickou reakce včetně stechiometrických koeficientů na konzoli a do textového souboru.
    reakce = " + ".join([str(x.stech_koef) + "x " + x.vzorec_molekuly for x in leva_strana]) + \
             " --> " + " + ".join([str(y.stech_koef) + "x " + y.vzorec_molekuly for y in prava_strana])
    soubor.write(reakce + "\n\n")
    print(reakce + "\n")


def hmot_soustavy(pole):
    # Výpočet celkové hmnotnosti soustavy (odpovídá hmotnosti látek na jedné straně reakce)
    suma = 0
    for molekula in pole:
        suma += molekula.molarni_hmot * molekula.stech_koef
    return suma


def vypocet_zlomek(citatel, jmenovatel):
    # Vypočet molárního či hmotnostního zlomku
    zlomek = round(((citatel / jmenovatel) * 100), 2)  # Zaokrouhlení na dvě desetinná čísla
    return zlomek


vycisleni_reakce()
