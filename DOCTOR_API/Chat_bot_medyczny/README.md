# 🩺 DoctorAPI

Mikroserwis oparty na FastAPI, służący do zarządzania informacjami o lekarzach oraz sprawdzania ich dostępności na podstawie danych z mikroserwisu kalendarza (CalendarAPI).

---

## 📦 Zawartość projektu

---
```
app/
├── routes/
│ └── User.py # Endpointy API lekarzy (GET, POST, PUT, DELETE, dostępność)
├── models/
│ └── User.py # Model SQLAlchemy dla lekarzy
├── schemas/
│ └── User.py # Schematy Pydantic do walidacji danych wejściowych
├── services/
│ └── availability.py # Sprawdzanie dostępności lekarzy na podstawie CalendarAPI
database.py # Połączenie z bazą danych
dependencies.py # Dependency injection dla sesji DB
main.py # Uruchomienie FastAPI, rejestracja routerów
test_main.http # Testy HTTP (REST Client/Postman)
.env.example # Przykład pliku środowiskowego
requirements.txt # Zależności projektu
```

## 🚀 Uruchamianie projektu

### 1. Przygotowanie środowiska

Zainstaluj zależności:

pip install -r requirements.txt
2. Skonfiguruj zmienne środowiskowe
Uzupełnij plik .env na podstawie .env.example:
`
DB_USER=twoj_uzytkownik
DB_PASSWORD=twoje_haslo
DB_HOST=localhost
DB_PORT=3306
DB_NAME=twoja_baza
`
3. Uruchom aplikację
uvicorn main:app --reload
Baza danych zostanie zainicjalizowana automatycznie, jeśli nie istnieje.

🔧 Endpointy API /doktor
| Metoda   | Endpoint                                      | Opis                                         |
| -------- | --------------------------------------------- | -------------------------------------------- |
| `POST`   | `/doktor/`                                    | Tworzy nowego lekarza                        |
| `PUT`    | `/doktor/{doctor_id}`                         | Aktualizuje dane lekarza                     |
| `DELETE` | `/doktor/{doctor_id}`                         | Usuwa lekarza                                |
| `GET`    | `/doktor/{doctor_id}`                         | Pobiera dane lekarza                         |
| `GET`    | `/doktor/{email}/dostepnosc?datetime=ISO8601` | Sprawdza dostępność lekarza w danym terminie |
| `GET`    | `/doktor/{email}/najblizszy_termin`           | Zwraca najbliższy wolny termin w ciągu 24h   |


🔁 Integracja z CalendarAPI
DoctorAPI integruje się z CalendarAPI, aby sprawdzić czy lekarz ma już wydarzenie (spotkanie) w danym dniu/godzinie. Wymagane jest uruchomienie CalendarAPI na http://127.0.0.1:9000.

✅ Testowanie
Użyj test_main.http (np. w VS Code z rozszerzeniem REST Client) lub importuj do Postmana.

##    📚 Wymagania
    css
    fastapi
    uvicorn[standard]
    sqlalchemy
    pymysql
    python-dotenv
    pydantic
    requests

##    📌 Przykładowe dane lekarza
    json
    {
      "imie": "Anna",
      "nazwisko": "Kowalska",
      "klasyfikacja": "Kardiolog",
      "email": "anna.kowalska@example.com"
    }
