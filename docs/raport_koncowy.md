# Raport końcowy projektu SafeSchool PL

**Identyfikator dokumentu:** DOC-SSP-001  
**Wersja:** 1.0  
**Autor:** Zespół SafeSchool PL  
**Data:** 2026-10-25  
**Status:** Zatwierdzony  

## Historia zmian

| Wersja | Data | Autor | Opis zmian |
|--------|------|-------|------------|
| 0.1 | 2026-10-20 | Zespół | Pierwsza wersja robocza |
| 1.0 | 2026-10-25 | Zespół | Wersja końcowa |

---

## 1. Cel projektu (ISO 21513 §5)

Celem projektu jest udostępnienie społeczeństwu, rodzicom, nauczycielom i organom prowadzącym placówki oświatowe przejrzystego narzędzia do analizy wypadków w przedszkolach, szkołach i placówkach oświatowych w Polsce. Dane pochodzą z otwartych zasobów dane.gov.pl (Ministerstwo Edukacji i Nauki). Projekt rozwiązuje problem rozproszenia i trudnej dostępności statystyk wypadków, które publikowane są jako osobne pliki CSV dla każdego roku szkolnego.

## 2. Zakres i rezultaty (ISO 21513 §6)

### 2.1 Rezultaty
- Aplikacja webowa (Flask) z dashboardem KPI, trendem rocznym i agregacjami.
- Wyszukiwarka rekordów z filtrowaniem i paginacją.
- Endpointy JSON (`/api/aggregate`, `/api/trend`, `/health`).
- Skrypt `scripts/fetch_data.py` odtwarzający zbiór danych z API dane.gov.pl.
- Testy jednostkowe i dymne (unittest).
- Dokumentacja open source (README, CONTRIBUTING, CODE_OF_CONDUCT, CHANGELOG).
- Konteneryzacja (Dockerfile, docker-compose.yml).

### 2.2 Metryki
- Liczba lat danych: 7 (2018/2019–2024/2025).
- Łączna liczba wypadków w zbiorze: ~ (zależne od roku) dziesiątki tysięcy.
- Czas ładowania dashboardu: < 1 s po załadowaniu danych do SQLite.
- Czas odpowiedzi zapytań filtrowanych: < 100 ms (indeksy SQLite).

## 3. Porównanie z planem (ISO 21513 §7)

| Planowane | Zrealizowane | Status |
|-----------|--------------|--------|
| Dashboard z wykresami | Tak | ✅ |
| Wyszukiwarka z filtrami | Tak | ✅ |
| Pobieranie danych z API | Tak | ✅ |
| Testy | Tak | ✅ |
| Docker deploy | Tak | ✅ |
| Mapa geograficzna | Nie (poza zakresem MVP) | ⚠️ |

## 4. Wpływ (ISO 21513 §8)

- Rodzice i nauczyciele mogą analizować wzorce wypadków (przyczyny, miejsca, zajęcia) i wspierać działania prewencyjne.
- Organizacje prowadzące placówki mogą porównywać regiony i typy placówek.
- Projekt demonstruje wartość otwartych danych publicznych (dane.gov.pl).

## 5. Wnioski (ISO 21513 §9)

Projekt pokazuje, że otwarte dane o wypadkach szkolnych można przekształcić w użyteczne narzędzie analityczne przy niskim koszcie. Kluczowe było zaprojektowanie schematu SQLite i indeksów dla szybkich zapytań. Ograniczeniem jest brak danych geolokalizacyjnych (brak współrzędnych w źródle), co uniemożliwia mapę.

## 6. Rekomendacje

- Dodać warstwę mapy (np. geokodowanie adresów placówek).
- Rozszerzyć o dane o liczbie uczniów (wskaźniki per capita).
- Dodać eksport wyników do CSV.
- Wdrożyć cache HTTP i paginację po stronie API.
