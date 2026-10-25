# SafeSchool PL 🛡️

> Przejrzysta wyszukiwarka i dashboard wypadków w polskich szkołach i placówkach oświatowych, zbudowany na otwartych danych z [dane.gov.pl](https://dane.gov.pl).

[![CI](https://img.shields.io/badge/CI-GitHub_Actions-blue)](.github/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Problem społeczny

Co roku w polskich szkołach dochodzi do tysięcy wypadków. Dane MEiN publikowane są jako osobne pliki CSV dla każdego roku szkolnego i typu placówki – trudne do analizy i porównania. SafeSchool PL agreguje je w jedno narzędzie: dashboard KPI, trendy roczne, rankingi województw/przyczyn/miejsc oraz wyszukiwarkę rekordów z filtrowaniem.

## Źródło danych

- **Portal:** dane.gov.pl
- **Zbiór:** "Wypadki w szkołach i placówkach oświatowych" (Ministerstwo Edukacji i Nauki), ID zbioru `40`.
- **Format:** CSV, po roku szkolnym (2018/2019 … 2024/2025).
- **Licencja danych:** CC0 / otwarte dane publiczne.

## Struktura repozytorium

```
.
├── src/safeschool/     # kod aplikacji (Flask)
├── tests/              # testy (unittest)
├── scripts/            # fetch_data.py – pobieranie danych z API
├── docs/               # dokumentacja (ISO 21513, PMI, ISO 10013)
├── .github/            # szablony i CI
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Wymagania

- Python 3.11+
- (opcjonalnie) Docker + Docker Compose

## Uruchomienie (jedna komenda)

### Lokalnie

```bash
pip install -r requirements.txt
cp .env.example .env
python run.py          # pobiera dane (jeśli brak) i uruchamia aplikację
```

W Windows PowerShell:
```powershell
python run.py
```

Otwórz: http://localhost:8000

### Docker (jedna komenda)

```bash
docker compose up --build
```

Aplikacja dostępna pod http://localhost:8000. Dane pobierane są automatycznie przy budowie obrazu.

## Testy

```bash
python -m unittest discover -s tests -v
```

## API

| Endpoint | Opis |
|----------|------|
| `GET /` | Dashboard |
| `GET /search` | Wyszukiwarka rekordów |
| `GET /api/aggregate?by=wojewodztwo` | Agregacja (wojewodztwo, typ_podmiotu, przyczyna, miejsce, zajecia, year, powiat, gmina) |
| `GET /api/trend` | Trend roczny |
| `GET /health` | Status |

Parametry filtrowania: `year`, `wojewodztwo`, `powiat`, `gmina`, `typ_podmiotu`, `przyczyna`, `miejsce`, `zajecia`, `rodzaj_wypadku`.

## Zmienne środowiskowe

Zobacz `.env.example`. Klucze i hasła nigdy nie są w kodzie.

## Licencja

MIT – zobacz [LICENSE](LICENSE).

## Dokumentacja

- [Raport końcowy (ISO 21513)](docs/raport_koncowy.md)
- [Lessons learned (PMI)](docs/lessons_learned.md)
- [Kontrola dokumentów (ISO 10013)](docs/kontrola_dokumentow.md)
- [CONTRIBUTING](CONTRIBUTING.md)
