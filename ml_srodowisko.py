# ==============================================================================
# PROJEKT UCZENIA MASZYNOWEGO (MACHINE LEARNING)
# TEMAT: Inteligentny system oceny spraw zanieczyszczenia środowiska
# ==============================================================================
# W tym programie nauczymy komputer, jak na podstawie danych historycznych
# oceniać nowe incydenty ekologiczne i decydować o priorytecie interwencji.
# ==============================================================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ==============================================================================
# KROK 1: ZBIÓR DANYCH (DATASET)
# W rzeczywistości dane pochodzą z czujników, baz danych i zgłoszeń mieszkańców.
# Tutaj tworzymy realistyczny zbiór danych historycznych (100 przypadków).
# ==============================================================================

def generuj_dane_historyczne(liczba_spraw=120):
    np.random.seed(42)  # Zapewnia powtarzalność wyników

    # Cechy incydentów (Features):
    # 1. PM2.5 (pył zawieszony w powietrzu, norma to ok. 15-25 ug/m3)
    pm2_5 = np.random.uniform(5, 180, liczba_spraw)
    
    # 2. Odległość od rzeki/zbiornika wodnego w metrach (im bliżej, tym gorzej)
    odleglosc_woda_m = np.random.uniform(10, 1500, liczba_spraw)
    
    # 3. Czy odpady/ścieki są toksyczne (0 = Nie, 1 = Tak)
    czy_toksyczne = np.random.choice([0, 1], size=liczba_spraw, p=[0.7, 0.3])
    
    # 4. Liczba zgłoszeń mieszkańców
    liczba_zgloszen = np.random.randint(1, 40, liczba_spraw)

    # Etykieta (Target - to, czego komputer ma się nauczyć przewidywać):
    # 0 = "NISKI" (rutynowa kontrola)
    # 1 = "SREDNI" (kontrola w ciągu 48h)
    # 2 = "PILNY" (natychmiastowa interwencja)
    priorytety = []
    for i in range(liczba_spraw):
        # Logika środowiskowa:
        zagrozenie = 0
        if pm2_5[i] > 80:
            zagrozenie += 1
        if pm2_5[i] > 130:
            zagrozenie += 2
        if odleglosc_woda_m[i] < 100:
            zagrozenie += 2
        elif odleglosc_woda_m[i] < 300:
            zagrozenie += 1
        if czy_toksyczne[i] == 1:
            zagrozenie += 3
        if liczba_zgloszen[i] > 20:
            zagrozenie += 1

        if zagrozenie >= 4:
            priorytety.append("PILNY")
        elif zagrozenie >= 2:
            priorytety.append("SREDNI")
        else:
            priorytety.append("NISKI")

    df = pd.DataFrame({
        "PM2_5": np.round(pm2_5, 1),
        "Odleglosc_od_wody_m": np.round(odleglosc_woda_m, 0),
        "Czy_toksyczne": czy_toksyczne,
        "Liczba_zgloszen": liczba_zgloszen,
        "Priorytet": priorytety
    })
    return df


# ==============================================================================
# KROK 2: GŁÓWNA PROCEDURA UCZENIA MODELU
# ==============================================================================

def trenuj_model_ochrony_srodowiska():
    print("==================================================")
    print("  SYSTEM UCZENIA MASZYNOWEGO: OCHRONA SRODOWISKA  ")
    print("==================================================")
    print("\n[1] Ladowanie i przygotowywanie danych...")
    df = generuj_dane_historyczne()
    print(f"Liczba wczytanych historycznych spraw: {len(df)}")
    print("\nOto pierwsze 5 przykladowych spraw:")
    print(df.head())

    # Rozdzielamy cechy (X) od etykiety docelowej (y)
    cechy = ["PM2_5", "Odleglosc_od_wody_m", "Czy_toksyczne", "Liczba_zgloszen"]
    X = df[cechy]
    y = df["Priorytet"]

    # Dzielimy dane: 80% do nauki komputera (trening), 20% do testu (sprawdzian)
    print("\n[2] Dzielenie danych na zbior treningowy (80%) i testowy (20%)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Wybieramy model: Random Forest (Las Losowy) - jeden z najlepszych modeli w ML!
    print("[3] Trenowanie modelu Lasu Losowego (Random Forest)...")
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    print("Model sie nauczyl wzorcow z danych!")

    # Sprawdzian: komputer ocenia sprawy, ktorych wczesniej NIE WIDZIAL
    print("\n[4] Ewaluacja (sprawdzian dokladnosci na sprawach testowych)...")
    predykcje = model.predict(X_test)
    dokladnosc = accuracy_score(y_test, predykcje)
    print(f"DOKLADNOSC MODELU: {dokladnosc * 100:.1f}%")

    # Wplyw poszczegolnych cech na decyzje modelu (Feature Importance)
    print("\n[5] Co bylo najwazniejsze dla modelu przy podejmowaniu decyzji?")
    waznosc_cech = pd.Series(model.feature_importances_, index=cechy).sort_values(ascending=False)
    for cecha, waga in waznosc_cech.items():
        print(f" - {cecha:20}: {waga * 100:.1f}% wplywu")

    return model


# ==============================================================================
# KROK 3: PREDYKCJA DLA NOWYCH SPRAW WPROWADZANYCH PRZEZ CZLOWIEKA
# ==============================================================================

def ocen_nowy_przypadek(model, pm2_5, odleglosc_woda, czy_toksyczne, liczba_zgloszen):
    nowy_przypadek = pd.DataFrame([{
        "PM2_5": pm2_5,
        "Odleglosc_od_wody_m": odleglosc_woda,
        "Czy_toksyczne": czy_toksyczne,
        "Liczba_zgloszen": liczba_zgloszen
    }])
    
    decyzja = model.predict(nowy_przypadek)[0]
    prawdopodobienstwa = model.predict_proba(nowy_przypadek)[0]
    klasy = model.classes_
    
    print("\n" + "="*50)
    print("  RAPORT ANALIZY NOWEJ SPRAWY PRZEZ MODEL AI")
    print("="*50)
    print(f"Parametry zgloszenia:")
    print(f"  * PM2.5:                 {pm2_5} ug/m3")
    print(f"  * Odleglosc od wody:     {odleglosc_woda} m")
    print(f"  * Toksycznosc:           {'TAK' if czy_toksyczne == 1 else 'NIE'}")
    print(f"  * Liczba zgloszen:       {liczba_zgloszen}")
    print(f"\nDECYZJA AI -> PRIORYTET: [{decyzja}]")
    print("Pewnosc modelu:")
    for klasa, prob in zip(klasy, prawdopodobienstwa):
        print(f"  - {klasa:6}: {prob * 100:.1f}%")
    print("="*50)


if __name__ == "__main__":
    # 1. Trenujemy model
    model = trenuj_model_ochrony_srodowiska()

    # 2. Testujemy 2 zupelnie nowe sytuacje:
    print("\n--- PRZYKLAD 1: Podejrzany wyciek w poblizu rzeki ---")
    ocen_nowy_przypadek(
        model=model,
        pm2_5=45.0,
        odleglosc_woda=40.0,      # bardzo blisko rzeki (40 m)
        czy_toksyczne=1,          # substancja toksyczna
        liczba_zgloszen=15
    )

    print("\n--- PRZYKLAD 2: Zwykly dym z komina na przedmiesciach ---")
    ocen_nowy_przypadek(
        model=model,
        pm2_5=30.0,
        odleglosc_woda=1200.0,    # daleko od wody
        czy_toksyczne=0,          # nietoksyczne
        liczba_zgloszen=2
    )

    # 3. Interaktywny tryb wprowadzania wlasnych danych z klawiatury (input)
    print("\n" + "="*50)
    print("  TRYB INTERAKTYWNY: WPROWADZ WLASNE ZGLOSZENIE")
    print("="*50)
    
    while True:
        wybor = input("\nCzy chcesz wprowadzic wlasne zgloszenie do oceny przez model? (t/n): ").strip().lower()
        if wybor not in ["t", "tak", "y", "yes"]:
            print("Zakonczono dzialanie programu. Dziekuje!")
            break

        try:
            print("\n--- Podaj parametry nowego incydentu ekologicznego ---")
            user_pm25 = float(input("1. Stezenie pylu PM2.5 (ug/m3, norma: ok. 25): "))
            user_woda = float(input("2. Odleglosc od rzeki/jeziora (w metrach): "))
            user_toks_str = input("3. Czy substancja jest toksyczna/chemiczna? (tak / nie): ").strip().lower()
            user_toks = 1 if user_toks_str in ["t", "tak", "1", "y", "yes"] else 0
            user_zgloszenia = int(input("4. Liczba zgloszen od zaniepokojonych mieszkancow: "))

            # Wywolujemy model ML dla danych podanych przez uzytkownika!
            ocen_nowy_przypadek(
                model=model,
                pm2_5=user_pm25,
                odleglosc_woda=user_woda,
                czy_toksyczne=user_toks,
                liczba_zgloszen=user_zgloszenia
            )
        except ValueError:
            print("[BLAD] Wprowadzono niepoprawna wartosc liczbowa! Sprobuj ponownie.")
