import os

from fastapi import FastAPI, Request, Response
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
def main(request: Request):
    user_data = ""
    sealed_session = request.cookies.get("wos_session")
    if sealed_session:
        try:
            session = workos.user_management.load_sealed_session(
                sealed_session=sealed_session,
                cookie_password=cookie_password
            )
            auth_response = session.authenticate()
            if auth_response.authenticated and auth_response.user:
                user = auth_response.user
                user_data = f"Welcome. {user.first_name or ''} {user.last_name or ''}! ({user.email})"
                print("User authenticated: ", user_data)
        except Exception as e:
            print("Error loading sealed session: ", e)
    
    with open("index.html") as f:
        html = f.read()
    updated_html = html.replace("{{USER_DATA}}", user_data)
    return Response(content=updated_html, media_type="text/html")


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
            auth_response.sealed_session,
            secure=True,
            httponly=True,
            samesite="lax",
        )

        return response
    
    except Exception as e:
        print ("Error authenticating with code: ", e)
        return RedirectResponse("/login")