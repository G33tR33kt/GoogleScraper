import json                                                 # Pre prácu s JSON súbormi (ukladanie výsledkov)
import pytest                                               # Testovací framework pytest
from unittest.mock import patch, MagicMock                  # Simulovanie objektov počas testovania
from app import app                                         # Importujeme Flask aplikáciu, ktorú budeme testovať

# Pytest fixture, ktorá vytvorí testovacieho klienta Flask aplikácie
@pytest.fixture
def client():
    app.testing = True                                      # Zapne testovací režim Flasku (lepšie spracovanie chýb)
    return app.test_client()                                # Vytvorí klienta, ktorý nám umožní simulovať HTTP požiadavky

# Test pre platný dotaz do /search endpointu
def test_search_valid_query(client):
    response = client.get("/search?q=test")                 # Pošleme GET požiadavku s query parametrom 'q=test'
    assert response.status_code == 200                      # Očakávame, že HTTP status bude 200 (OK)
    data = response.get_json()                              # Z odpovede získame JSON (výsledky vyhľadávania)
    assert isinstance(data, list)                           # Očakávame, že odpoveď je zoznam

    # Kontrolujeme, či každý výsledok obsahuje kľúče 'title' a 'url'
    assert all("title" in item and "url" in item for item in data)

# Test pre prípad, keď dotaz (query) chýba
def test_search_empty_query(client):
    response = client.get("/search")                        # Zavoláme /search bez query parametra
    assert response.status_code == 400                      # Očakávame chybu 400 (Bad Request)

# Test, ktorý simuluje zlyhanie volania vonkajšieho API (Google Custom Search)
@patch('app.requests.get')                                  # Nahradíme volanie requests.get mockom (simuláciou)
def test_search_api_failure(mock_get, client):
    mock_get.side_effect = Exception("API failure")         # Simulujeme výnimku pri volaní API
    response = client.get("/search?q=test")
    assert response.status_code == 500                      # Očakávame, že aplikácia vráti chybu 500 (Internal server error)
    data = response.get_json()
    assert "error" in data                                  # Očakávame, že odpoveď obsahuje kľúč "error" s popisom chyby

# Test overujúci, že výsledky sa správne ukladajú do súboru
@patch('app.requests.get')                                  # Opäť nahradíme requests.get mockom (simuláciou)
def test_search_save_results_to_file(mock_get, client, tmp_path):
    # Pripravíme simulovanú odpoveď API
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None      # Simulujeme úspešný HTTP status
    mock_response.json.return_value = {
        "items": [                                          # Simulované výsledky vyhľadávania
            {"title": "Test Title 1", "link": "http://example.com/1"},
            {"title": "Test Title 2", "link": "http://example.com/2"},
        ]
    }
    mock_get.return_value = mock_response                   # requests.get vráti náš mock_response (odpoveď simulácie)

    results_file = tmp_path / "results.json"                # Dočasný súbor vytvorený pytestom

    # Zavoláme endpoint s query a špecifikovaným výsledným súborom
    response = client.get(f"/search?q=test&results_file={results_file}")
    assert response.status_code == 200                      # Očakávame úspešnú odpoveď

    # Skontrolujeme, či súbor s výsledkami existuje
    assert results_file.exists()
    # Otvoríme súbor a načítame uložené výsledky
    with open(results_file, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
    assert isinstance(saved_data, list)                     # Malo by to byť pole (zoznam)
    # Každý záznam by mal obsahovať title a url
    assert all("title" in item and "url" in item for item in saved_data)
