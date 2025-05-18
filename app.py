from flask import Flask, render_template, request, jsonify      # Import Flask framework a pomocných funkcií
import requests                                                 # Pre vykonávanie HTTP požiadaviek (Google API)
import os                                                       # Na prácu s environmentálnymi premennými
import json                                                     # Pre prácu s JSON súbormi (ukladanie výsledkov)

# Inicializácia Flask aplikácie
app = Flask(__name__)

# Do premenných Načítame Google API kľúč a Custom Search Engine ID z prostredia Google aby sme obišli CAPTCHA overenie
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'VÁŠ_GOOGLE_API_KEY')
GOOGLE_CX = os.getenv('GOOGLE_CX', 'VÁŠ_GOOGLE_CX')

# Názov súboru, do ktorého sa budú ukladať výsledky vyhľadávania
RESULTS_FILE = 'results.json'

# Definícia endpointu pre domovskú stránku (metóda GET na URL '/') inicializácia index.html z tempalatu
@app.route('/')
def index():
    # Vráti obsah súboru index.html (kde sa nachádza vyhľadávaci formulár)
    return render_template('index.html')

# Definícia endpointu pre vyhľadávanie (GET na URL '/search')
@app.route('/search')
def search():
    # Získanie hodnoty parametra 'q' (dotaz na vyhľadávanie) z URL
    # Ak parameter neexistuje, nastaví sa na prázdny reťazec a orezanie medzier
    query = request.args.get('q', '').strip()

    # Ak nebol zadaný žiaden vyhľadávací výraz, vráti sa chyba 400 (Bad request) = ošetrenie vstupu
    if not query:
        return jsonify({"error": "Nezadal jste hledaný výraz"}), 400

    # Pripravíme URL a parametre pre Google Custom Search API
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': GOOGLE_API_KEY,                                      # API kľúč
        'cx': GOOGLE_CX,                                            # ID vlastného vyhľadávacieho nástroja
        'q': query,                                                 # Vyhľadávací dotaz
        'hl': 'cs',                                                 # Jazyk výsledkov (čeština)
        'num': 10                                                   # Počet výsledkov (max 10 pre bezplatné API)
    }

    # Získame možnosť prepísať názov výsledného súboru z query parametra 'results_file'
    # Ak sa nešpecifikuje, použije sa defaultný RESULTS_FILE ktorý potom použijeme pri jednotkových testoch
    results_file = request.args.get('results_file', RESULTS_FILE)

    try:
        # Vykonáme HTTP GET požiadavku na Google Custom Search API
        response = requests.get(url, params=params)
        # Ak server vráti chybu, vyhodíme exeption (napr. 403, 500), dopytujeme sa na status
        response.raise_for_status()
        # Parsujeme JSON odpoveď do Python dátovej štruktúry (slovník)
        data = response.json()

        # Získame pole 'items', ktoré obsahuje výsledky vyhľadávania
        items = data.get('items', [])
        results = []

        # Pre každý výsledok extrahujeme 'title' a 'link'
        for item in items:
            title = item.get('title')
            link = item.get('link')
            if title and link:
                # Ukladáme len výsledky, ktoré majú oboje (title aj url)
                results.append({'title': title, 'url': link})

        # Výsledky zapíšeme do JSON súboru s kódovaním UTF-8
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        # Vrátime výsledky aj ako JSON odpoveď klientovi
        return jsonify(results)
    
    # V prípade akejkoľvek chyby (sieťovej, parsing, atď.) vrátime chybové hlásenie s kódom 500 (Internal server error) = chyba v backende
    except Exception as e:
        return jsonify({"error": f"Chyba při volání Google API: {e}"}), 500


# Spustenie aplikácie na lokálnom serveri (debug režim zapnutý pre lepšiu spätnú väzbu pri vývoji)
if __name__ == '__main__':
    app.run(debug=True)
