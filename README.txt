### Spuštění programu "chemicka_rovnice.py" ###
Program lze spustit jediným příkazem z příkazové řádky (python chemicka_rovnice.py), program ale musí být ve zdrojové
složce "chemicka_rovnice", která obsahuje nezbytné soubory pro plné fungování programu.

Nezbytnými soubory jsou:
-> periodicka_tabulka_prvku.txt
--> Tento soubor obsahuje informace o chemických prvcích periodické soustavy prvků.
--> Na prvním řádku je celkový počet chemických prkvů.
--> Každý chemický prvek je pak v souboru zapsán podle následující šablony:
--------------------------------------
PRÁZDNÝ ŘÁDEK
protonové číslo prvku
značka prvku
český název prvku
latinský název prvku
relativní atomová hmotnost prvku
--------------------------------------
-> nacteni_PSP.py
--> Tento program načte informace z textového souboru "periodicka_tabulka_prvku.txt" a vytvoří periodickou tabulku
prvků, díky které je možno ověřovat existenci prvků zadaných v chemické reakci.
--> Program využívá modul os pro ověřování existence potřebného textového souboru.

Další soubory:
–> zkusebni_vstupy.txt
––> Tento soubor obsahuje příklady chemických rovnic, na kterých lze program "chemicka_rovnice.py" vyzkoušet.
-> vystup.txt
--> Do tohoto souboru se zapíše výstup programu "chemicka_rovnice.py". Každé nové spuštění programu existující obsah
přepíše! Pokud soubor ve složce chybí, program "chemicka_rovnice.py" si ho sám vytvoří.

Program "chemicka_rovnice.py" nevyužívá žádné speciální moduly, kromě modulu os v rámci dílčího programu "nacteni_PSP.py"


### Očekávaný vstup programu "chemicka_rovnice.py" ###

Očekávaným vstupem je zadání chemické reakce. Vstup je rozdělen na dva řádky, první řádek je pro reaktanty
(výchozí látky) chemické rovnice a druhý řádek je pro produkty reakce. Pro oba řádky platí, že jednotlivé látky je
potřeba oddělit pomocí mezer a plusu (" + ").
Pro všechny látky reakce platí, že musí být zadány s ohledem na velká a malá písmena a počet atomů v molekule je zapsán
číslem přímo za daným prvkem. Pokud vzorec molekuly obsahuje závorky ("()", "[]") je potřeba tyto závorky odstranit a
jednotlivé počty atomů pronásobit, stejně tak pro látky obsahující hydráty atd.
Např.:  (NH4)2Cr2O7 ==> N2H8Cr2O7, Cu(NO3)2 ==> CuN2O6
Příklad chemické rovnice: Te + HClO3 + H2O --> H6TeO6 + Cl2

Program je ošetřený kontrolami vstupu, některé chyby zápisu je možné opravit v rámci jednoho běhu programu.


### Vyčíslení chemické reakce ###

Program ze zadané reakce přečte jednotlivé reakční látky a jejich prvky, ze kterých sestaví matici, která reprezentuje
chemickou reakci. Pomocí Gaussovy eliminace následně vypočítá stechiometrické koeficienty (potřebná látková množství)
jednotlivých reakčních látek s co nejmenšími celočíselnými hodnotami.

Výstupem je vyčíslená chemická reakce a informace o jednotlivých reakčních látkách a jejich prvcích (molární zlomky,
hmotnostní zlomky, molární hmotnosti, atd.)

Příklad matice reakce:
H2 + O2 --> H2O
    H2  O2  H2O
H:  [2, 0,  -2] (V první látce dva atomy vodíku, ve druhé žádný, v prvním prodktu dva atomy vodíku)
O:  [0, 2,  -1] (V první látce žádný atom kyslíku, ve druhé dva atomy, v prvním prodktu jeden atom kyslíku)

(U produktů musí být hodnoty záporné, protože počet atomů daného prvku v reaktantech musí být stejný jako v produktech.
Čili součet atomů daného prvků v celé reakci musí být nulový.)

NaCl + H2O --> NaOH + HCl
    NaCl    H2O     NaOH    HCl
Na: [1,     0,      -1,     0]
Cl: [1,     0,      0,      -1]
H:  [0,     2,      -1,     -1]
O:  [0,     1,      -1,     0]
