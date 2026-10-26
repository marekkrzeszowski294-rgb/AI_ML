# ==============================================================================
# LEKCJA 1: FUNKCJE, ARGUMENTY I ZWRACANIE WARTOŚCI (RETURN)
# ==============================================================================
# Instrukcja:
# Uzupełnij miejsca oznaczone jako TODO.
# Na samym dole pliku znajdują się testy, które sprawdzą, czy Twój kod działa poprawnie!
# Możesz uruchomić ten plik poleceniem: python zadania.py
# ==============================================================================


# ------------------------------------------------------------------------------
# ZADANIE 1: Prosta funkcja logiczna
# ------------------------------------------------------------------------------
# Napisz funkcję 'czy_pelnoletni', która:
# - Przyjmuje jeden parametr: 'wiek' (liczba).
# - Zwraca True, jeśli wiek wynosi 18 lub więcej.
# - Zwraca False w przeciwnym razie.
#
# Podpowiedź: Pamiętaj o słowie kluczowym 'return'.
# ------------------------------------------------------------------------------


def czy_pelnoletni(wiek):
    return wiek >= 18


# ------------------------------------------------------------------------------
# ZADANIE 2: Domyślne wartości argumentów
# ------------------------------------------------------------------------------
# Napisz funkcję 'oblicz_cene_po_rabacie', która:
# - Przyjmuje: 'cena' oraz 'rabat_procent' (domyślna wartość rabatu ma wynosić 10).
# - Oblicza ostateczną cenę po obniżce.
#   Wzór: cena - (cena * (rabat_procent / 100))
# - Zwraca ostateczną cenę.
# ------------------------------------------------------------------------------

def oblicz_cene_po_rabacie(cena, rabat_procent=10):
    return cena - (cena * (rabat_procent / 100))


# ------------------------------------------------------------------------------
# ZADANIE 3: Przetwarzanie listy w funkcji
# ------------------------------------------------------------------------------
# Napisz funkcję 'filtruj_parzyste', która:
# - Przyjmuje listę liczb jako argument 'lista_liczb'.
# - Tworzy nową, pustą listę na liczby parzyste.
# - Przechodzi pętlą 'for' po elementach i dodaje parzyste (modulo % 2 == 0) metodą .append().
# - Zwraca nowo utworzoną listę liczb parzystych.
# ------------------------------------------------------------------------------

def filtruj_parzyste(lista_liczb):
    parzyste = []
    for liczba in lista_liczb:
        if liczba % 2 == 0:
            parzyste.append(liczba)
    return parzyste


# ==============================================================================
# KOD SPRAWDZAJĄCY (TESTY)
# Nie musisz nic zmieniać poniżej. Uruchom plik, aby sprawdzić swoje rozwiązania!
# ==============================================================================

if __name__ == "__main__":
    print("--- SPRAWDZAMY ROZWIĄZANIA ---")

    # Test Zadania 1
    try:
        assert czy_pelnoletni(20) is True, "Błąd w Zadaniu 1: dla wieku 20 powinno być True"
        assert czy_pelnoletni(18) is True, "Błąd w Zadaniu 1: dla wieku 18 powinno być True"
        assert czy_pelnoletni(15) is False, "Błąd w Zadaniu 1: dla wieku 15 powinno być False"
        print("[OK] Zadanie 1: ZALICZONE!")
    except AssertionError as e:
        print(f"[BLAD] Zadanie 1: {e}")
    except Exception as e:
        print(f"[UWAGA] Zadanie 1: Wystapil blad wykonania ({e})")

    # Test Zadania 2
    try:
        # Rabat domyślny 10% ze 100 zł -> 90.0 zł
        assert oblicz_cene_po_rabacie(100) == 90.0, "Błąd w Zadaniu 2: domyślny rabat dla 100 zł powinien dać 90.0"
        # Rabat podany własnoręcznie 20% ze 200 zł -> 160.0 zł
        assert oblicz_cene_po_rabacie(200, 20) == 160.0, "Błąd w Zadaniu 2: 20% rabatu z 200 zł powinno dać 160.0"
        print("[OK] Zadanie 2: ZALICZONE!")
    except AssertionError as e:
        print(f"[BLAD] Zadanie 2: {e}")
    except Exception as e:
        print(f"[UWAGA] Zadanie 2: Wystapil blad wykonania ({e})")

    # Test Zadania 3
    try:
        wynik_parzyste = filtruj_parzyste([1, 2, 3, 4, 5, 6, 7, 8])
        assert wynik_parzyste == [2, 4, 6, 8], f"Błąd w Zadaniu 3: Oczekiwano [2, 4, 6, 8], otrzymano {wynik_parzyste}"
        print("[OK] Zadanie 3: ZALICZONE!")
    except AssertionError as e:
        print(f"[BLAD] Zadanie 3: {e}")
    except Exception as e:
        print(f"[UWAGA] Zadanie 3: Wystapil blad wykonania ({e})")

    print("---------------------------------")
