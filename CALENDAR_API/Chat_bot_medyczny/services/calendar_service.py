import pickle
import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from models.User import Event
from typing import Optional, List
from datetime import datetime
import pytz


class CalendarService:
    def __init__(self):
        self.credentials = self.get_credentials()
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def get_credentials(self):
        credentials = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', 
                    ['https://www.googleapis.com/auth/calendar']
                )
                credentials = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(credentials, token)

        return credentials

    def create_event(self, event: Event):
        event_data = {
            'summary': event.summary,
            'location': event.location,
            'description': event.description,
            'start': {'dateTime': event.start_datetime, 'timeZone': 'Europe/Warsaw'},
            'end': {'dateTime': event.end_datetime, 'timeZone': 'Europe/Warsaw'},
            'attendees': [{'email': email} for email in (event.attendees or [])]
        }
        created_event = self.service.events().insert(calendarId='primary', body=event_data).execute()
        return created_event

    def update_event(self, event_id: str, event: Event):
        try:
            google_event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
        except Exception:
            return None  # event not found

        if event.summary:
            google_event['summary'] = event.summary
        if event.location:
            google_event['location'] = event.location
        if event.description:
            google_event['description'] = event.description
        if event.start_datetime:
            google_event['start']['dateTime'] = event.start_datetime
            google_event['start']['timeZone'] = 'Europe/Warsaw'
        if event.end_datetime:
            google_event['end']['dateTime'] = event.end_datetime
            google_event['end']['timeZone'] = 'Europe/Warsaw'
        if event.attendees is not None:
            google_event['attendees'] = [{'email': email} for email in event.attendees]

        updated_event = self.service.events().update(
            calendarId='primary', eventId=event_id, body=google_event
        ).execute()
        return updated_event

    def delete_event(self, event_id: str):
        self.service.events().delete(calendarId='primary', eventId=event_id).execute()

    def get_event(self, event_id: str):
        try:
            event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
            return event
        except Exception:
            return None

    def get_events_in_range(self, time_min: str, time_max: str):
        try:
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            return events_result.get('items', [])
        except Exception as e:
            print(f"Error fetching events in range: {e}")
            return []


    def get_events_by_hour(self, date_str: str, hour: int, email: Optional[str] = None) -> List[dict]:
        tz = pytz.timezone("Europe/Warsaw")
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        time_min = tz.localize(datetime(date_obj.year, date_obj.month, date_obj.day, hour, 0, 0))
        time_max = tz.localize(datetime(date_obj.year, date_obj.month, date_obj.day, hour + 1, 0, 0))

        try:
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=time_min.isoformat(),
                timeMax=time_max.isoformat(),
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])
        except Exception:
            events = []

        if email:
            events = [
                event for event in events
                if any(att.get("email") == email for att in event.get("attendees", []))
            ]

        return events
