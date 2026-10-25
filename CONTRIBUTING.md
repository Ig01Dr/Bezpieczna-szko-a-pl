# Contributing to SafeSchool PL

Dziękujemy za zainteresowanie projektem!

## Zgłaszanie błędów

1. Sprawdź, czy problem nie został już zgłoszony w Issues.
2. Użyj szablonu "Bug report" z katalogu `.github/ISSUE_TEMPLATE`.
3. Dołącz kroki reprodukcji, oczekiwane i rzeczywiste zachowanie oraz wersję Pythona.

## Proponowanie zmian

1. Zrób fork repozytorium i utwórz gałąź: `git checkout -b feat/opis`.
2. Zainstaluj zależności: `pip install -r requirements.txt`.
3. Uruchom testy: `python -m unittest discover -s tests`.
4. Upewnij się, że linter (ruff) nie zgłasza błędów.
5. Otwórz Pull Request używając szablonu PR.

## Styl kodu

- Python 3.11+, PEP 8.
- Typowanie (type hints) mile widziane.
- Testy dla nowej funkcjonalności.

## Dane

Dane pochodzą z dane.gov.pl (MEiN). Nie commituj dużych plików danych – używaj `scripts/fetch_data.py`.
