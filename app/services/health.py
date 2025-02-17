from fastapi import Depends, HTTPException
from loguru import logger

from app.db import DBFacadeInterface, get_db_facade


class HealthService:
    """Сервис для проверки работоспособности"""

    def __init__(
        self,
        db_facade: DBFacadeInterface = Depends(get_db_facade),
    ):
        self._db_facade = db_facade

    async def check_health(self) -> None:
        """Проверка работоспособности"""

        if not await self._db_facade.is_db_alive():
            logger.error("Базы данных не доступна")
            raise HTTPException(status_code=503, detail="Сервис не доступен. Не доступна база данных")
