# 📅 CalendarAPI

Mikroserwis oparty na **FastAPI**, integrujący się z **Google Calendar API**, umożliwiający tworzenie, edycję i usuwanie wydarzeń w kalendarzu użytkownika. Obsługuje również zarządzanie tokenem autoryzacyjnym Google.

---

## 📦 Zawartość projektu

| Ścieżka                        | Zawartość                                                                                           |
|--------------------------------|-----------------------------------------------------------------------------------------------------|
| `models/User.py`               | Modele danych (`User`, `Event`)                                                                     |
| `schemas/User.py`              | Schematy walidacyjne do tworzenia i edycji wydarzeń (`EventCreateSchema`, `EventUpdateSchema`)      |
| `routes/User.py`               | Endpointy API związane z operacjami na wydarzeniach                                                 |
| `services/calendar_service.py` | Integracja z **Google Calendar API** — logika tworzenia, edycji i usuwania wydarzeń                 |
| `main.py`                      | Główna aplikacja FastAPI i rejestracja routerów                                                     |
| `.gitignore`                   | Lista plików ignorowanych przez Git (np. `token.pickle`)                                            |
| `requirements.txt`             | Lista bibliotek wymaganych do uruchomienia aplikacji                                                |
| `test_main.http`               | Zbiór zapytań HTTP do testowania API (np. w REST Client lub Postman)                                |
| `credentials.json`             | (lokalnie, nie w repozytorium) Dane OAuth 2.0 z Google Cloud                                        |
| `token.pickle`                 | Plik z zapisanym tokenem Google API (generowany automatycznie po autoryzacji przy użyciu endpointu) |

---

## 🚀 Uruchamianie projektu

### 1. Instalacja zależności

Upewnij się, że masz zainstalowane Python 3.8+ oraz pip, a następnie uruchom:

```bash
pip install -r requirements.txt
```
### 2. 📄 Uzyskanie credentials.json (Google API)
Aby korzystać z Google Calendar API, musisz pobrać dane logowania OAuth 2.0:

    1. Przejdź do Google Cloud Console. (https://console.cloud.google.com/)

    2. Utwórz nowy projekt lub wybierz istniejący.

    3. W menu po lewej wybierz: APIs & Services → Credentials.
        * Wyszukaj Calendar API i uruchom 

    4. Przekieruje cie na panel Calendar Api wybierz w menu po lewej stronie → OAuth client ID.

    5. Jeśli to Twoje pierwsze użycie:
        * Skonfiguruj OAuth Consent Screen:
        * Wprowadź podstawowe dane (nazwa aplikacji, adres email)
        * Typ użytkownika: External
        * Podaj email kontaktowy

    6. Utwórz dane klienta w zakładce Clients:
        * Typ aplikacji: Desktop app
        * Nazwa: np.CalendarAPI

    7. Po utworzeniu kliknij Download JSON i zapisz plik jako credentials.json.

### 3. 📁 Umieszczenie danych logowania

Dodaj plik credentials.json do katalogu głównego projektu.

### 4. 🧪 Uzyskanie tokena (token.pickle)

    1. Uruchom Projekt ``uvicorn main:app --reload``

    2. Możesz pobrać token ręcznie z odpowiedniego endpointu (POST /refresh_token):

    3. Po pierwszym uruchomieniu aplikacji zostaniesz poproszony o zalogowanie się przez konto Google w celu autoryzacji.

## 🔐 Operacje na tokenie Google API (bez prefixu)

| Metoda   | Endpoint           | Opis                                                             |
| -------- |--------------------|------------------------------------------------------------------|
| `GET`    | `/token`           | Pobiera aktualny plik tokenu `token.pickle`, jeśli istnieje.     |
| `DELETE` | `/token`           | Usuwa token autoryzacyjny `token.pickle`.                        |
| `POST`   | `/refresh_token`   | Odświeża token Google API lub generuje nowy, jeśli nie istnieje. |

## 📅 Operacje na wydarzeniach (/user prefix)

| Metoda   | Endpoint                                            | Opis                                                                    |
|----------|-----------------------------------------------------|-------------------------------------------------------------------------|
| `POST`   | `/user/add_event`                                   | Tworzy nowe wydarzenie w kalendarzu Google.                             |
| `PUT`    | `/user/edit_event/{event_id}`                       | Aktualizuje dane istniejącego wydarzenia na podstawie jego ID.          |
| `DELETE` | `/user/delete_event/{event_id}`                     | Usuwa wydarzenie z kalendarza na podstawie jego ID.                     |
| `GET`    | `/user/event/{event_id}`                            | Zwraca szczegóły pojedynczego wydarzenia na podstawie jego ID.          |
| `GET`    | `/user/events_by_day?date=YYYY-MM-DD`               | Zwraca wydarzenia z konkretnego dnia (domyślnie strefa Europe/Warsaw).  |
| `GET`    | `/user/events_by_hour?date=YYYY-MM-DD&hour=HH`      | Zwraca wydarzenia z danej godziny i opcjonalnie e-maila uczestnika.     | 

## ✅ Testowanie
Do testowania możesz użyć pliku test_main.http w edytorze takim jak VS Code z rozszerzeniem REST Client lub importować go do Postmana.

## 📚 Wymagania
Wymagane biblioteki (patrz requirements.txt):

* fastapi
* uvicorn
* google-api-python-client
* google-auth
* google-auth-oauthlib
* pytz