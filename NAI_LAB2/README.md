# NAI | GIn I.7 - 75c | s27118, s27084

---

# Inteligentny System Sterowania Nawadnianiem — Logika Rozmyta (Python)

Projekt demonstracyjny systemu podejmowania decyzji o podlewaniu roślin z użyciem logiki rozmytej.
Na podstawie bieżących warunków środowiskowych system oblicza zalecany **czas podlewania (w minutach)**.

System analizuje 3 wejścia:
1) Wilgotność gleby (%)
2) Temperatura otoczenia (°C)
3) Wilgotność powietrza (%)

Wyjście: **czas podlewania** (0–60 min).

---

## Dlaczego logika rozmyta?

Warunki środowiskowe są nieprecyzyjne i zmienne — logika rozmyta pozwala na płynne, miękkie wnioskowanie,
zamiast sztywnych progów. Dzięki temu system skuteczniej odwzorowuje realne zależności w naturze.

---

## Wymagania środowiskowe

- Python **3.8+**
- Biblioteki: `numpy`, `scikit-fuzzy`, `matplotlib`

---

## Instalacja i uruchomienie

```bash
pip install numpy scikit-fuzzy matplotlib
python fuzzy_watering_system.py
```

---

## Co robi program?

- Inicjalizuje system wnioskowania rozmytego (Fuzzy Control System)
- Definiuje funkcje przynależności i reguły sterowania
- Wykonuje defuzyfikację do konkretnego czasu
- Udostępnia test jednostkowy i symulację zmian w czasie (24 kroki)
- Opcjonalnie rysuje wykresy funkcji przynależności

---

## Przykładowy test
Dla danych:
```
gleba = 25%   (sucho)
temp  = 35°C  (gorąco)
powietrze = 30% (niska wilg.)
```
System zwraca długi czas podlewania (np. ~45–60 min)

---
# Podsumowanie

Zadanie przygotowane w ramach zajęć:  
NAI GIn I.7 - 75c, LAB2

Twórcy:
- s27084  
- s27118
