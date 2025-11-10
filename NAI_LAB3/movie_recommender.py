"""
Problem: Silnik rekomendacji filmów i antyrekomendacji dla kursu z użyciem Pythona.
Autor: s27118, s27084

Opis:
Skrypt buduje prosty silnik rekomendacji oparty na filtracji współużytkowników.
Dla wybranego użytkownika wypisuje:
 - 5 rekomendowanych filmów, których użytkownik jeszcze nie oglądał,
 - 5 "antyrekomendacji" (filmy, których użytkownik nie powinien oglądać) — najniżej prognozowane oceny,
Dla każdej rekomendacji pobiera dodatkowe informacje z OMDb (klucz API: 980e199).

Pliki danych:
 - movies.csv i ratings.csv są osadzone w skrypcie (przykładowe, małe zestawy danych). Skrypt zapisze je lokalnie przy pierwszym uruchomieniu.

Instrukcja użycia:
1) Zainstaluj wymagane biblioteki:
   pip install pandas numpy scikit-learn requests

2) Uruchom skrypt (przykład):
   python movie_recommender.py --user 1

   Opcje:
   --user USER_ID     : id użytkownika, dla którego generujemy rekomendacje (domyślnie 1)
   --n N              : ile rekomendacji / antyrekomendacji (domyślnie 5)
   --apikey KEY       : (opcjonalne) nadpisuje domyślny klucz OMDb (domyślnie 980e199)
"""

from __future__ import annotations
import os
import argparse
import json
from typing import List, Dict, Any

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import requests

# Klucz API OMDb
OMDB_API_KEY = os.environ.get('OMDB_API_KEY', '980e199')

# --- Dane przykładowe osadzone w skrypcie ---
_movies_csv = """
movieId,title,genres
1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy
2,Jumanji (1995),Adventure|Children|Fantasy
3,Grumpier Old Men (1995),Comedy|Romance
4,Waiting to Exhale (1995),Comedy|Drama
5,Father of the Bride Part II (1995),Comedy
6,Heat (1995),Action|Crime|Thriller
7,Sabrina (1995),Comedy|Romance
8,Tom and Huck (1995),Adventure|Children
9,Sudden Death (1995),Action
10,GoldenEye (1995),Action|Adventure|Thriller
"""

_ratings_csv = """
userId,movieId,rating,timestamp
1,1,4.0,964982703
1,3,4.0,964981247
1,6,4.0,964982224
1,47,5.0,964983815
1,50,5.0,964982931
2,1,5.0,964982931
2,2,3.0,964982400
2,3,2.0,964982224
2,10,4.0,964982931
3,1,2.0,964982224
3,4,3.0,964982931
3,6,3.0,964982931
3,7,4.0,964982931
4,2,4.0,964982931
4,3,4.0,964982931
4,5,2.0,964982931
5,6,5.0,964982931
5,8,3.0,964982931
5,9,2.0,964982931
"""

DATA_DIR = '.'
MOVIES_CSV_PATH = os.path.join(DATA_DIR, 'movies.csv')
RATINGS_CSV_PATH = os.path.join(DATA_DIR, 'ratings.csv')


def ensure_data_files():
    """Zapisuje przykładowe pliki CSV jeśli nie istnieją lokalnie."""
    if not os.path.exists(MOVIES_CSV_PATH):
        with open(MOVIES_CSV_PATH, 'w', encoding='utf-8') as f:
            f.write(_movies_csv.strip())
    if not os.path.exists(RATINGS_CSV_PATH):
        with open(RATINGS_CSV_PATH, 'w', encoding='utf-8') as f:
            f.write(_ratings_csv.strip())


def load_data() -> (pd.DataFrame, pd.DataFrame):
    """Wczytuje pliki movies.csv i ratings.csv do DataFrame'ów.

    Zwraca: (movies_df, ratings_df)
    """
    ensure_data_files()
    movies = pd.read_csv(MOVIES_CSV_PATH)
    ratings = pd.read_csv(RATINGS_CSV_PATH)
    return movies, ratings


def build_user_item_matrix(ratings: pd.DataFrame) -> pd.DataFrame:
    """Buduje macierz użytkownik x film (wartości: oceny). Nieznane wartości -> NaN.

    Args:
        ratings: DataFrame z kolumnami ['userId','movieId','rating']
    Returns:
        pivot DataFrame z indeksami userId i kolumnami movieId
    """
    pivot = ratings.pivot_table(index='userId', columns='movieId', values='rating')
    return pivot


def compute_user_similarity(user_item: pd.DataFrame) -> pd.DataFrame:
    """Oblicza macierz podobieństwa między użytkownikami.

    Brakujące oceny traktujemy jako 0 w obliczeniach podobieństwa — proste przybliżenie.
    """
    mat = user_item.fillna(0).values
    sim = cosine_similarity(mat)
    sim_df = pd.DataFrame(sim, index=user_item.index, columns=user_item.index)
    return sim_df


def predict_ratings_for_user(user_id: int, user_item: pd.DataFrame, user_sim: pd.DataFrame) -> pd.Series:
    """Prognozuje oceny dla wszystkich filmów dla danego użytkownika używając ważonej średniej ocen innych użytkowników.

    Args:
        user_id: id użytkownika
        user_item: macierz user-item
        user_sim: macierz podobieństw między użytkownikami (indeksy muszą pasować)
    Returns:
        pandas Series indexed by movieId z prognozowaną oceną
    """
    if user_id not in user_item.index:
        # jeśli nie ma użytkownika w macierzy (nigdy nie ocenił), zwróć średnie oceny filmów jako prognozy
        global_mean = user_item.stack().mean()
        return pd.Series({mid: global_mean for mid in user_item.columns})

    sims = user_sim.loc[user_id]
    # Pobierz oceny wszystkich innych użytkowników
    ratings = user_item

    # dla każdego filmu: prognoza = suma(similarity * rating) / suma(|similarity|)
    numer = (ratings.T * sims).T.sum(axis=0)
    denom = sims.abs().sum()
    # Jeżeli denom == 0 -> fallback na średnią oceny filmu
    movie_means = ratings.mean(axis=0)
    with np.errstate(divide='ignore', invalid='ignore'):
        preds = numer / denom
    preds = preds.fillna(movie_means)
    return preds


def recommend_top_n(user_id: int, movies: pd.DataFrame, ratings: pd.DataFrame, n: int, user_item: pd.DataFrame=None, user_sim: pd.DataFrame=None) -> List[int]:
    """Zwraca listę movieId z top-n rekomendacji dla użytkownika.

    - Pomija filmy, które użytkownik już ocenił.
    """
    if user_item is None or user_sim is None:
        user_item = build_user_item_matrix(ratings)
        user_sim = compute_user_similarity(user_item)

    preds = predict_ratings_for_user(user_id, user_item, user_sim)
    seen = set(ratings[ratings['userId'] == user_id]['movieId'].tolist())
    unseen_preds = preds[~preds.index.isin(seen)]
    top_n = unseen_preds.sort_values(ascending=False).head(n).index.tolist()
    # zwracamy istniejące movieId z pliku movies
    available = set(movies['movieId'].unique())
    top_n_filtered = [mid for mid in top_n if mid in available]
    return top_n_filtered


def anti_recommendations(user_id: int, movies: pd.DataFrame, ratings: pd.DataFrame, n: int, user_item: pd.DataFrame=None, user_sim: pd.DataFrame=None) -> List[int]:
    """Zwraca listę movieId z antyrekomendacji (niskie prognozowane oceny).

    Kryterium: niskie prognozowane oceny wśród nieoglądanych filmów.
    """
    if user_item is None or user_sim is None:
        user_item = build_user_item_matrix(ratings)
        user_sim = compute_user_similarity(user_item)

    preds = predict_ratings_for_user(user_id, user_item, user_sim)
    seen = set(ratings[ratings['userId'] == user_id]['movieId'].tolist())
    unseen_preds = preds[~preds.index.isin(seen)]
    worst_n = unseen_preds.sort_values(ascending=True).head(n).index.tolist()
    available = set(movies['movieId'].unique())
    worst_n_filtered = [mid for mid in worst_n if mid in available]
    return worst_n_filtered


def fetch_omdb_info(title: str, api_key: str = None) -> Dict[str, Any]:
    """Pobiera informacje o filmie z OMDb na podstawie tytułu.

    Zwraca słownik z odpowiedzią JSON lub pusty słownik przy błędzie.
    """
    key = api_key or OMDB_API_KEY
    if not key:
        return {}
    params = {'t': title, 'apikey': key}
    try:
        resp = requests.get('http://www.omdbapi.com/', params=params, timeout=5)
        data = resp.json()
        if data.get('Response', 'False') == 'True':
            return data
        else:
            # np. Movie not found!
            return {'Error': data.get('Error', 'Not found')}
    except Exception as e:
        return {'Error': str(e)}


def movie_summary(movie_id: int, movies: pd.DataFrame) -> str:
    """Zwraca tytuł filmu na podstawie movieId (lub sam id jeśli brak).
    """
    row = movies[movies['movieId'] == movie_id]
    if not row.empty:
        return row.iloc[0]['title']
    return str(movie_id)


def main(args=None):
    parser = argparse.ArgumentParser(description='Prosty silnik rekomendacji filmów')
    parser.add_argument('--user', type=int, default=1, help='userId, dla którego generujemy rekomendacje')
    parser.add_argument('--n', type=int, default=5, help='ile rekomendacji / antyrekomendacji')
    parser.add_argument('--apikey', type=str, default=None, help='(opcjonalnie) klucz OMDb')
    parsed = parser.parse_args(args=args)

    if parsed.apikey:
        api_key = parsed.apikey
    else:
        api_key = OMDB_API_KEY

    movies, ratings = load_data()

    # movieId kolumny mają typ int
    movies['movieId'] = movies['movieId'].astype(int)
    ratings['movieId'] = ratings['movieId'].astype(int)

    user_item = build_user_item_matrix(ratings)
    user_sim = compute_user_similarity(user_item)

    uid = parsed.user
    n = parsed.n

    print(f"Rekomendacje dla userId={uid} (top {n}):")
    recs = recommend_top_n(uid, movies, ratings, n, user_item=user_item, user_sim=user_sim)
    for mid in recs:
        title = movie_summary(mid, movies)
        info = fetch_omdb_info(title, api_key)
        print('-' * 40)
        print(f"movieId: {mid}\nTytuł: {title}\nOMDb: {json.dumps(info, ensure_ascii=False)[:400]}")

    print('\n' + '=' * 60 + '\n')
    print(f"Antyrekomendacje dla userId={uid} (najniższe prognozy, {n}):")
    worst = anti_recommendations(uid, movies, ratings, n, user_item=user_item, user_sim=user_sim)
    for mid in worst:
        title = movie_summary(mid, movies)
        info = fetch_omdb_info(title, api_key)
        print('-' * 40)
        print(f"movieId: {mid}\nTytuł: {title}\nOMDb: {json.dumps(info, ensure_ascii=False)[:400]}")


if __name__ == '__main__':
    main()
