from fastapi import APIRouter, Request, Form
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse
Chat_bot_medyczny.app.services.receptionist_llm import generate_receptionist_response
import uuid

twilio_router = APIRouter()

@twilio_router.post("/twilio/voice")
async def twilio_voice_handler(
    request: Request,
    SpeechResult: str = Form(None),
    CallSid: str = Form(None)
):
    session_id = CallSid or str(uuid.uuid4())

    response = VoiceResponse()

    if not SpeechResult:
        # Pierwsza interakcja – powitanie i prośba o wypowiedź
        response.say(
            "Dzień dobry! Jestem Asystentem AI kliniki INFOTECH. W czym mogę pomóc?",
            voice='alice',
            language="pl-PL"
        )
        response.gather(
            input='speech',
            speechTimeout='auto',
            action='https://a6fd-212-33-84-66.ngrok-free.app/twilio/voice',
            method='POST'
        )
        return Response(content=str(response), media_type="application/xml")

    # Obsługa odpowiedzi użytkownika
    result = generate_receptionist_response(session_id, SpeechResult)
    response_text = result["response"]

    response.say(response_text, voice='alice', language="pl-PL")
    response.gather(
        input='speech',
        speechTimeout='auto',
        action='https://a6fd-212-33-84-66.ngrok-free.app/twilio/voice',
        method='POST'
    )
    return Response(content=str(response), media_type="application/xml")
