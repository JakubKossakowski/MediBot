import requests
from fastapi import HTTPException

def is_doctor_busy(email: str, date_str: str, hour: int) -> bool:
    try:
        response = requests.get(
            "http://127.0.0.1:9000/user/events_by_hour",
            params={"date": date_str, "hour": hour}
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Błąd połączenia z kalendarzem: {str(e)}")

    events = response.json().get("events", [])
    return any(
        email in [event.get("organizer", {}).get("email"), event.get("creator", {}).get("email")]
        for event in events
    )
