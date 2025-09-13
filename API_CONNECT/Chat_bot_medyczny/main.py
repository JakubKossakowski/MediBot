from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from receptionist_llm import generate_receptionist_response

app = FastAPI(title="Recepcjonistka AI")

class ChatInput(BaseModel):
    user_input: str

@app.post("/receptionist")
async def talk_to_receptionist(input: ChatInput):
    try:
        response = generate_receptionist_response(input.user_input)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
