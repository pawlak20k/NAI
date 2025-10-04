# NAI 
GIn I.7 - 75c | s27118, s27084

---

# Don't Say 21 (Python Game)

Działanie programu:

<img width="1096" height="648" alt="Screenshot 2025-10-04 at 11 09 00" src="https://github.com/user-attachments/assets/2713f737-ad36-4664-b723-6edb5000a108" />

Interaktywna gra konsolowa **„Don't Say 21”** - klasyczna gra strategiczna człowiek vs komputer.  
Celem jest **nie powiedzieć liczby 21**!

---

# Zasady gry
- Gracze na zmianę wypowiadają **1, 2 lub 3 kolejne liczby**, zaczynając od 1.  
- Kto **musi powiedzieć „21” — przegrywa**.  
- Optymalna strategia polega na **kończeniu swojej tury na liczbach będących wielokrotnościami 4** (4, 8, 12, 16, 20).

Źródło zasad i strategii:  
https://strategygameguide.com/dont-say-21-game/  
Autor zasad: **Andy (Strategy Game Guide)**

---

# Wymagania środowiskowe

- **Python 3.8+** (testowane na Python 3.8)  
- System operacyjny: dowolny (Windows / macOS / Linux)

---

# Instalacja i uruchomienie

1. Sklonuj repozytorium lub pobierz plik `dont_say_21.py`:
   `git clone https://github.com/<twoje-repo>/dont-say-21.git`

2. Uruchom grę w konsoli:
   `python dont_say_21.py`

3. Postępuj zgodnie z instrukcjami na ekranie.

---

# Logika komputera (AI)

Komputer wykorzystuje prostą strategię:
- Jeśli może zakończyć turę na wielokrotności 4 (4, 8, 12, 16, 20) — zrobi to.
- W przeciwnym razie wybiera losowo 1–3.

Dzięki temu gra staje się ciekawa, a wygrana zależy od Twojej taktyki

---
# Podsumowanie

Projekt przygotowany w ramach zajęć:  
NAI GIn I.7 - 75c

Twórcy:
- s27084  
- s27118
