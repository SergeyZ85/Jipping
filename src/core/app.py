from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI

from src.core.config import settings
from src.database.engine import Base, engine
from src.routes.peoples_and_finances import router

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При запуске приложения - пересоздаем таблицы
    logger.info("Recreating database tables...")
    Base.metadata.drop_all(bind=engine)  # Удаляем старые таблицы
    Base.metadata.create_all(bind=engine)  # Создаем новые таблицы
    yield
    # При остановке приложения - закрываем соединения
    logger.info("Closing database connections...")
    engine.dispose()

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME,lifespan=lifespan)
    app.include_router(router, prefix='')
    return app