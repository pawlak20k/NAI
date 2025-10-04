# Instrukcja gry: https://strategygameguide.com/dont-say-21-game/
# Autor źródła zasad: Andy (Strategy Game Guide). Źródło użyte do implementacji i strategii: powyższy link.
#
# Autorzy: s27084, s27118
#
# Nazwa pliku: dont_say_21.py
# Opis: Interaktywna gra konsolowa "Don't Say 21" (człowiek vs komputer).
#
# Instrukcja przygotowania środowiska:
# 1. Python 3.8+ (testowane na Python 3.8).
# 2. Skopiuj ten plik jako dont_say_21.py.
# 3. Uruchom: python dont_say_21.py
# 4. Gra działa w trybie tekstowym, podążaj za promptami.
#
#
# Zasady gry (w skrócie):
# a) Gracze na przemian mówią 1, 2 lub 3 kolejne liczby zaczynając od 1.
# b) Kto zmusi się do wypowiedzenia "21" przegrywa.
# c) Optymalna strategia to dążyć do kończenia tury na wielokrotnościach 4 (4,8,12,16,20).

import random
from typing import List, Tuple

TARGET = 21
MIN_SAY = 1
MAX_SAY = 3


def format_numbers(start: int, count: int) -> str:
    """
    Zwraca sformatowany ciąg wypowiedzianych liczb.

    Parameters:
    start (int): ostatnia wypowiedziana liczba przed ruchem (0 jeśli start gry).
    count (int): ile liczb ma być wypowiedzianych (1..3)

    Returns:
    str: łańcuch np. "1, 2, 3"
    """
    nums = [str(n) for n in range(start + 1, start + 1 + count)]
    return ", ".join(nums)


def legal_count_input(s: str) -> int:
    """
    Parsuje i weryfikuje wejście użytkownika dla liczby wypowiedzianych numerów.

    Parameters:
    s (str): surowe wejście

    Returns:
    int: wartość w zakresie [1,3]

    Raises:
    ValueError: jeśli niepoprawne wejście
    """
    try:
        v = int(s.strip())
    except Exception:
        raise ValueError("Proszę podać liczbę całkowitą 1, 2 lub 3.")
    if v < MIN_SAY or v > MAX_SAY:
        raise ValueError("Dozwolone są tylko wartości 1, 2 lub 3.")
    return v


def ai_choose_count(current: int, target: int = TARGET) -> int:
    """
    AI wybiera ile liczb wypowiedzieć (1..3).
    Strategia:
      - Jeśli AI może zakończyć turę na najbliższej wielokrotności 4 (tj. (current + k) % 4 == 0), wybiera takie k (1..3).
      - Jeśli nie może (czyli current % 4 == 0), wybiera losowo z [1,3].

    Parameters:
    current (int): aktualna ostatnia wypowiedziana liczba (0..target-1)
    target (int): docelowa liczba (domyślnie 21)

    Returns:
    int: liczba numerów które AI wypowie (1..3)
    """
    # Jeśli AI może od razu przegrać (np. current >= target-1), wybierz najmniejszą legalną liczbę
    if current >= target - 1:
        # musi powiedzieć 21 w tej turze — minimalny ruch
        return 1

    # cel: osiągnąć najbliższą wielokrotność 4 (4, 8, 12, 16, 20)
    remainder = current % (MAX_SAY + 1)  # current % 4
    if remainder == 0:
        # aI nie może natychmiast wymusić pozycji wielokrotności 4 (gra losowo)
        return random.randint(MIN_SAY, MAX_SAY)
    else:
        # zagra tyle, by doprowadzić do następnej wielokrotności 4
        to_next = (MAX_SAY + 1) - remainder
        # sprawdz czy to_next jest w zakresie 1..3
        if to_next < MIN_SAY or to_next > MAX_SAY:
            return random.randint(MIN_SAY, MAX_SAY)
        return to_next


def play_round(human_first: bool) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Przeprowadza jedną rundę gry do momentu osiągnięcia TARGET (21).

    Parameters:
    human_first (bool): True jeśli człowiek zaczyna, False jeśli AI zaczyna

    Returns:
    Tuple[str, List[Tuple[str, str]]]:
        - zwycięzca: "human" lub "ai"
        - log: lista krotek (gracz, wypowiedziane_liczby_string)
    """
    current = 0
    log: List[Tuple[str, str]] = []
    human_turn = human_first

    while current < TARGET:
        if human_turn:
            # ruch człowieka
            while True:
                try:
                    raw = input(f"Aktualna liczba: {current}. Ile liczb powiesz (1-3)? ")
                    count = legal_count_input(raw)
                    # sprawdz czy przekracza TARGET
                    if current + count > TARGET:
                        # dopuszczamy tylko jeśli ktoś ma powiedzieć dokładnie 21 (przegrana)
                        # ale nadal trzeba pozwolić na ruch, bo reguła dopuszcza powiedzenie do 21.
                        pass
                    break
                except ValueError as e:
                    print("Błąd:", e)
            said = format_numbers(current, count)
            current += count
            print(f"Ty: {said}")
            log.append(("human", said))
            if current >= TARGET:
                print(f"Powiedziałeś {TARGET} — przegrywasz!")
                return "ai", log
        else:
            # ruch ai
            count = ai_choose_count(current)
            # nie pozwol na ruch większy niż do targetu
            if current + count > TARGET:
                count = TARGET - current
                if count <= 0:
                    count = 1
            said = format_numbers(current, count)
            current += count
            print(f"Komputer: {said}")
            log.append(("ai", said))
            if current >= TARGET:
                print(f"Komputer powiedział {TARGET} — komputer przegrywa!")
                return "human", log

        human_turn = not human_turn

    # kontrola - powinno zakończyć się wcześniej
    return ("ai" if current == TARGET else "human"), log


def main():
    """
    Główna pętla gry — umożliwia rozgrywkę wielorundową oraz wybór kto zaczyna.
    """
    print("=== Don’t Say 21 (polska wersja interaktywna) ===")
    print("Zasady: powiedz 1, 2 lub 3 kolejne liczby. Kto powie pierwszy 21 to przegrywa")
    print("Źródło zasad i strategii: https://strategygameguide.com/dont-say-21-game/")
    random.seed()  # seed z czasu

    while True:
        # wybor kto zaczyna
        while True:
            who = input("Kto zaczyna? (1) Ty, (2) Komputer : ").strip()
            if who in ("1", "2"):
                human_first = (who == "1")
                break
            print("Wybierz '1' (Ty) lub '2' (Komputer).")

        winner, log = play_round(human_first)
        if winner == "human":
            print("Gratulacje — wygrałeś tę rundę!")
        else:
            print("Komputer wygrał tę rundę. Spróbuj ponownie!")

        # opcja wyjścia / kontynuacji
        again = input("Zagrać jeszcze raz? (T/N): ").strip().lower()
        if again != "t" and again != "y":
            print("Dziękuję za grę, do zobaczenia!")
            break


if __name__ == "__main__":
    main()
