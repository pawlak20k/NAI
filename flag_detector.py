"""
OPIS PROBLEMU: System wizyjny do automatycznego rozpoznawania i lokalizacji
trzech flag państwowych (Polska, Rosja, Ukraina) w strumieniu wideo.
Program identyfikuje układ barw i podaje współrzędne flagi na ekranie.

AUTORZY: s27118, s27084

INSTRUKCJA UŻYCIA:
1. Zainstaluj biblioteki: pip install opencv-python numpy.
2. Uruchom skrypt.
3. Umieść flagę przed kamerą (fizyczną lub na ekranie telefonu).
4. Program zaznaczy flagę ramką i wypisze jej nazwę oraz pozycję (x, y).
5. Naciśnij 'q', aby wyjść z programu.

REFERENCJE: Dokumentacja OpenCV (segmentacja kolorów HSV, detekcja konturów).
"""

import cv2
import numpy as np

def get_color_ranges():
    """
    Definiuje progi kolorów w przestrzeni HSV (Hue, Saturation, Value).

    Zakresy są zoptymalizowane pod kątem emisji światła przez ekrany telefonów
    oraz standardowe oświetlenie pokojowe.
    """
    return {
        # Biały: niskie nasycenie (S), wysoka jasność (V)
        "BIALY": ((0, 0, 180), (180, 60, 255)),
        # Czerwony: dwie maski ze względu na zawijanie się skali Hue (0-10 i 160-180)
        "CZERWONY_1": ((0, 70, 70), (10, 255, 255)),
        "CZERWONY_2": ((160, 70, 70), (180, 255, 255)),
        # Niebieski: zakres typowy dla barw flagowych
        "NIEBIESKI": ((90, 70, 50), (135, 255, 255)),
        # Żółty: jasny i nasycony
        "ZOLTY": ((20, 100, 100), (35, 255, 255))
    }

def has_color(roi_hsv, color_key):
    """
    Sprawdza obecność konkretnego koloru w danym wycinku obrazu (ROI).

    Args:
        roi_hsv: Wycinek obrazu w formacie HSV.
        color_key: Klucz koloru ze słownika get_color_ranges.

    Returns:
        bool: True, jeśli kolor zajmuje więcej niż 25% analizowanego obszaru.
    """
    ranges = get_color_ranges()
    if color_key == "CZERWONY":
        mask1 = cv2.inRange(roi_hsv, *ranges["CZERWONY_1"])
        mask2 = cv2.inRange(roi_hsv, *ranges["CZERWONY_2"])
        mask = cv2.bitwise_or(mask1, mask2)
    else:
        mask = cv2.inRange(roi_hsv, *ranges[color_key])

    # Obliczanie gęstości występowania koloru
    percentage = (np.sum(mask > 0) / mask.size) * 100
    return percentage > 25

def detect_flag(frame):
    """
    Główna funkcja przetwarzająca klatkę wideo w poszukiwaniu flag.

    Algorytm:
    1. Konwersja do HSV.
    2. Stworzenie maski zbiorczej dla wszystkich barw flagowych.
    3. Usunięcie szumów (morfologia).
    4. Znalezienie konturów i analiza układu pasów (góra/środek/dół).
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ranges = get_color_ranges()

    # Tworzenie maski zbiorczej, aby wykryć obiekt będący potencjalną flagą
    mask_all = cv2.bitwise_or(cv2.inRange(hsv, *ranges["BIALY"]),
                              cv2.bitwise_or(cv2.inRange(hsv, *ranges["NIEBIESKI"]),
                                             cv2.inRange(hsv, *ranges["ZOLTY"])))
    mask_red = cv2.bitwise_or(cv2.inRange(hsv, *ranges["CZERWONY_1"]), cv2.inRange(hsv, *ranges["CZERWONY_2"]))
    mask_all = cv2.bitwise_or(mask_all, mask_red)

    # Operacje morfologiczne - czyszczenie obrazu z drobnych zakłóceń
    kernel = np.ones((5, 5), np.uint8)
    mask_all = cv2.morphologyEx(mask_all, cv2.MORPH_OPEN, kernel)

    # Wyszukiwanie konturów obiektów o określonych kolorach
    contours, _ = cv2.findContours(mask_all, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # Filtrowanie konturów po wielkości (pominięcie małych obiektów w tle)
        if cv2.contourArea(cnt) > 8000:
            x, y, w, h = cv2.boundingRect(cnt)
            roi = hsv[y:y+h, x:x+w]

            # Podziały na sekcje do weryfikacji układu pasów
            top_3 = roi[0:h//3, :]      # Górny pas (dla flag 3-pasmowych)
            mid_3 = roi[h//3:2*h//3, :] # Środkowy pas
            bot_3 = roi[2*h//3:h, :]    # Dolny pas

            top_2 = roi[0:h//2, :]      # Górna połowa (dla flag 2-pasmowych)
            bot_2 = roi[h//2:h, :]      # Dolna połowa

            res_flag = "Nieznana"

            # Logika hierarchiczna (zapobiega błędnej klasyfikacji Rosji jako Polski)
            if has_color(top_3, "BIALY") and has_color(mid_3, "NIEBIESKI") and has_color(bot_3, "CZERWONY"):
                res_flag = "ROSJA"
            elif has_color(top_2, "NIEBIESKI") and has_color(bot_2, "ZOLTY"):
                res_flag = "UKRAINA"
            elif has_color(top_2, "BIALY") and has_color(bot_2, "CZERWONY"):
                # Polska tylko jeśli środkowy pas nie jest niebieski
                if not has_color(mid_3, "NIEBIESKI"):
                    res_flag = "POLSKA"

            # Wyświetlanie wyników: nazwa oraz pozycja x, y
            if res_flag != "Nieznana":
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(frame, f"{res_flag} Poz:[{x},{y}]", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    return frame

def main():
    """Inicjalizuje przechwytywanie wideo i pętlę główną programu."""
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Błąd: Nie można odebrać klatki z kamery.")
            break

        output = detect_flag(frame)
        cv2.imshow('System Rozpoznawania Flag - Computer Vision', output)

        # Wyjście z programu po naciśnięciu klawisza 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()