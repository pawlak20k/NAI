#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
================================================================================
OPIS PROBLEMU
================================================================================
Celem projektu jest stworzenie inteligentnego systemu sterowania nawadnianiem
roślin. System wykorzystuje logikę rozmytą do podejmowania decyzji o czasie
podlewania. Decyzja ta jest wypadkową trzech czynników wejściowych:
1. Wilgotności gleby (%)
2. Temperatury otoczenia (°C)
3. Wilgotności powietrza (%)

System generuje jedno wyjście:
1. Czas podlewania (w minutach)

Logika rozmyta pozwala na płynne podejmowanie decyzji w warunkach
niepewności i nieprecyzyjnych danych wejściowych, co jest idealne do
modelowania systemów biologicznych i środowiskowych.

================================================================================
AUTORZY ROZWIĄZANIA
================================================================================
- s27084, s27118

================================================================================
INSTRUKCJA PRZYGOTOWANIA ŚRODOWISKA
================================================================================
Do uruchomienia skryptu wymagany jest język Python (wersja 3.8+) oraz
kilka bibliotek.

1.  Upewnij się, że masz zainstalowanego Pythona i menedżer pakietów 'pip'.
2.  Zainstaluj wymagane biblioteki za pomocą poniższego polecenia:

    pip install numpy scikit-fuzzy matplotlib

3.  Uruchom skrypt bezpośrednio z terminala:

    python fuzzy_watering_system.py

================================================================================
KOD ŹRÓDŁOWY
================================================================================
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import time
import random


class InteligentnySystemPodlewania:
    """
    Klasa enkapsulująca logikę rozmytą dla systemu nawadniania.

    Definiuje zmienne lingwistyczne (wejścia/wyjścia), ich funkcje
    przynależności oraz zbiór reguł sterujących. Udostępnia metodę
    do obliczania konkretnego czasu podlewania na podstawie
    danych wejściowych (tzw. "crisp values").
    """

    def __init__(self):
        """
        Inicjalizuje system sterowania rozmytego.
        Definiuje wejścia, wyjścia, funkcje przynależności i reguły.
        """
        # Definicja uniwersum (zakresów wartości)
        # Wejście 1: Wilgotność gleby (0-100%)
        zakres_gleba = np.arange(0, 101, 1)
        # Wejście 2: Temperatura (0-45°C)
        zakres_temp = np.arange(0, 46, 1)
        # Wejście 3: Wilgotność powietrza (0-100%)
        zakres_powietrze = np.arange(0, 101, 1)
        # Wyjście: Czas podlewania (0-60 minut)
        zakres_podlewanie = np.arange(0, 61, 1)

        # Definicja Antecendentów (Wejść)
        self.wilgotnosc_gleby = ctrl.Antecedent(zakres_gleba, 'wilgotnosc_gleby')
        self.temperatura = ctrl.Antecedent(zakres_temp, 'temperatura')
        self.wilgotnosc_powietrza = ctrl.Antecedent(zakres_powietrze, 'wilgotnosc_powietrza')

        # Definicja Konsekwentu (Wyjścia)
        self.czas_podlewania = ctrl.Consequent(zakres_podlewanie, 'czas_podlewania')

        # Definicja funkcji przynależności (Membership Functions)
        self._definicja_funkcji_przynaleznosci()

        # Definicja reguł
        reguly = self._stworz_reguly()

        # Stworzenie systemu sterowania
        self.system_sterowania = ctrl.ControlSystem(reguly)

        # Stworzenie symulatora
        self.symulator = ctrl.ControlSystemSimulation(self.system_sterowania)

    def _definicja_funkcji_przynaleznosci(self):
        """
        Prywatna metoda definiująca funkcje przynależności dla
        wszystkich zmiennych lingwistycznych.
        Używamy głównie funkcji trójkątnych (trimf) i trapezowych (trapmf).
        """
        # Wilgotność gleby
        self.wilgotnosc_gleby['sucha'] = fuzz.trapmf(self.wilgotnosc_gleby.universe, [0, 0, 20, 40])
        self.wilgotnosc_gleby['wilgotna'] = fuzz.trimf(self.wilgotnosc_gleby.universe, [30, 50, 70])
        self.wilgotnosc_gleby['mokra'] = fuzz.trapmf(self.wilgotnosc_gleby.universe, [60, 80, 100, 100])

        # Temperatura
        self.temperatura['zimno'] = fuzz.trapmf(self.temperatura.universe, [0, 0, 10, 18])
        self.temperatura['cieplo'] = fuzz.trimf(self.temperatura.universe, [15, 23, 30])
        self.temperatura['goraco'] = fuzz.trapmf(self.temperatura.universe, [27, 35, 45, 45])

        # Wilgotność powietrza
        self.wilgotnosc_powietrza['niska'] = fuzz.trapmf(self.wilgotnosc_powietrza.universe, [0, 0, 25, 45])
        self.wilgotnosc_powietrza['srednia'] = fuzz.trimf(self.wilgotnosc_powietrza.universe, [35, 50, 65])
        self.wilgotnosc_powietrza['wysoka'] = fuzz.trapmf(self.wilgotnosc_powietrza.universe, [55, 75, 100, 100])

        # Czas podlewania (Defuzzylikacja metodą "centroid")
        self.czas_podlewania.defuzzify_method = 'centroid'
        self.czas_podlewania['brak'] = fuzz.trimf(self.czas_podlewania.universe, [0, 0, 10])
        self.czas_podlewania['krotki'] = fuzz.trimf(self.czas_podlewania.universe, [5, 15, 25])
        self.czas_podlewania['sredni'] = fuzz.trimf(self.czas_podlewania.universe, [20, 30, 40])
        self.czas_podlewania['dlugi'] = fuzz.trapmf(self.czas_podlewania.universe, [35, 45, 60, 60])

    def _stworz_reguly(self):
        """
        Prywatna metoda definiująca bazę reguł rozmytych.
        """
        # REGULY:
        # R1: Jeśli gleba jest mokra -> nie podlewaj
        r1 = ctrl.Rule(self.wilgotnosc_gleby['mokra'], self.czas_podlewania['brak'])

        # R2: Jeśli gleba jest sucha ORAZ jest gorąco -> podlewaj długo
        r2 = ctrl.Rule(self.wilgotnosc_gleby['sucha'] & self.temperatura['goraco'],
                       self.czas_podlewania['dlugi'])

        # R3: Jeśli gleba jest sucha ORAZ jest ciepło -> podlewaj średnio
        r3 = ctrl.Rule(self.wilgotnosc_gleby['sucha'] & self.temperatura['cieplo'],
                       self.czas_podlewania['sredni'])

        # R4: Jeśli gleba jest sucha ORAZ jest zimno -> podlewaj krótko
        r4 = ctrl.Rule(self.wilgotnosc_gleby['sucha'] & self.temperatura['zimno'],
                       self.czas_podlewania['krotki'])

        # R5: Jeśli gleba jest wilgotna ORAZ jest gorąco -> podlewaj średnio (szybko paruje)
        r5 = ctrl.Rule(self.wilgotnosc_gleby['wilgotna'] & self.temperatura['goraco'],
                       self.czas_podlewania['sredni'])

        # R6: Jeśli gleba jest wilgotna ORAZ jest ciepło -> podlewaj krótko
        r6 = ctrl.Rule(self.wilgotnosc_gleby['wilgotna'] & self.temperatura['cieplo'],
                       self.czas_podlewania['krotki'])

        # R7: Jeśli gleba jest wilgotna ORAZ jest zimno -> nie podlewaj
        r7 = ctrl.Rule(self.wilgotnosc_gleby['wilgotna'] & self.temperatura['zimno'],
                       self.czas_podlewania['brak'])

        # R8: Jeśli wilgotność powietrza jest niska ORAZ gleba jest sucha -> podlewaj długo
        # (reguła wzmacniająca R2)
        r8 = ctrl.Rule(self.wilgotnosc_powietrza['niska'] & self.wilgotnosc_gleby['sucha'],
                       self.czas_podlewania['dlugi'])

        # R9: Jeśli wilgotność powietrza jest wysoka ORAZ gleba NIE jest sucha -> nie podlewaj
        r9 = ctrl.Rule(self.wilgotnosc_powietrza['wysoka'] & ~self.wilgotnosc_gleby['sucha'],
                       self.czas_podlewania['brak'])

        return [r1, r2, r3, r4, r5, r6, r7, r8, r9]

    def oblicz_czas_podlewania(self, wilg_gleby, temp, wilg_powietrza):
        """
        Oblicza konkretny (crisp) czas podlewania na podstawie
        konkretnych wartości wejściowych.

        Args:
            wilg_gleby (float): Aktualna wilgotność gleby [0-100].
            temp (float): Aktualna temperatura [0-45].
            wilg_powietrza (float): Aktualna wilgotność powietrza [0-100].

        Returns:
            float: Obliczony czas podlewania w minutach.
        """
        # Przekazanie wartości wejściowych do symulatora
        self.symulator.input['wilgotnosc_gleby'] = wilg_gleby
        self.symulator.input['temperatura'] = temp
        self.symulator.input['wilgotnosc_powietrza'] = wilg_powietrza

        # Uruchomienie obliczeń (fazyfikacja, inferencja, defazyfikacja)
        self.symulator.compute()

        # Zwrócenie wyniku (crisp value)
        return self.symulator.output['czas_podlewania']

    def wizualizuj_funkcje(self):
        """
        Generuje i wyświetla wykresy funkcji przynależności
        dla wszystkich zmiennych lingwistycznych.
        Przydatne do demonstracji i debugowania.
        """
        print("Generowanie wykresów funkcji przynależności...")
        self.wilgotnosc_gleby.view()
        self.temperatura.view()
        self.wilgotnosc_powietrza.view()
        self.czas_podlewania.view()
        plt.show()


def symulacja_w_czasie_rzeczywistym(system, ilosc_krokow=24):
    """
    Funkcja demonstrująca działanie systemu w pętli symulacyjnej.
    Symuluje upływ 24 "godzin", gdzie co godzinę zmieniają się
    warunki środowiskowe, a system podejmuje decyzję.
    """
    print("\n" + "=" * 60)
    print("ROZPOCZYNAM DEMONSTRACJĘ W CZASIE RZECZYWISTYM")
    print(f"Symulacja {ilosc_krokow} kroków (np. 'godzin')")
    print("=" * 60 + "\n")

    # Początkowe warunki
    aktualna_wilg_gleby = 60.0
    aktualna_temp = 18.0
    aktualna_wilg_powietrza = 50.0

    for godzina in range(1, ilosc_krokow + 1):
        # Symulacja zmian środowiskowych
        # Temperatura rośnie w "dzień" i spada w "nocy"
        aktualna_temp += (10 - godzina % 24) * 0.5 + random.uniform(-1, 1)
        aktualna_temp = np.clip(aktualna_temp, 5, 40)  # Ograniczenie wartości

        # Wilgotność powietrza zmienia się odwrotnie do temperatury
        aktualna_wilg_powietrza -= (10 - godzina % 24) * 0.3 + random.uniform(-2, 2)
        aktualna_wilg_powietrza = np.clip(aktualna_wilg_powietrza, 20, 95)

        # Wilgotność gleby spada (wysycha)
        wysychanie = (aktualna_temp / 10) + (1 - aktualna_wilg_powietrza / 100)
        aktualna_wilg_gleby -= wysychanie + random.uniform(0, 1)
        aktualna_wilg_gleby = np.clip(aktualna_wilg_gleby, 10, 90)

        # Pobranie decyzji z systemu rozmytego
        zalecany_czas = system.oblicz_czas_podlewania(
            aktualna_wilg_gleby,
            aktualna_temp,
            aktualna_wilg_powietrza
        )

        print(f"--- KROK {godzina:02d} ---")
        print(f"  WARUNKI WEJŚCIOWE:")
        print(f"  > Wilg. Gleby:    {aktualna_wilg_gleby:4.1f}%")
        print(f"  > Temperatura:    {aktualna_temp:4.1f}°C")
        print(f"  > Wilg. Powietrza: {aktualna_wilg_powietrza:4.1f}%")
        print(f"  DECYZJA SYSTEMU (WYJŚCIE):")
        print(f"  > Czas podlewania: {zalecany_czas:4.1f} minut")

        # Symulacja efektu podlewania
        if zalecany_czas > 1:
            # Zakładamy, że podlewanie natychmiast zwiększa wilgotność gleby
            # (współczynnik 1.5 jest arbitralny dla celów symulacji)
            przyrost_wilg = zalecany_czas * 1.5
            print(f"  > AKCJA: Podlewanie! Wilgotność gleby +{przyrost_wilg:.1f}%")
            aktualna_wilg_gleby += przyrost_wilg
            aktualna_wilg_gleby = np.clip(aktualna_wilg_gleby, 10, 90)
        else:
            print(f"  > AKCJA: Brak podlewania.")

        print("-" * 20)
        time.sleep(0.5)  # Pauza dla efektu "czasu rzeczywistego"

    print("\n" + "=" * 60)
    print("ZAKOŃCZONO SYMULACJĘ")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    # 1. Inicjalizacja systemu
    system_nawadniania = InteligentnySystemPodlewania()
    print("Inicjalizacja systemu logiki rozmytej zakończona.")

    # 2. (Opcjonalnie) Wizualizacja funkcji przynależności
    # Odkomentuj poniższą linię, aby zobaczyć wykresy przed symulacją
    # system_nawadniania.wizualizuj_funkcje()

    # 3. Test jednostkowy - sprawdzenie pojedynczego przypadku
    print("\n--- TEST JEDNOSTKOWY ---")
    gleba = 25  # sucho
    temp = 35  # gorąco
    powietrze = 30  # nisko
    czas = system_nawadniania.oblicz_czas_podlewania(gleba, temp, powietrze)
    print(f"Test: Gleba={gleba}%, Temp={temp}°C, Powietrze={powietrze}% -> Czas={czas:.2f} min")
    # Oczekiwany wynik: "długi" czas (np. > 40 min)

    # 4. Uruchomienie demonstracji "w czasie rzeczywistym"
    symulacja_w_czasie_rzeczywistym(system_nawadniania, ilosc_krokow=24)