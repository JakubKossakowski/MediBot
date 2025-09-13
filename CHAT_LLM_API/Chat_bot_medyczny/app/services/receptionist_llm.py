# app/services/receptionist_llm.py
from .llm_client import send_to_openai
from .settings_store import get_settings_from_db
from .calendar_client import create_calendar_event
import json
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import re

_db_settings = get_settings_from_db()
CLINIC_ADDRESS = _db_settings.clinic_address
AVAILABLE_HOURS = _db_settings.available_hours()

BASE_PROMPT = f"""
Jesteś inteligentnym asystentem głosowym – recepcjonistką w prywatnej klinice.
Lokalizacja: {CLINIC_ADDRESS}
Twoim zadaniem jest:
- Umawianie wizyt,
- Informowanie o dostępnych terminach,
- Poproś o dane uzytkownika aby podawał je oddzielnie,
- Jeśli specjalizacja lekarza jest nie pełna poproś o sprecyzowanie, powtórzenie nazwy,
- Kiedy bedziesz prosiła o PESEL, przed odpowiedzią użytkownika poproś aby on go przeliterował,
- Zbieranie danych pacjenta (imię i nazwisko, specjalizacja, data/godzina, PESEL, lokalizacja),
- Utrzymywanie ciepłego i profesjonalnego tonu.
- Zawsze na początku rozmowy powiedz że jesteś Asystentem AI kliniki INFOTECH
"""

conversations = {}
DEFAULT_HOUR = 9

POLISH_HOUR_WORDS = {
    "siódma": 7, "ósma": 8, "dziewiąta": 9, "dziesiąta": 10, "jedenasta": 11,
    "dwunasta": 12, "trzynasta": 13, "czternasta": 14, "piętnasta": 15,
    "szesnasta": 16, "siedemnasta": 17
}

MONTHS_PL = {
    "stycznia": 1, "lutego": 2, "marca": 3, "kwietnia": 4, "maja": 5, "czerwca": 6,
    "lipca": 7, "sierpnia": 8, "września": 9, "października": 10, "listopada": 11, "grudnia": 12
}

def extract_patient_data(user_input: str) -> dict:
    extraction_prompt = f"""
Twoje zadanie to wyodrębnienie danych pacjenta z tekstu rozmowy. Zwróć wyłącznie JSON w poniższym formacie:

{{
  "imie": "imię pacjenta",
  "nazwisko": "nazwisko pacjenta",
  "specjalizacja": "do jakiego lekarza chce się umówić",
  "PESEL": "numer pesel pacjenta",
  "preferowana_data": "np. jutro, pojutrze, 17 czerwca 16:00"
}}

Jeśli którejś z informacji brakuje – wpisz wartość null.

Tekst pacjenta: "{user_input}"
"""

    response = send_to_openai([
        {"role": "system", "content": "Jesteś narzędziem do ekstrakcji danych medycznych. Odpowiadasz tylko poprawnym JSON-em."},
        {"role": "user", "content": extraction_prompt}
    ])

    try:
        if isinstance(response, dict) and "choices" in response:
            content = response["choices"][0]["message"]["content"]
        elif isinstance(response, str):
            content = response
        else:
            content = str(response)

        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        json_str = content[json_start:json_end]
        return json.loads(json_str)
    except Exception as e:
        print("Błąd ekstrakcji JSON:", e)
        print("Odpowiedź modelu:", response)
        return {"imie": None, "nazwisko": None, "specjalizacja": None, "PESEL": None, "preferowana_data": None}



def interpret_relative_date(text: str):
    now = datetime.now()
    today = now.replace(hour=DEFAULT_HOUR, minute=0, second=0, microsecond=0)
    if "dzisiaj" in text.lower():
        return now if now.hour >= DEFAULT_HOUR else today
    elif "jutro" in text.lower():
        return today + timedelta(days=1)
    elif "pojutrze" in text.lower():
        return today + timedelta(days=2)
    return None

def extract_hour_from_text(text: str) -> int | None:
    time_match = re.search(r'\b(\d{1,2})(?:[.:](\d{2}))?\b', text)
    if time_match:
        hour = int(time_match.group(1))
        if 7 <= hour <= 20:
            return hour

    polish_hour_match = re.search(r'(?:o|na)\s+(\d{1,2}|' + '|'.join(POLISH_HOUR_WORDS.keys()) + r')', text.lower())
    if polish_hour_match:
        hour_str = polish_hour_match.group(1)
        if hour_str.isdigit():
            hour = int(hour_str)
        else:
            hour = POLISH_HOUR_WORDS.get(hour_str)

        if hour and 7 <= hour <= 20:
            return hour

    number_match = re.search(r'\b(\d{1,2})\b', text)
    if number_match:
        hour = int(number_match.group(1))
        if 7 <= hour <= 20:
            return hour

    return None

def extract_datetime(datetime_str: str):
    try:
        relative = interpret_relative_date(datetime_str)
        if relative:
            extracted_hour = extract_hour_from_text(datetime_str)
            if extracted_hour is not None:
                return relative.replace(hour=extracted_hour, minute=0, second=0, microsecond=0)
            else:
                return relative

        now = datetime.now()
        current_year = now.year

        for pl_month, month_num in MONTHS_PL.items():
            if pl_month in datetime_str:
                datetime_str = datetime_str.replace(pl_month, str(month_num))

        dt = date_parser.parse(datetime_str, dayfirst=True, fuzzy=True)

        if dt.year < current_year:
            dt = dt.replace(year=current_year)

        if dt.hour == 0 and dt.minute == 0:
            hour = extract_hour_from_text(datetime_str)
            if hour is not None:
                dt = dt.replace(hour=hour, minute=0)
            else:
                dt = dt.replace(hour=DEFAULT_HOUR, minute=0)

        if dt.date() == now.date() and dt < now and now.hour >= DEFAULT_HOUR:
            dt = dt + timedelta(days=1)
            if dt.hour < DEFAULT_HOUR:
                 dt = dt.replace(hour=DEFAULT_HOUR, minute=0)
        elif dt.date() == now.date() and dt < now and now.hour < DEFAULT_HOUR:
            pass

        return dt
    except Exception as e:
        print("❌ Błąd parsowania daty:", e)
        return None

def generate_receptionist_response(session_id: str, user_input: str) -> dict:
    if session_id not in conversations:
        conversations[session_id] = {
            "history": [{"role": "system", "content": BASE_PROMPT}],
            "patient_data": {"imie": None, "nazwisko": None, "specjalizacja": None, "PESEL": None},
            "calendar_event_created": False,
            "appointment_datetime": None
        }

    extracted_data = extract_patient_data(user_input)
    for key in ["imie", "nazwisko", "specjalizacja", "PESEL"]:
        if extracted_data.get(key) and extracted_data[key] != "null":
            conversations[session_id]["patient_data"][key] = extracted_data[key]

    if extracted_data.get("preferowana_data"):
        new_appointment_datetime = extract_datetime(extracted_data["preferowana_data"])
        if new_appointment_datetime:
            hour_provided = False
            for hour_word in POLISH_HOUR_WORDS.keys():
                if hour_word in extracted_data["preferowana_data"].lower():
                    hour_provided = True
                    break
            if re.search(r'\b(\d{1,2})[.:]?(\d{2})?\b', extracted_data["preferowana_data"]):
                hour_provided = True

            if not hour_provided and new_appointment_datetime.hour == DEFAULT_HOUR:
                conversations[session_id]["appointment_datetime"] = new_appointment_datetime.replace(hour=DEFAULT_HOUR, minute=0)
                conversations[session_id]["history"].append({
                    "role": "assistant",
                    "content": f"Dostępne godziny tego dnia to: {', '.join(AVAILABLE_HOURS)}. Proszę wybierz preferowaną godzinę."
                })
            else:
                conversations[session_id]["appointment_datetime"] = new_appointment_datetime
        else:
            if not conversations[session_id]["appointment_datetime"]:
                 conversations[session_id]["history"].append({
                    "role": "assistant",
                    "content": "Przepraszam, nie zrozumiałam daty lub godziny. Czy możesz podać ją ponownie, np. 'jutro o 15:00' lub '17 czerwca o 11:00'?"
                })

    history = conversations[session_id]["history"]
    history.append({"role": "user", "content": user_input})

    if len(history) > 21:
        conversations[session_id]["history"] = [history[0]] + history[-20:]

    response = send_to_openai(conversations[session_id]["history"])
    conversations[session_id]["history"].append({"role": "assistant", "content": response})

    patient = conversations[session_id]["patient_data"]
    appointment_datetime = conversations[session_id]["appointment_datetime"]

    if all(patient.get(key) for key in ["imie", "nazwisko", "specjalizacja", "PESEL"]) and appointment_datetime and not conversations[session_id]["calendar_event_created"]:
        start_time = appointment_datetime
        formatted_hour = start_time.strftime("%H:%M")
        if formatted_hour not in AVAILABLE_HOURS:
            pass

        end_time = start_time + timedelta(minutes=30)

        event_data = {
            "start_datetime": start_time.isoformat(),
            "end_datetime": end_time.isoformat(),
            "summary": f"Wizyta: {patient['specjalizacja']}",
            "location": CLINIC_ADDRESS,
            "description": (
                f"Imię: {patient['imie']}\n"
                f"Nazwisko: {patient['nazwisko']}\n"
                f"Specjalizacja: {patient['specjalizacja']}\n"
                f"PESEL: {patient['PESEL']}"
            ),
            "attendees": []
        }

        try:
            create_calendar_event(event_data)
            conversations[session_id]["calendar_event_created"] = True
            print("[CalendarAPI] Wydarzenie utworzone:", event_data)
            print("📅 Wizyta została zapisana na:", start_time.strftime("%Y-%m-%d %H:%M"))
        except Exception as e:
            print("[CalendarAPI] Błąd tworzenia wydarzenia:", e)

    return {
        "response": response,
        "patient_data": conversations[session_id]["patient_data"]
    }
