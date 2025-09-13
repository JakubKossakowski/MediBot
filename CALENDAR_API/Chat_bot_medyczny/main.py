from fastapi import FastAPI
from routes.User import router as user_router
import os
from fastapi.responses import FileResponse, JSONResponse

from services.calendar_service import CalendarService

app = FastAPI()
app.include_router(user_router, prefix="/user", tags=["user"])

TOKEN_FILE = 'token.pickle'

@app.get("/token")
async def get_token():
    if os.path.exists(TOKEN_FILE):
        return FileResponse(TOKEN_FILE)
    else:
        return JSONResponse(status_code=404, content={"detail": "Token file not found."})

@app.delete("/token")
async def delete_token():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        return {"status": "success", "message": "Token deleted successfully."}
    else:
        return JSONResponse(status_code=404, content={"detail": "Token file not found."})


@app.post("/refresh_token")
async def refresh_token():
    calendar_service = CalendarService()
    credentials = calendar_service.get_credentials()
    if credentials:
        return {"status": "success", "message": "Token refreshed successfully."}
    else:
        return JSONResponse(status_code=400, content={"detail": "Failed to refresh token."})
