import requests

def create_calendar_event(event_data: dict):
    url = "http://localhost:8001/user/add_event"
    try:
        response = requests.post(url, json=event_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[CalendarAPI] Błąd podczas tworzenia wydarzenia: {e}")
        return None
