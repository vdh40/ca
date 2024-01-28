import uvicorn

from app.controllers.fastapi.factory import create_app
from app.core.config import config

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)
