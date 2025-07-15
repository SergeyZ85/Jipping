from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.config import settings
from src.database.engine import Base, engine
from src.routes.peoples_and_finances import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При запуске приложения - создаем таблицы
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    yield
    # При остановке приложения - закрываем соединения
    print("Closing database connections...")
    engine.dispose()

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME,lifespan=lifespan)
    app.include_router(router, prefix='')
    return app