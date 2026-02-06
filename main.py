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

cookie_password = os.getenv("WORKOS_COOKIE_PASSWORD")


@app.get("/")
def main():
    return FileResponse("index.html", media_type="text/html")


@app.get("/login")
def login():
    authorize_url = workos.user_management.get_authorization_url(
        provider="authkit", redirect_uri="http://localhost:8000/callback"
    )
    return RedirectResponse(authorize_url)

@app.get("/callback")
def callback(code: str):

    try:
        auth_response = workos.user_management.authenticate_with_code(
            code=code,
            session={"seal_session": True, "cookie_password": cookie_password},
        )

        response = RedirectResponse("/")
        response.set_cookie(
            "wos_session",
            auth_response.session_cookie,
            httponly=True,
            secure=True,
            samesite="lax",
        )

        return response
    
    except Exception as e:
        print ("Error authenticating with code: ", e)
        return RedirectResponse("/login")