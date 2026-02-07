# AuthKit Demo

A demonstration of [WorkOS AuthKit](https://www.authkit.com/) integration with FastAPI, showcasing secure authentication and session management.

## Setup

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. Install dependencies:
```bash
uv sync
```

2. Create a `.env` file in the project root:
```env
WORKOS_API_KEY=your_api_key_here
WORKOS_CLIENT_ID=your_client_id_here
WORKOS_COOKIE_PASSWORD=your_secret_password_here
```

3. Run the development server:
```bash
uv run uvicorn main:app --reload
```

4. Navigate to `http://localhost:8000`

## Features

- OAuth-based authentication flow
- Session management with encrypted cookies
- Protected routes
- Automatic session refresh on expiry
- Login/logout functionality
- User data display (name, email)

## Project Structure

This is a single-file FastAPI application (`main.py`) demonstrating core AuthKit capabilities in a minimal setup.

---

🏄 [brandonbellero](https://www.brandonbellero.com/)
