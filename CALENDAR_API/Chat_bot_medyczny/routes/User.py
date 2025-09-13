from fastapi import APIRouter, HTTPException
from models.User import Event
from services.calendar_service import CalendarService
from fastapi import Query
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from typing import Optional
import pickle
from datetime import datetime, timedelta
import pytz
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from services.calendar_service import CalendarService
import pytz

router = APIRouter()

@router.post("/add_event")
async def add_event(event: Event):
    calendar_service = CalendarService()
    created_event = calendar_service.create_event(event)
    return {"status": "success", "event": created_event}

@router.put("/edit_event/{event_id}")
async def edit_event(event_id: str, event: Event):
    calendar_service = CalendarService()
    updated_event = calendar_service.update_event(event_id, event)
    if updated_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"status": "success", "event": updated_event}

@router.delete("/delete_event/{event_id}")
async def delete_event(event_id: str):
    calendar_service = CalendarService()
    calendar_service.delete_event(event_id)
    return {"status": "success", "message": f"Event {event_id} deleted."}

@router.get("/event/{event_id}")
async def get_event(event_id: str):
    calendar_service = CalendarService()
    event = calendar_service.get_event(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"status": "success", "event": event}


@router.get("/events_by_day")
async def get_events_by_day(date: str = Query(...)):
    try:
        # Parsowanie daty (YYYY-MM-DD)
        parsed_date = datetime.strptime(date, "%Y-%m-%d")

        # Ustawienie początku dnia w strefie Warszawy
        warsaw = pytz.timezone("Europe/Warsaw")
        start = warsaw.localize(parsed_date.replace(hour=0, minute=0, second=0, microsecond=0))

        # Koniec dnia to start następnego dnia o północy
        end = start + timedelta(days=1)

        # Zamiana na UTC (Google Calendar API wymaga ISO 8601 z UTC)
        start_utc = start.astimezone(pytz.UTC)
        end_utc = end.astimezone(pytz.UTC)

        calendar_service = CalendarService()
        events = calendar_service.get_events_in_range(start_utc.isoformat(), end_utc.isoformat())

        return {"status": "success", "events": events}

    except Exception as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})

@router.get("/events_by_hour")
async def get_events_by_hour(
    date: str = Query(..., description="Format: YYYY-MM-DD"),
    hour: int = Query(..., ge=0, le=23),
    email: str = None
):
    calendar_service = CalendarService()
    events = calendar_service.get_events_by_hour(date, hour, email)

    return {
        "status": "success",
        "events": events
    }