
# 🤖 Recepcjonistka AI – INFOTECH

Aplikacja FastAPI wspierana przez OpenAI, która działa jako **głosowy asystent-recepcjonistka** w prywatnej klinice INFOTECH. Asystent pomaga umawiać wizyty, zbiera dane pacjenta oraz prowadzi profesjonalną rozmowę w języku polskim.

---

## 🔧 Wymagania
- **Python 3.10+**

- **API key do OpenAI** 

- **API key do Eleven Labs** 

---

## 🚀 Funkcjonalności

- ✅ Umawianie wizyt do wybranych specjalistów.
- ✅ Informowanie o lokalizacji i zasadach działania kliniki.
- ✅ Ekstrakcja danych pacjenta z naturalnej rozmowy:
  - Imię
  - Nazwisko
  - Specjalizacja (np. kardiolog)
  - Numer PESEL
- ✅ Rozpoznawanie kontekstu rozmowy (utrzymywana sesja dzięki `session_id`).
- ✅ Zapamiętywanie danych pacjenta w trakcie rozmowy.
- ✅ Przypomnienie o wysłaniu SMS-a dzień przed wizytą.
- ✅ Automatyczne nadawanie `session_id`, jeśli nie podano.

---

## 📦 Stos technologiczny

- **FastAPI** – backend API
- **OpenAI GPT-4o** – model językowy
- **Python-dotenv** – ładowanie zmiennych środowiskowych
- **Pydantic** – walidacja danych wejściowych
- **Uvicorn** – ASGI server

---

## 🛠️ Struktura projektu

```
app/
├── api/
│   └── routes.py           # Endpoint POST /receptionist
├── core/
│   └── config.py           # Konfiguracja (dotenv)
├── services/
│   ├── llm_client.py       # Klient OpenAI
│   └── receptionist_llm.py # Logika rozmowy, ekstrakcja danych
main.py                     # Uruchomienie FastAPI
```

---

## ▶️ Jak uruchomić?

### 1. Stwórz plik `.env` z kluczem API:
```env
OPENAI_API_KEY=sk-...

ELEVEN_API_KEY = sk...

ELEVEN_VOICE_ID = "....."

```

### 2. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

### 3. Uruchom serwer i voice chat:
```bash
uvicorn main:app --reload 
```

```bash
python voice_client.py
```

---

## 🧪 Przykład żądania `POST /receptionist`

### Request body:

```json
{
  "session_id": "1",
  "user_input": "Chciałbym umówić się do kardiologa, nazywam się Jan Kowalski, PESEL 90010112345"
}
```

### Response:

```json
{
  "session_id": "1",
  "response": "Dzień dobry, jestem Asystentem AI kliniki INFOTECH... (reszta odpowiedzi)",
  "patient_data": {
    "imie": "Jan",
    "nazwisko": "Kowalski",
    "specjalizacja": "kardiolog",
    "PESEL": "90010112345"
  }
}
```

---

## 📌 Uwagi

- Historia konwersacji jest przechowywana tymczasowo w pamięci RAM (resetuje się po restarcie serwera).
- Jeśli `session_id` nie zostanie przesłany, zostanie wygenerowany automatycznie.
