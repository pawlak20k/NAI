# NAI | GIn I.7 - 75c | s27118, s27084

---

# Auto Insurance in Sweden & Wine Classifier (Python)

**Klasyfikacja danych Auto Insurance in Sweden oraz Wine Dataset** przy użyciu **Drzew Decyzyjnych** oraz **SVM**.  
Program umożliwia trenowanie modeli, ocenę jakości klasyfikacji oraz eksperymentowanie z różnymi kernelami SVM.

---

# Działanie programu

Program wykonuje następujące kroki:  

1. **Ładowanie danych:**
   - `Auto Insurance in Sweden` - konwersja problemu regresji na klasyfikację binarną (Low vs High Payment).  
   - `Wine Dataset` - użycie tylko pierwszych dwóch cech (Alcohol, Malic Acid) dla wizualizacji 2D.

2. **Podział danych na zestawy treningowe i testowe** (`train_test_split`).

3. **Skalowanie danych** dla modeli SVM (`StandardScaler`).

4. **Trenowanie modeli klasyfikacyjnych:**
   - Drzewo Decyzyjne (`DecisionTreeClassifier`)  
   - SVM (`SVC`) z jądrem RBF

5. **Ewaluacja modeli:**
   - Dokładność (`accuracy`)  
   - Raport klasyfikacji (`classification_report`)  
   - Macierz pomyłek (`confusion_matrix`)

6. **Eksperyment z kernelami SVM** na zbiorze Wine (linear, poly, rbf, sigmoid) oraz różnymi wartościami parametru C.

7. **Przykładowa predykcja** dla nowych danych wejściowych.

---

# Wymagania środowiskowe

- **Python 3.8+** (testowane na Python 3.11)  
- Biblioteki:
  - `pandas`
  - `numpy`
  - `scikit-learn`
  - `matplotlib`
  - `seaborn`
- System operacyjny: dowolny (Windows / macOS / Linux)

---

# Instalacja i uruchomienie

1. Zainstaluj wymagane biblioteki:
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn
   ```

2. Uruchom program w terminalu:
   ```bash
   python swedish_ai_dataset.py
   ```

Program automatycznie:
- załaduje dane,  
- podzieli je na zestawy treningowe i testowe,  
- przetrenuje modele,  
- wyświetli wyniki klasyfikacji w konsoli,  
- wykona eksperyment z różnymi kernelami SVM.

---

# Logika działania

1. **Auto Insurance in Sweden**
   - Wypłaty powyżej mediany → klasa 1, poniżej mediany → klasa 0.  
   - Model Drzewa Decyzyjnego i SVM przewidują klasę wypłaty na podstawie liczby roszczeń.

2. **Wine Dataset**
   - Wykorzystanie dwóch cech: Alcohol i Malic Acid.  
   - Modele przewidują typ wina (3 klasy).

3. **Ewaluacja modeli**
   - Dokładność klasyfikacji  
   - Raport klasyfikacji z precision, recall, f1-score  
   - Macierz pomyłek

4. **Eksperymenty SVM**
   - Testowanie różnych kernelów (`linear`, `poly`, `rbf`, `sigmoid`)  
   - Testowanie różnych wartości parametru `C` (0.1, 1.0, 10.0)  
   - Porównanie dokładności modeli

---

# Struktura plików

```
SwedishAI_Wine/
├── swedish_ai_dataset.py   # Główny plik programu
├── README.md               # Dokumentacja projektu
└── visualization.png       # Przykładowa wizualizacja
```

---

# Przykład użycia

Program uruchomiony w konsoli generuje przykładową predykcję:  
```
=== Przykładowa Predykcja ===
Wejście Insurance (Liczba roszczeń): 50
 -> Drzewo: Klasa 1, SVM: Klasa 1

Wejście Wine (Alkohol, Kwas): [13.5, 2.5]
 -> Drzewo: Klasa 0, SVM: Klasa 0
```

Eksperyment z kernelami SVM zwraca tabelę dokładności dla różnych kombinacji kernel/C dla zbioru Wine.

---

# Podsumowanie

Projekt przygotowany w ramach zajęć:  
**NAI GIn I.7 - 75c, LAB4**

Twórcy:
- s27118  
- s27084