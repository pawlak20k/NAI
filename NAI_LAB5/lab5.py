"""
PROBLEM: Implementacja i porównanie sieci neuronowych w zadaniach regresji i klasyfikacji.
AUTORZY: s27118, s27084
INSTRUKCJA:
1. Wymagane biblioteki: pip install tensorflow pandas scikit-learn matplotlib seaborn pyarrow
2. Skrypt automatycznie pobiera dane lub generuje je lokalnie.
3. Wyniki (Confusion Matrix) wyświetlą się w osobnym oknie.
"""

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, confusion_matrix, classification_report
from sklearn.datasets import fetch_openml

# Konfiguracja wykresów
plt.style.use('ggplot')

def task_1_auto_insurance():
    """
    Zadanie 1: Porównanie regresji liniowej i sieci neuronowej.
    Zbiór: Swedish Auto Insurance.
    """
    print("\n--- ZADANIE 1: Swedish Auto Insurance ---")

    data = {
        'X': [108, 19, 13, 124, 40, 57, 23, 14, 45, 10, 5, 48, 11, 23, 7, 2, 24, 6, 3, 0, 9, 9, 7, 3, 29, 7, 4, 20, 7, 4, 0, 25, 6, 5, 22, 11, 61, 12, 4, 16, 13, 60, 41, 37, 55, 41, 11, 27, 8, 3, 17, 13, 13, 15, 8, 29, 30, 24, 9, 31, 14, 53, 26],
        'Y': [392.5, 46.2, 15.7, 422.2, 119.4, 170.9, 56.9, 77.5, 214, 65.3, 20.9, 248.1, 23.5, 39.6, 48.8, 6.6, 134.9, 50.9, 4.4, 4.4, 29.8, 98.1, 27.9, 10.2, 103.9, 31.3, 38.1, 98.1, 12, 38.1, 0, 69.2, 14.6, 40.3, 161.5, 57.2, 217.6, 58.1, 12.6, 59.6, 89.9, 202.4, 181.3, 152.8, 162.8, 73.4, 21.3, 92.6, 76.1, 39.9, 142.1, 93, 31.9, 32.1, 55.6, 133.3, 194.5, 137.9, 87.4, 209.8, 95.5, 244.6, 187.5]
    }
    df = pd.DataFrame(data)
    X = df[['X']].values
    y = df['Y'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Regresja Liniowa
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_rmse = np.sqrt(mean_squared_error(y_test, lr_model.predict(X_test)))

    # Sieć Neuronowa (Nowa składnia Input)
    nn_model = models.Sequential([
        layers.Input(shape=(1,)),
        layers.Dense(16, activation='relu'),
        layers.Dense(16, activation='relu'),
        layers.Dense(1)
    ])
    nn_model.compile(optimizer='adam', loss='mse')
    nn_model.fit(X_train, y_train, epochs=200, verbose=0)
    nn_rmse = np.sqrt(mean_squared_error(y_test, nn_model.predict(X_test, verbose=0)))

    print(f"Skuteczność (RMSE) - Regresja Liniowa: {lr_rmse:.2f}")
    print(f"Skuteczność (RMSE) - Sieć Neuronowa: {nn_rmse:.2f}")

def task_2_cifar10():
    """
    Zadanie 2: Rozpoznawanie zwierząt (CIFAR10).
    """
    print("\n--- ZADANIE 2: CIFAR10 (Zwierzęta) ---")
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    model = models.Sequential([
        layers.Input(shape=(32, 32, 3)),
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=3, batch_size=64, verbose=1)

    _, acc = model.evaluate(x_test, y_test, verbose=0)
    print(f"Dokładność CIFAR10: {acc:.2%}")

def task_3_fashion_mnist():
    """
    Zadanie 3: Ubrania (Fashion-MNIST) - Porównanie dwóch rozmiarów sieci.
    """
    print("\n--- ZADANIE 3: Fashion-MNIST (Dwa rozmiary) ---")
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    # Model Mały
    m1 = models.Sequential([layers.Input(shape=(28, 28)), layers.Flatten(), layers.Dense(16, activation='relu'), layers.Dense(10, activation='softmax')])
    # Model Duży
    m2 = models.Sequential([layers.Input(shape=(28, 28)), layers.Flatten(), layers.Dense(128, activation='relu'), layers.Dense(64, activation='relu'), layers.Dense(10, activation='softmax')])

    for m, name in zip([m1, m2], ["MAŁA", "DUŻA"]):
        m.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        m.fit(x_train, y_train, epochs=3, batch_size=128, verbose=0)
        _, acc = m.evaluate(x_test, y_test, verbose=0)
        print(f"Sieć {name} - Dokładność: {acc:.2%}")


def task_4_cancer():
    """
    Zadanie 4: Klasyfikacja medyczna (Breast Cancer Wisconsin).
    """
    print("\n--- ZADANIE 4: Custom Case (Klasyfikacja Medyczna) ---")

    from sklearn.datasets import load_breast_cancer

    # 1. Ładowanie danych bezpośrednio z pamięci komputera
    data = load_breast_cancer()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = data.target

    print(f"Dane załadowane lokalnie. Próbek: {len(X)}, Cech: {X.shape[1]}")

    # 2. Skalowanie danych (wyłącznie numerycznych)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded := y, test_size=0.2, random_state=42
    )

    # 3. Budowa sieci neuronowej
    model = models.Sequential([
        layers.Input(shape=(X_train.shape[1],)),
        layers.Dense(32, activation='relu'),
        layers.Dense(16, activation='relu'),
        layers.Dense(2, activation='softmax')  # 2 klasy: malignant / benign
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    print("Trenowanie sieci...")
    model.fit(X_train, y_train, epochs=30, batch_size=16, verbose=0)

    # 4. Predykcja i Macierz Konfuzji
    y_pred = np.argmax(model.predict(X_test, verbose=0), axis=1)
    cm = confusion_matrix(y_test, y_pred)

    # Wyświetlanie graficzne Confusion Matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='magma',
                xticklabels=data.target_names, yticklabels=data.target_names)
    plt.title('Macierz Błędów: Diagnoza Nowotworów')
    plt.ylabel('Stan faktyczny')
    plt.xlabel('Predykcja sieci')
    plt.tight_layout()
    plt.show()

    print("\nRaport klasyfikacji:")
    print(classification_report(y_test, y_pred, target_names=data.target_names))

if __name__ == "__main__":
    task_1_auto_insurance()
    task_2_cifar10()
    task_3_fashion_mnist()
    task_4_cancer()