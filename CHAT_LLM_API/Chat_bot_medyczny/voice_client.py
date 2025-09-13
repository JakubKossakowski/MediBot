from elevenlabs import ElevenLabs
import sounddevice as sd
import numpy as np
import soundfile as sf
from io import BytesIO
import speech_recognition as sr
import requests
from Chat_bot_medyczny.app.services.receptionist_llm  import generate_receptionist_response
import uuid
import os
from dotenv import load_dotenv
from Chat_bot_medyczny.app.services.receptionist_llm  import conversations
import datetime
from Chat_bot_medyczny.app.services.settings_store import get_settings_from_db

load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

def get_eleven_client():
    return ElevenLabs(api_key=ELEVEN_API_KEY)

def get_voice_id():
    settings = get_settings_from_db()
    return settings.voice

def play_beep():
    duration = 0.2
    frequency = 1000
    samplerate = 44100
    t = np.linspace(0, duration, int(samplerate * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    sd.play(tone, samplerate)
    sd.wait()

def recognize_speech() -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🔊 Ding! Mów teraz...")
        play_beep()
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="pl-PL")
            print(f"🗣️ Rozpoznano: {text}")
            return text
        except sr.UnknownValueError:
            print("😕 Nie zrozumiałem.")
        except sr.RequestError as e:
            print(f"❌ Błąd API: {e}")
    return ""

def speak(text: str):
    print("🧠 Generuję odpowiedź głosową...")
    client = get_eleven_client()
    voice_id = get_voice_id()
    response = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id="eleven_multilingual_v2",
        output_format="pcm_16000"
    )
    audio_bytes = b"".join(response)
    audio_data = np.frombuffer(audio_bytes, dtype=np.int16)
    sd.play(audio_data, 16000)
    sd.wait()

def add_to_calendar_api(data: dict):
    try:
        response = requests.post(
            "http://localhost:8001/user/add_event",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("📅 Wydarzenie dodane do kalendzara.")
        else:
            print(f"⚠️ Błąd kalendarza: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Błąd połączenia z CalendarAPI: {e}")

def run_continuous():
    session_id = str(uuid.uuid4())
    print("🤖 Rozpoczynam rozmowę. Powiedz 'do widzenia', by zakończyć.\n")

    welcome_text = (
        "Dzień dobry! Jestem Asystentem AI kliniki."
        "W czym mogę pomóc? Mogę umówić Cię na wizytę, udzielić informacji o terminach?"
        "Jeśli chcesz zakończyć rozmowę, powiedz 'do widzenia'."
        "Po każdym moim pytaniu usłyszysz krótki dźwięk – to znak, że możesz mówić."
    )
    speak(welcome_text)

    while True:
        user_input = recognize_speech()
        if not user_input:
            continue

        if "do widzenia" in user_input.lower():
            goodbye_text = "Dziękuję za rozmowę. Do widzenia i miłego dnia!"
            speak(goodbye_text)
            print("👋 Zakończono rozmowę.")

            patient = conversations.get(session_id, {}).get("patient_data", {})
            appointment_datetime = conversations.get(session_id, {}).get("appointment_datetime")

            if appointment_datetime:
                start_datetime = appointment_datetime
                end_datetime = start_datetime + datetime.timedelta(minutes=30)
            else:
                now = datetime.datetime.now()
                start_datetime = now
                end_datetime = now + datetime.timedelta(minutes=30)

            event_data = {
                "start_datetime": start_datetime.isoformat(),
                "end_datetime": end_datetime.isoformat(),
                "summary": f"Wizyta: {patient.get('specjalizacja', 'nieznana')}",
                "location": "Klinika INFOTECH, ul. Ciepła 40E, Białystok",
                "description": (
                    f"Imię: {patient.get('imie', 'brak')}\n"
                    f"Nazwisko: {patient.get('nazwisko', 'brak')}\n"
                    f"Specjalizacja: {patient.get('specjalizacja', 'brak')}\n"
                    f"PESEL: {patient.get('PESEL', 'brak')}"
                ),
                "attendees": []
            }
            add_to_calendar_api(event_data)
            break

        result = generate_receptionist_response(session_id, user_input)
        speak(result["response"])

    patient_data = conversations.get(session_id, {}).get("patient_data", {})
    print("\n📋 Dane pacjenta zebrane podczas rozmowy:")
    for key, value in patient_data.items():
        print(f"- {key.capitalize()}: {value if value else 'nie podano'}")

    appointment_datetime = conversations.get(session_id, {}).get("appointment_datetime")
    if appointment_datetime:
        print(f"\n📅 Wizyta została zapisana na: {appointment_datetime.strftime('%Y-%m-%d %H:%M')}")
    else:
        print("\n📅 Wizyta nie została zaplanowana.")

if __name__ == "__main__":
    run_continuous()