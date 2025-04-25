from typing import Dict

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

from src.utils import generate_short_id

app = FastAPI()

url_db = {}


class URLRequest(BaseModel):
    url: HttpUrl


@app.post("/", status_code=status.HTTP_201_CREATED)
async def shorten_url(request: URLRequest) -> Dict[str, str]:
    """
    Функция принимает URL и возвращает сокращённую версию.

    :param request: Исходный URL.
    :return: Словарь с коротким URL.
    """
    short_id = generate_short_id()

    while short_id in url_db:
        short_id = generate_short_id()

    url_db[short_id] = request.url
    return {"short_url": f"http://127.0.0.1:8000/{short_id}"}


@app.get("/all", status_code=status.HTTP_200_OK)
async def get_shorted_url():
    """
    Функция для возвращения всех сокращённых URL-адресов.

    :return: Словарь вида {short_id: original_url}.
    """
    return url_db


@app.get("/{short_id}")
async def redirect_to_url(short_id: str) -> RedirectResponse:
    """
    Функция для перенаправления на оригинальный URL по короткому идентификатору.

    :param short_id: Идентификатор сокращённого URL.
    :return: Ответ с редиректом.
    """
    original_url = url_db.get(short_id)
    if not original_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    return RedirectResponse(original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
