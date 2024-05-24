from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import string
import random

app = FastAPI()

# In-memory storage for shortened URLs
url_db = {}


class URLShortenRequest(BaseModel):
    url: str


class URLShortenResponse(BaseModel):
    short_url: str


def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url


@app.post("/shorten", response_model=URLShortenResponse)
async def shorten_url(request: URLShortenRequest):
    long_url = request.url
    if long_url in url_db.values():
        short_url = [key for key, value in url_db.items() if value == long_url][0]
    else:
        short_url = generate_short_url()
        url_db[short_url] = long_url
    return {"short_url": f"http://localhost:8000/{short_url}"}


@app.get("/{short_url}")
async def redirect_url(short_url: str):
    if short_url not in url_db:
        raise HTTPException(status_code=404, detail="URL not found")
    long_url = url_db[short_url]
    return {"redirect_url": long_url}
