import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from livekit import api

app = FastAPI()

# These are environment variables so we DON'T hardcode secrets in code.
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "ws://localhost:7880")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "devkey")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "77dbacb702862953bd1c73a56a98009a3774edb5dbffc29ee64584695fbdccd9")

class TokenReq(BaseModel):
    room_name: str
    participant_identity: str
    participant_name: str | None = None

@app.post("/getToken")
def get_token(req: TokenReq):
    # Basic validation (extra safety)
    if not LIVEKIT_API_SECRET:
        raise HTTPException(status_code=500, detail="LIVEKIT_API_SECRET is not set")

    token = (
        api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        .with_identity(req.participant_identity)
        .with_name(req.participant_name or req.participant_identity)
        .with_grants(api.VideoGrants(room_join=True, room=req.room_name))
        .to_jwt()
    )

    return {"server_url": LIVEKIT_URL, "participant_token": token}




# export LIVEKIT_URL="ws://172.20.10.9:7880"
# export LIVEKIT_API_KEY="devkey"
# export LIVEKIT_API_SECRET="YOUR_LONG_SECRET"
# uvicorn main:app --reload --host 0.0.0.0 --port 8000