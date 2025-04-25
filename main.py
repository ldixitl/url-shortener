import uvicorn

from src.url_services import app


if __name__ == "__main__":
    uvicorn.run(app)
