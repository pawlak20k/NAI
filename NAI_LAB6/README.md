# NAI | GIn I.7 - 75c | s27118, s27084

---

# Computer Vision - System Rozpoznawania Flag (Python)

Opis projektu:
Zbudowanie systemu rozpoznającego i lokalizującego flagę polską, rosyjską i ukraińską na strumieniu wideo. Program podaje nazwę rozpoznanej flagi oraz jej dokładną pozycję na ekranie. Projekt został zoptymalizowany pod kątem wykrywania obrazów wyświetlanych na ekranach telefonów oraz fizycznych wydruków.

---

# Działanie programu:

Kliknij w poniższy obrazek, aby obejrzeć nagranie z działania systemu (rozpoznawanie flag Polski, Rosji i Ukrainy):
[![Rozpoznawanie Flag - Scenariusz Testowy](https://img.youtube.com/vi/-ffJFoGQy1s/0.jpg)](https://www.youtube.com/watch?v=-ffJFoGQy1s)

1. Przechwytywanie wideo: Pobieranie obrazu z kamery w czasie rzeczywistym.
2. Przetwarzanie HSV: Konwersja klatek do przestrzeni barw HSV w celu eliminacji wpływu oświetlenia.
3. Segmentacja kolorów: Wyodrębnienie kluczowych barw (biały, czerwony, niebieski, żółty) przy użyciu masek binarnych.
4. Morfologia obrazu: Zastosowanie operacji otwarcia (Open) w celu usunięcia szumów z tła.
5. Detekcja konturów: Wyszukanie granic obiektów o określonym polu powierzchni.
6. Analiza układu pasów (ROI): Podział obszaru na sekcje poziome i sprawdzenie dominacji kolorów w pasach.
7. Wyświetlanie wyników: Narysowanie ramki oraz wypisanie nazwy kraju i współrzędnych.

---

# Wymagania środowiskowe:
- Python 3.8+
- Biblioteki: opencv-python, numpy
- Sprzęt: Kamera internetowa

---

# Instalacja i uruchomienie:
1. Zainstaluj wymagane paczki: `pip install opencv-python numpy`
2. Uruchom skrypt: `python flag_detector.py`
3. Obsługa: Skieruj kamerę na flagę. System oznaczy ją ramką i poda pozycję. Aby wyjść, naciśnij 'q'.

---

# Logika rozpoznawania flag:
Program stosuje hierarchiczną logikę sprawdzania warunków:
- Flaga Rosji: Sprawdzenie układu 3-pasmowego (Biały - Niebieski - Czerwony).
- Flaga Ukrainy: Sprawdzenie układu 2-pasmowego (Niebieski - Żółty).
- Flaga Polski: Sprawdzenie układu 2-pasmowego (Biały - Czerwony) z weryfikacją braku koloru niebieskiego w środku.

---

# Struktura plików:
- flag_detector.py: Skrypt z dokumentacją Docstring i komentarzami.
- README.md: Dokumentacja projektu.
- training_data/: Zbiór obrazów testowych przekazany prowadzącemu.

---

# Podsumowanie:
Projekt zrealizowany w ramach przedmiotu: NAI GIn I.7 - 75c, LAB6

Twórcy:
- s27118
- s27084

Kod źródłowy został opatrzony dokumentacją Python Docstring, a do repozytorium dołączono nagranie wideo prezentujące detekcję.
