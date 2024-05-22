from abc import ABC
from datetime import datetime

# Hozz létre egy Szoba absztrakt osztályt, amely alapvető attribútumokat definiál (ár, szobaszám). (5 pont)
class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

#Hozz létre az Szoba osztályból EgyagyasSzoba és KetagyasSzoba származtatott osztályokat, amelyek különböző attributumai vannak, és az áruk is különböző.(5 pont)
class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=5000, szobaszam=szobaszam)

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=8000, szobaszam=szobaszam)

#Hozz létre egy Szalloda osztályt, ami ezekből a Szobákból áll, és van saját attributuma is (név pl.) (10 pont)
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = {}

    def szoba_hozzaadas(self, szoba):
        self.szobak[szoba.szobaszam] = szoba

#Hozz létre egy Foglalás osztályt, amelybe a Szálloda szobáinak foglalását tároljuk (elég itt, ha egy foglalás csak egy napra szól) (10 pont)
class Foglalas:
    def __init__(self):
        self.foglalasok = {}

#Implementálj egy metódust, ami lehetővé teszi szobák foglalását dátum alapján, visszaadja annak árát. (15 pont)
#A foglalás létrehozásakor ellenőrizd, hogy a dátum érvényes (jövőbeni) és a szoba elérhető-e akkor. (10 pont)
    def foglal(self, szalloda, szobaszam, datum):
        if not self.datum_valid(datum):
            print("Hiba: Érvénytelen vagy múltbeli dátum!")
            return False, 0
        if szobaszam not in szalloda.szobak:
            print("Hiba: Érvénytelen szobaszám!")
            return False, 0
        if self.szoba_foglalt(szalloda, szobaszam, datum):
            print(f"Hiba: A szoba ({szobaszam}) ezen a napon ({datum}) már foglalt!")
            return False, 0
        if szobaszam not in self.foglalasok:
            self.foglalasok[szobaszam] = {}
        self.foglalasok[szobaszam][datum] = szalloda.szobak[szobaszam]
        print(f"Szoba ({szobaszam}) sikeresen lefoglalva {datum} napra.")
        return True, szalloda.szobak[szobaszam].ar

    def szoba_foglalt(self, szalloda, szobaszam, datum):
        return szobaszam in self.foglalasok and datum in self.foglalasok[szobaszam]

    def datum_valid(self, datum):
        try:
            datum_obj = datetime.strptime(datum, "%Y-%m-%d")
            return datum_obj > datetime.now()
        except ValueError:
            return False

#Implementálj egy metódust, ami lehetővé teszi a foglalás lemondását. (5 pont)
#Biztosítsd, hogy a lemondások csak létező foglalásokra lehetségesek. (5 pont)
    def foglalas_lemondas(self, szobaszam, datum):
        if szobaszam in self.foglalasok and datum in self.foglalasok[szobaszam]:
            del self.foglalasok[szobaszam][datum]
            print(f"Foglalás ({szobaszam}) törölve {datum}-kor.")
        else:
            print("Nincs ilyen foglalás, amit lemondhatna.")

#Implementálj egy metódust, ami listázza az összes foglalást. (5 pont)
    def foglalasok_listaja(self):
        if not self.foglalasok:
            print("Nincsen foglalás.")
            return
        for szobaszam in self.foglalasok:
            for datum in self.foglalasok[szobaszam]:
                print(f"Szobaszám: {szobaszam}, Dátum: {datum}")

#Készíts egy egyszerű felhasználói interfészt, ahol a felhasználó kiválaszthatja a kívánt műveletet (pl. foglalás, lemondás, listázás). (20 pont)
def user_interface(szalloda, foglalas_kezelo):
    while True:
        print("\n1. Foglalás")
        print("2. Lemondás")
        print("3. Listázás")
        print("4. Kilépés")
        valasztas = input("Válasszon egy opciót: ")
        if valasztas == "1":
            try:
                print("Elérhető szobaszámok:")
                for szobaszam in szalloda.szobak.keys():
                    print(szobaszam)
                szobaszam = int(input("Adja meg a szobaszámot: "))
                datum = input("Adja meg a dátumot (YYYY-MM-DD formátumban): ")
                sikeres, ar = foglalas_kezelo.foglal(szalloda, szobaszam, datum)
                if sikeres:
                    print(f"A foglalás ára: {ar} Ft")
                else:
                    raise ValueError("Hibás szobaszám vagy dátum.")
            except ValueError as e:
                print(e)
        elif valasztas == "2":
            try:
                szobaszam = int(input("Adja meg a szobaszámot, amit le szeretne mondani: "))
                datum = input("Adja meg a dátumot (YYYY-MM-DD formátumban): ")
                foglalas_kezelo.foglalas_lemondas(szobaszam, datum)
            except ValueError as e:
                print(e)
        elif valasztas == "3":
            foglalas_kezelo.foglalasok_listaja()
        elif valasztas == "4":
            print("Kilépés...")
            break
        else:
            print("Érvénytelen opció.")

#Töltsd fel az futtatás után a rendszert 1 szállodával, 3 szobával és 5 foglalással, mielőtt a felhasználói adatbekérés megjelenik. (10 pont)
def init_system():
    szalloda = Szalloda("Szalloda 1")
    szalloda.szoba_hozzaadas(EgyagyasSzoba(101))
    szalloda.szoba_hozzaadas(KetagyasSzoba(102))
    szalloda.szoba_hozzaadas(EgyagyasSzoba(103))
    foglalas_kezelo = Foglalas()

    foglalas_kezelo.foglal(szalloda, 101, "2024-11-01")
    foglalas_kezelo.foglal(szalloda, 102, "2024-10-02")
    foglalas_kezelo.foglal(szalloda, 103, "2024-07-03")
    foglalas_kezelo.foglal(szalloda, 101, "2024-08-04")
    foglalas_kezelo.foglal(szalloda, 102, "2024-12-05")
    return szalloda, foglalas_kezelo

szalloda, foglalas_kezelo = init_system()

user_interface(szalloda, foglalas_kezelo)
