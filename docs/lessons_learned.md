# Lessons Learned (PMI)

**Identyfikator dokumentu:** DOC-SSP-002  
**Wersja:** 1.0  
**Autor:** Zespół SafeSchool PL  
**Data:** 2026-10-25  

## Historia zmian

| Wersja | Data | Autor | Opis zmian |
|--------|------|-------|------------|
| 1.0 | 2026-10-25 | Zespół | Wersja końcowa |

---

## 1. Co zadziałało

- **Wybór SQLite** zamiast serwera DB – zero konfiguracji, szybkie zapytania, łatwy deploy.
- **Skrypt fetch_data.py** oparty na API dane.gov.pl – pełna odtwarzalność wyników.
- **Podział na moduły** (config, db, data_loader, app) – ułatwił testowanie.
- **Chart.js z CDN** – szybkie, estetyczne wykresy bez bundlera.
- **Testy dymne** (Flask test client) – wykryły błędy szablonów wcześniej.

## 2. Co nie zadziałało

- Dane źródłowe są w wielu plikach (po roku szkolnym) i wymagają agregacji.
- Brak geolokalizacji w danych – uniemożliwił mapę.
- Kodowanie CSV (UTF-8 z BOM) wymagało `encoding="utf-8-sig"`.
- Endpoint `/file` zwracał XLSX zamiast CSV – trzeba było użyć ścieżki `/csv`.

## 3. Co zrobilibyśmy inaczej

- Od początku zaplanowalibyśmy schemat danych i indeksy.
- Użylibyśmy DuckDB dla zapytań analitycznych (wydajniejsze GROUP BY).
- Dodalibyśmy cache HTTP i paginację po stronie API od startu.
- Przetestowalibyśmy pobieranie danych w CI (mock API).

## 4. Rekomendacje

1. Używać API dane.gov.pl do listowania zasobów zamiast hardkodować URL-e.
2. Przechowywać dane w formacie Parquet dla wydajności (opcjonalnie DuckDB).
3. Dodać monitoring i logowanie zapytań.
4. Rozszerzyć dokumentację o przykłady użycia API.
5. Automatyzować wydania (GitHub Releases) z changelogiem.
