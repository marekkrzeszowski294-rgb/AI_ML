# ==============================================================================
# BACKEND WEBOWY DLA MODELU UCZENIA MASZYNOWEGO (FLASK)
# ==============================================================================
# Ten plik łączy wytrenowany model uczenia maszynowego ze stroną internetową.
# Odbiera dane z przeglądarki (formularz), przesyła je do modelu AI i zwraca
# wynik w formacie JSON do wyświetlenia na stronie.
# ==============================================================================

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from ml_srodowisko import trenuj_model_ochrony_srodowiska

app = Flask(__name__)

# Trenujemy model przy uruchomieniu backendu
print("\n[BACKEND] Inicjalizacja modelu Machine Learning...")
model = trenuj_model_ochrony_srodowiska()
print("[BACKEND] Model jest gotowy do obslugi zapytan ze strony WWW!")


@app.route('/')
def strona_glowna():
    """Wyswietla strone glowna z formularzem."""
    return render_template('index.html')


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    Punkt końcowy API (Endpoint) odbierający dane z formularza WWW.
    Przekazuje dane do modelu Random Forest i zwraca werdykt w formacie JSON.
    """
    try:
        dane = request.get_json()
        if not dane:
            return jsonify({"status": "error", "message": "Brak danych w zapytaniu"}), 400

        pm2_5 = float(dane.get("pm2_5", 25.0))
        odleglosc = float(dane.get("odleglosc_woda", 500.0))
        toksyczne = int(dane.get("czy_toksyczne", 0))
        zgloszenia = int(dane.get("liczba_zgloszen", 1))

        # Przygotowujemy dane w formacie DataFrame oczekiwanym przez model
        przypadek = pd.DataFrame([{
            "PM2_5": pm2_5,
            "Odleglosc_od_wody_m": odleglosc,
            "Czy_toksyczne": toksyczne,
            "Liczba_zgloszen": zgloszenia
        }])

        # Wykonujemy predykcję za pomocą modelu
        priorytet = model.predict(przypadek)[0]
        prawdopodobienstwa = model.predict_proba(przypadek)[0]
        klasy = model.classes_

        pewnosc = {klasa: round(prob * 100, 1) for klasa, prob in zip(klasy, prawdopodobienstwa)}

        return jsonify({
            "status": "success",
            "priorytet": priorytet,
            "pewnosc": pewnosc
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  SERWER DZIALA! Otworz ponizszy adres w przegladarce:")
    print("  --> http://127.0.0.1:5000")
    print("="*60 + "\n")
    app.run(host='127.0.0.1', port=5000, debug=False)
