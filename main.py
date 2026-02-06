import os

from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from workos import WorkOSClient
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

workos = WorkOSClient(
    api_key=os.getenv("WORKOS_API_KEY"),
    client_id=os.getenv("WORKOS_CLIENT_ID"),
)


@app.get("/")
def main():
    return FileResponse("index.html", media_type="text/html")


@app.get("/login")
def login():
    authorize_url = workos.user_management.get_authorization_url(
        provider="authkit", redirect_uri="http://localhost:8000/callback"
    )
    return RedirectResponse(authorize_url)