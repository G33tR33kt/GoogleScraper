# Google Scraper Flask App

Jednoduchá Flask aplikácia, ktorá umožňuje vyhľadávanie pomocou Google Custom Search API. Výsledky sa zobrazia na stránke a zároveň uložia do `.json` súboru.

---

## 🔧 Funkcionalita

- Webové rozhranie na zadanie hľadaného výrazu
- Použitie Google Custom Search API
- Výpis výsledkov na stránke
- Uloženie výsledkov do `results.json`
- Testovanie pomocou `pytest`

---

## 🚀 Inštalácia a spustenie

### 1. Naklonuj repozitár alebo si ho priprav na disku

```bash
git clone <repo-url>
cd MYFLASKAPP
```

### 2. Vytvor virtuálne prostredie

```bash
python -m venv venv
```

### 3. Aktivuj virtuálne prostredie

- **Windows:**
  ```bash
  .\venv\Scripts\activate
  ```

- **Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```

### 4. Nainštaluj závislosti

Ak máš súbor `requirements.txt`, spusti:

```bash
pip install -r requirements.txt
```

Ak ho nemáš, nainštaluj závislosti manuálne:

```bash
pip install Flask requests pytest
```

---

## 🧪 Spustenie testov

Spusti testy pomocou:

```bash
pytest
```

---

## 🌐 Spustenie aplikácie

Po aktivovaní venv spusti:

```bash
python app.py
```

Aplikácia bude bežať na:

```
http://127.0.0.1:5000/
```

Do prehliadača môžeš napísať hľadaný výraz a výsledky sa zobrazia na stránke.

---

## ⚙️ Voliteľné: Premenné prostredia

Môžeš nastaviť vlastné Google API kľúče:

```bash
# Windows CMD
set GOOGLE_API_KEY=your_api_key
set GOOGLE_CX=your_custom_search_id

# Linux/macOS
export GOOGLE_API_KEY=your_api_key
export GOOGLE_CX=your_custom_search_id
```

Ak ich nenastavíš, použijú sa hodnoty prednastavené v `app.py`.

---

## 📁 Štruktúra projektu

```
MYFLASKAPP/
├── app.py               # Flask aplikácia
├── test_app.py          # Testy
├── templates/
│   └── index.html       # Webové rozhranie
├── results.json         # Výsledky vyhľadávania (uložené)
├── requirements.txt     # Zoznam závislostí
└── README.md            # Tento súbor
```

---

## 📄 requirements.txt (vzor)

Ak ho potrebuješ vytvoriť:

```
Flask
requests
pytest
```

Ulož to ako `requirements.txt`.

---

## 📘 Licencia

Tento projekt je určený na študijné a výukové účely.