# NAI | GIn I.7 - 75c | s27118, s27084

---

# Movie Recommender (Python)

Opis: **Silnik rekomendacji filmów i antyrekomendacji** wykorzystujący dane o ocenach użytkowników oraz zewnętrzne API OMDb do pobierania informacji o filmach.

---

# Działanie programu


*(Przykładowy widok konsoli po uruchomieniu programu)*

Program generuje rekomendacje filmowe w oparciu o **filtrację współużytkowników (user-based collaborative filtering)**.  
Dla wybranego użytkownika:
- proponuje **5 filmów, które mogą mu się spodobać**, a których jeszcze nie oglądał,
- oraz **5 filmów, których prawdopodobnie nie powinien oglądać** (antyrekomendacje),
- pobiera dodatkowe informacje o filmach (np. rok, reżyser, gatunek, ocena IMDb) z **OMDb API**.

---

# Wymagania środowiskowe

- **Python 3.8+** (testowane na Python 3.11)
- Biblioteki:
  - `pandas`
  - `numpy`
  - `scikit-learn`
  - `requests`
- System operacyjny: dowolny (Windows / macOS / Linux)

---

# Instalacja i uruchomienie

1. Zainstaluj wymagane biblioteki:
   ```bash
   pip install pandas numpy scikit-learn requests
   ```

2. Uruchom program w terminalu:
   ```bash
   python movie_recommender.py --user 1
   ```

   Dostępne opcje:
   ```bash
   --user USER_ID   # Identyfikator użytkownika, dla którego generujemy rekomendacje (domyślnie 1)
   --n N            # Liczba rekomendacji i antyrekomendacji (domyślnie 5)
   --apikey KEY     # (opcjonalnie) własny klucz API do OMDb
   ```

3. Program automatycznie utworzy pliki `movies.csv` i `ratings.csv` z przykładowymi danymi, jeśli nie istnieją.

4. Wyniki zostaną wyświetlone w konsoli — dla każdej rekomendacji pojawią się informacje pobrane z OMDb.

---

# Logika działania

Silnik rekomendacji oparty jest na **filtracji współużytkowników**:

1. Tworzona jest **macierz użytkownik–film** z ocenami.
2. Liczone jest **podobieństwo** między użytkownikami.
3. Dla każdego filmu nieocenionego przez danego użytkownika przewidywana jest ocena na podstawie ocen użytkowników podobnych.
4. Filmy z najwyższą prognozowaną oceną → rekomendacje.
5. Filmy z najniższą prognozowaną oceną → antyrekomendacje.

Dodatkowo, każdy film posiada rozwinięte informacje pobrane z **OMDb API** (rok, reżyser, obsada, ocena IMDb, gatunek itp.).

---

# Struktura plików

```
MovieRecommender/
├── movie_recommender.py      # Główny plik z kodem programu
├── movies.csv                # Dane przykładowych filmów
├── ratings.csv               # Dane ocen użytkowników
└── README.md                 # Dokumentacja projektu
```

---

# Klucz OMDb API

- W projekcie używany jest klucz API: **980e199** (domyślny w kodzie).
- Można go nadpisać własnym kluczem przez parametr `--apikey` lub zmienną środowiskową `OMDB_API_KEY`.

---

# Przykład użycia

```bash
python movie_recommender.py --user 2 --n 5
```

Przykładowy fragment wyniku:
```
Rekomendacje dla userId=2 (top 5):
----------------------------------------
movieId: 4
Tytuł: Waiting to Exhale (1995)
OMDb: {"Title": "Waiting to Exhale", "Year": "1995", "Genre": "Comedy, Drama", ...}

Antyrekomendacje dla userId=2 (najniższe prognozy, 5):
----------------------------------------
movieId: 9
Tytuł: Sudden Death (1995)
OMDb: {"Title": "Sudden Death", "Year": "1995", "Genre": "Action, Thriller", ...}
```

---

# Podsumowanie

Zadanie przygotowane w ramach zajęć:  
**NAI GIn I.7 - 75c, LAB3**

Twórcy:
- s27084  
- s27118
