# Autorzy: s27118, s27084
# Instrukcja przygotowania środowiska:
#   1. Zainstaluj Python 3.8+
#   2. Zainstaluj biblioteki: pip install pandas numpy scikit-learn matplotlib seaborn
#   3. Uruchom plik: python swedish_ai_dataset.py

"""
Moduł do klasyfikacji danych Auto Insurance in Sweden oraz Wine Dataset.
Wykorzystuje Drzewa Decyzyjne i SVM.
"""

import pandas as pd
import numpy as np
from io import StringIO
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn import datasets


def load_sweden_insurance_data():
    """
    Ładuje i przetwarza dane 'Auto Insurance in Sweden'.
    Konwertuje problem regresji na klasyfikację binarną (Low vs High Payment).

    Returns:
        tuple: X (cechy), y (etykiety), DataFrame
    """
    data_str = """X	Y
108	392,5
19	46,2
13	15,7
124	422,2
40	119,4
57	170,9
23	56,9
14	77,5
45	214
10	65,3
5	20,9
48	248,1
11	23,5
23	39,6
7	48,8
2	6,6
24	134,9
6	50,9
3	4,4
23	113
6	14,8
9	48,7
9	52,1
3	13,2
29	103,9
7	77,5
4	11,8
20	98,1
7	27,9
4	38,1
0	0
25	69,2
6	14,6
5	40,3
22	161,5
11	57,2
61	217,6
12	58,1
4	12,6
16	59,6
13	89,9
60	202,4
41	181,3
37	152,8
55	162,8
41	73,4
11	21,3
27	92,6
8	76,1
3	39,9
17	142,1
13	93
13	31,9
15	32,1
8	55,6
29	133,3
30	194,5
24	137,9
9	87,4
31	209,8
14	95,5
53	244,6
26	187,5"""

    # Zamiana formatu liczb (przecinek na kropkę)
    data_str_processed = data_str.replace(',', '.')
    df = pd.read_csv(StringIO(data_str_processed), sep='\t')

    # Tworzenie klas: 0 dla wypłat <- mediany, 1 dla wypłat > mediany
    median_payment = df['Y'].median()
    df['Target'] = (df['Y'] > median_payment).astype(int)

    X = df[['X']].values
    y = df['Target'].values
    return X, y, df


def load_wine_data():
    """
    Ładuje zbiór danych Wine Dataset.
    Link do danych: https://archive.ics.uci.edu/ml/datasets/wine

    Returns:
        tuple: X (cechy - tylko pierwsze 2 dla wizualizacji), y (etykiety)
    """
    wine = datasets.load_wine()
    X = wine.data[:, :2]  # Wybieramy Alcohol i Malic Acid dla łatwej wizualizacji 2D
    y = wine.target
    return X, y


def evaluate_model(model, X_train, y_train, X_test, y_test, name):
    """
    Trenuje model i drukuje metryki jakości klasyfikacji.

    Args:
        model: Instancja klasyfikatora (np. SVC, DecisionTreeClassifier)
        X_train, y_train: Dane treningowe
        X_test, y_test: Dane testowe
        name (str): Nazwa zbioru danych/modelu
    """
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print(f"--- {name} ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("Raport klasyfikacji:")
    print(classification_report(y_test, y_pred, zero_division=0))
    print("Macierz pomyłek:")
    print(confusion_matrix(y_test, y_pred))
    print("\n")


# --- Główna część programu ---

# 1. Przygotowanie danych
X1, y1, df1 = load_sweden_insurance_data()
X2, y2 = load_wine_data()

X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.3, random_state=42)
X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.3, random_state=42)

# Skalowanie danych (kluczowe dla SVM)
scaler1 = StandardScaler()
X1_train_scaled = scaler1.fit_transform(X1_train)
X1_test_scaled = scaler1.transform(X1_test)

scaler2 = StandardScaler()
X2_train_scaled = scaler2.fit_transform(X2_train)
X2_test_scaled = scaler2.transform(X2_test)

# 2. Inicjalizacja i trenowanie modeli
dt1 = DecisionTreeClassifier(max_depth=3, random_state=42)
dt2 = DecisionTreeClassifier(max_depth=3, random_state=42)
svm1 = SVC(kernel='rbf', C=1.0, random_state=42)
svm2 = SVC(kernel='rbf', C=1.0, random_state=42)

print("=== WYNIKI KLASYFIKACJI ===\n")
evaluate_model(dt1, X1_train, y1_train, X1_test, y1_test, "Insurance - Decision Tree")
evaluate_model(svm1, X1_train_scaled, y1_train, X1_test_scaled, y1_test, "Insurance - SVM")
evaluate_model(dt2, X2_train, y2_train, X2_test, y2_test, "Wine - Decision Tree")
evaluate_model(svm2, X2_train_scaled, y2_train, X2_test_scaled, y2_test, "Wine - SVM")

# 3. Eksperyment z Kernelami SVM
print("=== Eksperyment z Kernelami SVM (Dataset: Wine) ===")
kernels = ['linear', 'poly', 'rbf', 'sigmoid']
params_C = [0.1, 1.0, 10.0]

results = []
for kern in kernels:
    for C_val in params_C:
        svm_temp = SVC(kernel=kern, C=C_val, random_state=42)
        svm_temp.fit(X2_train_scaled, y2_train)
        acc = accuracy_score(y2_test, svm_temp.predict(X2_test_scaled))
        results.append({'Kernel': kern, 'C': C_val, 'Accuracy': acc})

results_df = pd.DataFrame(results)
print(results_df)

# 4. Przykładowa predykcja
input_sample_1 = np.array([[50]])  # 50 roszczeń
input_sample_2 = np.array([[13.5, 2.5]])  # Alkohol 13.5, Kwas 2.5

print("\n=== Przykładowa Predykcja ===")
print(f"Wejście Insurance (Liczba roszczeń): {input_sample_1[0][0]}")
pred_dt1 = dt1.predict(input_sample_1)[0]
pred_svm1 = svm1.predict(scaler1.transform(input_sample_1))[0]
print(f" -> Drzewo: Klasa {pred_dt1}, SVM: Klasa {pred_svm1}")

print(f"Wejście Wine (Alkohol, Kwas): {input_sample_2[0]}")
pred_dt2 = dt2.predict(input_sample_2)[0]
pred_svm2 = svm2.predict(scaler2.transform(input_sample_2))[0]
print(f" -> Drzewo: Klasa {pred_dt2}, SVM: Klasa {pred_svm2}")