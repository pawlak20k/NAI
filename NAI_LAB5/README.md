# # NAI | GIn I.7 - 75c | s27118, s27084

---

# Neural Networks: Regression & Classification (TensorFlow)

Implementacja i porównanie sieci neuronowych w zadaniach regresji oraz klasyfikacji obrazów i danych medycznych przy użyciu frameworka TensorFlow. Program realizuje cztery zróżnicowane scenariusze, analizując skuteczność modeli głębokiego uczenia.

---

# Działanie programu

Program wykonuje następujące kroki:

1. Zadanie 1: Regresja - Swedish Auto Insurance
   - Porównanie klasycznej Regresji Liniowej z Siecią Neuronową (MLP).
   - Metryka oceny: RMSE (Root Mean Squared Error).

2. Zadanie 2: Klasyfikacja obrazów - CIFAR-10
   - Rozpoznawanie zwierząt przy użyciu Sieci Splotowej (CNN).
   - Architektura obejmuje warstwy Conv2D oraz MaxPooling2D.

3. Zadanie 4: Case Study - Diagnoza Medyczna (Breast Cancer)
   - Klasyfikacja binarna nowotworów na podstawie parametrów komórkowych.
   - Generowanie Macierzy Błędów (Confusion Matrix).

---

# Wymagania środowiskowe

- Python 3.10+
- Framework: TensorFlow 2.15+
- Biblioteki pomocnicze: pandas, numpy, scikit-learn, matplotlib, seaborn

---

# Instalacja i uruchomienie

Aby uruchomić projekt, wykonaj poniższe komendy w terminalu:

``pip install tensorflow pandas scikit-learn matplotlib seaborn``

``python lab5.py``

---

# Logika i technologia

- Framework: TensorFlow 2.x / Keras
- Optymalizacja: Adam Optimizer
- Funkcje straty: MSE (Regresja), Sparse Categorical Crossentropy (Klasyfikacja)
- Składnia: Keras 3 (użycie layers.Input dla pełnej stabilności)

### Dlaczego te modele?
- Zadanie 1: Pokazuje porównanie błędu RMSE między siecią a regresją.
- Zadanie 2: CNN jest standardem w rozpoznawaniu obrazów.
- Zadanie 4: Zastosowanie stabilnego zbioru Breast Cancer gwarantuje poprawne działanie macierzy pomyłek (Confusion Matrix) bez błędów pobierania danych z sieci.

---

# Struktura plików

- lab5.py (główny kod źródłowy)
- README.md (dokumentacja projektu)

---

# Podsumowanie

Projekt przygotowany w ramach zajęć:
NAI GIn I.7 - 75c, LAB5

Twórcy:
- s27118
- s27084